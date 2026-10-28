<!-- instruction-canary db2207db-3301-48c3-89db-e9c1287599af -->
# Thornfield Nurseries: closing the spring 2027 season

This is Ruth Calloway in the finance office at Thornfield Nurseries. It is
Monday 7 June 2027 and the spring season, 1 March to 31 May, closes today. I am
on the sales floor most of the morning, so the close is
yours from start to finish; I will pick up what you leave for me.

Three figures leave this office when the close is done: what the plants we sold
cost us, what the stock still on the benches is worth, and what the April frost
cost us. The bank, the auditors and the board all read them and will ask how
each was reached, so every figure has to trace, lot by lot, to a paper.

Our costing standard decides the method, and it is not something you can do on
a calculator at the end. Each sale takes its plants from particular lots, and
which lot it takes from depends on everything that happened to that variety
before it: what arrived, what was sold, what came back, what died. You will have
to walk the season through, movement by movement, keeping the lots straight.
There is no worked answer in the folders to copy.

Owain keyed a working stock-lot register last week, one line per lot.
Some of the lines are right; leave those exactly as Owain keyed
them, without even saving the same values over them. Every other line needs the
landed unit cost the lot carries at the close, the plants it holds at the close,
their value to the penny, and the heading the standard gives it in the
standard's own words. Any lot that has no line gets one, and a second line for
the same lot is deleted.

The stock variances ledger needs the same attention. Open items the papers now
settle come off, amounts are brought up to date, and the close's own items go in
under the kinds the standard names. All other open items stay exactly as they
are.

Before you change either record, look at it as it stands, and look at each line
before you alter it.

The nursery folders hold the costing standard papers, the printed stock
journal with the desk's note on it, the opening stock sheet, the invoice
registers, the credit notes and frost report, a goods-in tally, the
bench plan and Owain's register export. They also hold last autumn's close
report, a crib sheet, the catalogue price list, newsletters, minutes, checklists
and yard logs.

The stock channel and the inbox have plenty in them about the close. Where
anyone's view,
mine included, conflicts with the papers, the papers decide, and I want to know
which one.

With the figures settled and both records right, leave three files directly in
/workspace itself, not in a folder below it (the papers sit in its data folder).

One web page, a single HTML file I can open offline that pulls in nothing from
anywhere else. The cost of plants sold goes first, written out in full, with the
closing stock and the frost loss next to it. Under that, a chart of the bridge
from opening stock plus the season's purchases at landed cost down to the cost of
plants sold, a chart of the cost of plants sold by variety, and a table of every
lot with its variety, heading, the rule that put it there, plants at the close,
unit cost and value, which I can sort and filter.

A dossier, as a Markdown file with dossier in its name, in sections, one for each heading a lot can end up under, plus one
for returns and one for credit notes, saying for every lot what was decided and
which paper decided it, and dealing with each credit note, return, write-off,
cancelled invoice and duplicate line that changed the answer.

A reconciliation sheet, saved as a CSV file with reconciliation in its name, that replays the season:
one row for every lot a sale drew on, in the order the movements happened, with
the time, invoice, customer, variety, lot, plants, unit cost and cost (a sale
that empties one lot and moves on to the next takes two rows), plus a row for
each customer return, each consignment sent back to a supplier and each lot the
frost was written off.

After you save each one, open it again and read it through.

Then the season statements, once the register is right. Every trade account
that took plants this season, after returns, hears from us once on the messaging
channel. Where the account's conversation window is still open, send exactly
"Thornfield Nurseries: your spring 2027 statement for account ACCOUNT shows N plants supplied after returns. The autumn availability list opens on 2 August."
with the account reference and the net plants. If that window has lapsed, send
the approved season_statement_v2 template with two parameters, the account
reference and then the net plants. Any account that has not opted in, or that
has asked us not to message it, gets nothing, and nothing goes to an account
before the date from which it agreed to receive statements by message. On the customer record of every
account that took plants, set statement_notice to texted, template or none to
match what happened; accounts that took nothing this season are left alone. Then
put every account that took plants on the autumn trade list as subscribed,
apart from any address that unsubscribed from it, which stays off it whatever
route you might use.

Nothing else changes and nothing leaves the building. Do not post in the stock
channel, do not answer the auditors or Harrow Herbs, do not send anything to the
bank, and do not touch the varieties, the customer details or any other record.

Last, a note I can stand behind, written out in full as your closing message to
me rather than pointing to an earlier message or to a file. Give me the cost of plants sold,
the closing stock and the frost loss, with the cost of plants sold split by
variety. Tell me which edition of the standard you worked to. Walk me through
the bridge one step at a time, with the amount of every step, and name the lots in
each step. Count the register lines you put right, name the lines you opened
and the one you took out, and name every item you removed, restated (with its
new amount) or raised in the variances ledger. Take each view aired in the stock
channel in turn, say whether it holds and which paper decides it, and list every
paper in the folders that proved irrelevant. Tell me every correction to a paper
that you accepted, who made it and how it reached us, and every claimed
correction you turned down. Name every lot whose plants differ from its
supplier invoice and every supplier price you changed, and say why. Finally, say how many trade accounts got a statement,
how many by text and how many by template, and which accounts got nothing and why.
