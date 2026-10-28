# October 2026 repairs compensation run - evidence dossier

Thornbeck Homes. Run `2026-10`, worked on Monday 2 November 2026 by the repairs performance officer. Every job completed in October 2026 was assessed under the **Repairs Service Standard, 4th edition (2026)**, which is in force for every repair completed on or after 1 April 2026.

- Jobs completed in October 2026 and assessed in this run: **86**
- Awards: **45**, total **GBP 1,076.00**
- Late completion GBP 866.00 + missed appointments GBP 225.00 - GBP 15.00 reduction for the per-job limit = GBP 1,076.00
- Paid by bank transfer GBP 930.00 (39 awards); credited to rent accounts GBP 146.00 (6 awards)
- Contractor recharges: 11 appointments at GBP 25.00 = GBP 275.00

## 1. Sources that changed an outcome

These are the jobs where a source other than the keyed planner/portal record decided the answer. Each is listed with the rule it turns on.

### RJ-25241 - 32 Beckside (T-12801, Ewan Oldroyd) - clock start moved

- Keyed `reported_on` 2026-10-12 (the day the job was raised on ticket 72475).
- Out-of-hours voicemail transcript, 2026-10-07 21:14, caller +447700900539: *"this is Ewan Oldroyd from 32 Beckside. Water is coming through my kitchen ceiling from the bathroom upstairs..."* +447700900539 is the mobile on T-12801's tenant record and the address and defect match the job ("Leak through kitchen ceiling from bathroom above").
- The out-of-hours line, including its voicemail, is a monitored channel (s.2). Under s.4.1 the clock starts on the day of the tenant's earliest report, so the clock start is **2026-10-07**, not 2026-10-12.
- Effect: urgent target 2026-10-14 instead of 2026-10-19; completed 2026-10-19; 3 working days late; **GBP 16.00 awarded where the keyed date would have given no award**.

### RJ-25243 - 2 Cragg View (T-11915, Fergus Fox) - portal no-show overturned

- AP-51992 (2026-10-13, Marrick) is keyed `Missed - operative did not attend`, note "No show recorded from the contractor's portal".
- Zendesk ticket 72480, internal note of 2026-10-12 19:46: *"Fergus Fox rang the out-of-hours line at 19:40 to cancel tomorrow morning's Marrick visit (AP-51992) - a family member has a hospital appointment... The contractor's portal may still show this as a no-show; it was the tenant's cancellation."* Rebooked for 20 October (note of 2026-10-14 10:12).
- Standard s.9.2 and Annex B2: a contact centre note made on the ticket at the time governs over an outcome code keyed afterwards from the contractor's portal.
- Effect: **no missed-appointment payment and no Schedule D recharge** for AP-51992. Under s.6.3 the tenant's cancellation moves the target later by the working days from the day after the cancelled appointment up to and including the next appointment (2026-10-14 to 2026-10-20 = 5 working days), so the routine target moves from 2026-10-12 to 2026-10-19. Completed 2026-10-23: 4 working days late, GBP 18.00.

### RJ-25364 - 21 Millrace Road (T-11933, Paula Netherwood) - 'attended' overturned

- AP-52156 (2026-10-14 AM, Marrick, Lee Carver) is keyed `Attended`, note "Work completed".
- Zendesk ticket 72552, internal note of 2026-10-14 09:30: *"Tenant rang to ask where the plumber was - she waited in all morning. Apologised; Marrick say the van broke down. Rebooked."*
- Corroborated by Marrick's email of 2026-10-15, subject "Van breakdown on 14 October": *"Sorry again about the visits we missed when the van broke down... We know these come back to us under the schedule."*
- Standard s.9.2: the contact centre note made at the time governs over the outcome code keyed afterwards. Under s.6.1 this is a missed appointment.
- Effect: **+GBP 15.00 to the tenant and a GBP 25.00 Schedule D recharge to Marrick**. The job is still completed on 2026-10-14 (s.9.1, the signed return RET-25364).

### RJ-25250 and RJ-25258 - Direct Works appointments auto-marked attended

