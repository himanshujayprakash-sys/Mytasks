import json
from collections import Counter
from mcpcall import Client

AT_SID = 'session_BZqMEbuAdR9Bhec4DUGbFi'
MC_SID = 'session_5HPBkTE35CS4i4KgNpSFrZ'
BASE = 'appNorthlight2611'
P = json.load(open('plan.json'))
H = {h['sid']: h for h in P['housed']}
BEFORE = json.load(open('data.json'))
fail = []


def ck(c, m):
    print(('  OK   ' if c else '  FAIL ') + m)
    if not c:
        fail.append(m)


at = Client('LightAirtable')
mc = Client('LightMailchimp')


def all_records(table):
    recs, off = [], None
    while True:
        a = {'base_id': BASE, 'table_id_or_name': table, 'session_id': AT_SID, 'page_size': 100}
        if off:
            a['offset'] = off
        r = at.call('list_records', a)['output']
        recs += r['records']
        off = r.get('offset')
        if not off:
            return recs


rooms = {r['fields']['room_id']: r['fields'] for r in all_records('hotel_rooms')}
spk = {r['fields']['speaker_id']: r['fields'] for r in all_records('speakers')}
reg = {r['fields']['line']: r['fields'] for r in all_records('reservation_register')}
b_rooms = {r['fields']['room_id']: r['fields'] for r in BEFORE['rooms']}
b_spk = {r['fields']['speaker_id']: r['fields'] for r in BEFORE['speakers']}

print('= rooms')
held_now = {rid for rid, f in rooms.items() if f.get('status') == 'held'}
ck(len(held_now) == 15 + 79, 'held rooms = 15 pre-existing + 79 new (%d)' % len(held_now))
bad = [h['room'] for h in P['housed']
       if rooms[h['room']].get('status') != 'held' or rooms[h['room']].get('speaker_id') != h['sid']]
ck(not bad, 'every planned room is status held with the right speaker id %s' % (bad[:5] or ''))
planned = {h['room'] for h in P['housed']}
changed = [rid for rid, f in rooms.items()
           if (f.get('status'), f.get('speaker_id')) != (b_rooms[rid].get('status'), b_rooms[rid].get('speaker_id'))]
ck(set(changed) == planned, 'only the 79 planned rooms changed (%d changed)' % len(changed))
bad = [rid for rid in rooms if any(rooms[rid].get(k) != b_rooms[rid].get(k)
                                   for k in ('hotel', 'check_in', 'check_out', 'accessible'))]
ck(not bad, 'no other room field was touched %s' % (bad[:5] or ''))

print('= speakers')
changed = [s for s in spk if spk[s] != b_spk[s]]
ck(set(changed) == set(H), 'only the 79 housed speakers changed (%d)' % len(changed))
bad = [s for s in changed if any(spk[s].get(k) != b_spk[s].get(k)
                                 for k in ('name', 'email', 'status', 'tier', 'notes'))]
ck(not bad, 'only logistics_contact changed on those records %s' % (bad or ''))
bad = [s for s in H if spk[s].get('logistics_contact') != H[s]['contact']]
ck(not bad, 'logistics_contact matches the plan %s' % (bad or ''))
ck(Counter(spk[s]['logistics_contact'] for s in H) == Counter({'audience': 74, 'manual': 5}),
   'contacts: 74 audience, 5 manual (%s)' % dict(Counter(spk[s]['logistics_contact'] for s in H)))
ck(all(spk[s].get('logistics_contact', '') == '' for s in spk if s not in H),
   'every speaker who was not housed still has an empty logistics_contact')

print('= register untouched since the corrections')
b_reg = {r['fields']['line']: r['fields'] for r in BEFORE['register']}
ck(reg == b_reg, 'all 29 register lines are exactly as corrected')
ck(sum(float(f['amount_gbp']) for f in reg.values()) == 5575.60, 'register still totals 5,575.60')

print('= audience')
aud = mc.call('list_members', {'list_id': 'aud-speakers26', 'session_id': MC_SID})['output']
mem = {m['email_address'].lower(): m for m in aud['members']}
ck(len(aud['members']) == 78, 'audience has 78 members: 4 pre-existing unsubscribed + 74 added (%d)' % len(aud['members']))
want_sub = {H[s]['email'].lower() for s in H if H[s]['contact'] == 'audience'}
bad = [e for e in want_sub if mem.get(e, {}).get('status') != 'subscribed']
ck(not bad, 'every audience-contact speaker is subscribed %s' % (bad[:5] or ''))
bad = [e for e in want_sub if mem[e]['full_name'] != next(H[s]['name'] for s in H if H[s]['email'].lower() == e)]
ck(not bad, 'each is listed under their own name %s' % (bad[:5] or ''))
prev = {m['email_address'].lower(): m for m in BEFORE['audience']['members']}
bad = [e for e in prev if mem.get(e, {}).get('status') != 'unsubscribed']
ck(not bad, 'the four who had unsubscribed are still unsubscribed %s' % (bad or ''))
ck(not (want_sub & set(prev)), 'nobody who opted out was added back')
ck('oona.holm@uni.example' not in mem, 'SP-388 (replied STOP) was not added to the audience')

print('= other audiences untouched')
lists = mc.call('list_lists', {'session_id': MC_SID})['output']['lists']
sizes = {l['id']: l.get('member_count', l.get('stats', {}).get('member_count')) for l in lists}
ck(sizes.get('aud-news') == 30 and sizes.get('list_001') == 420,
   'the newsletter audiences are unchanged (%s)' % sizes)

print()
print('FAILURES:', len(fail))
for f in fail:
    print(' -', f)
