import csv, json, html
from collections import defaultdict, OrderedDict

OUT = '/workspace/work'
rows = json.load(open(f'{OUT}/squad_rows.json'))
res = json.load(open(f'{OUT}/result.json'))
fams = json.load(open(f'{OUT}/families.json'))
status, lines, invoices = res['status'], res['lines'], res['invoices']

INV_NO = {
    'FAM-001': 'INV-2053', 'FAM-002': 'INV-2054', 'FAM-003': 'INV-2055', 'FAM-005': 'INV-2056',
    'FAM-006': 'INV-2057', 'FAM-007': 'INV-2058', 'FAM-009': 'INV-2059', 'FAM-022': 'INV-2060',
    'FAM-023': 'INV-2061', 'FAM-024': 'INV-2062', 'FAM-025': 'INV-2063', 'FAM-026': 'INV-2064',
    'FAM-027': 'INV-2065', 'FAM-029': 'INV-2066', 'FAM-030': 'INV-2067', 'FAM-031': 'INV-2068',
    'FAM-032': 'INV-2069', 'FAM-033': 'INV-2070', 'FAM-036': 'INV-2071', 'FAM-037': 'INV-2072',
    'FAM-038': 'INV-2073', 'FAM-039': 'INV-2074', 'FAM-041': 'INV-2075', 'FAM-042': 'INV-2076',
    'FAM-043': 'INV-2077', 'FAM-044': 'INV-2078', 'FAM-045': 'INV-2079', 'FAM-046': 'INV-2080',
}
TEAMS = ['U12', 'U14', 'U16']
LIMIT = {'U12': 16, 'U14': 16, 'U16': 18}
by_pid = {r['player_id']: r for r in rows}
line_of = {l['pid']: (fam, l) for fam, ls in lines.items() for l in ls}

reg_count = {t: sum(1 for r in rows if r['team'] == t and status[r['player_id']] == 'Registered') for t in TEAMS}
total_reg = sum(reg_count.values())
total_invoiced = round(sum(i['total'] for i in invoices.values()), 2)

# ---------------- CSV ----------------
with open(f'{OUT}/thornwick_2026-27_registered_fees.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['player', 'team', 'family', 'fee', 'sibling_discount', 'hardship',
                'deposit', 'balance', 'invoice_reference'])
    for t in TEAMS:
        for r in sorted((r for r in rows if r['team'] == t and status[r['player_id']] == 'Registered'),
                        key=lambda r: r['player_name']):
            fam, l = line_of[r['player_id']]
            ref = f'TJ26-{fam}' if fam in invoices and l['balance'] > 0 else (
                'none (hardship fund waiver)' if l['hardship'] else 'none (nil balance)')
            w.writerow([r['player_name'], t, fam, f"{l['fee']:.2f}", f"{l['discount']:.2f}",
                        'yes' if l['hardship'] else 'no', f"{l['deposit']:.2f}",
                        f"{l['balance']:.2f}", ref])