- AP-52008 (RJ-25250, 2026-10-15) and AP-52014 (RJ-25258, 2026-10-13) are both keyed `Attended` with no operative note, operative Dev Okafor.
- BambooHR time-off request `tor-tbh001`: Dev Okafor (emp-tbh10), Vacation, **approved**, 2026-10-12 to 2026-10-16.
- Supporting: Martin Crowther's email of 2026-10-09 ("With Dev on leave for the week of the 12th...") and Lucy Fairburn in #repairs-planning ("Moved most of Dev's slots for the week of the 12th across to Tomasz and Precious") - *most*, not all.
- Annex B1: the planner marks every Direct Works appointment "Attended" at 18:00 unless the operative raises an exception from their handset, and an operative on approved leave does not raise one. Where the booked operative had approved leave that day the appointment did not take place and is a missed appointment under s.6.1.
- Effect: **GBP 15.00 on each job**. RJ-25250 would otherwise have had no award at all (completed on target). Direct Works is not party to the responsive repairs contract (Schedule D3), so there is **no recharge** for these two.

### RJ-25503 - 23 Beckside (T-12704, Jamal Shackleton) - correction keyed during the run

- AP-52307 (2026-10-26, Ravensgill, Kyle Moss) was keyed `Attended` when the run was opened.
- Re-read during the run (as the run procedure requires) it reads `Missed - operative did not attend`, keyed by Helen Mortimer, note "Re-keyed 2 Nov from Ravensgill's signed job sheet: the operative did not attend; keyed as attended in error".
- The run procedure says the latest row counts as it stands when each line of the run is written. The award line was written after the correction.
- Effect: **+GBP 15.00 to the tenant (GBP 12.00 late + GBP 15.00 = GBP 27.00) and a GBP 25.00 recharge to Ravensgill**.

### RJ-25320 - Flat 18, Fold Yard (T-11544, Chantelle Hussain) - return posted during the run

- At the start of run day the job read `Awaiting contractor return` and RET-25320 was "Pending - not yet posted".
- Saving the first award row opened the run; the contractors' portal then posted its held returns (run procedure, "Opening the run"; Josh Kendall in #repairs-planning: "Kestle say their portal returns post at month end when the run opens, same as always").
- On the re-read, RET-25320 is `Posted`, signed by Pete Kestle, **completed_on 2026-10-29**, posted 2026-11-02. Under s.9.1 the job is completed on the date on the signed return, so it falls in the October run.
- Effect: a 45th award of **GBP 49.00** (12 working days late GBP 34.00 + 1 missed appointment GBP 15.00) and a **GBP 25.00 recharge to Kestle Roofing** for AP-52083 (2026-10-02).

### RJ-25374 - Flat 40, Gilstead Walk (T-12955, Quentin Fox) - late cancellation by us

- AP-52452 (2026-10-01) is keyed `Cancelled by us - late notice`, note "Cancelled by the contractor at 08:10 the same morning".
- s.6.1: an appointment we cancelled less than 24 hours before it was due is a missed appointment; Schedule D1 says the same for recharges. (By contrast AP-52229, AP-52400, AP-52188 and AP-52107 are `Cancelled by us - 24h+ notice`, which under s.6.2 is not a missed appointment and does not change the target.)
- Effect: **GBP 15.00 to the tenant and a GBP 25.00 recharge to Ravensgill**.

### RJ-25548 - 18 Millrace Road (T-11720, Orla Hirst) - notice channel

- Twilio inbound SMS, 2026-09-29 11:04 from +447700900955 to the repairs line (+44 7700 900010), body "Stop". +447700900955 is T-11720's mobile.
- Tenant communications policy s.2.1/2.3: STOP to any of our text numbers is an opt-out from all Thornbeck texts, and we never text an opted-out tenant, "not even to confirm good news".
- The tenant record holds no email address, so policy s.3.2 puts the notice by **letter**. `notice_channel` on CA-2026-10-33 is recorded as `Letter`; no text was sent.
- Not an opt-out: +447700900451 (T-12507, Bethany Bairstow) texted "Can you stop by after 2pm instead?" on 2026-10-20 - the word used in an ordinary sentence, policy s.2.2. She was texted as normal for CA-2026-10-10.

### Jobs excluded from compensation by scope (s.3.2)

Assessed and recorded as *No award (Oct 2026 run)* because of what they are, not how they ran:

| Job | Address | scheme_note | Would otherwise have been |
|---|---|---|---|
| RJ-25268 | Flat 4, Fold Yard | Communal area | 5 working days late |
| RJ-25270 | Flat 8, Rowan Court | Communal area | 21 working days late |
| RJ-25278 | 23 Dyehouse Street | Recharge - tenant damage | 5 working days late |
| RJ-25282 | Flat 13, Larch House | Recharge - tenant damage | 18 working days late |

