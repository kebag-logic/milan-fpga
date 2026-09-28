[A422] REVIEW READY
Commit: `1f039cfe86d5337f5c9b7248696dba1c4bdda67e` (tree `9ce926b9`, unchanged since the [A422] STOP; local, not pushed).
- It holds merge `9e3df3ed` (dev `7a7582f0` into `93262f25`) and the stale-statement commit.
- The processor gitlink stays `16be6768`.

Changed since the STOP: nothing in the tree. Under the [A10] disposition, option (a), the native evidence was renewed at this head.

Validation (rc 0 at `1f039cfe`; physical worktree, clean before and after, never piped):
- **Native arms.** 25 arms ran in fresh build directories, with simulations in parallel on CPUs 32-63:
  - the 15 service runs;
  - the `no-publish` control;
  - six capture arms and three capture controls.

  All 65 commands returned rc 0, and no STOP condition occurred.
- **Service regrade.** Each raw log and receipt was restored from the retained packet, then `run.py … --reuse-build --regrade` ran on all 15 service runs: 15 of 15 rc 0.
- **Byte comparison with round 3.** All 16 service simulation logs and all 9 capture logs are byte-identical, and every graded receipt field matches.
  - The only differences are in bound hashes: the three merged inputs, LiteX timestamp lines in the generated headers and `sim.v`, and `AEM_N_CONTROL_C = 1` in `adp_shape_defaults.svh`. `bios.bin` is identical.
  - Reason: #597 passes `N_AUDIO_UNIT_P`, `N_CLK_DOMAIN_P` and `N_CONTROL_P` as 1 on both AX7101 shapes, equal to the `protocol_processor_top` defaults.
- **Capture.** It was re-measured, because its 118 compiled sources include `hdl/milan/KL_pp_shadow.sv` and `hdl/milan/milan_datapath.sv`.
  - All 96 captures equal the committed receipt rows.
  - Every receipt-bound identity matches: CPU netlist, firmware, BIOS, gPTP microcode and configuration.
  - Figures: 8x8 at 50 MHz reaches 13.23352 ms (3.7027x the floor), 1x1 3.88779 ms, and the 100 MHz comparison 9.95464 ms. The byte-only control shows 1.83648x.
  - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6 and the receipt already state these figures, so nothing was edited.
- **Service figures.**
  - The twelve positive plans pass with zero findings.
  - Largest heartbeat gap: 322.47884 ms. MDIO transaction: 0.12457 ms. Complete poll: 0.83375 ms.
  - `remove-dispatch` gives 1051 per-line findings on `queued-builtins` and 350 on `queued-short`.
  - `late-sample` and `no-publish` are caught.
- **Checks.**
  - `check_nvm_capture` returns rc 0, with a log byte-identical to the STOP round's.
  - The packet verifier and audit return rc 0: 138 artifacts re-hashed, gzip-compressed above 200 KB, and no file over 200 KB.
  - Every other gate in the STOP comment ran at this same, unchanged head and remains rc 0.

Acceptance criteria: the merge-dev assignment's gate set now returns rc 0 at the merge head, including the 15 service regrades. The merge, its conflict resolution and `1f039cfe` are unchanged.

Open risks/questions:
- **Measured-commit lines.** `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1613-1614` and `docs/findings/397_SERVICE_BUDGET.md:37` still name `26a26e1f` as the measured commit. The merge-head runs reproduce those measurements byte for byte, so disposition item 3 left the text alone. Naming the reproduction would take a docs-only commit, if wanted.
- **Dev has advanced.** Dev is now at `ce550952` (#612, #613). It re-pins protocol-processor to `c951a9ff` and changes `sw/litex/milan_soc.py`; the service builds bind both and the capture harness compiles both.
  - A candidate on the live dev tip will make this native evidence stale again, and it will not keep the `16be6768` pin.
  - `git merge-tree` against that tip is clean. It was not merged, because that is outside this round.
- **Unchanged from round 3:**
  - the #599 acceptance 4 bench rerun;
  - the long built-in residual;
  - the unrun calibration.

Local only: no push, PR edit or merge. Next is the delta review by [R368].
