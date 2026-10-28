"""Work out the speaker rooming under NSP-03, third issue."""
import json
from datetime import date, timedelta

D = json.load(open('data.json'))

# ---------------------------------------------------------------- evidence
# Programme chair withdrawals in writing (chair = Imogen Vale, chair@northlightsummit.test / U9CHAIR)
WITHDRAWN = {
    'SP-524': 'chair email "Speaker withdrawals", 2026-11-09',
    'SP-514': 'chair email "Speaker withdrawals", 2026-11-09',
    'SP-447': 'chair email "Speaker withdrawals", 2026-11-09',
    'SP-560': 'chair post in the Slack #programme thread, 2026-11-10',
}
# Not withdrawals: hotels desk "grapevine" message about SP-582 in #logistics (not the chair).

# Signed sponsor letters taking on the speaker's hotel
SPONSOR_SIGNED = {'SP-302': 'Corvid Systems letter signed by R. Vasquez, 2026-11-02'}
# SP-641 Pellow Foundation letter is unsigned -> no effect.

# Chair tier changes in writing (email "Tier changes", 2026-11-10)
TIER_OVERRIDE = {'SP-448': 'keynote', 'SP-423': 'keynote', 'SP-639': 'invited'}

# Accessibility: form answer, plus signed requests held outside the form
ACCESS_SIGNED = {
    'SP-643': 'signed accessibility request scanned into the folder, 2026-11-05',
    'SP-629': 'signed accessibility request held on help desk ticket 64109, 2026-11-06',
}

# Rooms the hotels desk handed back (hotels desk email, 2026-10-20) - still "open" in the base
HANDED_BACK = ['RM-4003', 'RM-4006', 'RM-4028', 'RM-4037', 'RM-4052',
               'RM-4059', 'RM-4075', 'RM-4079', 'RM-4092']

# Hotels desk calendar: rooms out of service for nights slept in
OUT_OF_SERVICE = {
    'RM-4003': ['2026-11-23', '2026-11-24', '2026-11-25', '2026-11-26'],
    'RM-4002': ['2026-11-24', '2026-11-25'],
}
# RM-4015 deep clean 10:00-14:00 on 23 Nov is daytime housekeeping; the room stays lettable.

# Current hotel room schedules on the logistics wiki override the stale base copy
ACCESS_OVERRIDE = {'RM-4575': False}  # Quayside schedule v4: lost its wet room in the October refit

# Already unsubscribed from the speaker logistics audience
MC_UNSUB_EMAILS = {m['email_address'].lower() for m in D['audience']['members']
                   if m['status'] == 'unsubscribed'}
# Replied STOP to the speaker desk text line (+441632960531)
STOP_NUMBERS = {'+447700900618'}
STOP_SPEAKERS = {'SP-388'}  # the speaker desk addressed +447700900618 as "Oona (SP-388)"

TIER_ORDER = {'keynote': 0, 'invited': 1, 'contributed': 2}

# ---------------------------------------------------------------- inputs
spk = {r['fields']['speaker_id']: dict(r['fields'], rec=r['id']) for r in D['speakers']}
rank = {r['fields']['hotel']: int(r['fields']['rank']) for r in D['hotels']}

# newest SUBMITTED answer per speaker
answers = {}
for r in D['responses']:
    if not r.get('submitted_at'):
        continue  # a form someone opened and abandoned is not an answer
    a = {}
    for x in r['answers']:
        ref = x['field']['ref']
        a[ref] = x.get('text') if x['type'] == 'short_text' else x['choice']['label']
    sid = a.get('speaker_id')
    if not sid:
        continue
    cur = answers.get(sid)
    if cur is None or r['submitted_at'] > cur['submitted_at']:
        answers[sid] = dict(a, submitted_at=r['submitted_at'], response_id=r['response_id'])

abandoned_only = sorted({
    a['field']['ref'] and None or None for a in []} or
    {next(x.get('text') for x in r['answers'] if x['field']['ref'] == 'speaker_id')
     for r in D['responses'] if not r.get('submitted_at')} - set(answers))

# ---------------------------------------------------------------- who is housed
cands, excluded = [], []
for sid, s in spk.items():
    if s.get('status') != 'confirmed':
        continue
    if sid in WITHDRAWN:
        excluded.append((sid, 'withdrawn by the programme chair (%s)' % WITHDRAWN[sid]))
        continue
    a = answers.get(sid)
    if a is None:
        if sid in {next(x.get('text') for x in r['answers'] if x['field']['ref'] == 'speaker_id')
                   for r in D['responses'] if not r.get('submitted_at')}:
            excluded.append((sid, 'only an abandoned form, never submitted - not an answer'))
        continue
    if a.get('need_hotel') != 'yes':
        continue
    if not a.get('arrival') or not a.get('departure'):
        excluded.append((sid, 'submitted answer has no arrival/departure dates'))
        continue
    if sid in SPONSOR_SIGNED:
        excluded.append((sid, 'signed sponsor letter takes on the hotel (%s)' % SPONSOR_SIGNED[sid]))
        continue
    tier = TIER_OVERRIDE.get(sid, s.get('tier'))
    cands.append(dict(sid=sid, name=s['name'], email=s['email'], rec=s['rec'],
                      tier=tier, base_tier=s.get('tier'),
                      tier_changed=sid in TIER_OVERRIDE,
                      arrival=a['arrival'], departure=a['departure'],
                      submitted_at=a['submitted_at'], response_id=a['response_id'],
                      accessible=(a.get('accessible') == 'yes') or sid in ACCESS_SIGNED,
                      acc_why=('form answer' if a.get('accessible') == 'yes'
                               else (ACCESS_SIGNED[sid] if sid in ACCESS_SIGNED else ''))))