### Payment route - which arrears list applies (s.8.2)

Section 8.2 says to use the most recent arrears list circulated before the run, and that an earlier list is replaced by a later one. Two lists were in the repairs inbox:

1. Philippa Drake, "Income update - week ending 23 October", 2026-10-23 16:42 - superseded.
2. Philippa Drake, "Income update - week ending 30 October", 2026-10-30 16:55, plus her correction "Re: Income update - week ending 30 October" at 2026-10-30 17:48: remove T-12839 (balance cleared), add T-11486 (direct debit returned unpaid).

The list used is therefore: T-10403, T-10416, T-10424, T-10433, T-10443, T-11486, T-11683, T-11906, T-11933, T-12701, T-13132.

Consequences in this run:

- **T-11486** (RJ-25585, GBP 22.00) is on the corrected list only - paid as a **rent account credit**.
- **T-12839** (RJ-25603, GBP 22.00) was on the earlier list and on the 16:55 list but was taken off at 17:48 - paid by **bank transfer**.
- **T-10464** and **T-11770** were on the 23 October list but not the 30 October one. T-11770 has an award (RJ-25439, GBP 12.00) and is paid by **bank transfer**.
- The other rent-account credits are T-11683 (RJ-25430), T-11906 (RJ-25565), T-11933 (RJ-25364), T-12701 (RJ-25436) and T-13132 (RJ-25534), all of which appear on both lists.

### The SLA dashboard export was not used

`SLA_breach_dashboard_export_Oct2026.csv` disagrees with this run in many places (for example it shows RJ-25243 as 9 days over with 1 missed appointment). Annex B3 says the export works from the dates and codes keyed into the planner, is a planning view, and is not used to decide compensation; Gavin Holroyd said the same in #repairs-performance. It has been ignored.

## 2. The awards

Every award, with the dates it rests on and the arithmetic. Late completion is GBP 10.00 once plus GBP 2.00 for each day after target up to and including the completion day (calendar days for emergencies, working days otherwise), capped at GBP 50.00 a job (s.5.3/5.4). Missed appointments are GBP 15.00 each (s.6.1). The award for one job never exceeds GBP 80.00 (s.7.1).

### CA-2026-10-01 - RJ-25241 - 32 Beckside

- Tenant: Ewan Oldroyd (T-12801). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-10-07 (moved from the keyed report date - see section 1); target 2026-10-14; completed 2026-10-19.
- Late completion: 3 working days after target. GBP 10.00 + 3 x GBP 2.00 = GBP 16.00 -> **GBP 16.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 16.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Clock start moved to the out-of-hours voicemail of 2026-10-07 (see section 1).

### CA-2026-10-02 - RJ-25243 - 2 Cragg View

- Tenant: Fergus Fox (T-11915). Contractor: Marrick Plumbing & Heating. Priority: Routine.
- Dates: clock start 2026-09-14; target 2026-10-19 (base target 2026-10-12, moved by s.6.3); completed 2026-10-23.
  - AP-51992 on 2026-10-13 was a tenant cancellation or no-access visit; the next appointment was AP-51996 on 2026-10-20, so the target moves 5 working days (s.6.3).
- Late completion: 4 working days after target. GBP 10.00 + 4 x GBP 2.00 = GBP 18.00 -> **GBP 18.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 18.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Portal no-show overturned by the contact centre note; target moved 5 working days by the tenant's cancellation (see section 1).

### CA-2026-10-03 - RJ-25250 - Flat 29, Gilstead Walk

- Tenant: Jodie Gaunt (T-13317). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-10-09; target 2026-10-16; completed 2026-10-16.
- Late completion: completed on or before target - **GBP 0.00**.
- Missed appointment AP-52008 (2026-10-15, Direct Works, Dev Okafor): Standard s.9.3 / Annex B1. BambooHR tor-tbh001: Dev Okafor on approved leave 2026-10-12 to 2026-10-16, so nobody attended; the planner auto-marks Direct Works appointments attended at 18:00.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 15.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Missed appointment found through Annex B1 (operative on approved leave).

### CA-2026-10-04 - RJ-25258 - Flat 33, Gilstead Walk

