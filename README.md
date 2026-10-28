# Mytasks

Working set for producing Yuji stage-1 tasks on more than one laptop.

| Folder / file | What it is |
|---|---|
| `submit_20261024_v2/` | task sources (fix logs in `_fixlog/`) |
| `staging/` | bundles that passed the full QC, with their trajectories |
| `QC_PASSED_20261028/` | the QC reports of those bundles |
| `pipeline/` | the QC and run pipeline (`pipeline.sh`, `lib/`, `tools/`, `lead_qc/` = the lead's `qc (2).zip`) |
| `qc (2).zip` | the lead's QC: `static/10_structure.md`, `static/20_ruthless.md`, `traj/10_bundle_playbook.md` |
| `clean_trajectories.py` | trajectory cleanup before delivery (`--dry-run`, apply, `--check`) |

Not in this repo (get them separately):

- `yuji-workspace`: `git clone git@github.com:Animesh-Eth/yuji-workspace.git` (skills, reference sample `trajectories/5b10675f…`)
- the harness: `git clone https://github.com/148tabish/harness_mcp_atlas.git harness_mcp_atlas_main`, then `git checkout d731e757a6d7cca351f2ff4aad22486ca9fe1c5f` and `./setup.sh`
- secrets: `.env` files are never committed. Run `./setup.sh` in the harness, `claude` (log in) and `codex login`.

On Windows, work inside WSL2 (Ubuntu) with Docker Desktop's WSL 2 engine, and keep the clone in the Linux home folder, not under `/mnt/c`.
`pipeline/config.sh` holds this Mac's paths; set `DELIVERY`, `WORKSPACE` and `HMA_MAIN` in the environment on another machine.
Some pipeline scripts use macOS `stat -f`; on Linux use the harness directly (`./run.sh`) and bring results back for QC until those are ported.
