[R822] NEGATIVE - exact head d08d30c6ecbac2e45867c3a509ef309ed081ab15

# R822-2: external review of PR #881 (issue #871, S11 AECP REBOOT), round 2 delta

- Head under review: `d08d30c6ecbac2e45867c3a509ef309ed081ab15`, tree `42784db20be532a060bc927960ee12cf592a85c0`. The live PR head equals it.
- Delta: `b29f94d7..d08d30c6`, five one-line commits with one parent each. `git diff --check 1d6bf555 HEAD` is clean.
- Inputs, in this order:
  - AGENTS.md;
  - the #871 body;
  - the round 2 ruling (#871 issuecomment-6789331293);
  - the executor's TAKEN and REVIEW READY comments;
  - the full delta, read before any prior review;
  - R821-1 (issuecomment-6788965651) and R822-1 (issuecomment-6789318251), read after my own pass;
  - the author packet `review-evidence/665s11-r1/author-r2` at archive `009d1406`;
  - the hosted check-run list at the exact head.
- Verdict: NEGATIVE, for one open MINOR (F1) under Tests and Docs.
  - Conformance, RTL and Robustness are covered clean at this head.
  - Every round 1 finding is resolved at its cause.

## What I executed (receipts under `receipts/`)

All probes ran on a disposable copy of the head (`scratch/probe-tree`, never published). The review clone was never edited.

| Run | Result | Receipt |
|---|---|---|
| Host `platboot` at 1 and 2 interfaces, AECP `Core.Reboot*`, clean head | rc 0, rc 0, rc 0. B19, B20 and B21 OK at both interface counts | `probes/clean--*.log` |
| The head's own 13 platform REBOOT defects (`plat-reboot-*`), run through `ctrl_mutants.campaign` | 13 of 13 caught on their own words | `campaign-plat.log`, `.rc` |
| The head's own 13 AECP REBOOT defects (`reboot-*`), run through `aecp_mutants.campaign` after its table-drift control | 13 of 13 caught, including `reboot-lock-before-the-index` and `reboot-acceptance-unreported` | `campaign-aecp.log`, `.rc` |
| Five reviewer mutants (`scripts/r822_probes.py`) | 4 survive and 1 is caught (table below) | `probes/mutant-results.json`, `probes/<name>--*.log` |
| `docs/diagrams/cdc_census.gen.py` re-run, `rsvg-convert -w 1900` | drawio, svg and png byte-identical to the committed files | `census/census-regen.txt` |
| Author packet `receipts/INDEX.md`, every row re-hashed | 663 of 678 verify; 15 mismatch (S2) | `packet-index-verify.txt` |
| Review clone after all probes | HEAD, tree, `git ls-files -s` digest, submodule status and gitlinks equal to the baseline; worktree clean | `baseline-index.sha256`, `baseline-submodules.txt`, `gitlinks-after.txt` |

The five reviewer mutants:

| Reviewer mutant | Edit | Outcome |
|---|---|---|
| `gate-skips-maap-and-srp` | `ctrl_plat.c:191`: the receive gate is installed only for `ch < MBX_CH_MAAP` | **survives** (F1) |
| `depart-ignores-maap-and-srp-rings` | `ctrl_plat.c:357`: the DEPARTING waits only on the ACMP and AECP rings | **survives** (F1) |
| `accepted-from-the-poll` | `aecp.c:207`: `aecp_reboot_accepted` true only from `reboot >= 2` | survives (S1) |
| `quiet-only-after-the-port` | `depart()` services the store only once the port has fired | survives (S4; the effect is equivalent today) |
| `no-adp-poll-in-state-2` | the `adp_poll` call at `ctrl_plat.c:366` removed | caught by `Boot.B18ADepartingTheRingRefusedHoldsTheReset` |

## Ruling items and prior findings, resolved at this head

| Item / finding | Status | Evidence |
|---|---|---|
| Ruling 1, R821-F1, R822-F1: processor parity in the window | **RESOLVED at the cause**; residual test gap filed as F1 below | See "Ruling 1 in detail" after this table |
| Ruling 2, R821-F2, R822-F2: the early-reset plant | **RESOLVED** | The plant (`run.py` `PLANTS['reset-before-the-response']`) writes the port inside the take that accepts the REBOOT. The author's self-test catches it with "ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired" (`gates/lane/reboot.log:46`). `plant_point` now requires `plant.words in f`, and `control` requires every word of a control |
| Ruling 3, R822-F3: the hash seed | **RESOLVED** | `run.py:825` sets `os.environ['PYTHONHASHSEED'] = '0'` before `common()`. Every export is a child process that inherits it: `exported()` → `boot.run` → `subprocess.run` with no `env=`. The author's `reboot.log` and `reboot_plain.log` came from an environment that unsets the seed (`scripts/env/env.sh:7`), and both are rc 0 with `ctrl_reboot: PASS`. I did not rerun the simulation myself (limits) |
| Ruling 4, R821-F3, R822-S4: the bound | **RESOLVED** | See "Ruling 4 in detail" after this table |
| Ruling 5, R822-R1 | **RESOLVED**, exact text | `MAILBOX_SPLIT.md:1597` |
| R821-S1: index before lock | TAKEN | Test `test_aecp.cpp:1826` and defect `reboot-lock-before-the-index`, which I reran (caught). The author re-ran R821's probe at this head and it is caught |
| R821-S3, R822-S1: mixed-replay control | TAKEN | `CONTROLS['replay-mixed']`. `control()` now adds `grade_cut`. The author's self-test catches it with "a write half applied" (`reboot.log:57`) |
| R822-S2: the base side of S2 | TAKEN | `s2-base/` publishes both sides and the compare |
| R822-S3: CDC census row | TAKEN, via the generator | `cdc_census.gen.py:123`. My re-run reproduces drawio, svg and png byte for byte |
| R821-S4: tie `i_reboot_req` to 0 in the all-fabric instances | **NOT TAKEN; conflict published** | See "R821-S4 in detail" after this table |
| R821-S2: the face poll in `quiet()` | Not in the ruling; still a survivor | The author's re-run of R821's `quiet-without-the-face-poll` gives rc 0. It remains optional |

**Ruling 1 in detail.**
- The code:
  - `ctrl_plat.c:175-195`: every bound channel's take sits behind `taking()`, which reads `aecp_reboot_accepted` (`aecp.c:205-208`). That flag is set when the SUCCESS response is built (`aecp.c:402-406`).
  - `ctrl_plat.c:382-385`: once `aecp_reboot_due`, the loop is no longer serviced.
  - `ctrl_plat.c:352-375`: the DEPARTING is committed only after every other ring has drained, and the port fires after ADP's ring has drained.
  - `sw/firmware/ctrl/loop/` is untouched. The rebind goes through `ctrl_loop_bind_rx`/`ctrl_loop_set_rx_ready` (`ctrl_loop.c:18-33`), and the copied `ready` keeps each module's own context.
- The evidence:
  - Host B19, B20 and B21, with planted defects `plat-reboot-takes-frames-after-the-success`, `plat-reboot-transmits-after-the-departing` and `plat-reboot-departs-before-the-rings-drain`. I reran all three and each is caught.
  - B20's defect, rerun by the author, puts 18 frames on channels 1, 3 and 4 after the DEPARTING (`probes/b20mut.out`).
  - The author's re-run of R821's `behaviour-acmp-after-success`, unchanged at this head: `acmp_frames_after_success=0 sink_bound=0 frames_after_departing=0`, rc 0. R822's `run_probe_window.sh`: `sink.bound` 0, no ACMP frame.
  - CPU simulation (`reboot.log:37`): the BIND_RX reached the mailbox in the window at cycle 142,279,206, after the SUCCESS at 142,279,069 and before the port at 142,487,669. It was not answered. No non-ADP frame left after the DEPARTING.
  - `REBOOT_RESET.md` section 8 (`:264`, `:270-282`) is corrected.

**Ruling 4 in detail.**
- `REBOOT_RESET.md:295-304` states that the firmware stage has no bound while a ring is held, and quotes the processor's MAC sentence. It then gives "One measurement ... These are that scenario's figures, not a bound". The PR body does the same in the "Measurements" section. The simulation README's BOUND row reads "this scenario's measurement, not a bound".
- The figure is now 424,271 bus cycles (212,135 CPU cycles, 4.243 ms), not round 1's 445,707. The round 2 firmware and script changed the scenario.
- I checked every figure against the author's `gates/lane/reboot.log:37-39`:
  - SUCCESS 2.157 ms;
  - notification 2.300 ms;
  - DEPARTING 4.199 ms;
  - port 4.243 ms;
  - drain 581.124 ms;
  - window AEM command 2.157 ms and BIND_RX 2.158 ms.

**R821-S4 in detail.** The author's export diff (`exports/compare.txt`, `r1-tie`) shows that the tie adds `.i_reboot_req (1'd0),` to the generated all-fabric top at both shapes. So the ruling's "with the all-fabric exports still byte-identical" cannot hold together with the tie.
- The author did not take the suggestion, and published the conflict in REVIEW READY. That follows AGENTS.md section 2.
- The port is unread at `CTRL_SPLIT_P = 0`.
- Without the tie, the exports are byte-identical to the base apart from timestamps and hierarchy-comment order. Two exports of the base itself also differ in that order.
- This needs a manager decision. I do not count it as a finding against the lane.

## Findings

### F1 MINOR: the parity tests exercise fewer channels than they claim

- **Lenses:** Tests, Docs.
- **Where:**
  - The receive gate: `sw/firmware/ctrl/plat/ctrl_plat.c:187-195`.
  - The other-ring wait: `ctrl_plat.c:357`.
  - B19: `sw/firmware/ctrl/test/test_plat_boot.cpp:852-883`, header comment `:61-64`.
  - B21: `test_plat_boot.cpp:920-942`, header comment `:68-69`.
  - The claims: `docs/design/REBOOT_RESET.md:274` ("So no ADP, ACMP, AECP, MAAP or SRP frame is taken"); `REBOOT_RESET.md:309`, whose evidence row says B11 to B21 prove "no frame of any channel taken from the SUCCESS" and a DEPARTING "which waits for every other ring"; `sw/firmware/ctrl/plat/README.md:127`; the PR's ruling-1 rows.
- **Authority:**
  - The ruling's item 1: "no received frame of any channel is taken" and "a host test and a planted defect for each".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- **Evidence (executed):**
  - B19 puts frames only on ADP (ENTITY_DISCOVER), ACMP (BIND_RX) and AECP (AEM). B21 holds only ACMP's ring (`acmp_busy`). The CPU simulation sends only an AEM command and a BIND_RX.
  - My mutant `gate-skips-maap-and-srp` leaves MAAP and SRP ungated. It passes every `platboot` test (`probes/gate-skips-maap-and-srp--platboot1.log`, rc 0).
  - My mutant `depart-ignores-maap-and-srp-rings` lets the DEPARTING go out while a MAAP or SRP ring still holds a frame. It also passes every test (`probes/depart-ignores-maap-and-srp-rings--platboot1.log`, rc 0).
  - The head's own planted defects remove each mechanism for all channels at once, so they cannot show a per-channel loss.
- **Impact:**
  - Two of the five channels in the parity claim have no test that fails when they lose the gate or the drain wait.
  - Consider a later change that rebinds or re-readies SRP or MAAP after `gate()` runs, or that narrows either loop. It would let MSRP or MAAP frames be taken after the SUCCESS, or committed ahead of a DEPARTING that then precedes them on the wire, and every test would stay green.
  - The authoritative evidence row claims more than the tests prove.
- **Required outcome:** Either of the following:
  - B19 also delivers a MAAP and an SRP frame after the SUCCESS, and B21 also holds the SRP and MAAP rings (or every non-ADP ring in turn). Each is backed by a planted defect that removes the gate or the wait for one channel only, and that defect is caught on its own words.
  - The evidence claims at `REBOOT_RESET.md:309`, `plat/README.md:127`, the B19/B21 headers and the PR rows are narrowed to the channels actually exercised.

  The first is preferred, because the code's claim covers all five channels.
- **Verification:** At the fixed head, `python3 -B scripts/r822_probes.py <tree-copy> <out> gate-skips-maap-and-srp depart-ignores-maap-and-srp-rings` gives `platboot1` rc 1 for both. Alternatively, the narrowed text can be read.

### R1 RESIDUE: bench lane labels in new source comments (owner comment rule)

- **Lens:** Docs.
- **Where:** `sw/firmware/ctrl/test/test_plat_boot.cpp`:
  - `:61` `//   B19 from the REBOOT's SUCCESS ...`
  - `:65` `//   B20 once ENTITY_DEPARTING ...`
  - `:68` `//   B21 ENTITY_DEPARTING waits ...`
  - `:170` `// Set, reads of ACMP's TX_TAIL find its last word not yet taken (B21)`

  These are new in this delta. The edited `B17` (`:56`) and `(B12)` (`:187`) lines touch existing instances, which #746 tracks.