- Tenant: Farah Dobson (T-11304). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-09-09; target 2026-10-07; completed 2026-10-20.
- Late completion: 9 working days after target. GBP 10.00 + 9 x GBP 2.00 = GBP 28.00 -> **GBP 28.00**.
- Missed appointment AP-52014 (2026-10-13, Direct Works, Dev Okafor): Standard s.9.3 / Annex B1. BambooHR tor-tbh001: Dev Okafor on approved leave 2026-10-12 to 2026-10-16, so nobody attended; the planner auto-marks Direct Works appointments attended at 18:00.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 43.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Missed appointment found through Annex B1 (operative on approved leave).

### CA-2026-10-05 - RJ-25264 - 22 Millrace Road

- Tenant: Owen Sutcliffe (T-10730). Contractor: Marrick Plumbing & Heating. Priority: Routine.
- Dates: clock start 2026-08-03; target 2026-09-01; completed 2026-10-28.
- Late completion: 41 working days after target. GBP 10.00 + 41 x GBP 2.00 = GBP 92.00 (capped at GBP 50.00 by s.5.4) -> **GBP 50.00**.
- Missed appointment AP-52022 (2026-09-08, Marrick Plumbing & Heating, Lee Carver): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointment AP-52028 (2026-09-22, Marrick Plumbing & Heating, Jordan Platt): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointment AP-52031 (2026-10-06, Marrick Plumbing & Heating, Jordan Platt): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 3 x GBP 15.00 = **GBP 45.00**.
- GBP 50.00 + GBP 45.00 = GBP 95.00, reduced by GBP 15.00 to the GBP 80.00 per-job limit (s.7.1).
- **Total: GBP 80.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Three Marrick no-shows; both caps bite (see the arithmetic below).

### CA-2026-10-06 - RJ-25288 - Flat 14, Spinner Court

- Tenant: Tamsin Walsh (T-11048). Contractor: Marrick Plumbing & Heating. Priority: Emergency.
- Dates: clock start 2026-10-17; target 2026-10-18; completed 2026-10-19.
- Late completion: 1 calendar day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-07 - RJ-25297 - 28 Cragg View

- Tenant: Una Kaye (T-12231). Contractor: Castleton Electrical Services. Priority: Emergency.
- Dates: clock start 2026-10-09; target 2026-10-10; completed 2026-10-12.
- Late completion: 2 calendar days after target. GBP 10.00 + 2 x GBP 2.00 = GBP 14.00 -> **GBP 14.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 14.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-08 - RJ-25320 - Flat 18, Fold Yard

- Tenant: Chantelle Hussain (T-11544). Contractor: Kestle Roofing. Priority: Routine.
- Dates: clock start 2026-09-15; target 2026-10-13; completed 2026-10-29.
- Late completion: 12 working days after target. GBP 10.00 + 12 x GBP 2.00 = GBP 34.00 -> **GBP 34.00**.
- Missed appointment AP-52083 (2026-10-02, Kestle Roofing, Ollie Grange): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 49.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Brought into the run when the contractor's return posted on run day (s.9.1).

### CA-2026-10-09 - RJ-25330 - Flat 7, Fold Yard

- Tenant: Wendy Oates (T-12815). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-08-26; target 2026-09-24; completed 2026-10-07.
- Late completion: 9 working days after target. GBP 10.00 + 9 x GBP 2.00 = GBP 28.00 -> **GBP 28.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 28.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-10 - RJ-25335 - 10 Dyehouse Street

- Tenant: Bethany Bairstow (T-12507). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-09-10; target 2026-10-08; completed 2026-10-28.
- Late completion: 14 working days after target. GBP 10.00 + 14 x GBP 2.00 = GBP 38.00 -> **GBP 38.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 38.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-11 - RJ-25338 - 36 Weavers Rise

- Tenant: Hollie Dewhirst (T-13183). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-09-17; target 2026-10-15; completed 2026-10-20.
- Late completion: 3 working days after target. GBP 10.00 + 3 x GBP 2.00 = GBP 16.00 -> **GBP 16.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 16.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-12 - RJ-25343 - 16 Ouzel Close

- Tenant: Fiona Eastwood (T-13002). Contractor: Ravensgill Building Maintenance. Priority: Routine.
- Dates: clock start 2026-09-22; target 2026-11-03 (base target 2026-10-20, moved by s.6.3); completed 2026-10-21.
  - AP-52130 on 2026-10-07 was a tenant cancellation or no-access visit; the next appointment was AP-52133 on 2026-10-21, so the target moves 10 working days (s.6.3).
