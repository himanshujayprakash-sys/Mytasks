"""Re-open the written board page and check it against the ledger independently."""
import re
from decimal import Decimal as D
from html import unescape
from html.parser import HTMLParser

PATH = '/workspace/northlight_hotel_liability_statement_2026.html'
s = open(PATH, encoding='utf-8').read()
fail = []


def ck(cond, msg):
    print(('  OK   ' if cond else '  FAIL ') + msg)
    if not cond:
        fail.append(msg)


print('= file and self-containment')
ck(s.lstrip().startswith('<!DOCTYPE html>'), 'starts with a doctype')
ck(not re.search(r'https?://|<script[^>]+src|<link|@import|<iframe|url\(', s),
   'no network, no external file, nothing fetched from outside the file')
ck(s.count('<svg') == 2 and s.count('</svg>') == 2, 'two charts drawn inline as SVG')

print('= markup well formed')


class P(HTMLParser):
    void = {'meta', 'br', 'hr', 'img', 'input', 'link', 'source'}

    def __init__(self):
        super().__init__()
        self.st, self.err = [], []

    def handle_starttag(self, t, a):
        if t not in self.void:
            self.st.append(t)

    def handle_endtag(self, t):
        if self.st and self.st[-1] == t:
            self.st.pop()
        else:
            self.err.append(t)


p = P()
p.feed(s)
ck(not p.st and not p.err, 'every tag closed in order')

print('= register table read back off the page')
rows = re.findall(
    r'<tr data-h="(.*?)" data-hotel="(.*?)" data-c="(.*?)">'
    r'<td class="mono">(.*?)</td><td class="mono">(.*?)</td><td>(.*?)</td><td class="num">(.*?)</td>'
    r'<td>(.*?)</td><td class="rule">(.*?)</td><td class="num[^"]*">(.*?)</td></tr>', s)
ck(len(rows) == 29, 'all 29 register lines present (%d)' % len(rows))
reg = {}
for dh, dhotel, dc, res, line, page, hotel, heading, rule, amt in rows:
    a = D(amt.replace(',', ''))
    heading = unescape(heading)
    hotel = unescape(hotel)
    reg[res] = dict(line=line, page=page, hotel=hotel, heading=heading, amt=a, corrected=dc)
    ck(unescape(dh) == heading and unescape(dhotel) == hotel,
       '%s filter attributes match the visible cells' % res)

HEADINGS = {'Committed stay', 'Cancellation charge', 'Cancelled without charge', 'Not guaranteed',
            'Sponsor-billed', 'Superseded by re-booking', "Not this event's block",
            'Arrival outside the block window'}
ck(all(r['heading'] in HEADINGS for r in reg.values()),
   'every heading is one of the eight spelt in NSF-02 s6')
ck(all(r['amt'] == 0 for r in reg.values()
       if r['heading'] not in ('Committed stay', 'Cancellation charge')),
   'every line outside Committed stay / Cancellation charge carries 0.00')
ck(all(re.fullmatch(r'-?[\d,]+\.\d\d', a) for *_, a in rows), 'every amount is to the penny')

print('= expected ledger outcome, computed by hand from the papers')
EXP = {
    'NL-2601': ('Committed stay', '744.00'), 'NL-2602': ('Committed stay', '352.16'),
    'NL-2603': ('Committed stay', '400.80'), 'NL-2604': ('Cancellation charge', '79.20'),
    'NL-2605': ('Cancelled without charge', '0.00'), 'NL-2606': ('Cancelled without charge', '0.00'),
    'NL-2607': ('Cancelled without charge', '0.00'), 'NL-2608': ('Superseded by re-booking', '0.00'),
    'NL-2608R': ('Committed stay', '498.48'), 'NL-2609': ('Not guaranteed', '0.00'),
    'NL-2610': ('Not guaranteed', '0.00'), 'NL-2611': ('Not guaranteed', '0.00'),
    'NL-2612': ('Committed stay', '1066.08'), 'NL-2613': ('Sponsor-billed', '0.00'),
    'NL-2614': ('Committed stay', '285.60'), 'NL-2615': ("Not this event's block", '0.00'),
    'NL-2616': ('Arrival outside the block window', '0.00'), 'NL-2617': ('Committed stay', '258.00'),
    'NL-2618': ('Committed stay', '372.00'), 'NL-2619': ('Committed stay', '352.16'),
    'NL-2620': ('Not guaranteed', '0.00'), 'NL-2621': ('Not guaranteed', '0.00'),
    'NL-2622': ('Committed stay', '580.32'), 'NL-2623': ('Committed stay', '516.00'),
    'NL-2624': ('Cancellation charge', '70.80'), 'NL-2625': ('Not guaranteed', '0.00'),
    'NL-2626': ('Not guaranteed', '0.00'), 'NL-2627': ("Not this event's block", '0.00'),
    'NL-2628': ('Cancelled without charge', '0.00'),
}
ck(set(EXP) == set(reg), 'the page states exactly the 29 reservations of the register')
bad = [r for r in EXP if reg[r]['heading'] != EXP[r][0] or reg[r]['amt'] != D(EXP[r][1])]
ck(not bad, 'every heading and amount agrees with the hand computation %s' % (bad or ''))

