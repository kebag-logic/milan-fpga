[A683zo] REVIEW READY

Commit: `5bea2597ec514f0cde306e538261c6ddee66b456` (`665-s2b-cycles`).
- On round 29's `b2d39235`: nine ordinary commits (items 1 to 3); one merge commit of PR #892's round 4 head `8bc1dfc0`, which carries `dev-soft-core` `0fb66211` (`187eeed8`); then ten ordinary commits.
- No rebase, force or amend; nothing pushed. tsn-c-stack stays at `715589c`.

Changed (the ruling on round 29, issuecomment-6828629878, and the rulings on the round's three STOPs):
1. **The platform ledger** at 60.0 RAMB36, refused at 60.5, as ROM debt owed to S14. A new gate, `plat_ledger.py`, links the target platform's image at every point against its ledger, with seven planted ledgers.
2. **The SRP record cut's control** is held to this image's own unplanted record by 5 %. It is caught at 34,551 against 30,989 cycles.
3. **The suggestions:**
   - S1: rule windows off the 2 ms grid. The "W less two records" plant is refused, at this head at R5's W at 1x1/1if.
   - R712-8 S2: driver test T7, with its plant.
   - S5: `load_grade.py --check` refuses swapped columns.
   - S7: the ACMP expiry row names the pin move's kill test through `also`.
4. **The sync:** the merge, each conflict resolved from the composed tree.
5. **The first STOP** (issuecomment-6831583372): the size fixture's 8x8/2if entry at 58.5, the cap now fully used.
6. **The second STOP** (issuecomment-6835550732):
   - `KL_mbx_dma.sv` tracks a CPU request from its issue to `KL_mbx`'s answer (`cpu_wait_r`), for the merged port's two-cycle register read. The mover's own requests and beats wait for that answer.
   - Synthesised alone, it has 704 flops before and after, and LUTs go 484 to 487; no route was run.
   - The mover's bench gets the two-cycle model and D11, and three plants (among them the one-cycle routing) are caught, 24 of 24.
   - The split boot runs at both points at every sync.
7. **The harness at the merge:** its flash device takes writes only in the flash map's journal (KLJ3, 640 KiB at `0xe40000`). A save's container is the stage less KLJ3's 10-byte record header. Each fix has a check that a plant fails.
8. **The third STOP** (issuecomment-6842347916, option (b) amended):
   - `AECP_ROUND_COLD_US` 165 to 185 us at 8x8/2if. That is 2.7 % over the most measured 180.16 us, because 186 fails the retry search's 22 ms. The exception is stated in `aecp_mbx.h`, `FR_NFR.md` 3.4.1 and section 13, and expires at the 8x8/2if flip.
   - `CTRL_LOOP_BUILD_ONE_PASS_US` 405 to 430 and `CTRL_LOOP_BUILD_PASS_US` 900 to 1,010 at 1x1/1if, by the rule.
   - The AECP firm cap's test gives room for one notice past the cap. At 185 us a share no longer told the cap from the pass's room, and `retry-firm-uncapped` had escaped.
   - The four triggers did not fire:
     1. no implied cold cost over 183.1 us in any leg's rounds by n and k;
     2. no round or pass given whole over its stated cost on the fresh 8x8 build;
     3. no further firmware-stated cost over;
     4. 1x1/1if's load at 0.501.
9. **The re-grade:**
   - 8x8/2if: on fresh builds at `6c284a97`.
   - 1x1/1if: graded after the image and sample byte-compare.
   - The tables: from every leg's full tally. The polls base goes to 205 us at 1x1/1if and 325 at 8x8/2if, the walk to 35 at 1x1/1if, the rebuild to 690 at 8x8/2if, and an SRP record to 280 and a centisecond to 150 at 1x1/1if. The rest are in the PR body.

Validation: the full pass, once at this head, each job and gate on a clean clone, never piped.
- **Every `run:` step** of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`: 139 rc 0, 226 not run with their reasons, 0 bad (`verify_wf.py`).
  - bdd-conformance: 508 scenarios.
  - Mutants: control 698 of 698, AECP 227 `[ok]`, SRP 340 `[ok]`.
  - `fw_coverage.py --check` PASS over 39 files.
- **The full sweep**, as four shards: 65 suites passed, 0 failed, 0 timed out, 2,713,040 checks. In `mbx`, the record mover's mutants are 24 of 24.
- **The lane's own gates**, each rc 0 but the flip check, which exits 1 by design:
  - `load_grade.py --check` 0.501 and 0.499, and `--selftest` 25 of 25; `flip_grade.py --selftest` 132 of 132;
  - the harness self-test; `test_builder.py --require-rv32`; `test_ctrl_nvm.py --require-rv32 --self-test`;
  - `plat_ledger.py --self-test`; the split boot at 1x1/1if, 8x8/1if and 8x8/2if;
  - `cd tests && behave`.
- **The harness at this head:** each of the six legs rebuilt with its image and a sample log byte-identical, then every recorded group regraded. 0 refusals; the 14 recorded misses; no STATED line; each rc 0. The four cost controls are caught.

Receipts: the packet's `receipts/INDEX.md` (819 files) is generated after the host-path scrub.

Acceptance criteria: the ruling's items 1 to 6 and each STOP's ruling are met as above. The tier rows stay red (#894), and 8x8/2if waits on #890.

Open risks/questions:
- The cold start's 2.7 % margin at 8x8/2if is the ruled exception. GN8's rounds fit roughly 191.6 + 28.3k us. No k = 0 or k = 1 round in any leg is over the stated line (the dearest k = 1 at 81.41 us).
- The merge's cost moves are not attributed between the two-cycle register read, KLJ3 and the hot list.
- 1x1/1if's R4 by every source is 74.83 ms at this head (66.12 at round 29), for #894.
- The owner decision of 2026-11-13 06:47 (issuecomment-6845315282, 8x8 a must, 2if parts an option) re-scopes nothing here. Holding the rows at 8x8/1if is #894's next step; this head's flip check is unchanged.
- The candidate merge onto live `dev-soft-core` is the manager's.
