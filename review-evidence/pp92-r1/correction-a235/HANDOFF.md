# [A235] HANDOFF: PR #109 (issues #92/#93), correction round 1 for R278-1 and R279-1

- Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`, PR #109
- Branch: `92-93-boot-restore` in `$LANES/pp92-93-boot-restore`
- Reviewed head: `156c206cbaedf721f7caef5c94faa21876a28c32` (R278-1 and R279-1, both NEGATIVE)
- Fixed head: `f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3`. It is **local only and not pushed**:
  PR #109 still points at 156c206c. The push is the manager's step.
- Assignment: #92 comment 5807717711
- Simulator: the CI-pinned 5.050 (`$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin`).
  Its wrapper sha256 is `905795b9…e92f`, the same as the reviewers' `env.txt`.
- Parent: `kebag-logic/milan-fpga` `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`, cloned at
  `scratch/milan-fpga`. Its gitlink moved to the fixed head in local commit `44220afc7`, which
  was never pushed. No parent file changed and no ratchet was widened.

## Commits (`156c206..f8d30ec`, one-line subjects, no trailers)

| Commit | Subject | Finding |
|---|---|---|
| `d849257` | Keep a failed binding walk's saved records when the listener only restates its default (#92) | R278 F1 = R279 F3 (RTL and acmp_nvm N8/N9); R279 S5 |
| `6ac5504` | Grade the failed walk's saved record and the restore level pair at the top, every cycle (#92, #93) | R278 F1 (pp_top BW3), R278 F2 = R279 F2 (BW4) |
| `e88f50b` | Grade a device face that answers every read as erased media: done, not failed, blank (#93) | R279 F1 (acmp_nvm N9c) |
| `7297a64` | Say what each NVM tie-off reports and that a failed walk keeps the saved records (#92, #93) | R279 F1 and R278 F1 docs (05, 07, integrator, operator) |
| `39625c9` | Refuse a zero read deadline at elaboration instead of wrapping it to 2^32 clocks (#93) | R278 S1 |
| `f8d30ec` | Render the dataflow diagram's PNG again now that it shows the admission gate and the manager arbiter (#92, #93) | R279 S4 |

`git diff --stat 156c206..f8d30ec`: 11 files, +414 −54. One RTL file changed
(`KL_acmp_nvm_shadow.sv`). The top, the gate, the arbiter and the port are unchanged.

## 1. The shared MAJOR (R278 F1 = R279 F3): a failed walk keeps the saved records

### Reproduced at the reviewed head first (`logs/repro/`)

| Probe | Author | At 156c206 |
|---|---|---|
| P1, `run_p1.sh` (sinks 0, 3 and 7 saved; the walk fails at sink 3; one read-only GET of sink 0) | R278 | **16 checks: 7 PASS, 9 FAIL**. For causes 2, 3 and 1 the GET costs 1 erase and 1 write, sink 0's valid byte goes `03 → 00`, and a healthy reset restores 2 preloads of 3 (`p1-head.log`) |
| P2, `run_p2.sh` (pp_top BW3 with NVM settled before the BIND) | R278 | **FAIL**: region 0x20 takes 1 write and 1 erase, byte 8 goes `03 → 00` (`p2-head.log`) |
| FW, `probe_failed_walk.py` (causes 1-3) | R279 | **341 checks: 335 PASS, 6 FAIL**: every cause writes sink 0 unbound, and the healthy reboot reads valid `0x80` (`fw-head.log`) |

### The fix (`d849257`, `hdl/acmp/KL_acmp_nvm_shadow.sv`)

The capture compare now treats **two unbound records as equal, whatever their other fields
hold**:

```
assign c1_diff_w  = (c1_vld_r != valid_r[c1_sink_r])
                  || (c1_vld_r && (SHW_W_C'(c1_proj_r) != cmp_data_w));
```

This is one of the two outcomes both reviews named. The atomic reject still clears `valid_r` only,
and the rejected sinks' restored fields stay in the shadow RAM. After a failed walk the listener
writes back its default, which is an unbound record, and that no longer compares unequal. So it
is never captured, dirtied or flushed. The torn route (cause 1) is fixed by the same change, as
are the device route (2) and the deadline route (3). The alternative, the reject rewriting each
rejected sink's RAM image, was not taken: it would touch the walk's sequencing, and #93's
behaviour had to stay as it was.

Why the rule is safe:
- An unbound record carries no binding. Milan v1.2 5.3.8.3 clears the binding parameters on
  unbind.
- No walk preloads an unbound record: the replay skips `!valid_r`.
- A change of bound state still differs: bound→unbound (UNBIND) and unbound→bound (BIND) are both
  written.

The whole suite stayed green with the rule in place, so no existing case depended on two
unbound records differing.

**A consequence to review (decision 5 in PR-BODY.md).** After a failed walk, an UNBIND of a sink
the walk left unbound also writes nothing. The saved binding of that sink therefore comes back on
the next healthy boot. The listener cannot tell that UNBIND from a GET, because both restate an
unbound record. 07 §5.3 and the operator guide say so explicitly, and acmp_nvm N8b grades it.

### The regressions and their failing arms

- **`tb/acmp_nvm` N8a-c** (causes 1, 2, 3). Sinks 0, 3 and 7 are saved, the walk stores sink 0,
  and then it fails at sink 3.
  - A GET of sink 0 is held from reset through the window.
  - Afterwards, a GET of each saved sink is polled.
  - In N8b, an UNBIND of sink 3 follows.
  - Graded: the replies are on the default, in order; nothing is written or left pending; every
    saved record is still byte-exact in the device; and a healthy reset restores all three
    bindings.
- **`tb/pp_top` BW3.** After the device serves the abandoned read, every debounce and flush runs
  out *before* the case's BIND. Region 0x20 must then still hold the saved record, with no write
  and no erase. The BIND and its reset round trip follow as before.

| Arm (`tools/arms.py`, each in its own `git archive` extract) | Edit | Result at f8d30ec |
|---|---|---|
| F1-compare | `c1_diff_w` back to the reviewed head's form | acmp_nvm **9 of 349 FAIL**: N8a-c, three each. After every cause the held GET writes sink 0 unbound (`sink 0 holds 000000000000000000000000`), and the healthy reset restores 2 of 3 |
| F1-compare-top | the same edit | pp_top **2 of 1,414 FAIL**: BW3 "left sink 0's saved record in the device, nothing written (byte 8 03 -> 00)", and the BIND's region then written twice |

### The reviewers' own probes at the fixed head (`logs/probes/`)

| Probe | Result at f8d30ec |
|---|---|
| R278 P1 | **16 checks: 16 PASS**. All four cases: 0 writes, dirty 0x00, sink 0 valid byte `03` (`R278-P1-final.log`) |
| R278 P2 | **PASS**: "sink-0 region writes 0 erases 0 since the boot; saved byte8 03 now byte8 03" (`R278-P2-final.log`). The probe's text anchors no longer match, because BW3 now takes the same snapshot. `tools/p2_pp_top_bw3_get_rebased.py` is the reviewer's script with only its two anchors re-pointed, and its logic is unchanged. The same copy still FAILs at 156c206 (`logs/repro/p2-head-rebased.log`: byte 8 `03 → 00`) |
| R279 FW | **358 checks: 358 PASS** (349 suite + 9 probe). Every cause: after GET writes=0 erases=0, sink0 kept=1, byte8=03; healthy reboot valid=0x81 (`R279-FW-final.log`) |
| R279 unwired | **351 checks: 351 PASS**: no grant → done fail blank cause 3; err → done fail blank cause 2 (`R279-unwired-final.log`) |

## 2. R278 F2 = R279 F2: the top's `restore_done_o`/`restore_busy_o` composition (`6ac5504`)

`tb/pp_top/pp_top_wrap.sv` gains three observe-only taps:
- `dbg_lsn_released_o`, the gate's `released_o`;
- `dbg_lsn_preload_o`, the listener in X_PRELOAD;
- `dbg_lsn_arm_o`, the listener's A4 discovery arm.

**BW4** grades the top's pins in every cycle of every walk the run makes: section R's blank boot,
BW0-BW3, the boot after BW3, and a walk of its own whose last offer is sink 7's saved binding
seeded in the device model. Its checks:
- from a walk's first busy cycle to the next reset, `restore_busy_o || restore_done_o` holds;
- `restore_done_o` never reads 1 while the gate still owns the listener;
- no preload record write or discovery arm of a walk lands at or after the cycle its
  `restore_done_o` rose.

The walks' terminals lead the release by at least one cycle each, so the composition is exercised
rather than assumed. The S0 comment that claimed the level was "graded in S0" was corrected, and
it now points at BW4.

| Arm | Edit (the same as R278 X-top-* and R279 R1/R2) | Result at f8d30ec |
|---|---|---|
| F2-done-no-release | `assign restore_done_o = nvm_walk_done_w;` | pp_top **2 of 1,414 FAIL**: BW4 finds 8 cycles of done while owned, and in BW4's own walk the last discovery arm lands in the cycle done rose |
| F2-busy-gap | `assign restore_busy_o = nvm_walk_busy_w;` | pp_top **1 of 1,414 FAIL**: BW4 finds 8 cycles that read neither busy nor done |

## 3. R279 F1: the guides now match 07 §5.3's table (`7297a64`, `e88f50b`)

- **operator.md §6.** The two-sentence claim that an unwired backend "publishes the same two bits
  as one that restored every sink" is replaced by a table of what bits 2 and 3 read for each thing
  behind the device face:
  - media that holds the bindings: done, no fail;
  - erased media or a 0xFF tie-off: done, no fail (the same as a full restore);
  - a face that errs or ends a read before the 8-byte header: done and fail, a device error;
  - a face that never answers: done and fail after the deadline, with the port then blocked
    until reset.

  `restore_blank_o` separates the first two rows, and it is also set on a failed walk.
- **integrator.md NVM tie-off cell.** The self-contradicting first sentence is gone. The cell now
  gives the same three outcomes in the same order: erased media reads done, no fail, blank; err
  or a short done fails with a device error; a silent face fails at `NVM_RS_TMO_CYC_P` and
  quarantines the port.
- **The §7 "never wedges the control plane" sentence** is qualified: it covers the faces, not the
  boot controls, and a boot that never pulses `restore_go_i` leaves the ACMP listener held until
  reset.
- **Failed-walk wording.** 05 §5.1, 07 §5.3 (a new paragraph, "A failed walk keeps the saved
  records"), integrator step 3 and operator §6 now state that a failed walk rejects the image,
  not the media. 07 §5.3's "changes nothing here" is now true after a failed walk as well.
- **The verification the reviewer made optional** is now a regression: acmp_nvm N9a-c covers a
  face that never grants (cause 3, one request abandoned, port quarantined), a face that answers
  every READ with err (cause 2), and a face that answers as erased media (done, not failed, blank,
  one header read per sink, nothing preloaded or written).
- **Figure 21** was left as it is: the §7 sentence above it now carries the `restore_go_i` caveat.

## 4. Suggestions

| Suggestion | Disposition |
|---|---|
| R278 S1 = R279 carry: guard `RS_TMO_CYC_P >= 1` | Done (`39625c9`): an elaboration-time `$error`. Receipt `logs/rs-tmo-guard-default-warn.log`: 0 is refused ("RS_TMO_CYC_P must be at least 1") and 3000 elaborates clean. 1 is accepted by the guard, but the simulator's lint then notes that the unchanged compare `rs_wd_r >= 32'(RS_TMO_CYC_P - 1)` is constant (`>= 0`). The behaviour is still correct (every stall cycle expires), and the expression was left alone because the published arm B01 and the reviewers' deadline mutants anchor on its text |
| R279 S4: the stale `20-rtl-dataflow.png` | Done (`f8d30ec`), rendered from the committed SVG (`scratch/20-render.png`) |
| R279 S5: the shadow's `restore_fail_o` port comment says "torn read-back" | Done (`d849257`): "the WHOLE restore aborted, any cause" |
| R279 S1 (per-face top wiring), S2 (same-cycle err with done), S3 (manager-1 back-to-back starvation), S6 (fail/blank ungated for up to four cycles) | Not taken, carried forward as optional. None is required by the round, and S3 is unreachable while manager 1 is tied idle |

## 5. #93's behaviour is kept: every published arm still bites (`logs/arms/`, at f8d30ec)

acmp_nvm, 349 checks:

| Arm | Failures |
|---|---|
| LG01 | 107 |
| LG02 | 71 |
| LG03 | 45 |
| LG02t | 19 |
| LG03t | 7 |
| LG04 | 5 |
| LG05 | 12 |
| LRdone | 108 |
| B01 (no deadline) | 20 |
| B02 (#20's defect, both edits) | 12 |
| B03 (no drain) | 10 |
| BA1 (no abort) | 15 |
| BC1 (cause collapsed) | 13 |
| A01 | 1 |
| B04 | 120 of 342 |

pp_top, 1,414 checks:

| Arm | Failures |
|---|---|
| LG01-top | 8 (BW1 ×4, BW2, BW3's saved-record check, BW4 ×2) |
| B01-top | 2 |
| B03-top | 2 |

Every verdict is KILLED, with FAIL lines and a tally. The nvm_port cause arms C1-C4 are graded by
the figures gate, which passed at f8d30ec (the port RTL is unchanged). The tb READMEs record
these counts: acmp_nvm under "Mutation-proven", pp_top in rows M32-M37.

The pinned-wiring control (`make -C tb/acmp_nvm pinned`, which is expected to exit non-zero)
gives **349 checks: 242 PASS, 107 FAIL**, still including L05a's "sink 0 holds
000000000000000000000000" (`logs/gates/acmp_nvm-pinned.log`).

## 6. Gates

### Processor, lane at f8d30ec (`logs/gates/`, `rc.txt`, `env.txt`)

| Gate | Result |
|---|---|
| `./scripts/run_suites.sh` | exit 0, **31 suites, 15,797 checks, 0 failing**, UPC map PASS. acmp_nvm 349, pp_top 1,434 (1,414 + 20 fixture), lsn_admit 18, nvm_port 136 |
| `./scripts/lint_hdl.sh` | exit 0, 39 of 39 LINT OK |
| `make check` | exit 0: 41 mermaid and 18 wavedrom blocks, links 835, matrix 115 REQ, modmatrix 90 rows / 0 untested |
| `python3 scripts/gen_matrix.py --check` | exit 0, 90 rows, 0 untested |
| `check-links` | exit 0, 835 checked |
| `./syn/yosys/run.sh` | exit 0 |
| `make -C tb/nvm_port figures` | exit 0, "all measured figures agree with the tree" |
| `git diff --check 09f9bf38..HEAD` | exit 0, empty |

### Parent, scratch clone at 615b5a5d (`logs/parent-base-424c688/`, `logs/parent-after-f8d30ec/`)

`tools/parent_gates.sh` ran every gate at the parent's own gitlink (424c688), then again after
local commit `44220afc7` moved the gitlink to f8d30ec.

| Gate | gitlink 424c688 | gitlink f8d30ec |
|---|---|---|
| `check_cpp_idiom.py` | exit 0, every ratchet 0 <= 0 | **exit 0**, every ratchet 0 <= 0 (147 units) |
| `check_cpp_idiom.py --list` | no processor file | **no processor file** |
| `check_py_idiom.py` | exit 0: long function 9 <= 9, long module 10 <= 10, too many parameters 7 <= 7, os.path 1 <= 1 | **exit 0**, the same four figures (229 modules) |
| `check_py_idiom.py --list` | `hdl/aecp/ucode/gen_ucode.py` (pre-existing, inside the ratchet) | the same one file only |
| `--selftest`, both gates | exit 0 | exit 0 |
| `check_hygiene --check`, `check_sh_idiom`, `check_sv_idiom`, `check_todo_ownership`, `measure_naming --check`, `measure_fail_fast --check`, `measure_test_evidence --check` | exit 0 | exit 0 |
| `check_submodule_docs.py` | exit 0 | exit 1: "protocol-processor: documented pin differs from Git" and the stale submodule-boundary diagram |

`check_submodule_docs` fails because of the scratch gitlink move itself, as it did in the
earlier idiom round. The parent's pin-bump change updates those documents, so this is not a
processor finding. `scripts/cpp_idiom.budget` and `scripts/py_idiom.budget` are the files as
they are at 615b5a5d, untouched.

## Limits

- No hardware. No hosted CI at the fixed head, because it is not pushed.
- The manager's donor and parent banks were not run here. Only the parent gates above were
  run: the idiom gates plus the other source-reading gates.
- P2 ran as a re-anchored copy of the reviewer's script, for the reason in §1.
- `logs/dev-*` are the session's development iterations. The receipts for the fixed head are
  in `logs/gates`, `logs/arms`, `logs/probes` and `logs/repro`.
- The R279 S1/S2/S3/S6 suggestions are open (see §4).

## Posted

- #92: `[A235] REVIEW READY`,
  https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92#issuecomment-5808626794
  (text in `NOTE-92.md`). Nothing else was posted. The PR, its body and its head were not
  touched.

## Next (manager)

1. Push f8d30ec to PR #109 and replace the body with `PR-BODY.md`.
2. R278 and R279 re-review at that head.
3. The parent gitlink bump re-runs the consumer bank, including `pp_shadow` with a mid-walk
   refusal after a stored record.
