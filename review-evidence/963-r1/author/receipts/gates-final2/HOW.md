# The gates at the final head (re-run after the host crash of 2026-11-23 00:39)

- `firmware-shard{1,2,3}-50d3f10e/`: `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`, each on its own
  fresh clone. Shard 0 passed at `25d3dd7a` (`gates-current/firmware-0/`). `50d3f10e` changes only one row of the
  AECP plant table, which shard 2 runs, and no plant of shard 0's partition.
- `firmware-unit-50d3f10e/`: the firmware-unit job's other steps (tally and RV32 self-tests, the saved-state store
  suites, the coverage ratchet).
- `twin-50d3f10e/`: `make -C tb/verilator/milan_dp twin` and `twin-plants`.
- `images-50d3f10e/`: the target platform's split images (`ctrl_plat_image.py`) on the base product export's bus map
  and flash map.
- `portable-50d3f10e/`: the portable lane gates (`gates_b.sh`), every code and model gate.
- `portable-docs-4cca9569/`: the doc-reading gates again at the final head, after its design doc commit.
- `docs-4cca9569/`: the docs workflow's gate steps from `docs.yml` at the final head. The steps that depend on the
  hosted runner are run as the workflow runs them: the em-dash gate against the PR's merge base; the no-git docs gate
  on a fresh checkout; the builder legs with the RV32 SDK where CI installs it.