# ---------------- Markdown safeguarding dossier ----------------
COACH = OrderedDict([
 ('Dylan Marsh', dict(team='U12', role='Lead', result='Valid',
   rec='Coaches table TJ-V201: enhanced DBS issued 2025-03-11 (1 year 8 months old, within the three years '
       'allowed by safeguarding policy section 4); safeguarding course 2025-01-18, in date to 2028-01-18. '
       'No suspension on the club helpdesk; no approved leave in the volunteer register (only an approved '
       'Christmas holiday 26-31 December, tjv-to-66, which is outside the window test); accepted the U16... '
       'no - accepted the U12 season coaching invitation in the fixtures calendar.')),
 ('Gareth Pemberton', dict(team='U12', role='Assistant', result='Not valid - suspended',
   rec='Club helpdesk ticket 5201, internal note by the club welfare officer of 21 November 2026: suspended '
       'from all coaching and volunteering with immediate effect following a concern raised on 19 November, '
       'pending a county safeguarding review, and "must not be named as a coach for any team until I lift '
       'this in writing" - safeguarding policy section 6. His DBS (update service, status check 2026-08-30) '
       'and course (2024-10-05) are otherwise in date, but suspension comes first in the handbook\'s list.')),
 ('Sunita Varma', dict(team='U12', role='Reserve', result='Not valid - safeguarding course out of date',
   rec='Coaches table TJ-V203: safeguarding course 2023-06-14, which expired on 2026-06-14 (three years from '
       'the course date, safeguarding policy section 4). DBS issued 2025-06-20 is current; no suspension and '
       'no leave of absence.')),
 ('Moira Fennell', dict(team='U14', role='Lead', result='Valid',
   rec='Coaches table TJ-V204: enhanced DBS issued 2024-02-14, less than three years ago, so current on the '
       'first limb of safeguarding policy section 4 - the stale update-service status check of 2025-11-24 '
       'does not matter, because the two limbs are alternatives. Safeguarding course 2024-04-20, in date to '
       '2027-04-20. No suspension, no leave; accepted the U14 coaching invitation.')),
 ('Tom Ackroyd', dict(team='U14', role='Assistant', result='Valid',
   rec='Coaches table TJ-V205: enhanced DBS issued 2023-11-26, which is just inside three years at the close '
       'of the window on 26 November 2026; safeguarding course 2024-09-14, in date to 2027-09-14. His leave '
       'of absence in the volunteer register (tjv-to-62, 20 November to 31 December) is only *requested*, '
       'which safeguarding policy section 5 says does not count, and he accepted the U14 coaching invitation '
       'in the fixtures calendar.')),
 ('Rhys Dando', dict(team='U14', role='Reserve', result='Not valid - DBS out of date',
   rec='Coaches table TJ-V206: enhanced DBS issued 2022-05-03, more than three years ago, and he is not on '
       'the DBS update service, so neither limb of safeguarding policy section 4 is met. His course '
       '(2025-02-01) is in date. His "tentative" answer to the U14 coaching invitation is not a leave of '
       'absence (safeguarding policy section 5), but it does not save the DBS.')),
 ('Colin Rudge', dict(team='U16', role='Lead', result='Not valid - leave of absence',
   rec='Fixtures calendar, U16 season coaching invitation: declined, with the comment "I\'m taking a leave of '
       'absence from coaching from 1 November to 31 January for family reasons." Safeguarding policy section 5 '
       'counts a leave given as the reason for declining the team\'s season coaching invitation, so he is not '
       'available for this window. (Helpdesk ticket 5204 says the same in looser terms; the volunteer register '
       'holds no leave for him, so the calendar answer is what decides it.) His DBS (2024-11-12, update service '
       'check 2026-06-01) and course (2025-03-08) are both in date.')),
 ('Priyanka Lal', dict(team='U16', role='Assistant', result='Valid',
   rec='Coaches table TJ-V208: enhanced DBS issued 2025-08-19; safeguarding course 2025-09-27. Both well in '
       'date. The volunteer register shows an approved one-day *holiday* on 28 November (tjv-to-63), which is '
       'not a leave of absence under safeguarding policy section 5. Accepted the U16 coaching invitation.')),
 ('Ewan Kettle', dict(team='U16', role='Reserve', result='Valid',
   rec='Coaches table TJ-V209: enhanced DBS issued 2023-02-07 is more than three years old, but he is on the '
       'DBS update service and the club\'s last status check is 2026-02-10, nine months old and so inside the '
       'twelve months allowed by the second limb of safeguarding policy section 4. Safeguarding course '
       '2024-01-20, in date to 2027-01-20. His only volunteer-register entry is a cancelled holiday '
       '(tjv-to-65). Accepted the U16 coaching invitation.')),
])
COACH['Dylan Marsh']['rec'] = (
    'Coaches table TJ-V201: enhanced DBS issued 2025-03-11, well within the three years allowed by '
    'safeguarding policy section 4; safeguarding course 2025-01-18, in date to 2028-01-18. No suspension on '
    'the club helpdesk, no leave of absence in the volunteer register (only an approved Christmas holiday, '
    'tjv-to-66, 26-31 December), and he accepted the U12 season coaching invitation in the fixtures calendar.')

