import json, csv

SQUAD = """rec0416451beacfeb SR-26-001 TJ-P3003 Archie Eccles|U12|2015-06-23|FAM-002|3
recd6eabbda1afc49 SR-26-002 TJ-P3015 Archie Naylor|U12|2015-02-09|FAM-019|4
rece48610c8cdc27b SR-26-003 TJ-P3010 Archie Tattersall|U12|2015-06-18|FAM-009|5
recc9328ad87336ba SR-26-004 TJ-P3012 Esme Lomax|U12|2014-10-22|FAM-016|3
rec4caf6c9a4e32de SR-26-005 TJ-P3006 Finley Dalton|U12|2015-08-28|FAM-012|2
recc67462ff0ad5f2 SR-26-006 TJ-P3007 Finley Lowther|U12|2014-11-01|FAM-008|2
recee64bcd2af42c0 SR-26-007 TJ-P3001 Jack Beckett|U12|2015-07-31|FAM-001|1
rec8f9257795ebd9b SR-26-008 TJ-P3004 Jessica Beckett|U12|2014-10-20|FAM-011|3
recf24ea54deae69f SR-26-009 TJ-P3016 Layla Marsden|U12|2016-04-02|FAM-020|2
recfaf6884119ed0a SR-26-010 TJ-P3011 Max Greaves|U12|2015-01-09|FAM-015|1
recd1432c97ca67f7 SR-26-011 TJ-P3008 Niamh Kenyon|U12|2015-07-04|FAM-013|2
rec8577e20ae55038 SR-26-012 TJ-P3002 Oscar Whitworth|U12|2014-12-05|FAM-010|4
rec78e7dab3682efa SR-26-013 TJ-P3009 Reuben Pickles|U12|2015-06-15|FAM-014|4
rece6c2aff031a294 SR-26-014 TJ-P3017 Riley Ashby|U12|2016-08-01|FAM-021|5
recc6371f785d34c2 SR-26-015 TJ-P3005 Riley Ogden|U12|2015-01-08|FAM-005|1
rec4b05d52643058b SR-26-016 TJ-P3014 Toby Holt|U12|2015-04-30|FAM-018|3
rec57ac0ca6c44297 SR-26-017 TJ-P3013 Toby Jagger|U12|2015-03-03|FAM-017|2
rec3b58cabe5db05f SR-26-018 TJ-P3028 Alfie Mellor|U14|2012-09-19|FAM-027|3
rec6770fd05805252 SR-26-019 TJ-P3018 Archie Beckett|U14|2013-01-13|FAM-001|6
rec4794b800406653 SR-26-020 TJ-P3023 Archie Pickles|U14|2013-07-27|FAM-003|4
rec0920323230fd8c SR-26-021 TJ-P3034 Daniel Castle|U14|2014-07-17|FAM-033|1
rec05b88fa21456eb SR-26-022 TJ-P3033 Dexter Schofield|U14|2013-03-09|FAM-032|2
recb9b35c71812855 SR-26-023 TJ-P3020 Elliot Wilde|U14|2013-03-29|FAM-022|5
rec8664179192de62 SR-26-024 TJ-P3036 Esme Brightwell|U14|2013-02-04|FAM-004|0
recceb0c4200a7339 SR-26-025 TJ-P3031 Ethan Ashby|U14|2013-05-18|FAM-030|2
rec12dcc0209879d1 SR-26-026 TJ-P3038 Harry Hadley|U14|2013-08-25|FAM-035|2
rec10ba56560d839e SR-26-027 TJ-P3027 Imogen Holt|U14|2013-04-26|FAM-026|3
rec957ec92ef91957 SR-26-028 TJ-P3022 Imogen Wilde|U14|2013-05-05|FAM-023|5
rec800518dee185de SR-26-029 TJ-P3035 Isla Brightwell|U14|2013-02-04|FAM-004|0
reca257a4d8ffdb03 SR-26-030 TJ-P3030 Kai Tattersall|U14|2013-08-15|FAM-029|2
rece8e2c3ba790db3 SR-26-031 TJ-P3021 Kieran Lowther|U14|2012-10-26|FAM-008|5
rec989fffe1a805d1 SR-26-032 TJ-P3025 Leo Moss|U14|2013-01-01|FAM-025|4
rec58fafdada88fe0 SR-26-033 TJ-P3026 Noah Ogden|U14|2013-08-10|FAM-005|3
rec03c8c03187d2d4 SR-26-034 TJ-P3029 Oliver Shackleton|U14|2013-06-24|FAM-028|3
rec8e87b9179ceed8 SR-26-035 TJ-P3037 Olivia Sutcliffe|U14|2010-11-12|FAM-034|3
recc58d38eccba603 SR-26-036 TJ-P3019 Rory Haldane|U14|2013-02-21|FAM-007|6
rec96fa838cf62b88 SR-26-037 TJ-P3024 Samuel Carver|U14|2012-12-18|FAM-024|4
rec4d1efb7a10b245 SR-26-038 TJ-P3032 Sienna Tattersall|U14|2013-04-16|FAM-031|2
rece6354f39f255cb SR-26-039 TJ-P3041 Daniel Haldane|U16|2011-08-01|FAM-007|6
rece2f53795965137 SR-26-040 TJ-P3043 Daniel Pickles|U16|2011-07-31|FAM-003|6
reca297c2faf0e3e9 SR-26-041 TJ-P3045 Dexter Hadley|U16|2011-02-17|FAM-006|5
rec0e9a6d87e7901c SR-26-042 TJ-P3046 Finley Hadley|U16|2011-05-07|FAM-006|5
recdff641d7c7273b SR-26-043 TJ-P3053 George Fairbairn|U16|2010-11-19|FAM-043|2
rec0962f09883b114 SR-26-044 TJ-P3044 Imogen Moss|U16|2010-12-15|FAM-038|5
recb5afb0d139ada2 SR-26-045 TJ-P3056 Isla Marsden|U16|2011-06-30|FAM-046|1
rec000ac6803c47b0 SR-26-046 TJ-P3054 Jack Royle|U16|2011-03-29|FAM-044|2
rec141db1055bc3d0 SR-26-047 TJ-P3052 Jacob Tattersall|U16|2011-08-18|FAM-009|3
rec88a89259554c14 SR-26-048 TJ-P3055 Joshua Uttley|U16|2010-11-29|FAM-045|2
rec6537452571af4f SR-26-049 TJ-P3047 Leo Holt|U16|2011-06-14|FAM-039|4
recc4fa0c67e56e83 SR-26-050 TJ-P3039 Lewis Shackleton|U16|2011-06-28|FAM-036|7
rec6d2936edc02034 SR-26-051 TJ-P3058 Max Eccles|U16|2011-01-06|FAM-048|3
rec27922199d8f4b4 SR-26-052 TJ-P3050 Poppy Greaves|U16|2011-04-10|FAM-041|3
rec778d5622d41c26 SR-26-053 TJ-P3048 Reuben Fairbairn|U16|2011-01-09|FAM-040|4
rec99db1db21a3b70 SR-26-054 TJ-P3057 Riley Walmsley|U16|2010-10-01|FAM-047|1
rec1889bcd3a97160 SR-26-055 TJ-P3040 Thomas Eccles|U16|2010-12-12|FAM-002|7
rec0d976566a7a04c SR-26-056 TJ-P3042 Thomas Schofield|U16|2011-08-03|FAM-037|6
reca4efb5c32e1a1d SR-26-057 TJ-P3051 Toby Gill|U16|2011-11-18|FAM-042|3
rec2ce0190a551964 SR-26-058 TJ-P3049 Zachary Ogden|U16|2011-07-01|FAM-005|4"""

