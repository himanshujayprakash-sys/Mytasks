VERDICT: PASS
critical/blocker: 0  major: 0  minor: 0

## VERDICT: PASS

Task: `605132cd-8a3a-5561-a4fb-1b4dcc0b4d57` (`$TASK=/tmp/qc/leadqc/structure/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`)
Playbook: `pipeline/lead_qc/static/10_structure.md`. Section 1 script run once, as written; evidence below is copied from its output.

| Check | Result | Code | Evidence |
|---|---|---|---|
| S1 required files/dirs | PASS | | `missing_files: none`, `empty_files: none`, `missing_dirs: none`; `world_data_json : 27 files (minimum 2)`; `data_files : 35`; `old_env.json : True`; `harness_owned_in_tests: none`; `helper_modules : none` |
| S1 rubric file | PASS | | `rubric_file : ['tests/judge.toml']` (shape=authoring); `both_rubrics : False` |
| S2 parse | PASS | | `parse_errors: none` (all parse) |
| S3 task.toml | PASS | | `harness_owned_blocks: none`; `schema_version : 1.4`; `task.name : atlas/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57`; `task.description : present`; `task.authors` present (1 author); `metadata.mcp_servers: 27`; `metadata.apps : 9`; `apps_not_wired : []`; `wired_without_world : none`; `world_not_wired : none`; `metadata.category : mcp_tool_calling`; `metadata.tags : 17`; `metadata.gradeable : True` |
| S4a weights ↔ tests | PASS | | `weight_shape=components weighted=55 defined=55 dynamic_minting=False`; phantom=0 (`weighted_but_undefined: none`); unweighted=0 (`defined_but_unweighted: none`); `zero_or_nonnumeric_weights: none`; `positive_total=76 penalty_total=33 guards=7`; `threshold=0.7 null_floor=0.0 guard_polarity=pass_charges gate={'require_no_guards': True}`; `threshold_ok: True`, `null_floor_ok: True`, `guard_polarity_ok: True \| guards_without_polarity: False` |
| S4b criteria | PASS | | `shape=authoring criteria=30`; dups=0 (`duplicate_ids: none`, `duplicate_numbers: none`); `missing_description: none`; `bad_weight: none`; polarity issues=0 (`no_polarity: none`, `weight_sign_vs_polarity_mismatch: none`); `negate_used: none`; `non_binary_scoring: none`; `bad_target: none`; `positive_total=35 penalty_total=17 max_single_positive=3`; targets=`{'final_answer': 30}` |
| S4c identity / canary / servers | PASS | | identity minted; `folder_name_is_uuid: True`; `instruction_canaries_found: ['accb0e32-7806-444a-8e49-9c07e68b5486']` matches identity `instruction_canary`; `canary_binding_ok: True`; `gt_env_shape : flat`; `gt_env_servers` = 9; `in_gt_not_world : none`; `old_env_servers : 9 not in world: none` |
| S5 hygiene | PASS | | stray-file `find`: no output; `du -sh`: `3.5M`; files > 20M: none; credential grep: no matches; `slug ok`; symlink `find`: no output |

## BLOCKERS
- none

## MAJOR
- none

## MINOR
- none

## INFO
- S4c `in_world_not_gt` non-empty (INFO per the decision table): 18 seeded, wired servers the oracle leaves unchanged: `['LightAsana', 'LightBox', 'LightCalendly', 'LightConfluence', 'LightDiscord', 'LightDrive', 'LightHubspot', 'LightJira', 'LightMicrosoftTeams', 'LightMonday', 'LightNotes', 'LightOkta', 'LightOutlook', 'LightQuickBooks', 'LightSendGrid', 'LightTelegram', 'LightTrello', 'LightXero']`. These are distractor servers: 27 are wired and 9 are graded (`metadata.apps`), and those 9 match `gt_env_servers` exactly.
- S4c `harbor_canary_carriers`: `['.identity.json', 'environment/Dockerfile', 'solution/TRUTH.md', 'solution/gt_env.json', 'solution/solve.py', 'solution/solve.sh', 'tests/oracle.json', 'tests/test_outputs.py', 'tests/test_weights.json']` (recorded only; no decision row applies).
- S4a: `guard_polarity=pass_charges` is set explicitly for the 7 guards; `gate={'require_no_guards': True}`.

## Counts
- files: 80  size: 3.5M  data files: 35  world servers: 27  tests: 55 (guards 7)  criteria: 30
