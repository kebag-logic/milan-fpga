[A761c] REVIEW READY
Commit: 049f0e4dd7b0b514d1ea9689822901750129c044 (branch `665-s11-aecp-reboot`, one commit on round 3's `6171d65473`; not pushed)

Changed (round 4, under the ruling issuecomment-6809457669 on R821-3 and R822-3, option (b)). Comments and documents only; no code line changed:
- The reason, as B21 states its own: AECP starts no frame after its SUCCESS, so `NoOtherChannelTransmitsAfterTheDeparting`'s AECP check has no defect of its own. Each of the three AECP layers carries one:
  - the loop's stop: `plat-reboot-transmits-after-the-departing`, on B20's ACMP, MAAP and SRP words;
  - the receive gate: `plat-reboot-takes-aecp-frames-after-the-success`, on B19's and B23's AECP words;
  - AECP's own silence after its SUCCESS: `reboot-serves-after-its-success` and `reboot-probes-after-its-success` in `aecp_mutants.py`.
- Stated in the four places the ruling lists:
  - B20's comment and its header entry in `test_plat_boot.cpp`;
  - the loop-on defect's entry in `plat_mutants.py`;
  - `REBOOT_RESET.md:309` with `plat/README.md:127`;
  - the PR body's ruling rows: a round 4 table, and the round 3 rows "No channel but ADP's ..." and "A planted defect per channel ...".
- On the same lines, the two reviews' residue:
  - `(B12)` is now named as the test, `TheResetWaitsForTheResponseToLeave`, in both comments;
  - "the pass that takes the REBOOT" is stated as the MAAP, SRP and second AECP frames queued with it, in `REBOOT_RESET.md` and the README;
  - the PR body's round 2 parity row now lists B19's five channels, B22, B23 and their defects.

Validation (each on a fresh clean clone of `049f0e4d`, the ruling's gates):
- The platform host tests, `test_ctrl_firmware.py --require-rv32 --self-test`: PASS, control campaign 592 of 592. `plat-reboot-transmits-after-the-departing` fails 88 checks.
- `docs.yml`: 64 `run:` steps rc 0, 31 not run with reasons, 0 bad.
- `git diff --check` against the merge base: clean.
- Before the commit, on the lane tree, each rc 0: `docs_check.py`, `check_doc_paths.py`, `check_em_dash.py`, `check_doc_style.py`, `check_cpp_idiom.py`, `check_py_idiom.py` and `gen_toc.py --verify-anchors` / `--check`.
- Round 3's gates at `6171d654` still cover the AECP driver (153 of 153) and the REBOOT simulation (12 of 12). The round 4 delta changes only comments and two documents.

Acceptance criteria: items 2 to 5 met. Item 1 is met for six of the eight items and the binding, so the PR still says Relates to #871, as ruled.

Open risks/questions:
- Not taken: R822-2 R2 (the wording of when ADP's poll runs), as in round 3.
- Still pending from round 2: the decision on R821 S4 (a 0 tie adds one line to the all-fabric top `.v`), and a new issue for the split boot simulation's unpinned hash seed.
