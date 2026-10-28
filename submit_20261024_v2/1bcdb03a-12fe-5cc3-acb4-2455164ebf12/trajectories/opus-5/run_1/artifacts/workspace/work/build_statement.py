"""Build the Northlight Summit 2026 hotel liability statement as one offline HTML page.

Figures follow NSF-02 second edition (statement dated 2026-11-12).
"""
import json
from decimal import Decimal, ROUND_HALF_UP

D = Decimal


def p(x):
    return D(x).quantize(D('0.01'), rounding=ROUND_HALF_UP)


# --- Appendix A contract rates (second edition; amendment 1 does not apply to Nov arrivals)
RATES = {
    'Quayside Northlight': {'peak': D('168.00'), 'shoulder': D('132.00')},
    'Harbour Inn': {'peak': D('142.00'), 'shoulder': D('118.00')},
    'Corrin Lodge': {'peak': D('119.00'), 'shoulder': D('96.00')},
}
# --- block calendar drawing rev B
PEAK_NIGHTS = {'2026-11-24', '2026-11-25'}
# --- Port Corrin boundary drawing
LEVY_HOTELS = {'Quayside Northlight': True, 'Harbour Inn': True, 'Corrin Lodge': False}
VAT = D('0.20')
LEVY = D('0.04')
# --- Appendix E
CONTRACTED = {'Quayside Northlight': 20, 'Harbour Inn': 10, 'Corrin Lodge': 20}
QUOTED = {'Quayside Northlight': D('189.00'), 'Harbour Inn': D('165.00'), 'Corrin Lodge': D('139.00')}

from datetime import date, timedelta


def nights(arrival, n):
    a = date.fromisoformat(arrival)
    return [(a + timedelta(days=i)).isoformat() for i in range(n)]


def room_charge(hotel, arrival, n):
    tot = D('0.00')
    for d in nights(arrival, n):
        tot += RATES[hotel]['peak' if d in PEAK_NIGHTS else 'shoulder']
    return tot


def levy_base(hotel, arrival, n):
    if not LEVY_HOTELS[hotel]:
        return D('0.00')
    tot = D('0.00')
    for d in nights(arrival, n)[:5]:
        tot += RATES[hotel]['peak' if d in PEAK_NIGHTS else 'shoulder']
    return tot


def committed(hotel, arrival, n):
    rc = room_charge(hotel, arrival, n)
    vat = p(rc * VAT)
    levy = p(levy_base(hotel, arrival, n) * LEVY)
    return p(rc + vat + levy), rc, vat, levy


def cancellation(hotel, arrival, ack):
    first = RATES[hotel]['peak' if arrival in PEAK_NIGHTS else 'shoulder']
    incl = p(first * (1 + VAT))
    days = (date.fromisoformat(arrival) - date.fromisoformat(ack)).days
    if days > 21:
        return D('0.00'), days, incl, 'none'
    if days >= 8:
        return p(incl / 2), days, incl, '50%'
    return incl, days, incl, '100%'


# ---------------------------------------------------------------- register
# nights = room-nights as settled by the ledger (Corrin bed-nights / occupancy)
R = []


def add(line, res, hotel, page, heading, amount, rule, booked_nights, detail=''):
    R.append(dict(line=line, res=res, hotel=hotel, page=page, heading=heading,
                  amount=p(amount), rule=rule, booked=p(booked_nights * QUOTED[hotel]),
                  detail=detail))


Q, H, C = 'Quayside Northlight', 'Harbour Inn', 'Corrin Lodge'

a, rc, v, l = committed(Q, '2026-11-23', 4)
add('rr-2601', 'NL-2601', Q, '11', 'Committed stay', a,
    'NSF-02 2nd ed s3 (deposit cleared, DR-9B6B5) + s4 Appendix A/B', 4,
    f'4 room-nights, contract rates {rc} + VAT {v} + levy {l}')
a, rc, v, l = committed(H, '2026-11-24', 2)
add('rr-2602', 'NL-2602', H, '11', 'Committed stay', a,
    'NSF-02 2nd ed s3 (deposit cleared, DR-DC6EC) + s4 Appendix A/B', 2,
    f'2 room-nights, contract rates {rc} + VAT {v} + levy {l}')
a, rc, v, l = committed(C, '2026-11-23', 3)
add('rr-2603', 'NL-2603', C, '11', 'Committed stay', a,
    'NSF-02 2nd ed s4 (6 Corrin bed-nights / occupancy 2 = 3 room-nights); no levy, outside city boundary', 3,
    f'3 room-nights, contract rates {rc} + VAT {v}, no levy')