rows = []
for line in SQUAD.strip().split('\n'):
    head, team, dob, fam, yrs = line.split('|')
    rec, ref, pid, name = head.split(' ', 3)
    rows.append(dict(rec_id=rec, reg_ref=ref, player_id=pid, player_name=name, team=team,
                     dob=dob, family_id=fam, years_at_club=yrs))
json.dump(rows, open('/workspace/work/squad_rows.json', 'w'), indent=1)

FORMS = """TJ-P3001 Yes N/A 2026-09-01T08:11:00Z
TJ-P3002 Yes N/A 2026-09-01T18:51:00Z
TJ-P3003 Yes N/A 2026-09-01T22:27:00Z
TJ-P3004 Yes N/A 2026-09-02T06:51:00Z
TJ-P3005 Yes N/A 2026-09-02T16:27:00Z
TJ-P3006 Yes N/A 2026-09-02T20:34:00Z
TJ-P3007 Yes N/A 2026-09-03T05:11:00Z
TJ-P3008 Yes N/A 2026-09-03T10:51:00Z
TJ-P3009 Yes N/A 2026-09-03T19:27:00Z
TJ-P3010 Yes N/A 2026-09-04T04:19:00Z
TJ-P3011 Yes N/A 2026-09-04T06:27:00Z
TJ-P3012 Yes N/A 2026-09-04T13:19:00Z
TJ-P3013 Yes N/A 2026-09-04T23:11:00Z
TJ-P3014 Yes N/A 2026-09-05T08:34:00Z
TJ-P3015 Yes N/A 2026-09-05T10:34:00Z
TJ-P3016 Yes Yes 2026-09-05T20:51:00Z
TJ-P3017 Yes No 2026-09-06T05:19:00Z
TJ-P3018 Yes N/A 2026-09-06T12:27:00Z
TJ-P3019 Yes N/A 2026-09-06T18:27:00Z
TJ-P3020 Yes N/A 2026-09-06T21:19:00Z
TJ-P3021 Yes N/A 2026-09-07T07:51:00Z
TJ-P3022 Yes N/A 2026-09-07T13:34:00Z
TJ-P3023 Yes N/A 2026-09-07T19:19:00Z
TJ-P3024 Yes N/A 2026-09-08T03:11:00Z
TJ-P3025 Yes N/A 2026-09-08T12:34:00Z
TJ-P3026 Yes N/A 2026-09-08T15:03:00Z
TJ-P3027 Yes N/A 2026-09-09T00:19:00Z
TJ-P3028 Yes N/A 2026-09-09T05:19:00Z
TJ-P3029 Yes N/A 2026-09-09T13:51:00Z
TJ-P3030 Yes N/A 2026-09-09T23:34:00Z
TJ-P3031 Yes N/A 2026-09-10T07:27:00Z
TJ-P3032 Yes N/A 2026-09-10T14:34:00Z
TJ-P3033 Yes N/A 2026-09-10T19:19:00Z
TJ-P3034 Yes Yes 2026-09-10T23:51:00Z
TJ-P3035 Yes N/A 2026-09-11T06:27:00Z
TJ-P3036 Yes N/A 2026-09-11T06:27:00Z
TJ-P3037 Yes N/A 2026-09-11T21:19:00Z
TJ-P3039 Yes N/A 2026-09-12T15:34:00Z
TJ-P3040 Yes N/A 2026-09-12T18:42:00Z
TJ-P3041 Yes N/A 2026-09-13T04:11:00Z
TJ-P3042 Yes N/A 2026-09-13T07:03:00Z
TJ-P3043 Yes N/A 2026-09-13T18:27:00Z
TJ-P3044 Yes N/A 2026-09-14T00:11:00Z
TJ-P3045 Yes N/A 2026-09-14T04:11:00Z
TJ-P3046 Yes N/A 2026-09-14T11:34:00Z
TJ-P3047 Yes N/A 2026-09-14T23:11:00Z
TJ-P3048 Yes N/A 2026-09-15T03:11:00Z
TJ-P3049 Yes N/A 2026-09-15T08:03:00Z
TJ-P3050 Yes N/A 2026-09-15T15:27:00Z
TJ-P3051 Yes Yes 2026-09-16T03:51:00Z
TJ-P3052 Yes N/A 2026-09-16T08:27:00Z
TJ-P3053 Yes N/A 2026-09-16T14:19:00Z
TJ-P3054 Yes N/A 2026-09-17T00:42:00Z
TJ-P3055 Yes N/A 2026-09-17T04:03:00Z
TJ-P3056 Yes N/A 2026-09-17T11:42:00Z
TJ-P3057 Yes N/A 2026-09-17T16:19:00Z
TJ-P3058 No N/A 2026-09-18T02:34:00Z"""
forms = {}
for line in FORMS.strip().split('\n'):
    pid, consent, playup, sub = line.split()
    forms[pid] = dict(consent=consent, play_up=playup, submitted=sub)
