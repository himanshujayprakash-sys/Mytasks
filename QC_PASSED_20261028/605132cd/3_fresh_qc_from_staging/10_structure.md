VERDICT: PASS
Critical/blocker: 0 | Major: 0 | Minor: 0

## VERDICT: PASS

Task: `605132cd-8a3a-5561-a4fb-1b4dcc0b4d57` (`$TASK=/tmp/qc/leadqc/structure/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`)
Playbook: `pipeline/lead_qc/static/10_structure.md`, Section 1 script run once, verbatim, against `$TASK`.

| Check | Result | Code | Evidence |
|---|---|---|---|
| S1 required files/dirs | PASS | | `missing_files : none`, `empty_files : none`, `missing_dirs : none`; `world_data_json : 27 files (minimum 2)`; `data_files : 35`; `old_env.json : True`; `harness_owned_in_tests: none`; `helper_modules : none` |
| S1 rubric file | PASS | | `rubric_file : ['tests/judge.toml']` (shape=authoring), `both_rubrics : False` |
| S2 parse | PASS | | `parse_errors: none` (all parse) |
| S3 task.toml | PASS | | `harness_owned_blocks: none`; `schema_version : 1.4`; `task.description : present`; `task.authors : [{'name': 'himanshu.jayprakash', …}]`; `metadata.mcp_servers: 27`, `metadata.apps : 9`; `apps_not_wired : []`; `wired_without_world : none`; `world_not_wired : none`; `metadata.category : mcp_tool_calling`; `metadata.tags : 17`; `metadata.gradeable : True` |
| S4a weights ↔ tests | PASS | | `weight_shape=components weighted=55 defined=55 dynamic_minting=False`; phantom=0 (`weighted_but_undefined: none`), unweighted=0 (`defined_but_unweighted: none`); `zero_or_nonnumeric_weights: none`; `positive_total=76 penalty_total=33 guards=7`; `threshold=0.7 null_floor=0.0 guard_polarity=pass_charges gate={'require_no_guards': True}`; `threshold_ok: True`, `null_floor_ok: True`, `guard_polarity_ok: True \| guards_without_polarity: False` |
| S4b criteria | PASS | | `shape=authoring criteria=30`; dups=0 (`duplicate_ids: none`, `duplicate_numbers: none`); `missing_description: none`; `bad_weight: none`; polarity=0 issues (`no_polarity: none`, `weight_sign_vs_polarity_mismatch: none`); `negate_used: none`; `non_binary_scoring: none`; `bad_target: none`; `positive_total=35 penalty_total=17 max_single_positive=3` (3 ≤ 17.5 = half of 35; 17 < 35); targets=`{'final_answer': 30}` |
| S4c identity / canary / servers | PASS | | `folder_name_is_uuid: True`; identity `instruction_canary: None` → `canary_binding_ok: n/a (identity records none; the build mints it)`; `instruction_canaries_found: ['accb0e32-7806-444a-8e49-9c07e68b5486']`; `gt_env_shape : flat`; `in_gt_not_world : none`; `old_env_servers : 9 not in world: none` |
| S5 hygiene | PASS | | stray-file find: no output; `du -sh`: `3.5M`; >20M find: no output; secret grep: no output; `slug ok`; symlink find: no output |

## BLOCKERS
- none

## MAJOR
- none

## MINOR
- none

## INFO
- S1: `helper_modules : none` — nothing extra ships beside the tests.
- S4c: `in_world_not_gt` is non-empty (18 seeded servers the oracle does not change): `['LightAsana', 'LightBox', 'LightCalendly', 'LightConfluence', 'LightDiscord', 'LightDrive', 'LightHubspot', 'LightJira', 'LightMicrosoftTeams', 'LightMonday', 'LightNotes', 'LightOkta', 'LightOutlook', 'LightQuickBooks', 'LightSendGrid', 'LightTelegram', 'LightTrello', 'LightXero']`. The table rates this INFO: they are wired distractor servers, and the 9 graded apps all appear in gt_env.
- S4c: `.identity.json` records `instruction_canary: None`, but `instruction.md` already has one instruction canary (`accb0e32-…`). The script reports binding as n/a. There is only one canary, so no two-canary conflict exists. The build mints and binds it.
- S4c: `harbor_canary_carriers: ['.identity.json', 'environment/Dockerfile', 'solution/TRUTH.md', 'solution/gt_env.json', 'solution/solve.py', 'solution/solve.sh', 'tests/oracle.json', 'tests/test_outputs.py', 'tests/test_weights.json']`.
- Method note: the script was run unchanged. Its combined output was piped through a display-only `sed` redaction filter as a precaution against printing secrets. The secret grep printed nothing, so the filter changed nothing.

## Counts
- files: 80  size: 3.5M  data files: 35  world servers: 27  tests: 55 (guards 7)  criteria: 30