- Late completion: completed on or before target - **GBP 0.00**.
- Missed appointment AP-52450 (2026-10-06, Ravensgill Building Maintenance, Darren Beaumont): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 15.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Target moved 10 working days by the no-access visit of 2026-10-07 (s.6.3); the award is the missed appointment of 2026-10-06 only.

### CA-2026-10-13 - RJ-25358 - 40 Millrace Road

- Tenant: Vikram Jowett (T-11010). Contractor: Ravensgill Building Maintenance. Priority: Routine.
- Dates: clock start 2026-09-25; target 2026-10-23; completed 2026-10-26.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-14 - RJ-25364 - 21 Millrace Road

- Tenant: Paula Netherwood (T-11933). Contractor: Marrick Plumbing & Heating. Priority: Routine.
- Dates: clock start 2026-09-08; target 2026-10-06; completed 2026-10-14.
- Late completion: 6 working days after target. GBP 10.00 + 6 x GBP 2.00 = GBP 22.00 -> **GBP 22.00**.
- Missed appointment AP-52156 (2026-10-14, Marrick Plumbing & Heating, Lee Carver): Standard s.9.2. Zendesk 72552, contact centre note 2026-10-14 09:30: the tenant rang to ask where the plumber was after waiting in all morning; Marrick's van had broken down (Marrick email 2026-10-15 'Van breakdown on 14 October'). The 'Attended' code was keyed afterwards.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 37.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.
- Note: 'Attended' overturned by the contact centre note of 2026-10-14 (see section 1).

### CA-2026-10-15 - RJ-25368 - 22 Tenter Lane

- Tenant: Lewis Eastwood (T-11817). Contractor: Castleton Electrical Services. Priority: Routine.
- Dates: clock start 2026-09-22; target 2026-10-20; completed 2026-10-28.
- Late completion: 6 working days after target. GBP 10.00 + 6 x GBP 2.00 = GBP 22.00 -> **GBP 22.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 22.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-16 - RJ-25374 - Flat 40, Gilstead Walk

- Tenant: Quentin Fox (T-12955). Contractor: Ravensgill Building Maintenance. Priority: Urgent.
- Dates: clock start 2026-09-25; target 2026-10-02; completed 2026-10-08.
- Late completion: 4 working days after target. GBP 10.00 + 4 x GBP 2.00 = GBP 18.00 -> **GBP 18.00**.
- Missed appointment AP-52452 (2026-10-01, Ravensgill Building Maintenance, Darren Beaumont): cancelled by us with less than 24 hours' notice (s.6.1).
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 33.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: AP-52452 cancelled by the contractor at 08:10 on the day = missed (s.6.1).

### CA-2026-10-17 - RJ-25387 - 34 Beckside

- Tenant: Janet Dobson (T-11266). Contractor: Castleton Electrical Services. Priority: Routine.
- Dates: clock start 2026-09-30; target 2026-10-28; completed 2026-10-26.
- Late completion: completed on or before target - **GBP 0.00**.
- Missed appointment AP-52444 (2026-10-13, Castleton Electrical Services, Anil Desai): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 15.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Completed inside the moved target; the award is the missed appointment only.

### CA-2026-10-18 - RJ-25409 - 29 Cragg View

- Tenant: Hollie Rushworth (T-12332). Contractor: Ravensgill Building Maintenance. Priority: Urgent.
- Dates: clock start 2026-10-15; target 2026-10-22; completed 2026-10-26.
- Late completion: 2 working days after target. GBP 10.00 + 2 x GBP 2.00 = GBP 14.00 -> **GBP 14.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 14.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-19 - RJ-25429 - Flat 46, Larch House

- Tenant: Hamid Ackroyd (T-12874). Contractor: Castleton Electrical Services. Priority: Routine.
- Dates: clock start 2026-10-01; target 2026-10-29; completed 2026-10-22.
- Late completion: completed on or before target - **GBP 0.00**.
- Missed appointment AP-52439 (2026-10-12, Castleton Electrical Services, Mark Tunstall): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 15.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Completed inside target; the award is the missed appointment only.

### CA-2026-10-20 - RJ-25430 - 29 Dyehouse Street

