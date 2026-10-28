VERDICT: PASS
Findings: critical/blocker 0, major 0, minor 0

# STRUCTURE QC — a1acd72c-ccb0-5eb6-9893-691b1872e0ef

Playbook: `pipeline/lead_qc/static/10_structure.md`, Section 1 script run once as written against
`$TASK=/tmp/qc/leadqc/structure/a1acd72c-ccb0-5eb6-9893-691b1872e0ef`.

| Check | Result | Code | Evidence |
|---|---|---|---|
| S1 required files/dirs | PASS | | `missing_files: none`, `empty_files: none`, `missing_dirs: none`; `world_data_json : 24 files (minimum 2)`; `data_files: 34`; `old_env.json: True`; `harness_owned_in_tests: none`; `helper_modules: none` |
| S1 rubric file | PASS | | `rubric_file: ['tests/judge.toml']` (shape=authoring), `both_rubrics: False` |
| S2 parse | PASS | | `parse_errors: none` (all parse) |
| S3 task.toml | PASS | | `harness_owned_blocks: none`; `schema_version: 1.4`; `task.description: present`; `task.authors: [{'name': 'himanshu.jayprakash', …}]`; `metadata.mcp_servers: 24`, `metadata.apps: 8`; `apps_not_wired: []`; `wired_without_world: none`; `world_not_wired: none`; `metadata.category: mcp_tool_calling`; `metadata.tags: 14`; `metadata.gradeable: True` |
| S4a weights ↔ tests | PASS | | `weight_shape=components weighted=67 defined=67 dynamic_minting=False`; phantom=0 (`weighted_but_undefined: none`), unweighted=0 (`defined_but_unweighted: none`); `zero_or_nonnumeric_weights: none`; `positive_total=116 penalty_total=25 guards=5`; `threshold=0.7 null_floor=0.0 guard_polarity=pass_charges gate={'require_no_guards': True}`; `threshold_ok: True`, `null_floor_ok: True`, `guard_polarity_ok: True \| guards_without_polarity: False` |
| S4b criteria | PASS | | `shape=authoring criteria=22`; dups=0 (`duplicate_ids: none`, `duplicate_numbers: none`); `missing_description: none`; `bad_weight: none`; polarity issues=0 (`no_polarity: none`, `weight_sign_vs_polarity_mismatch: none`); `negate_used: none`; `non_binary_scoring: none`; `bad_target: none`; `positive_total=39 penalty_total=21 max_single_positive=5` (5 ≤ 19.5, 21 < 39); targets=`{'final_answer': 22}` |
| S4c identity / canary / servers | PASS | | `folder_name_is_uuid: True`; `instruction_canaries_found: ['a1acd72c-ccb0-5eb6-9893-691b1872e0ef']`; `canary_binding_ok: n/a (identity records none; the build mints it)`; `gt_env_shape: flat`; `in_gt_not_world: none`; `old_env_servers: 24 not in world: none`; INFO `in_world_not_gt` (16 servers, see below) |
| S5 hygiene | PASS | | stray-file `find`: no output; `du -sh`: `3.9M`; `find -size +20M`: no output; credential grep: no output; `slug ok`; symlink `find`: no output |

## BLOCKERS
- none

## MAJOR
- none

## MINOR
- none

## INFO
- S4c `in_world_not_gt`: `['LightAsana', 'LightBox', 'LightCalendly', 'LightConfluence', 'LightDocuSign', 'LightDropbox', 'LightGoogleCalendar', 'LightJira', 'LightMailchimp', 'LightMicrosoftTeams', 'LightNotion', 'LightOutlook', 'LightPagerDuty', 'LightSendGrid', 'LightTrello', 'LightXero']`. These are wired and seeded servers that the oracle leaves unchanged. The table marks this INFO.
- S4c `.identity.json` has `instruction_canary: None`. `instruction.md` already carries `instruction-canary a1acd72c-ccb0-5eb6-9893-691b1872e0ef`, which matches the folder uuid. Binding is reported as `n/a (identity records none; the build mints it)`.
- S4c `harbor_canary_carriers: ['.identity.json', 'environment/Dockerfile', 'solution/TRUTH.md', 'solution/gt_env.json', 'solution/solve.py', 'solution/solve.sh', 'tests/old_env.json', 'tests/oracle.json', 'tests/test_outputs.py', 'tests/test_weights.json']`. Recorded only; no decision-table row applies.
- S1 `helper_modules: none`.

## Counts
- files: 76  size: 3.9M  data files: 34  world servers: 24  tests: 67 (guards 5)  criteria: 22