json.dump(forms, open('/workspace/work/forms.json', 'w'), indent=1)

FAMS = """FAM-001|Claire Beckett|claire.beckett@mailbox.example|+447700900337|
FAM-002|Mark Eccles|mark.eccles@homemail.example|+447700900413|
FAM-003|Joanne Pickles|joanne.pickles@inbox.example|+447700900291|
FAM-004|Paul Brightwell|paul.brightwell@mailbox.example|+447700900236|
FAM-005|Sarah Ogden|sarah.ogden@homemail.example||
FAM-006|Andrew Hadley|andrew.hadley@inbox.example|+447700900170|
FAM-007|Rachel Haldane|rachel.haldane@mailbox.example|+447700900195|
FAM-008|Neil Lowther|neil.lowther@homemail.example|+447700900543|
FAM-009|Helen Tattersall|helen.tattersall@inbox.example|+447700900446|
FAM-010|Simon Whitworth|simon.whitworth@mailbox.example|+447700900103|
FAM-011|Kerry Beckett|kerry.beckett@homemail.example|+447700900273|
FAM-012|Darren Dalton|darren.dalton@inbox.example|+447700900357|
FAM-013|Gemma Kenyon|gemma.kenyon@mailbox.example|+447700900599|
FAM-014|Lee Pickles|lee.pickles@homemail.example||
FAM-015|Nicola Greaves|nicola.greaves@inbox.example|+447700900559|
FAM-016|Craig Lomax|craig.lomax@mailbox.example|+447700900409|
FAM-017|Vicky Jagger|vicky.jagger@homemail.example|+447700900141|
FAM-018|Stephen Holt|stephen.holt@inbox.example|+447700900271|
FAM-019|Leanne Naylor|leanne.naylor@mailbox.example|+447700900383|
FAM-020|Gary Marsden|gary.marsden@homemail.example|+447700900579|
FAM-021|Amanda Ashby|amanda.ashby@inbox.example|+447700900415|
FAM-022|Jason Wilde|jason.wilde@mailbox.example|+447700900458|
FAM-023|Lisa Wilde|lisa.wilde@homemail.example||
FAM-024|Wayne Carver|wayne.carver@inbox.example|+447700900120|STOP
FAM-025|Tracy Moss|tracy.moss@mailbox.example|+447700900472|
FAM-026|Dean Holt|dean.holt@homemail.example|+447700900294|
FAM-027|Kelly Mellor|kelly.mellor@inbox.example|+447700900186|
FAM-028|Ian Shackleton|ian.shackleton@mailbox.example|+447700900460|
FAM-029|Louise Tattersall|louise.tattersall@homemail.example|+447700900331|
FAM-030|Martin Ashby|martin.ashby@inbox.example|+447700900471|
FAM-031|Claire Tattersall|claire.tattersall@mailbox.example|+447700900316|
FAM-032|Mark Schofield|mark.schofield@homemail.example||
FAM-033|Joanne Castle|joanne.castle@inbox.example|+447700900180|
FAM-034|Paul Sutcliffe|paul.sutcliffe@mailbox.example|+447700900576|
FAM-035|Sarah Hadley|sarah.hadley@homemail.example|+447700900221|
FAM-036|Andrew Shackleton|andrew.shackleton@inbox.example|+447700900126|
FAM-037|Rachel Schofield|rachel.schofield@mailbox.example|+447700900156|
FAM-038|Neil Moss|neil.moss@homemail.example|+447700900167|
FAM-039|Helen Holt|helen.holt@inbox.example|+447700900359|
FAM-040|Simon Fairbairn|simon.fairbairn@mailbox.example|+447700900546|
FAM-041|Kerry Greaves|kerry.greaves@homemail.example||
FAM-042|Darren Gill|darren.gill@inbox.example|+447700900402|
FAM-043|Gemma Fairbairn|gemma.fairbairn@mailbox.example|+447700900132|
FAM-044|Lee Royle|lee.royle@homemail.example|+447700900496|
FAM-045|Nicola Uttley|nicola.uttley@inbox.example|+447700900452|
FAM-046|Craig Marsden|craig.marsden@mailbox.example|+447700900296|
FAM-047|Vicky Walmsley|vicky.walmsley@homemail.example|+447700900504|
FAM-048|Stephen Eccles|stephen.eccles@inbox.example|+447700900482|"""
CONTACT = """FAM-001 tjc00000-2026-0000-0000-c691f728ce7c
FAM-002 tjc00001-2026-0000-0000-7d93145319af
FAM-003 tjc00002-2026-0000-0000-99e1d94cf44b
FAM-004 tjc00003-2026-0000-0000-8d45ab7a8ee2
FAM-005 tjc00004-2026-0000-0000-ec94134f3df8
FAM-006 tjc00005-2026-0000-0000-aa50bfff59ff
FAM-007 tjc00006-2026-0000-0000-baf2356c74d3
FAM-008 tjc00007-2026-0000-0000-f04cdc1ef486
FAM-009 tjc00008-2026-0000-0000-41f50e46207a
FAM-010 tjc00009-2026-0000-0000-15f17806ecf7
FAM-011 tjc00010-2026-0000-0000-d7648d20ce74
FAM-012 tjc00011-2026-0000-0000-bffa0a35336d
FAM-013 tjc00012-2026-0000-0000-84cd35905f1a
FAM-014 tjc00013-2026-0000-0000-dcff73d06cc4
FAM-015 tjc00014-2026-0000-0000-d72a9ec16414
FAM-016 tjc00015-2026-0000-0000-a41a24b7c5d9
FAM-017 tjc00016-2026-0000-0000-19b0958ab422
FAM-018 tjc00017-2026-0000-0000-c88174232656
FAM-019 tjc00018-2026-0000-0000-0a01566c4666
FAM-020 tjc00019-2026-0000-0000-388b68c910bf
FAM-021 tjc00020-2026-0000-0000-72acf44153de
FAM-022 tjc00021-2026-0000-0000-3b0b9ec39d03
FAM-023 tjc00022-2026-0000-0000-a9c73135eade
FAM-024 tjc00023-2026-0000-0000-1869af37f947
FAM-025 tjc00024-2026-0000-0000-ee9341e84ca2
FAM-026 tjc00025-2026-0000-0000-f2e4eb342f87
FAM-027 tjc00026-2026-0000-0000-849b00a1381f
FAM-028 tjc00027-2026-0000-0000-74aca53eeb03
FAM-029 tjc00028-2026-0000-0000-40790fbc4fae
FAM-030 tjc00029-2026-0000-0000-8a5e97c0ba23
FAM-031 tjc00030-2026-0000-0000-568a8c8fba0d
FAM-032 tjc00031-2026-0000-0000-82ca3ef35fff
FAM-033 tjc00032-2026-0000-0000-f25736439e1b
FAM-034 tjc00033-2026-0000-0000-f39f4b5607a1
FAM-035 tjc00034-2026-0000-0000-9ddd743bb406
FAM-036 tjc00035-2026-0000-0000-97907de5a6ca
FAM-037 tjc00036-2026-0000-0000-3331493b996e
FAM-038 tjc00037-2026-0000-0000-bbc24f72d4e0
FAM-039 tjc00038-2026-0000-0000-e7f6aa4df400
FAM-040 tjc00039-2026-0000-0000-c16dff79883e
FAM-041 tjc00040-2026-0000-0000-07b0c79a333f
FAM-042 tjc00041-2026-0000-0000-df25907746f2
FAM-043 tjc00042-2026-0000-0000-2c85f42096df
FAM-044 tjc00043-2026-0000-0000-548aa52fb2b3
FAM-045 tjc00044-2026-0000-0000-be62cf71cd13
FAM-046 tjc00045-2026-0000-0000-a1d397438b74
FAM-047 tjc00046-2026-0000-0000-429bf0470e5b
FAM-048 tjc00047-2026-0000-0000-72f025417038"""
cid = dict(l.split() for l in CONTACT.strip().split('\n'))
fams = {}
for line in FAMS.strip().split('\n'):
    fid, name, email, mobile, stop = line.split('|')
    fams[fid] = dict(parent_name=name, email=email, mobile=mobile,
                     stop=bool(stop), contact_id=cid[fid])
