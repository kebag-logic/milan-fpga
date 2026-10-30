# Superseded receipts

Kept for the record; none is cited as evidence for the head.

- `gates-early-ac0da94e/`: the first battery, at `ac0da94e`. It found `doc_style`, `py_idiom` and `doc_paths`, fixed in `6260c53c` and `1767346a`.
- `gates-c71364bd/`: the battery at `c71364bd`, before the capture re-measure (`check_nvm_capture.py` rc 1 there, as expected).
- `capture-stale-dc7b1417/`, `service-stale-dc7b1417/`: runs on the first firmware form, stopped when the heartbeat was restructured in `c71364bd` (the digest changed).
- `nvm_cosim-dc7b1417.log`, `profile-contract-dc7b1417.log`: nvm_cosim and the builder's resolver gate on the first firmware form; both re-run on `c71364bd`.
- `*-worktree-38fd88f3-content.log`: the dynmap leg and the three volatile mutants run from the lane worktree before `38fd88f3` was committed (same content); re-run from a clean clone at `c71364bd`.
- `volatile-mutants-64-66-c71364bd-without-make-dynmap.log`: an invalid attempt in a fresh clone without `make dynmap` first, so the leg's ROM images were absent and the clean control failed. The driver keeps them unmade by design; the valid run builds the leg first.