- **Note:** R821-1 read these IDs as the file's own test-ID scheme. The owner's rule names `B17` as an example of a bench lane label, so I apply the rule.
- **Exact fix:**
  - At `:61`, `:65` and `:68`, key the header entries by the test names: `NoFrameOfAnyChannelIsTakenFromTheSuccess`, `NoOtherChannelTransmitsAfterTheDeparting` and `TheDepartingWaitsForEveryOtherRing`.
  - Line 170 becomes `// Set, reads of ACMP's TX_TAIL find its last word not yet taken, so the DEPARTING must wait for that ring`.

  Test identifiers and failure strings are not comments and are out of scope here.

### R2 RESIDUE: ADP's poll is said to run "from the loop's last pass"

- **Lens:** Docs.
- **Where:** `docs/design/REBOOT_RESET.md:290`, `sw/firmware/ctrl/plat/README.md:88` and `sw/firmware/ctrl/plat/ctrl_plat.h:37-38`.
- **What is wrong:** `depart()` calls `adp_poll` only in state 2 (`ctrl_plat.c:363-367`), that is, after every other ring has drained. It does not run from the loop's last pass. The store and its F_NVM are serviced from the loop's last pass, as stated.
- **Exact fix:**
  - `REBOOT_RESET.md:290`: "From the loop's last pass the platform services the saved-state store on its own centisecond and its F_NVM, and, once every other ring has drained, ADP's poll until the port fires."
  - `README.md:88`: the same wording.
  - `ctrl_plat.h:37-38`: "... services the saved-state store and its F_NVM, and, from ADP's shutdown, ADP until the port."