print('= totals add up on the page itself')
reg_total = sum(r['amt'] for r in reg.values())
foot = D(re.search(r'Register total \(committed stays and cancellation charges\)</td><td class="num">([\d,.]+)', s).group(1).replace(',', ''))
ck(foot == reg_total, 'register footer %s equals the sum of its lines %s' % (foot, reg_total))

hotel_rows = re.findall(r'<tr><td>(Quayside Northlight|Harbour Inn|Corrin Lodge)</td>'
                        r'<td class="num">([\d,.]+)</td><td class="num">([\d,.]+)</td>'
                        r'<td class="num b">([\d,.]+)</td></tr>', s)
ck(len(hotel_rows) == 3, 'three hotels in the split')
split = {}
for h, b, a, t in hotel_rows:
    b, a, t = (D(x.replace(',', '')) for x in (b, a, t))
    split[h] = t
    ck(b + a == t, '%s bookings + attrition = total' % h)
    ck(b == sum(r['amt'] for r in reg.values() if r['hotel'] == h),
       '%s booking charges tie to its register lines' % h)

total_shown = D(re.search(r'<div class="total">GBP ([\d,.]+)</div>', s).group(1).replace(',', ''))
ck(sum(split.values()) == total_shown, 'hotel split sums to the headline total %s' % total_shown)

attr_rows = re.findall(r'<tr><td>(Quayside Northlight|Harbour Inn|Corrin Lodge)</td>'
                       r'<td class="num">(\d+)</td><td class="num">(\d+)</td><td class="num">(\d+)</td>'
                       r'<td class="num">(\d+)</td><td class="num">([\d,.]+)</td>'
                       r'<td class="num">([\d,.]+)</td><td class="num">([\d,.]+)</td>', s)
ck(len(attr_rows) == 3, 'three attrition rows')
attr_sum = D('0.00')
for h, contracted, thr, pu, miss, sh, vat, tot in attr_rows:
    contracted, thr, pu, miss = int(contracted), int(thr), int(pu), int(miss)
    sh, vat, tot = (D(x.replace(',', '')) for x in (sh, vat, tot))
    attr_sum += tot
    ck(thr == contracted * 85 // 100, '%s threshold is 85%% of contracted, rounded down' % h)
    ck(miss == max(0, thr - pu), '%s shortfall = threshold - pickup' % h)
    ck(sh * miss + vat == tot and vat == (sh * miss * D('0.20')), '%s damages = shortfall x shoulder + VAT' % h)
ck(attr_sum == sum(D(a.replace(',', '')) for _, _, a, _ in hotel_rows),
   'attrition rows tie to the hotel split')

print('= bridge')
bridge_html = s.split('Bridge from the gross booked value')[1].split('</section>')[0]
bridge = re.findall(r'<tr class="(start|down|up|total)"><td>(.*?)</td><td class="num">(-?\+?[\d,.]+)</td>'
                    r'<td class="num">([\d,.]+)</td>', bridge_html)
ck(len(bridge) == 11, 'bridge has 11 rows: opening, six classes removed, re-pricing, cancellations, attrition, total (%d)' % len(bridge))
run = None
for kind, label, delta, running in bridge:
    dv = D(delta.replace(',', '').replace('+', ''))
    rv = D(running.replace(',', ''))
    if kind in ('start', 'total'):
        ck(dv == rv, '%s row states its own running total' % kind)
        run = rv
    else:
        ck(run + dv == rv, 'step "%s" moves the running total correctly' % label[:44])
        run = rv
ck(run == total_shown, 'bridge lands exactly on the headline total')
ck(D(bridge[0][3].replace(',', '')) == D('13900.00'), 'opening gross booked value is 13,900.00')

print('= svg geometry inside the viewBox')
for m in re.finditer(r'<svg viewBox="0 0 (\d+) (\d+)"', s):
    pass
for svg in re.findall(r'<svg viewBox="0 0 (\d+) (\d+)".*?</svg>', s, re.S):
    pass
svgs = re.findall(r'(<svg viewBox="0 0 (\d+) (\d+)".*?</svg>)', s, re.S)
for body, w, hh in svgs:
    w, hh = int(w), int(hh)
    ok = True
    for rx, ry, rw, rh in re.findall(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([-\d.]+)" height="([-\d.]+)"', body):
        rx, ry, rw, rh = float(rx), float(ry), float(rw), float(rh)
        if rx < 0 or ry < -1 or rx + rw > w + 1 or ry + rh > hh + 1 or rw < 0 or rh < 0:
            ok = False
    ck(ok, 'all bars fall inside the %dx%d drawing area' % (w, hh))
    ck('<title>' in body, 'bars carry hover titles')

print('= table controls')
ck(all(x in s for x in ('id="q"', 'id="fh"', 'id="fo"', 'id="fc"', 'th class="s"')),
   'search box, heading / hotel / corrected filters and sortable headings all present')
ck(len(re.findall(r'<th class="s[ "]', s)) == 7, 'all seven columns sortable')
ck(len(re.findall(r'<option value="[^"]+">', s)) >= 11, 'filter options populated')
corr = sum(1 for r in reg.values() if r['corrected'] == 'y')
ck(corr == 20, '20 lines flagged corrected, %d left untouched' % (29 - corr))
ck(('<b>%d corrected</b>' % corr) in s, 'header states the corrected count')

print()
print('TOTAL ON PAGE: GBP', total_shown)
print('FAILURES:', len(fail))
for f in fail:
    print(' -', f)
