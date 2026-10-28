VERDICT: PASS
Critical/blocker: 0 · Major: 0 · Minor: 0

## VERDICT: PASS

Task: `605132cd-8a3a-5561-a4fb-1b4dcc0b4d57` (`$TASK=/tmp/qc/leadqc/structure/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`)
Playbook: `pipeline/lead_qc/static/10_structure.md`, Section 1 script run once, unmodified.

| Check | Result | Code | Evidence |
|---|---|---|---|
| S1 required files/dirs | PASS | | `missing_files : none`, `empty_files : none`, `missing_dirs : none`; `world_data_json : 27 files (minimum 2)`; `data_files : 35`; `old_env.json : True`; `harness_owned_in_tests: none` |
| S1 rubric file | PASS | | `rubric_file : ['tests/judge.toml']`, `both_rubrics : False`; judge.toml (`shape=authoring`) |
| S2 parse | PASS | | `parse_errors: none` (all parse) |
| S3 task.toml | PASS | | `harness_owned_blocks: none`; `schema_version : 1.4`; `task.description : present`; `task.authors : [{'name': 'himanshu.jayprakash', …}]`; `metadata.mcp_servers: 27`, `metadata.apps : 9`; `apps_not_wired : []`; `wired_without_world : none`; `world_not_wired : none`; `metadata.category : mcp_tool_calling`; `metadata.tags : 17`; `metadata.gradeable : True` |
| S4a weights ↔ tests | PASS | | `weight_shape=components weighted=55 defined=55 dynamic_minting=False`; phantom=0 (`weighted_but_undefined: none`), unweighted=0 (`defined_but_unweighted: none`); `zero_or_nonnumeric_weights: none`; `positive_total=76 penalty_total=33 guards=7`; `threshold=0.7 null_floor=0.0 guard_polarity=pass_charges gate={'require_no_guards': True}`; `threshold_ok: True`, `null_floor_ok: True`, `guard_polarity_ok: True \| guards_without_polarity: False` |
| S4b criteria | PASS | | `shape=authoring criteria=30`; dups=0 (`duplicate_ids: none`, `duplicate_numbers: none`); `missing_description: none`; `bad_weight: none`; polarity=0 issues (`no_polarity: none`, `weight_sign_vs_polarity_mismatch: none`); `negate_used: none`; `non_binary_scoring: none`; `bad_target: none`; `positive_total=35 penalty_total=17 max_single_positive=3` (3 ≤ 17.5 = half of positive_total; 17 < 35); targets=`{'final_answer': 30}` |
| S4c identity / canary / servers | PASS | | `folder_name_is_uuid: True`; `instruction_canaries_found: ['accb0e32-7806-444a-8e49-9c07e68b5486']` = identity `instruction_canary`; `canary_binding_ok: True`; `gt_env_shape : flat`; `in_gt_not_world : none`; `old_env_servers : 9 not in world: none` |
| S5 hygiene | PASS | | stray-file `find`: no output; `du -sh`: `3.5M`; >20M `find`: no output; credential `grep`: no output; `slug ok`; symlink `find`: no output |

## BLOCKERS
- none

## MAJOR
- none

## MINOR
- none

## INFO
- S1 `helper_modules : none` (nothing ships beside the tests).
- S4c `in_world_not_gt` non-empty (INFO per table): 18 servers are seeded and wired but the oracle doesn't change them: `LightAsana, LightBox, LightCalendly, LightConfluence, LightDiscord, LightDrive, LightHubspot, LightJira, LightMicrosoftTeams, LightMonday, LightNotes, LightOkta, LightOutlook, LightQuickBooks, LightSendGrid, LightTelegram, LightTrello, LightXero`. The 9 `gt_env_servers` match the 9 graded `metadata.apps`.
- S4c identity is minted: `uuid 605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`; harbor canary present in `.identity.json, environment/Dockerfile, solution/TRUTH.md, solution/gt_env.json, solution/solve.py, solution/solve.sh, tests/oracle.json, tests/test_outputs.py, tests/test_weights.json` (canary value not repeated here).

## Counts
- files: 80  size: 3.5M  data files: 35  world servers: 27  tests: 55 (guards 7)  criteria: 30

## Raw script output (verbatim)

