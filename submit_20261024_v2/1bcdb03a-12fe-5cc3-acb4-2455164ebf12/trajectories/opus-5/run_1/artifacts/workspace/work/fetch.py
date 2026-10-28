import json
from mcpcall import Client

S = {
    'tf': 'session_APipnhRsQeMQu8iJaiZrCy',
    'at': 'session_BZqMEbuAdR9Bhec4DUGbFi',
    'mc': 'session_5HPBkTE35CS4i4KgNpSFrZ',
}

out = {}

tf = Client('LightTypeform')
out['responses'] = tf.call('list_responses', {'form_id': 'frm-travel26', 'session_id': S['tf']})['output']['items']

at = Client('LightAirtable')


def all_records(table):
    recs, offset = [], None
    while True:
        args = {'base_id': 'appNorthlight2611', 'table_id_or_name': table,
                'session_id': S['at'], 'page_size': 100}
        if offset:
            args['offset'] = offset
        r = at.call('list_records', args)['output']
        recs += r['records']
        offset = r.get('offset')
        if not offset:
            return recs


out['speakers'] = all_records('speakers')
out['rooms'] = all_records('hotel_rooms')
out['hotels'] = all_records('hotels')
out['register'] = all_records('reservation_register')

mc = Client('LightMailchimp')
out['audience'] = mc.call('list_members', {'list_id': 'aud-speakers26', 'session_id': S['mc']})['output']

with open('data.json', 'w') as f:
    json.dump(out, f, indent=1)

print('responses', len(out['responses']))
print('speakers', len(out['speakers']))
print('rooms', len(out['rooms']))
print('register', len(out['register']))
from collections import Counter
print('speaker status', Counter(r['fields'].get('status') for r in out['speakers']))
print('room status', Counter(r['fields'].get('status') for r in out['rooms']))
print('submitted', sum(1 for r in out['responses'] if r.get('submitted_at')))