### Suggestions (do not affect coverage)

- **S1 (Tests): the gate's start point is not pinned.**
  - `accepted-from-the-poll` makes `aecp_reboot_accepted` true only from AECP's next poll (`reboot == 2`), and it survives both the host and the AECP arms.
  - The only frames it could let through are MAAP and SRP frames already in their rings in the same service pass as the REBOOT. Those channels are serviced after AECP's (`ctrl_loop.c:145-149`).
  - The extended B19 under F1 could deliver those frames in the REBOOT's own pass, which would pin "from the SUCCESS" exactly.
- **S2 (Docs, author packet): the receipts index is stale for 15 files.** `receipts/INDEX.md` in archive `009d1406` disagrees with 15 published files: 5 under `gates/docs/` and 10 under `gates/wf/` (listed in `packet-index-verify.txt`).
  - Each published file is smaller than its indexed size and carries the `<home-path>` placeholder. So a second placeholder pass ran after the index was generated.
  - All 15 are generic gate logs whose `.rc` files verify (rc 0). None is a REBOOT-specific receipt.
  - In one placeholder, a path is spliced to `<scratch>/gates<home-path>/host/bin/...`.
  - Fix: regenerate `INDEX.md` after the last sanitising pass.
  - The packet carries no detached signature or signed manifest. I verified the index hashes only.