amt, days, incl, band = cancellation(Q, '2026-11-23', '2026-11-08')
add('rr-2604', 'NL-2604', Q, '11', 'Cancellation charge', amt,
    'NSF-02 2nd ed s2 (newest entry CANCELLED 2026-11-05) + Appendix C', 3,
    f'hotel acknowledged 2026-11-08 (cancellation log HR-B4EE-73), {days} days to arrival, {band} of first night incl VAT {incl}')
add('rr-2605', 'NL-2605', H, '11', 'Cancelled without charge', 0,
    'NSF-02 2nd ed s2 + Appendix C (acknowledged 2026-10-20, 36 days to arrival, more than 21)', 2,
    'cancellation log HR-58C5-74')
add('rr-2606', 'NL-2606', Q, '11', 'Cancelled without charge', 0,
    'NSF-02 2nd ed s2 + Appendix C (acknowledged 2026-10-30, 25 days to arrival, more than 21)', 2,
    'cancellation log HR-0B9C-75')
add('rr-2607', 'NL-2607', H, '12', 'Cancelled without charge', 0,
    'NSF-02 2nd ed s2 read by event time (CANCELLED 2026-10-30 09:00 is newer than AMENDED 2026-10-28 15:30) + s4 earlier written acknowledgement by WhatsApp 2026-10-30, 25 days to arrival', 3,
    'WhatsApp wamid.nl04.010 from Harbour Inn beats the log date 2026-11-03')
add('rr-2608', 'NL-2608', Q, '12', 'Superseded by re-booking', 0,
    'NSF-02 2nd ed s2 (moved to NL-2608R; the old number is no longer stated)', 3)
