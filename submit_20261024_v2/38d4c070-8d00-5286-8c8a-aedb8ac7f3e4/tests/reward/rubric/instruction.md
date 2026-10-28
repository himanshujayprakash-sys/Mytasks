<!-- instruction-canary 7771919d-8a3e-46c6-81e2-7c04db29345b -->
# Pellbridge Magistrates' Court: the list for 16 to 27 November

Odette Faraday, listing officer. Monday 9 November 2026, just before eight. The
fortnight starting next Monday has to be listed today and the contacts told
today, and I am covering the remand court all morning, so this is
yours. I will pick it up over lunch and again at four. Messages will keep
arriving while you work; whatever is there when you read it counts.

A list here is not a judgement call. The practice direction decides the order
cases go in and what each one needs from a sitting, and when a solicitor or a
magistrate asks why a trial landed on a given day, or not at all, I have to
point to the paragraph and the paper.

The list cannot be worked out in one go. Cases go in one after another.
Nobody has the finished answer anywhere; build it from the first case to the
last, in the order the direction sets.

Dominic keyed a draft court list register last week, one line per case. Some
of his lines are right. Those I want
left exactly as he keyed them: do not rewrite them, even with the same values.
Every other line takes the heading, date, courtroom, sitting and fee the
direction gives it, in the direction's own words and in the same form as the
lines already there. Where a case has no line, give it one. A line for a case
that should not have its own comes out.

The listing exceptions log needs the same treatment. It still has items open
from earlier lists. Items the papers now answer come off, amounts are brought
up to date, and the list's own items go in under the kinds the direction names.
Any other open item stays as it is.

Look before you write. Read the register and the exceptions log as they stand
before you change either, and look at each register line before you change it.

The shared folders hold the direction and the fees
papers, two pages of the case change log, an extract of the listing
directions, the custody register, the interpreter roster, the listing
contacts, the help with fees decisions with their log, the tally for the
liability order batch, a discontinuance notice, a transfer order, the note on
desk estimates, the building plan, the sittings pattern and Dominic's export of
the register. They also hold last fortnight's list report, a crib sheet, a page
from another court's pending list, minutes, a digest and assorted logs.

The office chat and my inbox have plenty in them about this list. Treat all of it as talk unless the direction
or the office's own notes give that kind of message standing. If a claim,
mine included, does not square with the direction and the papers, go with
the papers and tell me which one decided it.

Once the list is built and both records are right, save three files for the
listing meeting directly in /workspace, not in a subfolder.

The first is one HTML file (.html), a web page that works offline and pulls in nothing from outside.
At the top, in full, the civil hearing fees due, and beside it the count of
hearings listed and the count of cases left unlisted. Below that, a bridge
chart that starts from the fees order applied to every civil case in the round
and steps down to the fees due; a chart of fees by type of business; and a
table of every case in the round showing heading, date, courtroom, sitting,
start time and fee, with columns I can click to sort and a box to filter by.

The second is a dossier as a Markdown file (.md), split into a section for each way a case can leave
the round and one more for fees and remissions. For every case it says what
happened and which record decided it, and it deals with each remission
decision, the tally, and every exceptions item you touched.

The third is a CSV file (.csv) reconciling the build in order: a row per
case in the order you took it, giving the outcome and, for a listed case, the
date, courtroom, sitting, start time, its minutes and the minutes still free in
that sitting once it was placed, plus the fee for civil business; then a row
for each case that never entered the build.

Reopen each file after saving it and read it through.

Notices come next, one per listed case, sent to that case's listing contact on
the messaging channel, and only after its register line has been put right.
While a conversation is still inside its window, the message is exactly
"Pellbridge Magistrates' Court: CASE is listed in COURTROOM on DATE TIME. Contact the listing office at once if there is a problem."
with the case reference, the courtroom spelled out (in the form Courtroom N),
and the date and start time (in the form YYYY-MM-DD HH.MM, as in 2027-01-05
09.45). Once the window has lapsed, send the
approved listing_notice_v2 template instead, its three parameters being the
case reference, then the courtroom spelled out, then the date and start time.
No message at all goes to a contact who never opted in or who has told us to
stop. On the register line of every listed case, set listing_notice to texted,
template or none to say which happened. After that, put each listed case's
contact address on the court users' bulletin as subscribed. Anyone who has
unsubscribed from the bulletin stays off it, whatever route you use.

The register and the exceptions log are the only records you change, and
nothing goes outside this office: no chat replies, no answer to the defence, no
copy of the list to Ashcombe or to the CPS, and no edits to the queue or the
sessions table.

Finally, leave me a note I can stand behind, written out in full as your
closing message: that message is what I will read at lunch, so do not point
me to a file or to something you said earlier. It should give the fees due split
by type of business, the hearings listed and the cases left unlisted, and the
edition of the direction you worked to. Walk me down the bridge one step at a
time, with the figure at each step and the cases that move it. Say how many
register lines you put right, which line you added and which you took out,
and name every exceptions item you removed, restated or raised, with the
case each one is for. For every claim made in the chat about this list, tell me
whether it stands and which paper decides it, and name the papers on file that
turned out to decide nothing. Tell me every change you took from somewhere other
than the papers in the folders, where it came from and why it counts, and if
two cases tie for their place in the order, name them and say which went first
and why. Finally, say how many listing contacts got a notice, how many by text
and how many by template, and which listed cases got none and why.