- Tenant: Jodie Fawcett (T-11683). Contractor: Marrick Plumbing & Heating. Priority: Urgent.
- Dates: clock start 2026-10-05; target 2026-10-12; completed 2026-10-20.
- Late completion: 6 working days after target. GBP 10.00 + 6 x GBP 2.00 = GBP 22.00 -> **GBP 22.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 22.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.

### CA-2026-10-21 - RJ-25432 - 45 Millrace Road

- Tenant: Carys Riaz (T-11832). Contractor: Castleton Electrical Services. Priority: Routine.
- Dates: clock start 2026-09-28; target 2026-10-26; completed 2026-10-27.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-22 - RJ-25436 - Flat 3, Rowan Court

- Tenant: Lewis Ogden (T-12701). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-10-01; target 2026-10-29; completed 2026-10-19.
- Late completion: completed on or before target - **GBP 0.00**.
- Missed appointment AP-52459 (2026-10-12, Direct Works, Tomasz Wren): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 15.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.
- Note: Completed inside target; the award is the missed appointment only. Direct Works no-show, so no recharge (Schedule D3).

### CA-2026-10-23 - RJ-25439 - Flat 25, Spinner Court

- Tenant: Hollie Uttley (T-11770). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-10-12; target 2026-10-19; completed 2026-10-20.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-24 - RJ-25447 - 33 Weavers Rise

- Tenant: Saeed Bairstow (T-10873). Contractor: Marrick Plumbing & Heating. Priority: Routine.
- Dates: clock start 2026-08-18; target 2026-09-16; completed 2026-10-05.
- Late completion: 13 working days after target. GBP 10.00 + 13 x GBP 2.00 = GBP 36.00 -> **GBP 36.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 36.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-25 - RJ-25451 - Flat 4, Gilstead Walk

- Tenant: Craig Illingworth (T-12581). Contractor: Marrick Plumbing & Heating. Priority: Urgent.
- Dates: clock start 2026-09-22; target 2026-09-29; completed 2026-10-05.
- Late completion: 4 working days after target. GBP 10.00 + 4 x GBP 2.00 = GBP 18.00 -> **GBP 18.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 18.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-26 - RJ-25457 - Flat 39, Gilstead Walk

- Tenant: Yasmin Netherwood (T-12110). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-10-13; target 2026-10-20; completed 2026-10-26.
- Late completion: 4 working days after target. GBP 10.00 + 4 x GBP 2.00 = GBP 18.00 -> **GBP 18.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 18.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-27 - RJ-25483 - Flat 7, Gilstead Walk

- Tenant: Sabina Ackroyd (T-11689). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-09-25; target 2026-10-02; completed 2026-10-05.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-28 - RJ-25503 - 23 Beckside

- Tenant: Jamal Shackleton (T-12704). Contractor: Ravensgill Building Maintenance. Priority: Urgent.
- Dates: clock start 2026-10-21; target 2026-10-28; completed 2026-10-29.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointment AP-52307 (2026-10-26, Ravensgill Building Maintenance, Kyle Moss): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 27.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Missed appointment added by the contract manager's correction on run day.

### CA-2026-10-29 - RJ-25505 - 41 Millrace Road

- Tenant: Kofi Lumb (T-10494). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-09-24; target 2026-10-01; completed 2026-10-06.
- Late completion: 3 working days after target. GBP 10.00 + 3 x GBP 2.00 = GBP 16.00 -> **GBP 16.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 16.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-30 - RJ-25509 - 17 Weavers Rise

- Tenant: Vince Moorhouse (T-10598). Contractor: Castleton Electrical Services. Priority: Routine.
- Dates: clock start 2026-08-24; target 2026-09-22; completed 2026-10-05.
- Late completion: 9 working days after target. GBP 10.00 + 9 x GBP 2.00 = GBP 28.00 -> **GBP 28.00**.
- Missed appointment AP-52434 (2026-09-14, Castleton Electrical Services, Anil Desai): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 43.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-31 - RJ-25534 - Flat 20, Rowan Court

- Tenant: Yasmin Rushworth (T-13132). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-09-30; target 2026-10-07; completed 2026-10-08.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.

### CA-2026-10-32 - RJ-25542 - 33 Millrace Road

