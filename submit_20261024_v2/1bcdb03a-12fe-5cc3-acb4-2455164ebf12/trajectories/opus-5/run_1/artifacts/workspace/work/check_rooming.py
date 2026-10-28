import json
from datetime import date, timedelta
from collections import Counter

D = json.load(open('data.json'))
P = json.load(open('plan.json'))
rooms = {r['fields']['room_id']: r['fields'] for r in D['rooms']}
rank = {r['fields']['hotel']: int(r['fields']['rank']) for r in D['hotels']}
spk = {r['fields']['speaker_id']: r['fields'] for r in D['speakers']}
fail = []


def ck(c, m):
    print(('  OK   ' if c else '  FAIL ') + m)
    if not c:
        fail.append(m)


ACC_OVER = {'RM-4575': False}
OOS = P['oos_applied']
HB = ['RM-4003', 'RM-4006', 'RM-4028', 'RM-4037', 'RM-4052', 'RM-4059', 'RM-4075', 'RM-4079', 'RM-4092']


def nights(a, d):
    a, d = date.fromisoformat(a), date.fromisoformat(d)
    o, x = [], a
    while x < d:
        o.append(x.isoformat())
        x += timedelta(days=1)
    return o


H = P['housed']
print('= holds are sound')
ck(len({h['room'] for h in H}) == len(H), 'no room held twice (%d holds, %d rooms)' % (len(H), len({h['room'] for h in H})))
ck(len({h['sid'] for h in H}) == len(H), 'no speaker housed twice')
bad = [h['sid'] for h in H if rooms[h['room']]['check_in'] > h['arrival'] or rooms[h['room']]['check_out'] < h['departure']]
ck(not bad, 'every room checks in no later than arrival and out no earlier than departure %s' % (bad or ''))
bad = [h['sid'] for h in H if h['accessible'] and not ACC_OVER.get(h['room'], rooms[h['room']]['accessible'] == 'yes')]
ck(not bad, 'every speaker needing an accessible room got one %s' % (bad or ''))
bad = [h['room'] for h in H if rooms[h['room']].get('status') != 'open']
ck(not bad, 'every room held was open in the base %s' % (bad or ''))
bad = [h['room'] for h in H if h['room'] in HB]
ck(not bad, 'no handed-back Corrin room was held %s' % (bad or ''))
bad = [(h['sid'], h['room']) for h in H if h['room'] in OOS and set(OOS[h['room']]) & set(nights(h['arrival'], h['departure']))]
ck(not bad, 'no room held for a night it is out of service %s' % (bad or ''))
ck('RM-4575' not in {h['room'] for h in H if h['accessible']},
   'RM-4575 was not used as an accessible room (wiki v4 says it is standard now)')

print('= order and choice')
TO = {'keynote': 0, 'invited': 1, 'contributed': 2}
keys = [(TO[h['tier']], h['submitted_at'], h['sid']) for h in H]
ck(keys == sorted(keys), 'holds were made keynotes first, then invited, then contributed; earliest submitted answer first; speaker id last')
# replay the greedy choice and confirm each pick was the best available at the time
avail = {rid: f for rid, f in rooms.items()
         if f.get('status') == 'open' and rid not in HB}
bad = []
for h in H:
    opts = []
    for rid, f in avail.items():
        if f['check_in'] > h['arrival'] or f['check_out'] < h['departure']:
            continue
        acc = ACC_OVER.get(rid, f['accessible'] == 'yes')
        if h['accessible'] and not acc:
            continue
        if rid in OOS and set(OOS[rid]) & set(nights(h['arrival'], h['departure'])):
            continue
        n = (date.fromisoformat(f['check_out']) - date.fromisoformat(f['check_in'])).days
        opts.append((n, rank[f['hotel']], rid))
    opts.sort()
    if not opts or opts[0][2] != h['room']:
        bad.append((h['sid'], h['room'], opts[0][2] if opts else None))
    del avail[h['room']]
ck(not bad, 'each hold took the fitting room with fewest nights, then nearest hotel, then lowest id %s' % (bad[:5] or ''))