CLEAR = {
 'U12': ('Not cleared', 'Dylan Marsh', '',
   'The lead, Dylan Marsh, is valid. The assistant, Gareth Pemberton, is not valid (suspended), so under '
   'RH-26 section 2 the reserve would take the assistant\'s place - but the reserve, Sunita Varma, is not '
   'valid either (safeguarding course out of date). The assistant\'s place is therefore left blank, the team '
   'has only one valid coach, and it is Not cleared.'),
 'U14': ('Cleared', 'Moira Fennell', 'Tom Ackroyd',
   'The lead (Moira Fennell) and the assistant (Tom Ackroyd) are both valid, so the reserve is not needed '
   'and the team has its two valid coaches.'),
 'U16': ('Cleared', 'Ewan Kettle', 'Priyanka Lal',
   'The lead, Colin Rudge, is not valid (leave of absence), so under RH-26 section 2 the reserve, Ewan '
   'Kettle, who is valid, takes the lead\'s place in coach_1. The assistant, Priyanka Lal, is valid and '
   'stays in coach_2. Two valid coaches, so the team is Cleared.'),
}

md = ['# Safeguarding dossier: MDYL winter registration window 2026-27',
      '',
      'Thornwick Juniors FC. Prepared 25 November 2026 by the registration secretary for the window closing '
      'at 12:00 on 26 November 2026.',
      '',
      'Every coach named for the U12, U14 and U16 teams in the coaching structure diagram '
      '(`Safeguarding/team_coaching_structure.svg`, names as at 1 September 2026) was checked under the '
      'club\'s *Safeguarding policy (volunteers), 2026* and recorded on the coaches table with one of the '
      'five results fixed by RH-26 section 2: Valid; Not valid - suspended; Not valid - leave of absence; '
      'Not valid - DBS out of date; Not valid - safeguarding course out of date. Where more than one applied, '
      'the first in that list was used.',
      '',
      '## Coaches checked', '']
for name, c in COACH.items():
    md += [f"### {name} - {c['team']} {c['role']}", '',
           f"**Result: {c['result']}**", '', c['rec'], '']
md += ['## Team clearance', '']
for t in TEAMS:
    st, c1, c2, why = CLEAR[t]
    md += [f'### {t} ({st})', '',
           f"- coach_1 (lead\u2019s place): {c1 or '*blank*'}",
           f"- coach_2 (assistant\u2019s place): {c2 or '*blank*'}", '', why, '']
md += ['## Effect on the squads', '',
       'Because the U12 team is Not cleared, every U12 player who reached question 6 of RH-26 section 3 is '
       '*Held - team not cleared* and no U12 player is registered in this window. The U14 and U16 teams are '
       'Cleared, so their players went forward to the league\u2019s squad limits.', '',
       '## Papers that did not decide anything here', '',
       '- The eight mini-soccer and girls-section coaches on the coaches table (TJ-V210 to TJ-V217) are marked '
       '"Not in the MDYL winter window" and were left untouched.',
       '- The U9, U10 and U13 Girls clearance rows belong to other leagues and were left untouched.', '']
open(f'{OUT}/thornwick_safeguarding_dossier_2026-27.md', 'w').write('\n'.join(md))

# ---------------- HTML ----------------
STATUSES = ['Registered', 'Held - squad full', 'Held - tie at squad limit', 'Held - team not cleared',
            'Held - not renewed', 'Held - no consent', 'Refused - wrong age group',
            'Refused - registered elsewhere', 'Withdrawn by parent']