- Tenant: Jamal Jessop (T-13079). Contractor: Kestle Roofing. Priority: Routine.
- Dates: clock start 2026-09-14; target 2026-10-12; completed 2026-10-26.
- Late completion: 10 working days after target. GBP 10.00 + 10 x GBP 2.00 = GBP 30.00 -> **GBP 30.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 30.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-33 - RJ-25548 - 18 Millrace Road

- Tenant: Orla Hirst (T-11720). Contractor: Ravensgill Building Maintenance. Priority: Routine.
- Dates: clock start 2026-08-27; target 2026-09-25; completed 2026-10-08.
- Late completion: 9 working days after target. GBP 10.00 + 9 x GBP 2.00 = GBP 28.00 -> **GBP 28.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 28.00**, paid by bank transfer (s.8.1). Notice: letter.
- Note: Tenant has opted out of texts; notice by letter (see section 1).

### CA-2026-10-34 - RJ-25565 - 39 Millrace Road

- Tenant: Leanne Tolson (T-11906). Contractor: Ravensgill Building Maintenance. Priority: Routine.
- Dates: clock start 2026-08-31; target 2026-09-28; completed 2026-10-16.
- Late completion: 14 working days after target. GBP 10.00 + 14 x GBP 2.00 = GBP 38.00 -> **GBP 38.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 38.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.

### CA-2026-10-35 - RJ-25569 - Flat 27, Rowan Court

- Tenant: Zara Tasker (T-11170). Contractor: Ravensgill Building Maintenance. Priority: Urgent.
- Dates: clock start 2026-10-19; target 2026-10-26; completed 2026-10-29.
- Late completion: 3 working days after target. GBP 10.00 + 3 x GBP 2.00 = GBP 16.00 -> **GBP 16.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 16.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-36 - RJ-25574 - 29 Weavers Rise

- Tenant: Danuta Mahmood (T-12519). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-09-14; target 2026-10-12; completed 2026-10-26.
- Late completion: 10 working days after target. GBP 10.00 + 10 x GBP 2.00 = GBP 30.00 -> **GBP 30.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 30.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-37 - RJ-25585 - Flat 13, Gilstead Walk

- Tenant: Gareth Umpleby (T-11486). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-09-22; target 2026-09-29; completed 2026-10-07.
- Late completion: 6 working days after target. GBP 10.00 + 6 x GBP 2.00 = GBP 22.00 -> **GBP 22.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 22.00**, paid by rent account credit because the tenant's rent account is in arrears on the Income team's list of 30 October (s.8.2). Notice: text.
- Note: Rent account credit - T-11486 added to the arrears list by the 17:48 correction.

### CA-2026-10-38 - RJ-25592 - 23 Millrace Road

- Tenant: Rhian Kaye (T-13327). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-09-29; target 2026-10-06; completed 2026-10-08.
- Late completion: 2 working days after target. GBP 10.00 + 2 x GBP 2.00 = GBP 14.00 -> **GBP 14.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 14.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-39 - RJ-25597 - Flat 19, Spinner Court

- Tenant: Kieran Bairstow (T-10703). Contractor: Marrick Plumbing & Heating. Priority: Urgent.
- Dates: clock start 2026-09-29; target 2026-10-06; completed 2026-10-07.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-40 - RJ-25603 - 11 Beckside

- Tenant: Ivor Fox (T-12839). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-09-11; target 2026-10-09; completed 2026-10-19.
- Late completion: 6 working days after target. GBP 10.00 + 6 x GBP 2.00 = GBP 22.00 -> **GBP 22.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 22.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Bank transfer - T-12839 removed from the arrears list by the 17:48 correction.

### CA-2026-10-41 - RJ-25624 - 12 Weavers Rise

- Tenant: Kieran Exley (T-12263). Contractor: Direct Works. Priority: Routine.
- Dates: clock start 2026-08-18; target 2026-09-16; completed 2026-10-05.
- Late completion: 13 working days after target. GBP 10.00 + 13 x GBP 2.00 = GBP 36.00 -> **GBP 36.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 36.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-42 - RJ-25628 - 2 Ouzel Close

- Tenant: Kofi Ramsden (T-11282). Contractor: Marrick Plumbing & Heating. Priority: Urgent.
- Dates: clock start 2026-10-02; target 2026-10-09; completed 2026-10-12.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-43 - RJ-25637 - 49 Millrace Road