add('rr-2609', 'NL-2609', C, '12', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 (provisional hold, no guarantee entry)', 2)
add('rr-2610', 'NL-2610', H, '12', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 (card authority unsigned)', 3)
add('rr-2611', 'NL-2611', Q, '12', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 + Appendix D (signed by P. Ferris on 2026-10-06, off the register from 2026-09-30)', 3)
a, rc, v, l = committed(Q, '2026-11-22', 6)
add('rr-2612', 'NL-2612', Q, '12', 'Committed stay', a,
    'NSF-02 2nd ed s3 + Appendix D (L. Marsh signed 2026-10-20, on the register from 2026-10-15) + Appendix A/B', 6,
    f'6 room-nights, contract rates {rc} + VAT {v} + levy {l} (levy on the first five nights only)')
add('rr-2613', 'NL-2613', H, '13', 'Sponsor-billed', 0,
    'NSF-02 2nd ed s3 (signed sponsor billing letter, R. Vasquez 2026-10-16)', 2)
a, rc, v, l = committed(C, '2026-11-24', 2)
add('rr-2614', 'NL-2614', C, '13', 'Committed stay', a,
    'NSF-02 2nd ed s3 (sponsor billing letter unsigned, no effect) + Appendix A/B', 2,
    f'2 room-nights, contract rates {rc} + VAT {v}, no levy')
add('rr-2615', 'NL-2615', H, '13', "Not this event's block", 0,
    'NSF-02 2nd ed s1 + scope memo (event code HTW belongs to Harbour Tech Week)', 3)
add('rr-2616', 'NL-2616', Q, '13', 'Arrival outside the block window', 0,
    'NSF-02 2nd ed s1 (arrival 2026-11-21 is before 22 November)', 6)
a, rc, v, l = committed(C, '2026-11-25', 2)
add('rr-2617', 'NL-2617', C, '13', 'Committed stay', a,
    'NSF-02 2nd ed s4 (4 Corrin bed-nights / occupancy 2 = 2 room-nights) + Appendix A/B', 2,
    f'2 room-nights, contract rates {rc} + VAT {v}, no levy')
a, rc, v, l = committed(Q, '2026-11-23', 2)
add('rr-2618', 'NL-2618', Q, '13', 'Committed stay', a,
    'NSF-02 2nd ed s2 (newest entry AMENDED 2026-11-02 resets the stay to 2 nights) + Appendix A/B', 2,
    f'2 room-nights, contract rates {rc} + VAT {v} + levy {l}')
a, rc, v, l = committed(H, '2026-11-24', 2)
add('rr-2619', 'NL-2619', H, '14', 'Committed stay', a,
    'NSF-02 2nd ed s1 (block by arrival date, not booking date) + s3 (deposit cleared DR-FD789) + Appendix A/B', 2,
    f'2 room-nights, contract rates {rc} + VAT {v} + levy {l}; booked 2026-11-11, after the review date')
add('rr-2620', 'NL-2620', C, '14', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 (deposit DR-A64A5 returned unpaid 2026-11-10 per the bank return notice in the second mailbox)', 4)
add('rr-2621', 'NL-2621', H, '14', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 + Appendix D (L. Marsh signed 2026-10-09, before joining the register on 2026-10-15)', 2)
a, rc, v, l = committed(Q, '2026-11-24', 3)
add('rr-2622', 'NL-2622', Q, '14', 'Committed stay', a,
    'NSF-02 2nd ed s3 (deposit cleared DR-40289) + Appendix A/B', 3,
    f'3 room-nights, contract rates {rc} + VAT {v} + levy {l}')
a, rc, v, l = committed(C, '2026-11-22', 4)
add('rr-2623', 'NL-2623', C, '14', 'Committed stay', a,
    'NSF-02 2nd ed s4 (Corrin never totalled; occupancy tally gives 8 bed-nights / occupancy 2 = 4 room-nights) + Appendix A/B', 4,
    f'4 room-nights, contract rates {rc} + VAT {v}, no levy')
amt, days, incl, band = cancellation(H, '2026-11-23', '2026-11-10')
add('rr-2624', 'NL-2624', H, '14', 'Cancellation charge', amt,
    'NSF-02 2nd ed s2 (newest entry CANCELLED 2026-11-10) + Appendix C', 3,
    f'hotel acknowledged 2026-11-10 (cancellation log HR-29A4-93), {days} days to arrival, {band} of first night incl VAT {incl}')
add('rr-2625', 'NL-2625', Q, '15', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 (deposit DR-096BA returned unpaid 2026-11-03 on the deposit receipts log)', 2)
add('rr-2626', 'NL-2626', C, '15', 'Not guaranteed', 0,
    'NSF-02 2nd ed s3 (provisional hold, no guarantee entry)', 2)
add('rr-2627', 'NL-2627', Q, '15', "Not this event's block", 0,
    'NSF-02 2nd ed s1 + scope memo (event code HTW belongs to Harbour Tech Week)', 2)
add('rr-2628', 'NL-2628', H, '15', 'Cancelled without charge', 0,
    'NSF-02 2nd ed s4 earlier written acknowledgement by email 2026-11-02, 22 days to arrival, more than 21', 2,
    'Harbour Inn email of 2026-11-02 16:20 beats the log date 2026-11-04')
a, rc, v, l = committed(H, '2026-11-23', 3)
add('rr-2608R', 'NL-2608R', H, '12', 'Committed stay', a,
    'NSF-02 2nd ed s2 (the re-booked number is the one stated) + s3 (deposit cleared DR-8FD3A) + Appendix A/B', 3,
    f'3 room-nights, contract rates {rc} + VAT {v} + levy {l}')

# ---------------------------------------------------------------- attrition
PICKUP = {
    Q: [('NL-2601', 4), ('NL-2612', 6), ('NL-2618', 2), ('NL-2622', 3)],
    H: [('NL-2602', 2), ('NL-2608R', 3), ('NL-2613', 2)],
    C: [('NL-2603', 3), ('NL-2614', 2), ('NL-2617', 2), ('NL-2623', 4)],
}
attr = {}
for h, rows in PICKUP.items():
    pu = sum(n for _, n in rows)
    thr = CONTRACTED[h] * 85 // 100
    missing = max(0, thr - pu)
    base = RATES[h]['shoulder'] * missing
    vat = p(base * VAT)
    attr[h] = dict(pickup=pu, contracted=CONTRACTED[h], threshold=thr, missing=missing,
                   base=p(base), vat=vat, total=p(base + vat),
                   rows=rows)

# ---------------------------------------------------------------- bridge
gross = sum((r['booked'] for r in R), D('0.00'))
CLASSES = ["Not this event's block", 'Arrival outside the block window',
           'Superseded by re-booking', 'Not guaranteed', 'Sponsor-billed']
steps = [dict(label='Gross booked value (five sheets, nights at quoted rates)',
              delta=gross, kind='start',
              note='29 register lines; nights as the ledger states them, at the rate each booking quotes')]
run = gross
for cls in CLASSES:
    rows = [r for r in R if r['heading'] == cls]
    amt = sum((r['booked'] for r in rows), D('0.00'))
    run -= amt
    steps.append(dict(label='Less ' + cls, delta=-amt, kind='down',
                      note=', '.join(r['res'] for r in rows)))
canc_rows = [r for r in R if r['heading'] in ('Cancellation charge', 'Cancelled without charge')]
canc_booked = sum((r['booked'] for r in canc_rows), D('0.00'))
run -= canc_booked
steps.append(dict(label='Less booked value of cancelled bookings', delta=-canc_booked, kind='down',
                  note=', '.join(r['res'] for r in canc_rows)))
comm_rows = [r for r in R if r['heading'] == 'Committed stay']
comm_total = sum((r['amount'] for r in comm_rows), D('0.00'))
reprice = comm_total - run
run = comm_total
steps.append(dict(label='Re-price committed stays at contract rates, VAT and levy',
                  delta=reprice, kind='down' if reprice < 0 else 'up',
                  note='Appendix A contract rates replace quoted rates; Appendix B VAT and visitor levy'))
canc_total = sum((r['amount'] for r in R if r['heading'] == 'Cancellation charge'), D('0.00'))
run += canc_total
steps.append(dict(label='Add cancellation charges', delta=canc_total, kind='up',
                  note='Appendix C: ' + ', '.join(r['res'] for r in R if r['heading'] == 'Cancellation charge')))
attr_total = sum((attr[h]['total'] for h in attr), D('0.00'))
run += attr_total
steps.append(dict(label='Add attrition damages', delta=attr_total, kind='up',
                  note='Appendix E: shortfall room-nights at the shoulder rate plus VAT'))
steps.append(dict(label='Statement total', delta=run, kind='total', note=''))

TOTAL = run

by_hotel = {}
for h in (Q, H, C):
    bookings = sum((r['amount'] for r in R if r['hotel'] == h), D('0.00'))
    by_hotel[h] = dict(bookings=bookings, attrition=attr[h]['total'], total=p(bookings + attr[h]['total']))
assert p(sum(by_hotel[h]['total'] for h in by_hotel)) == TOTAL, (by_hotel, TOTAL)

# ---------------------------------------------------------------- render
def money(x):
    return '{:,.2f}'.format(x)


WORDS = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
         8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
         14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
         19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty',
         70: 'seventy', 80: 'eighty', 90: 'ninety'}


def w99(n):
    if n in WORDS:
        return WORDS[n]
    return WORDS[n // 10 * 10] + '-' + WORDS[n % 10]


def w999(n):
    if n < 100:
        return w99(n)
    s = WORDS[n // 100] + ' hundred'
    if n % 100:
        s += ' and ' + w99(n % 100)
    return s


def in_words(amount):
    pounds = int(amount)
    pence = int((amount - pounds) * 100)
    parts = []
    if pounds >= 1000:
        parts.append(w999(pounds // 1000) + ' thousand')
        rest = pounds % 1000
        if rest:
            parts.append(('and ' if rest < 100 else '') + w999(rest))
    else:
        parts.append(w999(pounds))
    s = ' '.join(parts) + ' pounds'
    s += ' and ' + w99(pence) + ' pence' if pence else ' exactly'
    return s[0].upper() + s[1:]


# waterfall svg
def waterfall(steps):
    W, Hh = 1080, 460
    pad_l, pad_b, pad_t = 70, 150, 30
    plot_h = Hh - pad_b - pad_t
    vals = []
    run = D('0.00')
    for s in steps:
        if s['kind'] in ('start', 'total'):
            vals.append((D('0.00'), s['delta']))
            run = s['delta']
        else:
            nxt = run + s['delta']
            vals.append((min(run, nxt), max(run, nxt)))
            run = nxt
    top = max(v[1] for v in vals)
    scale = plot_h / float(top)
    n = len(steps)
    bw = (W - pad_l - 30) / n * 0.62
    gap = (W - pad_l - 30) / n
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Bridge from gross booked value to the statement total" class="chart">' % (W, Hh)]
    for i in range(6):
        y = pad_t + plot_h - plot_h * i / 5
        val = top * D(i) / 5
        out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="grid"/>' % (pad_l, y, W - 20, y))
        out.append('<text x="%d" y="%.1f" class="ax" text-anchor="end">%s</text>' % (pad_l - 8, y + 4, money(p(val))))
    for i, (s, (lo, hi)) in enumerate(zip(steps, vals)):
        x = pad_l + 12 + i * gap
        y = pad_t + plot_h - float(hi) * scale
        h = max(1.5, (float(hi) - float(lo)) * scale)
        cls = {'start': 'b-start', 'total': 'b-total', 'down': 'b-down', 'up': 'b-up'}[s['kind']]
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="%s"><title>%s: %s</title></rect>'
                   % (x, y, bw, h, cls, esc(s['label']), money(s['delta'])))
        lab = ('%s' % money(s['delta'])) if s['kind'] in ('start', 'total') else ('%s%s' % ('+' if s['delta'] > 0 else '', money(s['delta'])))
        out.append('<text x="%.1f" y="%.1f" class="val" text-anchor="middle">%s</text>' % (x + bw / 2, y - 6, lab))
        out.append('<text x="%.1f" y="%.1f" class="cat" transform="rotate(-38 %.1f %.1f)" text-anchor="end">%s</text>'
                   % (x + bw / 2, pad_t + plot_h + 14, x + bw / 2, pad_t + plot_h + 14, esc(short(s['label']))))
    out.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" class="axis"/>' % (pad_l, pad_t + plot_h, W - 20, pad_t + plot_h))
    out.append('</svg>')
    return '\n'.join(out)


def short(label):
    return (label.replace('Gross booked value (five sheets, nights at quoted rates)', 'Gross booked value')
            .replace('Re-price committed stays at contract rates, VAT and levy', 'Re-price at contract rates')
            .replace('Less booked value of cancelled bookings', 'Less cancelled bookings'))


def bars(data):
    W, Hh = 1080, 300
    pad_l, pad_b, pad_t = 180, 50, 20
    plot_w = W - pad_l - 140
    top = max(float(v['total']) for v in data.values())
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Statement total split by hotel" class="chart">' % (W, Hh)]
    rows = sorted(data.items(), key=lambda kv: -kv[1]['total'])
    bh = (Hh - pad_t - pad_b) / len(rows) * 0.55
    gap = (Hh - pad_t - pad_b) / len(rows)
    for i, (h, v) in enumerate(rows):
        y = pad_t + i * gap + (gap - bh) / 2
        wb = plot_w * float(v['bookings']) / top
        wa = plot_w * float(v['attrition']) / top
        out.append('<text x="%d" y="%.1f" class="cat2" text-anchor="end">%s</text>' % (pad_l - 12, y + bh / 2 + 5, esc(h)))
        out.append('<rect x="%d" y="%.1f" width="%.1f" height="%.1f" class="s-book"><title>%s bookings: %s</title></rect>'
                   % (pad_l, y, wb, bh, esc(h), money(v['bookings'])))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="s-attr"><title>%s attrition: %s</title></rect>'
                   % (pad_l + wb, y, wa, bh, esc(h), money(v['attrition'])))
        out.append('<text x="%.1f" y="%.1f" class="val2">%s</text>' % (pad_l + wb + wa + 10, y + bh / 2 + 5, money(v['total'])))
    out.append('</svg>')
    return '\n'.join(out)


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))


KEYED = {
    'rr-2601': ('Committed stay', '600.00'), 'rr-2602': ('Committed stay', '260.00'),
    'rr-2603': ('Committed stay', '630.00'), 'rr-2604': ('Committed stay', '450.00'),
    'rr-2605': ('Cancelled without charge', '0.00'), 'rr-2606': ('Cancelled without charge', '0.00'),
    'rr-2607': ('Committed stay', '260.00'), 'rr-2608': ('Superseded by re-booking', '0.00'),
    'rr-2609': ('Not guaranteed', '0.00'), 'rr-2610': ('Not guaranteed', '0.00'),
    'rr-2611': ('Committed stay', '450.00'), 'rr-2612': ('Committed stay', '900.00'),
    'rr-2613': ('Committed stay', '260.00'), 'rr-2614': ('Committed stay', '210.00'),
    'rr-2615': ("Not this event's block", '0.00'),
    'rr-2616': ('Arrival outside the block window', '0.00'),
    'rr-2617': ('Committed stay', '420.00'), 'rr-2618': ('Committed stay', '450.00'),
    'rr-2619': ('Committed stay', '260.00'), 'rr-2620': ('Committed stay', '420.00'),
    'rr-2621': ('Committed stay', '260.00'), 'rr-2622': ('Committed stay', '450.00'),
    'rr-2623': ('Committed stay', '840.00'), 'rr-2624': ('Committed stay', '390.00'),
    'rr-2625': ('Committed stay', '300.00'), 'rr-2626': ('Not guaranteed', '0.00'),
    'rr-2627': ("Not this event's block", '0.00'), 'rr-2628': ('Committed stay', '260.00'),
    'rr-2608R': ('Committed stay', '390.00'),
}
for r in R:
    k = KEYED[r['line']]
    r['corrected'] = (k[0] != r['heading']) or (D(k[1]) != r['amount'])
    r['keyed'] = '%s / %s' % k

n_corr = sum(1 for r in R if r['corrected'])

rows_html = []
for r in sorted(R, key=lambda x: x['res']):
    rows_html.append(
        '<tr data-h="%s" data-hotel="%s" data-c="%s">'
        '<td class="mono">%s</td><td class="mono">%s</td><td>%s</td><td class="num">%s</td>'
        '<td>%s</td><td class="rule">%s%s</td><td class="%s">%s</td></tr>' % (
            esc(r['heading']), esc(r['hotel']), 'y' if r['corrected'] else 'n',
            esc(r['res']), esc(r['line']), esc(r['page']), esc(r['hotel']),
            esc(r['heading']),
            esc(r['rule']),
            ('<span class="d">' + esc(r['detail']) + '</span>') if r['detail'] else '',
            'num' + (' zero' if r['amount'] == 0 else ''), money(r['amount'])))

bridge_rows = []
run = D('0.00')
for s in steps:
    if s['kind'] in ('start', 'total'):
        run = s['delta']
        d = money(s['delta'])
    else:
        run += s['delta']
        d = ('+' if s['delta'] > 0 else '') + money(s['delta'])
    bridge_rows.append('<tr class="%s"><td>%s</td><td class="num">%s</td><td class="num">%s</td><td class="d2">%s</td></tr>'
                       % (s['kind'], esc(s['label']), d, money(p(run)), esc(s['note'])))

attr_rows = []
for h in (Q, H, C):
    aa = attr[h]
    attr_rows.append('<tr><td>%s</td><td class="num">%d</td><td class="num">%d</td><td class="num">%d</td>'
                     '<td class="num">%d</td><td class="num">%s</td><td class="num">%s</td><td class="num">%s</td>'
                     '<td class="d2">%s</td></tr>'
                     % (esc(h), aa['contracted'], aa['threshold'], aa['pickup'], aa['missing'],
                        money(RATES[h]['shoulder']), money(aa['vat']), money(aa['total']),
                        esc(', '.join('%s (%d)' % (r, n) for r, n in aa['rows']))))

hotel_rows = []
for h in (Q, H, C):
    v = by_hotel[h]
    hotel_rows.append('<tr><td>%s</td><td class="num">%s</td><td class="num">%s</td><td class="num b">%s</td></tr>'
                      % (esc(h), money(v['bookings']), money(v['attrition']), money(v['total'])))

HTML = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Northlight Summit 2026 - hotel liability statement, staff-and-guest allocation</title>
<style>
:root{--ink:#16202b;--mut:#5d6b7a;--line:#d7dee6;--bg:#f6f8fa;--card:#fff;
--down:#c2593f;--up:#2f7d6b;--start:#44617f;--total:#1d3752;--attr:#8aa6bd}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 "Segoe UI",system-ui,-apple-system,Helvetica,Arial,sans-serif}
.wrap{max-width:1160px;margin:0 auto;padding:28px 20px 80px}
header.top{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:26px 28px;margin-bottom:26px}
h1{margin:0 0 4px;font-size:20px;letter-spacing:.2px}
.sub{color:var(--mut);font-size:13px;margin-bottom:22px}
.total-label{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.total{font-size:46px;font-weight:650;letter-spacing:-.5px;margin:2px 0 2px}
.total-words{font-size:15px;color:var(--mut);font-style:italic}
.meta{display:flex;flex-wrap:wrap;gap:10px 34px;margin-top:20px;padding-top:18px;border-top:1px solid var(--line);font-size:13px;color:var(--mut)}
.meta b{color:var(--ink);font-weight:600}
section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:22px 24px;margin-bottom:24px}
h2{margin:0 0 4px;font-size:16px}
.hint{color:var(--mut);font-size:13px;margin:0 0 16px}
svg.chart{width:100%;height:auto;display:block}
.grid{stroke:#e9eef3;stroke-width:1}
.axis{stroke:#b9c4cf;stroke-width:1}
text{font-family:inherit}
.ax{font-size:11px;fill:var(--mut)}
.cat{font-size:11.5px;fill:var(--mut)}
.cat2{font-size:13px;fill:var(--ink)}
.val{font-size:11.5px;fill:var(--ink);font-weight:600}
.val2{font-size:13px;fill:var(--ink);font-weight:600}
rect.b-start{fill:var(--start)}rect.b-total{fill:var(--total)}
rect.b-down{fill:var(--down)}rect.b-up{fill:var(--up)}
rect.s-book{fill:var(--start)}rect.s-attr{fill:var(--attr)}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--mut);margin-top:12px}
.sw{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;vertical-align:-1px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#eef2f6;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.zero{color:#94a2b1}
td.b{font-weight:650}
.mono{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:12.5px;white-space:nowrap}
tr.start td,tr.total td{font-weight:650;background:#eef2f6}
tr.total td{border-top:2px solid #9aa9b8}
.rule{color:var(--mut);font-size:12.5px;max-width:430px}
.d,.d2{display:block;color:#7c8a99;font-size:12px;margin-top:3px}
.d2{display:block;max-width:360px;margin-top:0}
.ctl{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:14px}
.ctl input,.ctl select{font:inherit;font-size:13.5px;padding:6px 9px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink)}
.ctl input[type=text]{min-width:230px}
.ctl label{font-size:12.5px;color:var(--mut)}
th.s{cursor:pointer;user-select:none}
th.s:hover{color:var(--ink)}
th.s::after{content:"\\2195";opacity:.35;margin-left:5px;font-size:11px}
th.s.asc::after{content:"\\2191";opacity:.9}
th.s.desc::after{content:"\\2193";opacity:.9}
.count{font-size:12.5px;color:var(--mut)}
footer{color:var(--mut);font-size:12.5px;line-height:1.7}
.tagc{display:inline-block;font-size:11px;padding:1px 7px;border-radius:9px;background:#fdeee9;color:#a8482f;margin-left:6px}
</style>
</head>
<body>
<div class="wrap">

<header class="top">
  <h1>Northlight Summit 2026 &mdash; hotel liability statement</h1>
  <div class="sub">Staff-and-guest allocation of the hotel block. Prepared under NSF-02 second edition. Statement date 12 November 2026.</div>
  <div class="total-label">Total owed to the three block hotels</div>
  <div class="total">GBP __TOTAL__</div>
  <div class="total-words">__WORDS__</div>
  <div class="meta">
    <div>Standard: <b>NSF-02 second edition</b> (approved 2026-09-14)</div>
    <div>Amendment 1: <b>not in force here</b> (arrivals from 2026-12-01)</div>
    <div>Block window: <b>arrivals 22&ndash;27 November 2026</b></div>
    <div>Attrition review date: <b>10 November 2026</b></div>
    <div>Register lines: <b>29</b>, of which <b>__NCORR__ corrected</b></div>
  </div>
</header>

<section>
  <h2>Bridge from the gross booked value to the statement total</h2>
  <p class="hint">One step per class of booking removed, then the move to contract charges, then cancellations, then attrition.</p>
  __WATERFALL__
  <div class="legend">
    <span><span class="sw" style="background:var(--start)"></span>Opening booked value</span>
    <span><span class="sw" style="background:var(--down)"></span>Reduction</span>
    <span><span class="sw" style="background:var(--up)"></span>Addition</span>
    <span><span class="sw" style="background:var(--total)"></span>Statement total</span>
  </div>
  <table style="margin-top:20px">
    <thead><tr><th>Step</th><th class="num">Movement</th><th class="num">Running total</th><th>Reservations / basis</th></tr></thead>
    <tbody>__BRIDGEROWS__</tbody>
  </table>
</section>

<section>
  <h2>Statement total by hotel</h2>
  <p class="hint">Booking charges (committed stays and cancellation charges) plus attrition damages.</p>
  __BARS__
  <div class="legend">
    <span><span class="sw" style="background:var(--start)"></span>Booking charges</span>
    <span><span class="sw" style="background:var(--attr)"></span>Attrition damages</span>
  </div>
  <table style="margin-top:20px">
    <thead><tr><th>Hotel</th><th class="num">Booking charges</th><th class="num">Attrition damages</th><th class="num">Total</th></tr></thead>
    <tbody>__HOTELROWS__</tbody>
    <tfoot><tr class="total"><td>Total</td><td class="num">__BOOKTOT__</td><td class="num">__ATTRTOT__</td><td class="num">__TOTAL__</td></tr></tfoot>
  </table>
</section>

<section>
  <h2>Attrition, NSF-02 Appendix E</h2>
  <p class="hint">Pickup is the room-nights of stays committed on 10 November 2026, counting only stays booked on or before that date, whoever pays. Threshold is 85% of the contracted room-nights, rounded down.</p>
  <table>
    <thead><tr><th>Hotel</th><th class="num">Contracted</th><th class="num">Threshold</th><th class="num">Pickup</th>
    <th class="num">Shortfall</th><th class="num">Shoulder rate</th><th class="num">VAT</th><th class="num">Damages</th><th>Stays counted (room-nights)</th></tr></thead>
    <tbody>__ATTRROWS__</tbody>
  </table>
</section>

<section>
  <h2>Reservation register</h2>
  <p class="hint">Every line of the keyed register with the rule that settled it. Click a column heading to sort; use the boxes to filter.</p>
  <div class="ctl">
    <input type="text" id="q" placeholder="Search reservation, hotel or rule&hellip;" aria-label="Search the register">
    <select id="fh" aria-label="Filter by heading"><option value="">All headings</option>__OPTH__</select>
    <select id="fo" aria-label="Filter by hotel"><option value="">All hotels</option>__OPTO__</select>
    <select id="fc" aria-label="Filter by corrected"><option value="">Keyed and corrected lines</option><option value="y">Corrected lines only</option><option value="n">Lines left untouched</option></select>
    <span class="count" id="cnt"></span>
  </div>
  <table id="reg">
    <thead><tr>
      <th class="s" data-k="0">Reservation</th><th class="s" data-k="1">Register line</th>
      <th class="s" data-k="2">Page</th><th class="s" data-k="3">Hotel</th>
      <th class="s" data-k="4">Heading</th><th class="s" data-k="5">Deciding rule</th>
      <th class="s num" data-k="6" data-n="1">Amount GBP</th>
    </tr></thead>
    <tbody>__REGROWS__</tbody>
    <tfoot><tr class="total"><td colspan="6">Register total (committed stays and cancellation charges)</td><td class="num">__REGTOT__</td></tr></tfoot>
  </table>
</section>

<footer>
  <p><b>Papers behind this statement:</b> NSF-02 second edition (standard, Appendices A&ndash;E); block reservations ledger printed pages 11&ndash;15;
  reservations clock note; Corrin reservations office note and the NL-2623 occupancy tally; scope memo on shared hotels;
  block calendar drawing rev B; Port Corrin city boundary drawing; deposit receipts log and the bank return notice of 10 November 2026;
  card authorities NL-2610, NL-2611, NL-2612, NL-2621; sponsor billing letters NL-2613 and NL-2614;
  hotel reference map and the hotels' cancellation log, with the Harbour Inn WhatsApp message of 30 October 2026 and
  the Harbour Inn email of 2 November 2026 as earlier written acknowledgements; board pack specification.</p>
  <p><b>Not used:</b> NSF-02 first edition (withdrawn for statements from 1 October 2026); NSF-02 amendment 1 (no arrival on or after 1 December 2026);
  the April away-day crib sheet; the 2025 statement print; the hotels' own pickup report.</p>
  <p>This page is self-contained: no network access, no external files and no scripts beyond the sorting and filtering of the register table below. Figures in pounds sterling, rounded to the penny.</p>
</footer>

</div>
<script>
(function(){
  var tb=document.querySelector('#reg tbody'),rows=[].slice.call(tb.rows);
  var q=document.getElementById('q'),fh=document.getElementById('fh'),
      fo=document.getElementById('fo'),fc=document.getElementById('fc'),
      cnt=document.getElementById('cnt');
  function apply(){
    var t=q.value.toLowerCase(),h=fh.value,o=fo.value,c=fc.value,n=0;
    rows.forEach(function(r){
      var ok=(!h||r.dataset.h===h)&&(!o||r.dataset.hotel===o)&&(!c||r.dataset.c===c)
             &&(!t||r.textContent.toLowerCase().indexOf(t)>=0);
      r.style.display=ok?'':'none'; if(ok)n++;
    });
    cnt.textContent=n+' of '+rows.length+' lines shown';
  }
  [q,fh,fo,fc].forEach(function(el){el.addEventListener('input',apply);});
  var cur=-1,dir=1;
  [].slice.call(document.querySelectorAll('#reg th.s')).forEach(function(th){
    th.addEventListener('click',function(){
      var k=+th.dataset.k,num=th.dataset.n==='1';
      dir=(cur===k)?-dir:1; cur=k;
      [].slice.call(document.querySelectorAll('#reg th.s')).forEach(function(o){o.classList.remove('asc','desc');});
      th.classList.add(dir>0?'asc':'desc');
      rows.sort(function(a,b){
        var x=a.cells[k].textContent.trim(),y=b.cells[k].textContent.trim();
        if(num){x=parseFloat(x.replace(/,/g,''))||0;y=parseFloat(y.replace(/,/g,''))||0;
          return (x-y)*dir;}
        return x.localeCompare(y)*dir;
      });
      rows.forEach(function(r){tb.appendChild(r);});
    });
  });
  apply();
})();
</script>
</body>
</html>
"""

headings_order = ['Committed stay', 'Cancellation charge', 'Cancelled without charge', 'Not guaranteed',
                  'Sponsor-billed', 'Superseded by re-booking', "Not this event's block",
                  'Arrival outside the block window']
opth = ''.join('<option value="%s">%s</option>' % (esc(h), esc(h)) for h in headings_order)
opto = ''.join('<option value="%s">%s</option>' % (esc(h), esc(h)) for h in (Q, H, C))
reg_total = sum((r['amount'] for r in R), D('0.00'))
book_tot = sum((by_hotel[h]['bookings'] for h in by_hotel), D('0.00'))

html = (HTML
        .replace('__TOTAL__', money(TOTAL))
        .replace('__WORDS__', in_words(TOTAL))
        .replace('__NCORR__', str(n_corr))
        .replace('__WATERFALL__', waterfall(steps))
        .replace('__BRIDGEROWS__', '\n'.join(bridge_rows))
        .replace('__BARS__', bars(by_hotel))
        .replace('__HOTELROWS__', '\n'.join(hotel_rows))
        .replace('__BOOKTOT__', money(book_tot))
        .replace('__ATTRTOT__', money(attr_total))
        .replace('__ATTRROWS__', '\n'.join(attr_rows))
        .replace('__REGROWS__', '\n'.join(rows_html))
        .replace('__REGTOT__', money(reg_total))
        .replace('__OPTH__', opth)
        .replace('__OPTO__', opto))

with open('/workspace/northlight_hotel_liability_statement_2026.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('TOTAL', money(TOTAL), in_words(TOTAL))
print('register total', money(reg_total), 'attrition', money(attr_total))
for h in (Q, H, C):
    print(h, by_hotel[h])
print('corrected lines', n_corr, 'untouched', 29 - n_corr)
for s in steps:
    print('%-62s %12s' % (s['label'], money(s['delta'])))
print(json.dumps({h: {k: str(v) for k, v in attr[h].items() if k != 'rows'} for h in attr}, indent=1))
