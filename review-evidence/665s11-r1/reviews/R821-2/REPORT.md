[R821] NEGATIVE - exact head d08d30c6ecbac2e45867c3a509ef309ed081ab15

# R821-2: internal cleared-context review of PR #881 (issue #871, AECP REBOOT on the split CPU), round 2 delta

- Head `d08d30c6ecbac2e45867c3a509ef309ed081ab15`, tree `42784db20be532a060bc927960ee12cf592a85c0`. The delta reviewed is `b29f94d7..d08d30c6`: five author commits made under the manager's round 2 ruling (#871 issuecomment-6789331293). The whole lane `1d6bf555..d08d30c6` was read where the delta depends on it.
- **Summary.** The code now does what the ruling asked. From the SUCCESS, every channel's take sits behind a gate. The loop stops once the REBOOT's frames are out. ENTITY_DEPARTING goes last, and the port fires after it.
  - R821-1's behaviour probe passes unchanged at this head, and every round-1 finding is resolved at its cause.
  - **One MINOR is open (F1, Tests and Docs).** The new parity tests cannot fail for two plausible defects of the gate they claim to prove: a gate that leaves the MAAP and SRP channels open, and a gate that closes at the frames' handover instead of at the SUCCESS. Both escape every host test, and the second also escapes the AECP core tests.
  - So Tests and Docs are unclean and the verdict is NEGATIVE. Conformance, RTL and Robustness are clean.

## Findings

### F1 MINOR - Tests, Docs - the parity tests do not prove "any channel" or "from the SUCCESS"

