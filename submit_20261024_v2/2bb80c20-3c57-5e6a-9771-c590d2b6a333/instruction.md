<!-- instruction-canary a79e430b-413e-5dd0-a6cf-caac9eb15ad8 -->
# Tidelines: closing the inbound loans

Tamsin Rook writing, registrar at Brennock Museum and Art Gallery. It is Monday
30 November 2026, about quarter past nine. The loans freeze for Tidelines, our
spring exhibition, fell on Friday evening, and I am away on a courier run until
Wednesday. I need you to close the inbound loans today, all of it: the loan
register, the trips and their couriers, the notices, and the paperwork.

None of this is mine to decide. Our loans procedure, LP-7, sets out when a loan
counts as confirmed, how the objects travel and who goes with them, and how
lenders and couriers are told; our insurance standard, IS-2, sets out what each
object is worth in pounds, how it is covered and what it costs us. Both point to
the records they rely on. Work out which papers actually speak for this
exhibition, apply them to the letter, and leave a trail the office can follow.

The loans base is half done. A volunteer keyed the register in early November,
there are thirteen trips requested with the shipping agent, and nobody has
recorded how any lender is being told. Some register rows will already be right;
leave those alone completely, because writing the same values back still counts
as touching them. Every other row needs the status, insured value, cover, premium
and trip reference the procedures give it, worded as they word it. The trip
records need the same attention: every vehicle that will travel, with its dates,
courier, number of objects, value and status, including any vehicle the
procedures call for that is not in the table yet. Look through each table before
you change anything in it.

Everything you need is to hand. The folders hold both editions of LP-7, IS-2, the
broker's rate schedules, the indemnity approval, the courier rota, a note for the
registrar's desk and every loan agreement as it came back to us, together with
sheets, plans and drafts that mostly have nothing to do with this. Lenders reach
us by email, on the loans desk and by the other routes the desk note lists. The
loans base, the HR system, the text account, the WhatsApp line, the calendars,
the mailbox and the team chat are all open to you.

People in #tidelines-loans have opinions about exchange rates, cover, vans,
couriers and which pictures are coming, and one or two of them are senior. A
post in the channel is not a record. Where anything anyone says, me included,
disagrees with the procedures and the papers, the papers win; tell me which one
settled it.

Once the register and the trips are right, send each courier's texts and each
lender's confirmation exactly as LP-7 words them, record on the lenders table how
each lender was told, book every arrival on the loading bay calendar as LP-7
describes, and send the broker the commercial schedule IS-2 asks for, by email to
fineart@keel-lantern.example with the subject "Tidelines commercial schedule".
Nothing else goes out, and nothing else in the base, the calendars or the
channels changes.

Leave three files directly in /workspace as well (not in a folder inside it), and open each
one again once it is saved:

1. `tidelines_loans.html`, a page that works offline and loads nothing from
   outside. Across the top, large, the total insured value of the confirmed
   loans, with the number of objects confirmed and the number not confirmed
   beside it. Under that, a bridge chart that starts from the lenders' agreed
   values, converted at each agreement's rate, for every object in the register,
   takes one step for each reason objects dropped out and one step for value
   revisions, and ends at that total; a chart of the insured value under the
   indemnity and under commercial cover; and a table of every object with its
   lender, status, insured value, cover, premium and trip, sortable on any column
   and with a box to filter it.
2. `tidelines_loans_dossier.md`, a section for each lender: what happened to each
   of its objects, which vehicle and courier it travels with, and the record that
   settled each point.
3. `tidelines_loans_reconciliation.csv`, one row per object in object order with
   its lender, currency, the agreed value you used, the agreement rate, the
   insured value, cover, premium, trip reference and status, followed by one row
   per vehicle with the combined insured value of what it carries.

Last, write me a closing note I can stand behind, and make it your final reply: the
whole note there, not a pointer to an earlier message or to the files. Give me the
total insured value of the confirmed loans, how much of it is under the indemnity
and how much under commercial cover, and the total premium. Say how many objects are confirmed and
how many are not, naming each one that is not and why. Walk me down the bridge,
each step with its amount and the running total. Tell me how many vehicles
travel, which consignments needed more than one, and who accompanies every
vehicle. Tell me which changes from lenders you applied and which you did not,
and on what record; how each lender is being told; and give me the id the base
gave every trip record you created. For each claim in the channel, say whether it
stands and which paper decides it.