- **S3 (Tests): the window's AEM command is not checked to arrive inside the window.** The ORDER grade checks that the window's BIND_RX arrived between the SUCCESS and the port (`run.py:563-564`). It reports the window's AEM command but does not check it.
  - Today it arrives at 2.157 ms, inside the window.
  - Add `log.rx_end.get('after-success')` to the same bound, so that a timing shift cannot make "the AEM command after the SUCCESS is not answered" pass vacuously.
- **S4 (Tests): store service before the port is claimed but not pinned.** `quiet-only-after-the-port` survives: the store is not serviced between the loop's stop and the port.
  - Today that is equivalent in effect: the window is about 2 ms, and the write resumes after the port.
  - Section 8 claims the service, so a test that holds a ring across a store deadline would pin it. This is optional.

## Lens coverage (this round)

| Lens | Result | Artifacts examined at `d08d30c6` |
|---|---|---|
| Conformance | PASS | See "Conformance in detail" below |
| RTL | PASS | See "RTL in detail" below |
| Robustness | PASS | See "Robustness in detail" below |
| Tests | UNCLEAN (F1) | See "Tests in detail" below |
| Docs | UNCLEAN (F1); R1 and R2 RESIDUE | See "Docs in detail" below |

**Conformance in detail.**
- `ctrl_plat.c:175-195` and `:352-390`, and `aecp.c:197-208` and `:402-406`, checked against:
  - the ruling's items 1 to 4;
  - REQ-FWX-001 and the processor's section 6.11 as quoted in `REBOOT_RESET.md` section 8;
  - IEEE 1722.1-2021 7.4.43, for the refusal order, now with index before lock (`test_aecp.cpp:1826`);
  - Milan v1.2 5.6.3.3, for the DEPARTING before the port.
