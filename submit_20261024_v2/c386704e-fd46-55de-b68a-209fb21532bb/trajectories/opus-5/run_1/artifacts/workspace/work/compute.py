import csv, json, datetime as dt
from collections import defaultdict

TODAY = dt.date(2026, 11, 25)

BANDS = {
    'U12': (dt.date(2014, 9, 1), dt.date(2015, 8, 31)),
    'U14': (dt.date(2012, 9, 1), dt.date(2013, 8, 31)),
    'U16': (dt.date(2010, 9, 1), dt.date(2011, 8, 31)),
}
# age group immediately below a team = the twelve-month band of players one year younger
BELOW = {t: (dt.date(f.year + 1, 9, 1), dt.date(t_.year + 1, 8, 31)) for t, (f, t_) in BANDS.items()}
FEES = {'U12': 120.00, 'U14': 135.00, 'U16': 150.00}
LIMIT = {'U12': 16, 'U14': 16, 'U16': 18}

rows = json.load(open('/workspace/work/squad_rows.json'))
forms = json.load(open('/workspace/work/forms.json'))        # player_id -> {consent, play_up, submitted}
families = json.load(open('/workspace/work/families.json'))  # family_id -> {...}
deposits = json.load(open('/workspace/work/deposits.json'))  # player name -> amount
dual = json.load(open('/workspace/work/dual.json'))          # list of (name, dob, status)
withdrawn = {'TJ-P3019'}
hardship = {'FAM-028', 'FAM-040'}
cleared = {'U12': False, 'U14': True, 'U16': True}

d = lambda s: dt.date(*map(int, s.split('-')))

# dual registration lookup by (name, dob)
dualmap = {(r['player_name'], r['dob']): r['status'] for r in dual}

status = {}
forward = defaultdict(list)
for r in rows:
    pid, team, dob = r['player_id'], r['team'], d(r['dob'])
    f = forms.get(pid)
    if pid in withdrawn:
        status[pid] = 'Withdrawn by parent'; continue
    ds = dualmap.get((r['player_name'], r['dob']))
    if ds is not None and not ds.startswith('Released - transfer cleared'):
        status[pid] = 'Refused - registered elsewhere'; continue
    lo, hi = BANDS[team]
    if not (lo <= dob <= hi):
        blo, bhi = BELOW[team]
        if not (blo <= dob <= bhi and f and f['play_up'] == 'Yes'):
            status[pid] = 'Refused - wrong age group'; continue
    if not f:
        status[pid] = 'Held - not renewed'; continue
    if f['consent'] != 'Yes':
        status[pid] = 'Held - no consent'; continue
    if not cleared[team]:
        status[pid] = 'Held - team not cleared'; continue
    forward[team].append(r)

for team, lst in forward.items():
    lst.sort(key=lambda r: (-int(r['years_at_club']), forms[r['player_id']]['submitted']))
    lim = LIMIT[team]
    keys = [(-int(r['years_at_club']), forms[r['player_id']]['submitted'][:16]) for r in lst]
    for i, r in enumerate(lst):
        tied = [j for j, k in enumerate(keys) if k == keys[i]]
        if len(tied) > 1 and min(tied) < lim <= max(tied):
            status[r['player_id']] = 'Held - tie at squad limit'
        elif i < lim:
            status[r['player_id']] = 'Registered'
        else:
            status[r['player_id']] = 'Held - squad full'

reg = [r for r in rows if status[r['player_id']] == 'Registered']
print('registered total', len(reg))
for t in ('U12', 'U14', 'U16'):
    print(' ', t, sum(1 for r in reg if r['team'] == t), '/ drafted', sum(1 for r in rows if r['team'] == t))
print()
for r in rows:
    if status[r['player_id']] != 'Registered':
        print(f"  {r['team']} {r['player_name']:<20} {status[r['player_id']]}")

# fees
byfam = defaultdict(list)
for r in reg:
    byfam[r['family_id']].append(r)
lines = {}
for fam, kids in byfam.items():
    kids.sort(key=lambda r: (-FEES[r['team']], d(r['dob'])))
    out = []
    for i, r in enumerate(kids):
        fee = FEES[r['team']]
        disc = 0.0 if (i == 0 or fam in hardship) else round(fee * 0.10, 2)
        net = 0.0 if fam in hardship else round(fee - disc, 2)
        dep = deposits.get(r['player_name'], 0.0) if fam not in hardship else 0.0
        bal = round(net - dep, 2)
        out.append(dict(player=r['player_name'], team=r['team'], pid=r['player_id'], fee=fee,
                        discount=disc, hardship=fam in hardship, deposit=dep, balance=bal))
    lines[fam] = out

invoices = {}
for fam in sorted(lines):
    billable = [l for l in lines[fam] if l['balance'] > 0]
    if billable:
        invoices[fam] = dict(ref=f'TJ26-{fam}', lines=billable,
                             total=round(sum(l['balance'] for l in billable), 2))
print()
print('invoices', len(invoices), 'total', round(sum(i['total'] for i in invoices.values()), 2))
for fam, inv in invoices.items():
    m = families[fam]['mobile']; stop = families[fam].get('stop')
    ch = 'text' if (m and not stop) else 'email'
    print(f"  {inv['ref']} {families[fam]['parent_name']:<22} {inv['total']:>7.2f} {ch:5} " +
          '; '.join(f"{l['player']} ({l['team']}) {l['balance']:.2f}" for l in inv['lines']))
print()
print('texts', sum(1 for f in invoices if families[f]['mobile'] and not families[f].get('stop')))
print('emails', sum(1 for f in invoices if not (families[f]['mobile'] and not families[f].get('stop'))))

json.dump({'status': status, 'lines': lines, 'invoices': invoices},
          open('/workspace/work/result.json', 'w'), indent=1)