cands.sort(key=lambda c: (TIER_ORDER[c['tier']], c['submitted_at'], c['sid']))

# ---------------------------------------------------------------- rooms
rooms, ruled_out = [], []
for r in D['rooms']:
    f = r['fields']
    rid = f['room_id']
    acc = ACCESS_OVERRIDE.get(rid, f.get('accessible') == 'yes')
    row = dict(rec=r['id'], room_id=rid, hotel=f['hotel'], check_in=f['check_in'],
               check_out=f['check_out'], accessible=acc, status=f.get('status'),
               nights=(date.fromisoformat(f['check_out']) - date.fromisoformat(f['check_in'])).days)
    if f.get('status') == 'withdrawn':
        ruled_out.append((rid, f['hotel'], 'withdrawn in the hotels desk room-inventory handover'))
        continue
    if f.get('status') == 'held':
        ruled_out.append((rid, f['hotel'], 'already held in the base before this run'))
        continue
    if rid in HANDED_BACK:
        ruled_out.append((rid, f['hotel'],
                          'handed back to Corrin Lodge (hotels desk email, 2026-10-20); the base still shows it open'))
        continue
    rooms.append(row)


def nights_of(arr, dep):
    a, d = date.fromisoformat(arr), date.fromisoformat(dep)
    out, x = [], a
    while x < d:
        out.append(x.isoformat())
        x += timedelta(days=1)
    return out


def fits(room, c):
    if room['check_in'] > c['arrival'] or room['check_out'] < c['departure']:
        return False
    if c['accessible'] and not room['accessible']:
        return False
    oos = OUT_OF_SERVICE.get(room['room_id'])
    if oos and set(oos) & set(nights_of(c['arrival'], c['departure'])):
        return False
    return True


free = {r['room_id']: r for r in rooms}
housed, unhoused = [], []
for c in cands:
    opts = [r for r in free.values() if fits(r, c)]
    if not opts:
        unhoused.append(dict(c, reason='no open allocation room free from %s to %s%s'
                             % (c['arrival'], c['departure'],
                                ' that is accessible' if c['accessible'] else '')))
        continue
    opts.sort(key=lambda r: (r['nights'], rank[r['hotel']], r['room_id']))
    pick = opts[0]
    del free[pick['room_id']]
    housed.append(dict(c, room=pick['room_id'], room_hotel=pick['hotel'],
                       room_in=pick['check_in'], room_out=pick['check_out'],
                       room_nights=pick['nights'], room_rec=pick['rec'],
                       room_accessible=pick['accessible']))

for h in housed:
    off = h['email'].lower() in MC_UNSUB_EMAILS or h['sid'] in STOP_SPEAKERS
    h['contact'] = 'manual' if off else 'audience'
    h['contact_why'] = ('already unsubscribed from the speaker logistics audience'
                        if h['email'].lower() in MC_UNSUB_EMAILS
                        else ('replied STOP to the speaker desk text line' if h['sid'] in STOP_SPEAKERS
                              else ''))

json.dump(dict(housed=housed, unhoused=unhoused, excluded=excluded,
               ruled_out=ruled_out, cands=cands,
               oos_applied={k: v for k, v in OUT_OF_SERVICE.items()}),
          open('plan.json', 'w'), indent=1)

from collections import Counter
print('candidates', len(cands), Counter(c['tier'] for c in cands))
print('housed', len(housed), Counter(h['tier'] for h in housed))
print('unhoused', len(unhoused))
print('manual contacts', [h['sid'] for h in housed if h['contact'] == 'manual'])
print('rooms ruled out', len(ruled_out))
print('accessible needed', [(c['sid'], c['acc_why']) for c in cands if c['accessible']])
print()
print('excluded (confirmed but not housed by rule):')
for sid, why in sorted(excluded):
    print('  ', sid, spk[sid]['name'], '-', why)
print()
print('unhoused:')
for u in unhoused:
    print('  ', u['sid'], u['name'], u['tier'], u['arrival'], u['departure'], '-', u['reason'])
print()
print('first 12 holds:')
for h in housed[:12]:
    print('  %-8s %-10s %-16s %s %s->%s room %s (%s, %d nights) %s'
          % (h['sid'], h['tier'], h['name'], h['submitted_at'], h['arrival'], h['departure'],
             h['room'], h['room_hotel'], h['room_nights'], h['contact']))