- The CPU-simulation ORDER and REFUSE receipts (`reboot.log:37-59`).
- Acceptance items 2 to 5 are still met. Item 1 is unchanged (partial; "Relates to #871" is kept, per ruling 7).

**RTL in detail.**
- The delta changes no HDL.
- The firmware state machine (`ctrl_plat.h:127`, `reboot` 0/1/2/3; `ctrl_plat.c:352-390`) is complete: each state has its exit, and the error or held path is an explicit unbounded wait, documented.
- The loop and mailbox contracts are unchanged: `sw/firmware/ctrl/loop/` is untouched, and binding goes through the public API (`ctrl_loop.c:18-33`, service order `:143-160`).
- The all-fabric exports are byte-identical apart from timestamps and order (`exports/compare.txt`).
- The CDC census was regenerated identical (`census/census-regen.txt`).

**Robustness in detail.**
- Repeated commands in the window: AECP's own `ready` (`aecp.c:197`) and the gate. Caught by `reboot-serves-after-its-success` and by B19.
- Held and refused rings: B12, B18 and B20 (DEPARTING held 5 s), and B21.
- Two interfaces: `platboot2` passes.
- Feature disabled: the gate is installed only with a reset port (`ctrl_plat.c:320-322`), and `plat-reboot-without-a-port` is caught.
- The unbounded held ring is documented as matching the processor (`REBOOT_RESET.md:295-298`).
- Reset during activity: the B16 and JOURNAL receipts.