- Tenant: Vikram Priestley (T-10592). Contractor: Kestle Roofing. Priority: Urgent.
- Dates: clock start 2026-10-09; target 2026-10-16; completed 2026-10-19.
- Late completion: 1 working day after target. GBP 10.00 + 1 x GBP 2.00 = GBP 12.00 -> **GBP 12.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 12.00**, paid by bank transfer (s.8.1). Notice: text.

### CA-2026-10-44 - RJ-25645 - 17 Beckside

- Tenant: Lorna Sutcliffe (T-12731). Contractor: Direct Works. Priority: Urgent.
- Dates: clock start 2026-10-13; target 2026-10-20; completed 2026-10-26.
- Late completion: 4 working days after target. GBP 10.00 + 4 x GBP 2.00 = GBP 18.00 -> **GBP 18.00**.
- Missed appointment AP-52454 (2026-10-19, Direct Works, Shona Petrie): keyed as 'Missed - operative did not attend' by the planner.
- Missed appointments: 1 x GBP 15.00 = **GBP 15.00**.
- **Total: GBP 33.00**, paid by bank transfer (s.8.1). Notice: text.
- Note: Direct Works no-show on 2026-10-19 (keyed as missed); no recharge (Schedule D3).

### CA-2026-10-45 - RJ-25652 - Flat 9, Fold Yard

- Tenant: Brendan Sutcliffe (T-11733). Contractor: Ravensgill Building Maintenance. Priority: Routine.
- Dates: clock start 2026-08-19; target 2026-09-17; completed 2026-10-06.
- Late completion: 13 working days after target. GBP 10.00 + 13 x GBP 2.00 = GBP 36.00 -> **GBP 36.00**.
- Missed appointments: none - **GBP 0.00**.
- **Total: GBP 36.00**, paid by bank transfer (s.8.1). Notice: text.

## 3. Contractor recharges (Schedule D1)

| Recharge | Appointment | Job | Date | Contractor | Amount |
|---|---|---|---|---|---|
| CR-2026-10-01 | AP-52022 | RJ-25264 | 2026-09-08 | Marrick Plumbing & Heating | GBP 25.00 |
| CR-2026-10-02 | AP-52028 | RJ-25264 | 2026-09-22 | Marrick Plumbing & Heating | GBP 25.00 |
| CR-2026-10-03 | AP-52031 | RJ-25264 | 2026-10-06 | Marrick Plumbing & Heating | GBP 25.00 |
| CR-2026-10-04 | AP-52083 | RJ-25320 | 2026-10-02 | Kestle Roofing | GBP 25.00 |
| CR-2026-10-05 | AP-52450 | RJ-25343 | 2026-10-06 | Ravensgill Building Maintenance | GBP 25.00 |
| CR-2026-10-06 | AP-52156 | RJ-25364 | 2026-10-14 | Marrick Plumbing & Heating | GBP 25.00 |
| CR-2026-10-07 | AP-52452 | RJ-25374 | 2026-10-01 | Ravensgill Building Maintenance | GBP 25.00 |
| CR-2026-10-08 | AP-52444 | RJ-25387 | 2026-10-13 | Castleton Electrical Services | GBP 25.00 |
| CR-2026-10-09 | AP-52439 | RJ-25429 | 2026-10-12 | Castleton Electrical Services | GBP 25.00 |
| CR-2026-10-10 | AP-52307 | RJ-25503 | 2026-10-26 | Ravensgill Building Maintenance | GBP 25.00 |
| CR-2026-10-11 | AP-52434 | RJ-25509 | 2026-09-14 | Castleton Electrical Services | GBP 25.00 |

- Marrick Plumbing & Heating: 4 appointments, GBP 100.00
- Castleton Electrical Services: 3 appointments, GBP 75.00
- Ravensgill Building Maintenance: 3 appointments, GBP 75.00
- Kestle Roofing: 1 appointment, GBP 25.00

Total recharged: **GBP 275.00** over 11 appointments. The two Direct Works no-shows (AP-52008 on RJ-25250, AP-52014 on RJ-25258) and the Direct Works no-shows on RJ-25436 (AP-52459) and RJ-25645 (AP-52454) are paid to the tenants but not recharged: Direct Works is not party to the responsive repairs contract (Schedule D3).

Worst contractor of the month on missed appointments, as the reporting note defines it: **Marrick Plumbing & Heating** with 4. Direct Works is our own team and is reported separately in the Direct Works report, not in this measure.