counts = {t: {s: 0 for s in STATUSES} for t in TEAMS}
for r in rows:
    counts[r['team']][status[r['player_id']]] += 1
used = [s for s in STATUSES if any(counts[t][s] for t in TEAMS)]
PALETTE = {'Registered': '#1b7f3b', 'Held - squad full': '#c47f10', 'Held - tie at squad limit': '#8a6d1f',
           'Held - team not cleared': '#2f5d9e', 'Held - not renewed': '#6b4fa0',
           'Held - no consent': '#9c3f8c', 'Refused - wrong age group': '#b5312c',
           'Refused - registered elsewhere': '#7a2420', 'Withdrawn by parent': '#5a6066'}
maxn = max(counts[t][s] for t in TEAMS for s in used)

bars = []
for t in TEAMS:
    cells = []
    for s in used:
        n = counts[t][s]
        pct = 0 if maxn == 0 else round(n * 100.0 / maxn, 2)
        cells.append(
            f'<div class="bar-row"><div class="bar-lab">{html.escape(s)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{PALETTE[s]}">'
            f'</div></div><div class="bar-num">{n}</div></div>')
    bars.append(f'<div class="chart-team"><h3>{t} <span class="muted">'
                f'({sum(counts[t].values())} drafted, {reg_count[t]} registered, '
                f'squad limit {LIMIT[t]})</span></h3>{"".join(cells)}</div>')

trows = []
for r in rows:
    s = status[r['player_id']]
    trows.append(
        f'<tr><td>{html.escape(r["player_name"])}</td><td>{r["team"]}</td>'
        f'<td class="num" data-v="{r["years_at_club"]}">{r["years_at_club"]}</td>'
        f'<td><span class="pill" style="background:{PALETTE[s]}">{html.escape(s)}</span></td></tr>')

irows = []
for fam in sorted(invoices):
    inv = invoices[fam]
    kids = '<br>'.join(
        f'{html.escape(l["player"])} ({l["team"]}) &mdash; &pound;{l["balance"]:.2f}' for l in inv['lines'])
    ch = 'text to ' + fams[fam]['mobile'] if (fams[fam]['mobile'] and not fams[fam]['stop']) \
         else 'email to ' + fams[fam]['email']
    irows.append(f'<tr><td>{inv["ref"]}</td><td>{INV_NO[fam]}</td>'
                 f'<td>{html.escape(fams[fam]["parent_name"])} ({fam})</td><td>{kids}</td>'
                 f'<td class="num">&pound;{inv["total"]:.2f}</td><td>{html.escape(ch)}</td></tr>')

nohtml = []
for fam in sorted(lines):
    if fam not in invoices:
        for l in lines[fam]:
            nohtml.append(f'<li>{html.escape(fams[fam]["parent_name"])} ({fam}) &mdash; '
                          f'{html.escape(l["player"])} ({l["team"]}): hardship fund waiver, '
                          f'nil balance, no invoice</li>')