**Tests in detail.**
- `test_plat_boot.cpp` (B17, B19, B20, B21);
- `test_aecp.cpp:1813-1844`;
- `plat_mutants.py` and `aecp_mutants.py`;
- `run.py` PLANTS, CONTROLS, `plant_point` and `control`;
- `sim_main.cpp` `answered`;
- my 26 reruns of the head's own defects and 5 new mutants;
- the author's self-test and the two unseeded runs.

**Docs in detail.**
- `REBOOT_RESET.md` section 8 and its contents line;
- `MAILBOX_SPLIT.md:1597`;
- `SPLIT_CONTROL_MEMORY.md:97`, together with `ctrl_memory.py` and `ctrl_memory_ledger.py`, against the ledger figures in REVIEW READY;
- the two READMEs and the simulation README, whose figures I checked against `reboot.log` and `reboot_plain.log`;
- `gtest/README.md:324`'s coverage-exclusion row: the composition order checks out, and `MBX_N_CH` is 5;
- the PR body, which equals the packet's `PR-BODY.md` apart from a trailing newline;
- the comment-rule scan of every added comment.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_plat.c:175-195,352-390`; `aecp.c:197-208,402-406`; `REBOOT_RESET.md` section 8; the author's CPU receipts `gates/lane/reboot.log`, `reboot_plain.log`; the R821 and R822 probe re-runs | R822-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| RTL | CLEAN | Delta with no HDL; firmware FSM `ctrl_plat.h:127`, `ctrl_plat.c:352-390`; `ctrl_loop.c:18-33,120-160` (untouched contract); `exports/compare.txt`; census regenerated identical | R822-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Robustness | CLEAN | B12, B16-B21 at if1 and if2 (`probes/clean--platboot*.log`); `campaign-plat.log`; `campaign-aecp.log`; the held-ring statement `REBOOT_RESET.md:295-298` | R822-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Tests | UNCLEAN (F1) | `test_plat_boot.cpp:852-942`; `plat_mutants.py`; `aecp_mutants.py`; `run.py` PLANTS, CONTROLS, `plant_point`; `probes/mutant-results.json` | R822-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |
| Docs | UNCLEAN (F1) | `REBOOT_RESET.md:264-310`; `MAILBOX_SPLIT.md:1597`; `plat/README.md:79-135`; `aecp/README.md:160-168`; `ctrl_reboot/README.md`; `gtest/README.md:324`; the PR body | R822-2 | d08d30c6ecbac2e45867c3a509ef309ed081ab15 |

The RESIDUE items R1 and R2 do not affect coverage; they belong on the manager's residue checklist.

## Real limits

- I did not run the CPU REBOOT simulation (`tb/verilator/ctrl_reboot/run.py`) myself at this head. For ruling items 2 and 3, the plant and control words, and the figures, I rely on the author's published receipts (`gates/lane/reboot.log`, `reboot_plain.log`, rc 0) and on reading the code.
- No full banks were run, by instruction: no full sweep, builder, Yosys, publication census, S2 harness or docs workflow. Those rest on the author's receipts.
- No manager source bank exists at this head, and I claim none.
- At review time the hosted checks at the exact head were 12 success, 1 skipped and 38 queued or in progress, with none failed. They are not evidence yet, and the manager owns hosted and local-replica acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof. Builder gate 11's calibration arm is not run on the author's host.
- I found no signature in the author packet, so verification is by the packet's own index hashes (S2).

## Pending manager duties

- Decide R821-S4's conflict with the ruling's byte-identical condition: either the tie with a one-line export change, or no tie.
- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) with the builder and native banks, and link the receipts.
- Accept the hosted exact-head gates once they complete, and the local replica.
- Carry R1 and R2 to the residue checklist. Have the author regenerate the packet index (S2).
- After the F1 fix, re-review the Tests and Docs lenses at the new head. A test-only or doc-only change keeps the Conformance, RTL and Robustness coverage only if no artifact in their scope is touched.
- Item 1 stays partial, so #871 stays open ("Relates to #871").

R822-2 FINISHED
