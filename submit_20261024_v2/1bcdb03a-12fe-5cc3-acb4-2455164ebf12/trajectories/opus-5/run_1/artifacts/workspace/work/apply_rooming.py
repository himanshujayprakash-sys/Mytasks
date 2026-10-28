"""Apply the NSP-03 rooming: hold rooms, set logistics_contact, update the speaker logistics audience.

Nothing else in the base, no other audience, no messages.
"""
import json
import sys
from mcpcall import Client

DRY = '--apply' not in sys.argv
P = json.load(open('plan.json'))
H = P['housed']

AT_SID = 'session_BZqMEbuAdR9Bhec4DUGbFi'
MC_SID = 'session_5HPBkTE35CS4i4KgNpSFrZ'
BASE = 'appNorthlight2611'
AUD = 'aud-speakers26'

at = Client('LightAirtable')
mc = Client('LightMailchimp')

log = []
print('%d holds, %d contacts, %d audience adds' %
      (len(H), len(H), sum(1 for h in H if h['contact'] == 'audience')))

for i, h in enumerate(H, 1):
    if DRY:
        print('would hold %s -> %s ; contact %s' % (h['room'], h['sid'], h['contact']))
        continue
    r = at.call('update_record', {
        'base_id': BASE, 'table_id_or_name': 'hotel_rooms', 'record_id': h['room_rec'],
        'fields': {'status': 'held', 'speaker_id': h['sid']}, 'session_id': AT_SID})
    assert r.get('status') == 'ok', (h['room'], r)
    r2 = at.call('update_record', {
        'base_id': BASE, 'table_id_or_name': 'speakers', 'record_id': h['rec'],
        'fields': {'logistics_contact': h['contact']}, 'session_id': AT_SID})
    assert r2.get('status') == 'ok', (h['sid'], r2)
    if h['contact'] == 'audience':
        r3 = mc.call('create_member', {
            'list_id': AUD, 'email_address': h['email'], 'full_name': h['name'],
            'status': 'subscribed', 'session_id': MC_SID})
        assert r3.get('status') == 'ok', (h['sid'], r3)
        log.append(('audience', h['sid'], h['email']))
    if i % 20 == 0:
        print('  ...%d/%d' % (i, len(H)))

if not DRY:
    print('applied %d holds' % len(H))
    json.dump(log, open('applied.json', 'w'), indent=1)