```
=== S1 (605132cd-8a3a-5561-a4fb-1b4dcc0b4d57)
missing_files   : none
empty_files     : none
missing_dirs    : none
rubric_file     : ['tests/judge.toml']
both_rubrics    : False
world_data_json : 27 files (minimum 2): ['LightAirtable', 'LightAsana', 'LightBox', 'LightCalendly', 'LightConfluence', 'LightDiscord', 'LightDrive', 'LightGmail', 'LightGoogleCalendar', 'LightHubspot', 'LightJira', 'LightMailchimp', 'LightMicrosoftTeams', 'LightMonday', 'LightNotes', 'LightNotion', 'LightOkta', 'LightOutlook', 'LightQuickBooks', 'LightSendGrid', 'LightSlack', 'LightTelegram', 'LightTrello', 'LightTwilio', 'LightWhatsApp', 'LightXero', 'LightZendesk']
data_files      : 35
old_env.json    : True
helper_modules  : none
harness_owned_in_tests: none
=== S2
parse_errors: none
=== S3
harness_owned_blocks: none
schema_version      : 1.4
task.name           : atlas/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57
task.description    : present
task.authors        : [{'name': 'himanshu.jayprakash', 'email': 'himanshu.jayprakash@ethara.ai'}]
metadata.mcp_servers: 27
metadata.apps       : 9
apps_not_wired      : []
wired_without_world : none
world_not_wired     : none
metadata.category   : mcp_tool_calling
metadata.tags       : 17
metadata.gradeable  : True
=== S4a
weight_shape=components weighted=55 defined=55 dynamic_minting=False
weighted_but_undefined: none
defined_but_unweighted: none
zero_or_nonnumeric_weights: none
positive_total=76 penalty_total=33 guards=7
threshold=0.7 null_floor=0.0 guard_polarity=pass_charges gate={'require_no_guards': True}
threshold_ok: True 
null_floor_ok: True
guard_polarity_ok: True | guards_without_polarity: False
=== S4b
shape=authoring criteria=30
duplicate_ids: none
duplicate_numbers: none
missing_description: none
bad_weight: none
no_polarity: none
weight_sign_vs_polarity_mismatch: none
negate_used: none
non_binary_scoring: none
bad_target: none
positive_total=35 penalty_total=17 max_single_positive=3
targets: {'final_answer': 30}
=== S4c
identity: {'uuid': '605132cd-8a3a-5561-a4fb-1b4dcc0b4d57', 'canary': '<redacted in report>', 'instruction_canary': 'accb0e32-7806-444a-8e49-9c07e68b5486'}
folder_name_is_uuid: True
instruction_canaries_found: ['accb0e32-7806-444a-8e49-9c07e68b5486']
canary_binding_ok: True
harbor_canary_carriers: ['.identity.json', 'environment/Dockerfile', 'solution/TRUTH.md', 'solution/gt_env.json', 'solution/solve.py', 'solution/solve.sh', 'tests/oracle.json', 'tests/test_outputs.py', 'tests/test_weights.json']
gt_env_shape    : flat
gt_env_servers  : ['LightAirtable', 'LightGmail', 'LightGoogleCalendar', 'LightMailchimp', 'LightNotion', 'LightSlack', 'LightTwilio', 'LightWhatsApp', 'LightZendesk']
in_gt_not_world : none
in_world_not_gt : ['LightAsana', 'LightBox', 'LightCalendly', 'LightConfluence', 'LightDiscord', 'LightDrive', 'LightHubspot', 'LightJira', 'LightMicrosoftTeams', 'LightMonday', 'LightNotes', 'LightOkta', 'LightOutlook', 'LightQuickBooks', 'LightSendGrid', 'LightTelegram', 'LightTrello', 'LightXero']
old_env_servers : 9 not in world: none
3.5M	/tmp/qc/leadqc/structure/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57
slug ok
```

S5 notes: the stray-file `find`, the `>20M` `find`, the credential `grep` and the symlink `find` printed nothing. File count (80) is from `find "$TASK" -type f | wc -l`. The only edit to the output above is the harbor canary GUID, which is replaced with `<redacted in report>` so the report doesn't carry it.

## Rules applied
- No BLOCKER, so `VERDICT: PASS`.
- Nothing in the task folder was changed.
