<!-- instruction-canary 5c2bbea2-3031-521d-a006-70a110705fbc -->
# Blackmoss: settling the Year 7 residential

It's Ruth Okafor, educational visits coordinator at Kestrel Ridge Academy. It is
Monday 8 February 2027, half past eight. Friday at four o'clock was the deadline
for the Year 7 residential to Blackmoss Outdoor Centre (10 to 12 March), and I am
out with Year 10 on their field day until tonight. Please settle the trip today:
who is going, what every family owes or is owed, who travels on which vehicle,
the centre's numbers, the refunds and the messages home.

Nothing here is a judgement call. EV-3, our educational visits policy, decides
who goes, how the vehicles are filled and how families are told; CR-2, our
charging and remissions policy, decides what each pupil owes, what counts as
paid and how refunds are made. Both name the records they depend on. Work out
which version of each paper actually governs this trip, apply it exactly, and
leave a trail Janet in finance could audit.

The trip register in the trips base was keyed by Janet last Monday from the card
payments report alone, before the deadline, so many lines will be wrong and some
will be right. A line that is already right must not be written to, not even with
the same values. Every other line needs the status, amount due, amount paid,
balance, refund due, vehicle and notice that the policies give it, worded as
they word them and with money to the penny. The vehicles table needs to show
what will actually travel. Read the register and the vehicles table before you
change either of them.

Everything you need is open to you. The folders hold both versions of each
policy, the hardship fund guidance, the letter to parents, the coach operator's
booking confirmation and the centre's, the cash and cheque book, the form lists
and a pile of school paperwork that mostly does not matter. Parents' forms are
in the online forms account and card payments in the online payments account.
Parents write to the trips inbox, the trips WhatsApp line and the office
helpdesk; the school's texts, my mailbox and the staff chat are there too.

The staff channel for the trip has views on deposits, discounts, coaches, refunds
and particular pupils, one of them from the deputy head. A message in the channel
is not a record. Where anyone, me included, says something the policies and the
records do not support, follow the papers and tell me which one decided it.

When the register is settled: make every refund the way CR-2 says, through the
online payments account and, where CR-2 says so, as refund requests in the trips
base; tell the family of every pupil who is not going exactly as EV-3 words it;
and send the centre the numbers EV-3 asks for, by email to
bookings@blackmoss-centre.example with the subject "Kestrel Ridge Year 7
numbers". Nothing else is sent, refunded or changed anywhere.

Save three files directly in /workspace (not in a subfolder) and reopen each one
after saving it:

1. `blackmoss_trip.html`, a page that works with no internet connection and
   fetches nothing. Across the top, large, the number of pupils going and the
   total of refunds due. Below that a bridge chart from the full price for every
   pupil in the register, through one step for sibling reductions, one for
   hardship remissions and one for the pupils not going, to the total due from
   the pupils who are going; a chart of how many pupils travel on each vehicle;
   and a table of every pupil with form, status, amount due, amount paid,
   balance, refund due and vehicle, sortable on every column and with a filter
   box.
2. `blackmoss_trip_dossier.md`, a section for each form saying what happened to
   every pupil in it and which record settled it, plus a section on refunds and
   one on vehicles.
3. `blackmoss_trip_reconciliation.csv`, one row per pupil in register order
   showing what was paid by card, in cash or by cheque, and by bank transfer, the
   amount due, the refund back to card, the refund by cheque, the status and the
   vehicle.

Finally, a closing note I can hand to the head. Write the whole note in your
closing message itself, not in an earlier message or only in a file. Tell me
how many pupils are going and how many are not, naming each pupil who is not and why; the total of refunds
due, how much goes back to cards and how much by cheque; the bridge, step by
step with the running total; what is travelling, how many pupils are on each
vehicle and which pupils, if any, are not on a coach; the numbers you sent the
centre; which changes from families and colleagues you acted on and which you
did not, and on what record; how each family not going was told; and the id of
every record you created. For each claim in the staff channel, say whether it
stands and which paper decides it.
