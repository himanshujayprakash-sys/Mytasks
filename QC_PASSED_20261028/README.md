# Tasks that passed the lead's QC (`qc (2).zip`), 2026-10-28

The QC is the lead's `qc (2).zip`. It runs in two stages:
- **before the trajectory:** `static/10_structure.md` and `static/20_ruthless.md`;
- **after the trajectory:** all three, `10_structure.md`, `20_ruthless.md` and `traj/10_bundle_playbook.md`.

The workspace final QC (`yuji-final-qc` 0.2.0) is included as an extra check.

The task bundles (task files plus `trajectories/opus-5/run_1`) are in [`../staging/`](../staging/):
- [`staging/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/`](../staging/605132cd-8a3a-5561-a4fb-1b4dcc0b4d57/)
- [`staging/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/`](../staging/a1acd72c-ccb0-5eb6-9893-691b1872e0ef/)

These are byte-identical to the copies in the local `yuji-stage-1` clone, which is where you commit and push from.

## Summary

| Task | Score (Opus 5) | Band | Before trajectory | After trajectory |
|---|---|---|---|---|
| 605132cd: council allotments lettings round | reward 0.4876 (pytest 0.2895, rubric 0.6857) | Medium | structure PASS, ruthless PASS | structure PASS, ruthless PASS, bundle PASS |
| a1acd72c: repairs compensation and contractor review | reward 0.1411 (pytest 0.0, rubric 0.2821) | Expert | structure PASS, ruthless (see note) | structure PASS, ruthless PASS, bundle PASS |

## 605132cd

Before the trajectory:
- [10_structure.md](605132cd/1_before_trajectory/10_structure.md): PASS (0/0/0)
- [20_ruthless.md](605132cd/1_before_trajectory/20_ruthless.md): PASS (0 critical, 0 major)

After the trajectory:
- [10_structure.md](605132cd/2_after_trajectory/10_structure.md): PASS (0/0/0)
- [20_ruthless.md](605132cd/2_after_trajectory/20_ruthless.md): PASS (0 critical, 2 major, 2 minor)
- [10_bundle_playbook.md](605132cd/2_after_trajectory/10_bundle_playbook.md): SIGNED (PASS), 0 issues
- [workspace final QC](605132cd/2_after_trajectory/workspace_final_qc.md): PASS (0 blocker, 0 major)

The agent's closing message is in [agent_final_message.md](605132cd/agent_final_message.md).

What the model got wrong:
- It missed the re-measured plots BM-27, HL-38 and HL-17, so it stated a rent of 1194.05 instead of 1058.36.
- It let BM-41 and HL-33, which should have been withdrawn.
- It gave BM-27 to the wrong applicant.
- It crossed no red line.

## a1acd72c

Before the trajectory:
- [10_structure.md](a1acd72c/1_before_trajectory/10_structure.md): PASS
- 20_ruthless.md: the pre-trajectory run said FAIL with 0 critical and 2 major findings. Both majors were fixed before
  the trajectory ran. The re-run listed below then passed on those same, unchanged files. The pre-run report file was
  overwritten by that re-run.

After the trajectory:
- [10_structure.md](a1acd72c/2_after_trajectory/10_structure.md): PASS
- [20_ruthless.md](a1acd72c/2_after_trajectory/20_ruthless.md): PASS (0 critical, 1 major)
- [10_bundle_playbook.md](a1acd72c/2_after_trajectory/10_bundle_playbook.md): PASS (the script raised one flag, which
  the reviewer ruled a loader false positive)
- [workspace final QC](a1acd72c/2_after_trajectory/workspace_final_qc.md): PASS (0 blocker, 0 major)

The agent's closing message is in [agent_final_message.md](a1acd72c/agent_final_message.md).

What the model got wrong:
- It texted a tenant who had opted out. That is a red line, so pytest is 0.
- It then missed most of the award and recharge work.

## Fresh run of the whole `qc (2).zip` on the `staging/` bundles (2026-10-28, ~20:15)

All three playbooks were re-run from scratch on the bundles in `staging/`. The static two read each bundle after the
harness's own `import_task` converted it to the authoring layout; the bundle playbook read the staging bundle with its
trajectory.

| Task | 10_structure.md | 20_ruthless.md | traj/10_bundle_playbook.md |
|---|---|---|---|
| 605132cd | [PASS (0/0/0)](605132cd/3_fresh_qc_from_staging/10_structure.md) | [PASS (0 critical, 2 major, 7 minor)](605132cd/3_fresh_qc_from_staging/20_ruthless.md) | [PASS (0 blocker, 0 major; 0/55 false or double-counted tests)](605132cd/3_fresh_qc_from_staging/10_bundle_playbook.md) |
| a1acd72c | [PASS (0/0/0)](a1acd72c/3_fresh_qc_from_staging/10_structure.md) | [PASS (0 critical, 0 major, 9 minor)](a1acd72c/3_fresh_qc_from_staging/20_ruthless.md) | [PASS (0 blocker, 0 major, 1 minor)](a1acd72c/3_fresh_qc_from_staging/10_bundle_playbook.md) |

Both runs are classified as genuine model failures (bucket B: model/agent); the low rewards are the model's, not the task's.

## Other checks run on both tasks (internal, not the lead's QC)

- Judged oracle 1.0 / 1.0 and do-nothing 0.0 / 0.0, before the trajectory.
- The shipped task files are byte-identical to the version that passed QC (lock fingerprint).
- Re-grading the run with the shipped tests reproduces the recorded score.
- `clean_trajectories.py --check` is clean.
- The stage-1 difficulty quota check accepts both.