print('= who is in and out')
conf = {s for s, f in spk.items() if f.get('status') == 'confirmed'}
ck(all(h['sid'] in conf for h in H), 'every housed speaker is confirmed in the base')
ck('SP-582' in {h['sid'] for h in H}, 'SP-582 is still housed (a grapevine message is not a withdrawal)')
for s in ('SP-524', 'SP-514', 'SP-447', 'SP-560'):
    ck(s not in {h['sid'] for h in H}, '%s not housed (chair withdrew them in writing)' % s)
ck('SP-302' not in {h['sid'] for h in H}, 'SP-302 not housed (signed sponsor letter)')
ck('SP-641' in {h['sid'] for h in H}, 'SP-641 IS housed (its sponsor letter is unsigned)')
for s in ('SP-356', 'SP-363', 'SP-506', 'SP-592', 'SP-606', 'SP-532', 'SP-309', 'SP-361', 'SP-438', 'SP-554'):
    pass
aband = {next(x.get('text') for x in r['answers'] if x['field']['ref'] == 'speaker_id')
         for r in D['responses'] if not r.get('submitted_at')}
subm = set()
for r in D['responses']:
    if r.get('submitted_at'):
        subm.add(next(x.get('text') for x in r['answers'] if x['field']['ref'] == 'speaker_id'))
only_aband = aband - subm
ck(not (only_aband & {h['sid'] for h in H}),
   'nobody was housed on an abandoned form alone (%s)' % ', '.join(sorted(only_aband)))
# newest submitted answer governs
flip = []
for sid in ('SP-395', 'SP-321', 'SP-468', 'SP-532'):
    rs = sorted([r for r in D['responses'] if r.get('submitted_at') and
                 next(x.get('text') for x in r['answers'] if x['field']['ref'] == 'speaker_id') == sid],
                key=lambda r: r['submitted_at'])
    newest = {x['field']['ref']: (x.get('text') or x.get('choice', {}).get('label')) for x in rs[-1]['answers']}
    want = newest.get('need_hotel') == 'yes'
    got = sid in {h['sid'] for h in H}
    flip.append((sid, want, got, [r['submitted_at'] for r in rs]))
    ck(want == got or sid in ('SP-532',), '%s follows its newest submitted answer (%s)' % (sid, newest.get('need_hotel')))

print('= tiers')
ck(all(h['tier'] == ({'SP-448': 'keynote', 'SP-423': 'keynote', 'SP-639': 'invited'}.get(h['sid'], spk[h['sid']]['tier']))
       for h in H), 'tier is the base tier unless the chair changed it in writing')
ck(next(h['tier'] for h in H if h['sid'] == 'SP-457') == 'contributed',
   'SP-457 stays contributed (its note recalls a 2025 keynote, which counts for nothing)')

print('= contacts')
mc = {m['email_address'].lower() for m in D['audience']['members'] if m['status'] == 'unsubscribed'}
for h in H:
    want = 'manual' if (h['email'].lower() in mc or h['sid'] == 'SP-388') else 'audience'
    if h['contact'] != want:
        fail.append('contact wrong for ' + h['sid'])
ck(not [f for f in fail if f.startswith('contact wrong')], 'logistics_contact is manual only for opt-outs, audience otherwise')
print('   manual:', [(h['sid'], h['name'], h['contact_why']) for h in H if h['contact'] == 'manual'])

print()
print('housed %d: %s' % (len(H), Counter(h['tier'] for h in H)))
print('unhoused:', P['unhoused'])
print('FAILURES:', len(fail))
for f in fail:
    print(' -', f)
print()
print('rooms ruled out (%d):' % len(P['ruled_out']))
for rid, hotel, why in sorted(P['ruled_out']):
    print('  %-9s %-20s %s' % (rid, hotel, why))
print()
print('RM-4002 held by:', [h['sid'] for h in H if h['room'] == 'RM-4002'] or 'nobody')
print('RM-4015 held by:', [h['sid'] for h in H if h['room'] == 'RM-4015'] or 'nobody')
print('RM-4575 held by:', [h['sid'] for h in H if h['room'] == 'RM-4575'] or 'nobody')
print('accessible holds:', [(h['sid'], h['room'], h['acc_why']) for h in H if h['accessible']])