json.dump(fams, open('/workspace/work/families.json', 'w'), indent=1)

DEP = """Oscar Whitworth
Archie Eccles
Archie Beckett
Elliot Wilde
Archie Pickles
Imogen Holt
Kai Tattersall
Lewis Shackleton
Thomas Eccles
Daniel Pickles
Leo Holt
Poppy Greaves
George Fairbairn"""
json.dump({n: 50.0 for n in DEP.strip().split('\n')},
          open('/workspace/work/deposits.json', 'w'), indent=1)

DUAL = """Dexter Naylor|2011-08-18|Released - transfer cleared
James Kenyon|2013-05-19|Registered
Emily Yates|2011-03-17|Released - transfer cleared
Florence Ackerley|2010-12-24|Registered
Thomas Eccles|2015-10-16|Registered
Elsie Beckett|2013-11-15|Released - transfer cleared
Isla Lister|2012-09-25|Registered
Archie Sutcliffe|2010-05-14|Released - transfer cleared
Lewis Shackleton|2013-04-26|Registered
Alfie Ramsden|2015-11-08|Released - transfer cleared
Layla Dalton|2010-01-24|Registered
Niamh Nuttall|2011-01-24|Released - transfer cleared
Amelia Uttley|2014-06-21|Registered
Martha Greaves|2012-05-27|Registered
Emily Cooke|2010-10-10|Released - transfer cleared
Leo Shackleton|2015-12-08|Released - transfer cleared
Phoebe Carver|2011-08-19|Released - transfer cleared
William Pollard|2015-04-13|Released - transfer cleared
Millie Garside|2011-01-05|Registered
Ava Fairbairn|2011-04-09|Released - transfer cleared
Freya Jagger|2010-02-11|Registered
Callum Jagger|2012-01-24|Released - transfer cleared
Toby Eccles|2011-03-21|Released - transfer cleared
Joshua Pickles|2014-11-22|Released - transfer cleared
Ethan Garside|2012-03-04|Registered
Amelia Ashby|2013-12-24|Released - transfer cleared
Elliot Beckett|2015-07-01|Registered
Alfie Walmsley|2011-01-14|Released - transfer cleared
Daisy Ackerley|2014-11-11|Released - transfer cleared
Martha Whitworth|2014-01-20|Released - transfer cleared
Harriet Jagger|2010-08-20|Released - transfer cleared
Alfie Beckett|2013-03-28|Registered
Erin Uttley|2011-12-17|Registered
Evie Garside|2012-11-10|Released - transfer cleared
Poppy Lister|2012-09-21|Released - transfer cleared
Evie Holt|2013-07-17|Released - transfer cleared
Imogen Moss|2010-12-15|Released - transfer cleared 2026-11-10
Kieran Lowther|2012-10-26|Released - transfer cleared 2026-11-19"""
dual = []
for line in DUAL.strip().split('\n'):
    n, dob, st = line.split('|')
    dual.append(dict(player_name=n, dob=dob, status=st))
json.dump(dual, open('/workspace/work/dual.json', 'w'), indent=1)

# cross-check: any drafted player matching a dual row by name only
names = {r['player_name'] for r in rows}
print('name-only dual matches:', [(d['player_name'], d['dob'], d['status']) for d in dual if d['player_name'] in names])
print('rows', len(rows), 'forms', len(forms))