- **Where:**
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:852` (B19). It sends only an ENTITY_DISCOVER (adp), a BIND_RX (acmp) and an AEM command (aecp), and only 20 ms after the REBOOT, by which time the REBOOT's frames have long been handed over.
  - `sw/firmware/ctrl/test/test_aecp.cpp:1844`. `aecp_reboot_accepted` is checked only after four `aecp_poll`s, when `reboot` is already 2.
  - The claims:
    - `docs/design/REBOOT_RESET.md:272-274` ("So no ADP, ACMP, AECP, MAAP or SRP frame is taken");
    - the evidence row at `REBOOT_RESET.md:309` ("no frame of any channel taken from the SUCCESS");
    - B19's own name and its header comment (`test_plat_boot.cpp:61`);
    - the PR's ruling-item-1 row.
- **Authority:**
  - The ruling's item 1 says: "From the REBOOT's SUCCESS, no received frame of any channel is taken ... Add a host test and a planted defect for each."
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
  - The processor's contract (`06_aecp_engine.md` 6.11) takes acceptance at the SUCCESS's TX grant, and "A command already queued behind the REBOOT is never served".
- **Evidence (executed; `scripts/probe_plat.py`, `scripts/probe_aecp.py`, receipts `receipts/probe-*.log`):**
  - **Control, `head`:** platboot1 rc 0, all REBOOT tests pass.
  - **`gate-skips-maap-and-srp`:** `gate` (`ctrl_plat.c:187`) is limited to `ch < MBX_CH_MAAP`, so channels 3 and 4 are taken after the SUCCESS. The probe gives platboot1 rc 0 and 0 failed checks. B19, B20 and B21 pass.
  - **`gate-from-the-handover`:** `aecp_reboot_accepted` is changed to `a->reboot >= 2u`, so the gate closes only once the REBOOT's frames are handed to the mailbox. The probe gives platboot1 rc 0 with 0 failed checks. The AECP core arm (`Core.Reboot*`, app mode, two interfaces) also gives rc 0, with all 3 tests passing.
  - This second defect is observable in the product:
    - `aecp_rx` sets `reboot = 1` in the AECP take (channel 2), and `aecp_poll` sets 2 only in the loop's poll phase (`aecp.c:635-641`, reached from `aecp_mbx.c` `poll`).
    - So in the pass that takes the REBOOT, a MAAP or SRP frame already in its ring (channels 3 and 4, serviced after AECP in `ctrl_loop_service`) is taken under the defect and left in its ring by the head.
    - The same happens on any channel for as long as the response cannot be handed over (a full AECP transmit ring).
  - The CPU simulation sends its window frames only after the SUCCESS has left the mailbox (`run.py:262-266`, graded at `:563`), so it cannot see either defect.
  - The shipped defect `plat-reboot-takes-frames-after-the-success` removes the whole gate, and `reboot-acceptance-unreported` makes acceptance never true. Neither covers a partial gate or a late one.
- **Impact:** The head's code is correct on both points; I read it and it is not in question. But the evidence the ruling required proves the gate for three of five channels, and only once it has been closed for some time. A later edit that narrows the gate, or moves its onset to the handover, ships green. The authoritative document cites B19 for exactly those two properties.
- **Required outcome:**
  - A host test delivers a frame on each of the five channels after the SUCCESS and requires none taken.
  - A host test delivers frames that are queued with the REBOOT, or that arrive while its response cannot be handed over, and requires none taken.
  - The AECP core test requires `aecp_reboot_accepted` true straight after `aecp_rx` of the REBOOT, before any poll.
  - Each of these has a planted defect refused on its own words.
  - If this is not done, the claims at `REBOOT_RESET.md:272-274` and `:309`, and in the PR text, are narrowed to what the tests prove.
- **Verification:** At the fixed head, `python3 -I scripts/probe_plat.py <repo> <scratch> gate-skips-maap-and-srp` and `... gate-from-the-handover`, and `python3 -I scripts/probe_aecp.py <repo> <scratch> handover`, each report a failed REBOOT test on its words. The `head` control still passes.

### Residue

None recorded.

On the comment rule, the delta adds `B17`, `B19`, `B20`, `B21` and `B12` test-ID labels in source comments: `test_plat_boot.cpp:56, 61, 65, 68, 170, 187`. As in R821-1, I read these as that file's own test-ID scheme, the prefix of each gtest name (`Boot.B19NoFrameOfAnyChannelIsTakenFromTheSuccess`), not bench lane labels. Nothing else in the delta's added comments names a lane, round, reviewer or issue comment. The owner's rule gives "B17" as its example of a lane label, though. If the manager reads that example literally, these six lines are RESIDUE, and the exact fix is to drop the label from each comment, or name the test in full.

### Suggestions (do not affect coverage)

- **S1 Tests.** `run.py:571` refuses an answered `after-success` AEM command, but only the BIND_RX's arrival is graded to fall inside the window (`run.py:563`). The AEM's arrival is only reported. Grade it the same way, so the AEM half of the window check cannot pass vacuously.
- **S2 Tests.** The new ORDER clause "a frame left the mailbox after the reset port fired" has no grader control of its own. Host B17's defect `plat-reboot-serves-the-loop-after-the-port` covers it on the host. A control that inserts a TX line after the port would cover it in the CPU simulation.
- **S3 Tests (R821-1 S2, retained, not taken by the ruling).** `quiet-without-the-face-poll` still escapes at this head (`receipts/fw_probes-r1-script-at-head.json`).
- **S4 RTL (R821-1 S4, retained; needs a decision).** The author measured the conflict between the ruling's two conditions. A 0 tie adds `.i_reboot_req (1'd0),` to the all-fabric top at 1x1 and 8x8 (`author-r2/receipts/exports/compare.txt`, r1-tie). I confirmed the receipt. So the tie and byte-identical exports cannot both hold. Publishing the conflict, rather than choosing, was correct.
  - Separately, the port's own contract at `hdl/milan/milan_datapath.sv:618` still says "tie 0" while the all-fabric SoC leaves it unconnected. It is harmless, since the port is unread at `CTRL_SPLIT_P = 0`.
  - My recommendation is to accept the one-line export change. Otherwise, reword the port comment to say the all-fabric SoC leaves the port unconnected and unread.
- **S5 Tests.** B20 (`test_plat_boot.cpp:895`) holds "ADP's next commit" and calls it the DEPARTING without checking it is one. Asserting the held frame's message_type (ENTITY_DEPARTING) would pin the claim. The later all-frames-after-the-DEPARTING check is robust either way.
- **S6 RTL.** `aecp_reboot_accepted` (`aecp.c:205`) is the only AECP accessor without `aecp_enter`, because it takes a `const` pointer. It is harmless from the platform's gate. A comment saying why it needs no re-entry guard would keep a reader from "fixing" it.

## Round-1 findings, resolved or retained at this head

I read these after my own pass over the delta.

| Finding | State at d08d30c6 | Evidence |
|---|---|---|
| R821-1 F1 / R822-1 F1, commands after SUCCESS and frames after DEPARTING | **Resolved at its cause** (option (a)). The test-coverage gap left by the fix is the new F1 above. | `ctrl_plat.c:175-196` gate, `:352-375` depart, `:377` step. R821-1's `fw_probes.py` (sha256 `5683e03e71502a02...`, unchanged) at this head: `behaviour-acmp-after-success` rc 0, no failed check, `acmp_frames_after_success=0 sink_bound=0 frames_after_departing=0`, `acmp_frames_after_departing=0 port_writes=1` (`receipts/fw_probes-r1-script-at-head.*`). Host B19-B21, B17 and their defects; CPU-simulation BIND_RX and AEM in the window. |
| R821-1 F2 / R822-1 F2, early-reset plant | **Resolved** | The plant writes the port in the take that accepts the REBOOT. In the author's self-test receipt (`author-r2/receipts/gates/lane/reboot.log:46`) it is caught by "ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired". `plant_point` matches `plant.words in f`, and `control` matches every word. |
| R821-1 F3 / R822 S4, the bound | **Resolved** | `REBOOT_RESET.md:295-305`: no firmware-stage bound while a ring is held, with the processor's MAC sentence quoted. 424,271 bus cycles is stated as one scenario's measurement, and the figure is re-measured because the sequence changed. The receipt (`reboot.log:37-38`) gives port − REBOOT = 142,487,669 − 142,063,398 = 424,271. The PR body and the simulation README agree. |
| R822-1 F3, hash seed | **Resolved** | `run.py:825` sets `PYTHONHASHSEED=0` before any export. Child exports inherit it (`run.py:376` builds its env from `os.environ`). Author receipts: `reboot.rc` 0 (self-test) and `reboot_plain.rc` 0, run under the published `scripts/env/env.sh`, which `unset PYTHONHASHSEED`. I did not re-run the CPU simulation. |
| R822-1 R1 | **Resolved**, exact text | `MAILBOX_SPLIT.md:1596-1598` |
| R821-1 S1, index before lock | **Resolved** | `test_aecp.cpp` ENTITY 1 under a foreign lock asks for NO_SUCH_DESCRIPTOR; defect `reboot-lock-before-the-index`. My R821-1 probe `lock-before-the-index` is now caught: rc 1, expected test and words. |
| R821-1 S3 / R822 S1, mixed-replay control | **Resolved** | control `replay-mixed`, caught with "a write half applied" (`reboot.log:57`) |
| R821-1 S2 | Not taken (ruling); retained as S3 | still escapes |
| R821-1 S4 | Not taken: a conflict, published; retained as S4 | export receipts |
| R822 S2, S2 base side | **Resolved** | `author-r2/receipts/s2-base/`: tables, logs, `results.json` digests, the compare reproducing 31 at the base and 5.416 ms |
| R822 S3, CDC census row | **Resolved** | `cdc_census.gen.py:122`; I regenerated it at the head and the SVG and drawio are byte-identical (`receipts/cdc-regen.log`) |

## Lens results (this round, at d08d30c6)

```text
[R821] PASS Conformance — sw/firmware/ctrl/plat/ctrl_plat.c:175-196,352-388; aecp/aecp.c:195-208,402-406,635-642; aecp_commands.c:547-569; protocol-processor docs/architecture/06_aecp_engine.md 6.11 at a9e84b66; author-r2 gates/lane/reboot.log — the window against 6.11 and the ruling's items 1-4: no take from the SUCCESS (gate on every bound channel), loop stopped once the REBOOT's frames are out, DEPARTING committed only once every other ring has drained (stricter than 6.11's in-flight allowance, so DEPARTING is last), port after ADP's ring; the 7.4.43 routes unchanged; acceptance 2-5 met, item 1 partial as ruled (item 7)
[R821] PASS RTL — ctrl_plat.c gate/taking/taken/depart/step and ctrl_plat.h:23-41,127-129 against sw/firmware/ctrl/loop/ctrl_loop.c (unchanged) — the loop's bind API is used as specified (bind_rx refuses only ch>=MBX_N_CH or a NULL fn, neither reachable; set_rx_ready keeps the wrapped ready; the ADP tap chain is wrapped whole); no runtime rebind after the gate (only boot-time attaches, srp destroy only on init failure); reboot FSM 0->1->2->3 with no exit, ring compares at 16 bits as before; no HDL in the delta; ledger sizes 18,528/20,016/19,184/21,328 B carried by sw/litex/ctrl_memory.py:217, ctrl_memory_ledger.py:26, SPLIT_CONTROL_MEMORY.md:97
[R821] PASS Robustness — ctrl_plat.c:331-346 quiet() (store timed on the NOW_MS register, mbx.c:513; face and console still polled), :352-375; REBOOT_RESET.md:295-298 — held ring documented as unbounded, as the processor documents for its MAC; a repeated REBOOT after acceptance is never taken (AECP gated); refusals and no-port leave the gate open (B13, B14, Core refusals); frames left in rings drop whole at the mailbox (RX_DROP, mbx_contract.h:846-866); events not drained after the loop stops affect nothing before the reset
[R821] MINOR Tests — test_plat_boot.cpp:852, test_aecp.cpp:1844 — F1 (two gate defects escape every host test; one escapes the AECP core arm)
[R821] MINOR Docs — REBOOT_RESET.md:272-274,309, PR ruling-item-1 row — F1 (evidence claims "any channel" and "from the SUCCESS" beyond what B19 proves); every other changed doc checked: REBOOT_RESET.md section 8 figures against the receipt, MAILBOX_SPLIT.md:1596-1598, both READMEs, gtest README exclusion row, SPLIT_CONTROL_MEMORY.md:97, ctrl_reboot README tables and counts (5 plants, 7 controls; plat 53 / 13 REBOOT; AECP 152 / 13 REBOOT; control 583, counted from the tables at the head)
```

Tests outside F1 that I checked and found sound:

- B20's and B21's defects;
- the B17 widening;
- plant and control word matching;
- the `frame-after-the-departing` control's DEPARTING detection (byte 15 message_type 1);
- the `replay-mixed` edit;
- `answered`/`NOANSWER` in `sim_main.cpp`. NOANSWER is not graded, but every ORDER clause still applies.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ctrl_plat.c, aecp.c, aecp_commands.c, 06_aecp_engine.md 6.11, the ruling, author reboot receipts | R821-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| RTL | CLEAN | ctrl_plat.c/.h against ctrl_loop.c/.h, module attaches, ledger sources, milan_datapath.sv:614-619 and :10149, milan_soc.py:1376-1385 | R821-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Robustness | CLEAN | ctrl_plat.c quiet/depart, mbx.c:513, mbx_contract.h RX_DROP, REBOOT_RESET.md section 8 | R821-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Tests | UNCLEAN (F1) | test_plat_boot.cpp B17-B21, test_aecp.cpp REBOOT tests, plat_mutants.py, aecp_mutants.py, run.py, sim_main.cpp; my probes | R821-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Docs | UNCLEAN (F1) | REBOOT_RESET.md, MAILBOX_SPLIT.md, SPLIT_CONTROL_MEMORY.md, aecp/plat/gtest/ctrl_reboot READMEs, cdc_census.*, PR body, REVIEW READY | R821-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |

## What I executed

All of this ran in disposable copies under the packet's `scratch/`. Nothing ran in the review clone.

- **Archive check.** `scripts/verify_manifest.py` on archive `009d1406`: all 683 `author-r2/` files match their published sha256, none is unlisted, and 15 are path-redacted (`receipts/manifest-verify.txt`).
- **Host probes**, run with the repository's own arms (platboot1, and the AECP core arm in app mode at two interfaces). Each plants into a copy, as the campaign's own `plant()` does: `head`, `gate-skips-maap-and-srp`, `gate-from-the-handover`, and the AECP `head`/`handover` pair.
- **R821-1's `fw_probes.py`**, unchanged, on a shared clone of the head with its submodules at their gitlinks: `behaviour-acmp-after-success`, `lock-before-the-index`, `quiet-without-the-face-poll`.
- **CDC census.** `cdc_census.gen.py` regenerated into scratch: SVG and drawio byte-identical to the head's.
- **Hosted checks.** A read-only snapshot of the hosted check runs at the head (`receipts/hosted-checks-snapshot.txt`, 19:38Z). Most contexts were queued or in progress. `changes`, `docs-check-no-git`, `docs-gates-1`, `wire-accountability` and `full-ci-gate` were complete-success; physical gPTP was skipped. No `rtl-fast` verdict was present yet. This is not acceptance evidence; the manager owns it.
- **Restore check (`receipts/restore-check.txt`).** HEAD and tree are exact, the worktree equals the index and the index equals HEAD. The index modes and blobs equal the HEAD tree. All five submodule gitlinks are at their recorded commits, with `external` uninitialised as at the start. Importing the repository's test modules left eight ignored `__pycache__/` directories, untracked and listed in the receipt. No tracked byte changed.

## Real limits

- I did not re-run the REBOOT CPU simulation. Its PASS, the 12-of-12 self-test and the two unseeded runs rest on the author's archived receipts, which I verified against the manifest and spot-read.
- I did not run any firmware campaign, sweep, census, builder, behave or workflow bank. Those rest on the author's gate receipts.
- I did not re-run R822's `run_probe_window.sh`. My own behaviour probe covers the same window.
- The CPU simulation builds no datapath, so "on the wire" means the mailbox's transmit face. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank runs at this head, and I infer none.

## Pending manager duties

- The decision on S4 (the tie, or byte-identical exports).
- Whether the comment-rule note above makes RESIDUE.
- The current-dev merge candidate (source base 1d6bf555, live dev fa6c094b8e196666a8a8865788d5e83b5bbaea09) with the builder and native banks, and its receipts.
- Hosted and act acceptance at the exact head (`rtl-fast`, then `verilator-suites` and `yosys-portability` once ready).
- The external review.
- Item 1 stays partial and the PR stays "Relates to #871", as ruled.

R821-2 FINISHED