page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thornwick Juniors FC &mdash; MDYL winter registration window 2026-27</title>
<style>
:root {{ --ink:#1c2024; --line:#d7dce1; --soft:#f4f6f8; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:28px 20px 60px; font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--ink); background:#fff; line-height:1.45; }}
.wrap {{ max-width:1080px; margin:0 auto; }}
h1 {{ font-size:1.5rem; margin:0 0 4px; }}
h2 {{ font-size:1.15rem; margin:36px 0 10px; border-bottom:2px solid var(--line); padding-bottom:6px; }}
h3 {{ font-size:1rem; margin:18px 0 8px; }}
.sub {{ color:#5c646c; margin:0 0 24px; }}
.muted {{ color:#5c646c; font-weight:400; font-size:.86rem; }}
.heads {{ display:flex; flex-wrap:wrap; gap:16px; }}
.big {{ flex:1 1 230px; border:1px solid var(--line); border-radius:12px; padding:18px 20px; background:var(--soft); }}
.big .n {{ font-size:3.4rem; font-weight:700; line-height:1; letter-spacing:-2px; }}
.big .l {{ text-transform:uppercase; letter-spacing:.07em; font-size:.72rem; color:#4a5158; margin-top:8px; }}
.teams {{ flex:1 1 320px; border:1px solid var(--line); border-radius:12px; padding:14px 18px; }}
.teams table {{ margin:0; }}
.chart {{ display:flex; flex-wrap:wrap; gap:22px; }}
.chart-team {{ flex:1 1 320px; border:1px solid var(--line); border-radius:12px; padding:12px 16px 16px; }}
.bar-row {{ display:flex; align-items:center; gap:8px; margin:5px 0; font-size:.8rem; }}
.bar-lab {{ flex:0 0 170px; text-align:right; color:#39414a; }}
.bar-track {{ flex:1 1 auto; background:#eceff2; border-radius:4px; height:16px; overflow:hidden; }}
.bar-fill {{ height:100%; border-radius:4px; min-width:0; }}
.bar-num {{ flex:0 0 26px; text-align:right; font-variant-numeric:tabular-nums; font-weight:600; }}
table {{ border-collapse:collapse; width:100%; margin:10px 0 0; font-size:.88rem; }}
th,td {{ border-bottom:1px solid var(--line); padding:7px 10px; text-align:left; vertical-align:top; }}
th {{ background:var(--soft); }}
td.num, th.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
#squad th[data-sort] {{ cursor:pointer; user-select:none; }}
#squad th[data-sort]::after {{ content:" \\2195"; color:#97a0a8; font-size:.8em; }}
#squad th[data-sort].asc::after {{ content:" \\25B2"; color:var(--ink); }}
#squad th[data-sort].desc::after {{ content:" \\25BC"; color:var(--ink); }}
.pill {{ color:#fff; border-radius:999px; padding:2px 9px; font-size:.76rem; white-space:nowrap; display:inline-block; }}
.controls {{ display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-top:10px; }}
input[type=text], select {{ font:inherit; padding:7px 10px; border:1px solid #b9c0c7; border-radius:7px; }}
input[type=text] {{ min-width:260px; }}
.count {{ color:#5c646c; font-size:.84rem; }}
tfoot td {{ font-weight:700; background:var(--soft); }}
ul {{ margin:8px 0 0 18px; }}
footer {{ margin-top:40px; color:#5c646c; font-size:.8rem; border-top:1px solid var(--line); padding-top:12px; }}
</style>
</head>
<body><div class="wrap">

<h1>Thornwick Juniors FC &mdash; Merrowdale &amp; District Youth League winter registration window 2026-27</h1>
<p class="sub">Squads settled 25 November 2026; the window closes at 12:00 on 26 November 2026.
Statuses follow registration handbook RH-26; fees follow schedule FS-26; squad limits follow MDYL rule 4.2
as amended by the AGM of 14 November 2026.</p>

<div class="heads">
  <div class="big"><div class="n">{total_reg}</div><div class="l">players registered</div></div>
  <div class="big"><div class="n">&pound;{total_invoiced:,.2f}</div><div class="l">total invoiced
      ({len(invoices)} family invoices)</div></div>
  <div class="teams"><h3>Registered by team</h3>
    <table><thead><tr><th>Team</th><th class="num">Registered</th><th class="num">Drafted</th>
    <th class="num">Squad limit</th></tr></thead><tbody>
    {''.join(f'<tr><td>{t}</td><td class="num">{reg_count[t]}</td>'
             f'<td class="num">{sum(counts[t].values())}</td>'
             f'<td class="num">{LIMIT[t]}</td></tr>' for t in TEAMS)}
    </tbody></table>
  </div>
</div>

<h2>Status of every drafted player, team by team</h2>
<div class="chart">{''.join(bars)}</div>

<h2>All squad rows</h2>
<div class="controls">
  <input type="text" id="filter" placeholder="Filter by player, team or status&hellip;" aria-label="Filter">
  <select id="teamsel" aria-label="Team">
    <option value="">All teams</option>{''.join(f'<option>{t}</option>' for t in TEAMS)}
  </select>
  <select id="statsel" aria-label="Status">
    <option value="">All statuses</option>{''.join(f'<option>{html.escape(s)}</option>' for s in used)}
  </select>
  <span class="count" id="count"></span>
</div>
<table id="squad">
<thead><tr><th data-sort="text">Player</th><th data-sort="text">Team</th>
<th data-sort="num" class="num">Years at club</th><th data-sort="text">Status</th></tr></thead>
<tbody>{''.join(trows)}</tbody>
</table>

<h2>Family invoices</h2>
<table>
<thead><tr><th>Reference</th><th>Invoice</th><th>Family</th><th>Lines</th><th class="num">Total</th>
<th>Reminder</th></tr></thead>
<tbody>{''.join(irows)}</tbody>
<tfoot><tr><td colspan="4">{len(invoices)} invoices</td>
<td class="num">&pound;{total_invoiced:,.2f}</td><td></td></tr></tfoot>
</table>
<h3>Registered players not invoiced</h3>
<ul>{''.join(nohtml)}</ul>

<footer>Offline page: all content, styling and behaviour are contained in this file; there are no external
links, images or scripts. Amounts shown are the membership balances charged under RH-26 section 6
(fee, less any 10% sibling discount, less any early-bird deposit already paid).</footer>

<script>
(function () {{
  var table = document.getElementById('squad');
  var tbody = table.tBodies[0];
  var all = Array.prototype.slice.call(tbody.rows);
  var f = document.getElementById('filter');
  var ts = document.getElementById('teamsel');
  var ss = document.getElementById('statsel');
  var c = document.getElementById('count');

  function apply() {{
    var q = f.value.toLowerCase().trim();
    var t = ts.value, s = ss.value, shown = 0;
    all.forEach(function (row) {{
      var team = row.cells[1].textContent.trim();
      var stat = row.cells[3].textContent.trim();
      var txt = row.textContent.toLowerCase();
      var ok = (!q || txt.indexOf(q) > -1) && (!t || t === team) && (!s || s === stat);
      row.style.display = ok ? '' : 'none';
      if (ok) shown++;
    }});
    c.textContent = 'showing ' + shown + ' of ' + all.length + ' rows';
  }}

  function sortBy(i, kind, dir) {{
    var rows = all.slice();
    rows.sort(function (a, b) {{
      var x = a.cells[i], y = b.cells[i];
      if (kind === 'num') {{
        return dir * (parseFloat(x.getAttribute('data-v')) - parseFloat(y.getAttribute('data-v')));
      }}
      return dir * x.textContent.trim().localeCompare(y.textContent.trim());
    }});
    rows.forEach(function (r) {{ tbody.appendChild(r); }});
  }}

  Array.prototype.slice.call(table.tHead.rows[0].cells).forEach(function (th, i) {{
    var kind = th.getAttribute('data-sort');
    if (!kind) return;
    th.addEventListener('click', function () {{
      var dir = th.classList.contains('asc') ? -1 : 1;
      Array.prototype.slice.call(table.tHead.rows[0].cells).forEach(function (o) {{
        o.classList.remove('asc'); o.classList.remove('desc');
      }});
      th.classList.add(dir === 1 ? 'asc' : 'desc');
      sortBy(i, kind, dir);
    }});
  }});

  f.addEventListener('input', apply);
  ts.addEventListener('change', apply);
  ss.addEventListener('change', apply);
  apply();
}})();
</script>
</div></body></html>
'''
open(f'{OUT}/thornwick_window_2026-27.html', 'w').write(page)
print('written', total_reg, total_invoiced, len(invoices))
