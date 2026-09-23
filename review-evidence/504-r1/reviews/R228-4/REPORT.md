[R228] POSITIVE - exact head 4876423d4cf8e89b820c56f8339f230abefb4827

External independent review, round R228-4, issue #504 / PR #521 (Tests-only follow-up).
Head `4876423d4cf8e89b820c56f8339f230abefb4827`, tree `b2fb9e0516aa4ed9a17cdedfb1ae25460270d408`, parent `97aa1ec943ac740a27b942210a248f6512ae3ff6` (the head of my round R228-3).
Source base `574c29fa111c74e5e5ed63e4670aff1f492e28e2`. Live `dev` at review time: `ede8d48ecd7c7f589a14b957951f040d92c99c70`, read-only.
I reviewed from public state and a detached clone. The clone was never written: 860 tracked blobs are byte- and mode-exact before and after, and the required gitlinks are intact.

## Verdict summary

- **No open BLOCKER, MAJOR or MINOR finding at this head.** All five lenses are CLEAN.
- **R228-F6 (MINOR, Tests) is RESOLVED.** Its required outcome and verification are both met.
  - The complete gate 1b KILLS the `>=` to `>` revert of `key[-1] + 3 >= start` (`sw/builder/test_builder.py:1508`), with the SDK mapped and with the compiler absent.
  - The literal controls kill it too.
  - The two byte-3 compiled plants are REFUSED at this head.
- **The boundary is now pinned from both sides, per caller.**
  - Narrowing: the new stale probes (`test_builder.py:5281-5282` for the frame, `:5297-5298` for the static) kill 5 of 5 narrowing mutants.
  - Widening: the new kept probes (`:5328-5331`) kill 5 of 5 widening mutants.
  - Each new probe alone kills the mutant confined to its own caller. The frame and static branches share `_rv32_forget_overlap`, and I measured each branch separately.
  - At `97aa1ec9` the same narrowing mutants SURVIVE, as does the statics-only widening. The new kills come from this commit.
- **The new probes guard a real compiled consequence.** Take the F6 revert and delete only the new stale probes: both byte-3 plants then write `ADP_CTRL` and pass the whole boot contract. Delete only one branch's probe and narrow only that branch: that branch's plant is ACCEPTED and the other's is still REFUSED.
- **The delta touches only the Tests scope.**
  - It is one file, `sw/builder/test_builder.py`, +20/-7.
  - An AST comparison shows that only three statements changed, all inside `test_baremetal_profile_contract`: `stale_probes`, `kept_probes` and the printed note. No resolver, gate, installer, workflow, doc or RTL byte changed.
- **Optional suggestions are retained** (they do not affect coverage): R228-S2, S3, S5, S6, S7 and S8, and R227-3-S1 and S2. S8 is the companion high boundary. Both of its directions still survive at this head; the author declined it as optional.

## Reconstruction

- **Authority.** AGENTS.md sections 2-8, CONTRIBUTING.md sections 2-3, docs/README.md, and REQUIREMENTS.md REQ-VER-03/04.
- **Issue #504.** The body (acceptance 1-5, scope, "No text refusal is retired in this task") and the manager decisions 5771447690, 5771915061 and 5778746031. Also the assignments 5789172582, 5790944031 and 5793839488. The last assigns the Tests-only follow-up for the single MINOR that R227-3 and R228-3 raised at `97aa1ec9`.
- **Author statements.** The public A194 statement is REVIEW READY 5794053679. The review start is 5795035906.
- **Diff and history.**
  - `git diff 574c29fa..4876423d` covers 10 files, +1673/-67.
  - `git diff 97aa1ec9..4876423d` is one file (`receipts/scope.txt`).
  - The commit subject is one line with no trailers.
- **Evidence read.**
  - The author packet `review-evidence/504-r1/correction-a194/` at `ecf88577`.
  - The exact-head check runs and two job logs, read-only (`receipts/hosted/`).

## Findings

None open at this head.

### R228-F6 MINOR - Tests - RESOLVED at 4876423d

**Required outcome at R228-3.** A control fails under the `>=` to `>` revert. My verification runs `overlap-last-byte` and `overlap-last-byte-gate1b` and needs both KILLED, and needs the two byte-3 plants to stay REFUSED.

**Evidence at this head.** All runs were in disposable copies. Each mutated file was restored and its SHA-256 re-verified.

| Check | Result | Receipt |
|---|---|---|
| R228-3's `overlap-last-byte` (literal controls) | KILLED: "after a byte store at a frame slot's last byte the RV32 resolver still placed the next store ([2147487744])", which is 0x80001000 | `receipts/prior-mutants-head/overlap-last-byte.*` |
| `lb-gt-gate1b`: the same revert through the complete gate 1b, SDK mapped | KILLED, rc 1, on the same sentence | `receipts/gate1b/lb-gt-gate1b.*` |
| `lb-gt-gate1b-absent`: the same revert through the complete gate 1b, compiler absent | KILLED, rc 1, on the same sentence | `receipts/gate1b/lb-gt-gate1b-absent.*` |
| Compiled byte-3 plants at the head, judged by the gate's own `assert_boot_contract()` | frame union REFUSED, static union REFUSED ("a STORE this gate cannot PLACE"); byte-0 reference REFUSED | `receipts/gate-plants/head.*` |
| Pristine head, complete gate 1b, SDK mapped (scoped Verilator 5.050) | PASS, rc 0: 217/217, 17/17 and 4/4, 46/46 elaborated; 0 NOT RUN; 235 compiles; 242 audited invocations with 0 argv tails changed; prints "15 rewrites ... while 5 stores ... left exactly theirs" | `receipts/gate1b/null-gate1b.*` |
| Pristine head, complete gate 1b, compiler absent | PASS, rc 0: 182/182, 17/17 and 4/4, 46/46; 1 NOT RUN (the compiled census); 0 compiles | `receipts/gate1b/null-gate1b-absent.*` |

**Both directions, per caller, and which arm kills.** Script `scripts/r228_4_mutate.py`. A verdict is KILLED only on a failing assertion. The probe named by that assertion is recorded.

| Mutant (edit to `:1508` unless stated) | 97aa1ec9 | 4876423d | Killing arm at the head |
|---|---|---|---|
| `lb-gt`: `+ 3 > start` (the F6 revert) | SURVIVED | KILLED | new frame stale probe |
| `lb-plus2`: `+ 2 >= start` | SURVIVED | KILLED | new frame stale probe |
| `lb-plus0`: `>= start` | KILLED | KILLED | new frame stale probe (an older static byte-1 probe at the previous head) |
| `lb-gt-sym-only`: narrowed for statics only | SURVIVED | KILLED | new static stale probe |
| `lb-gt-frame-only`: narrowed for frame slots only | SURVIVED | KILLED | new frame stale probe |
| `lb-plus4`: `+ 4 >= start` (over-forget) | KILLED | KILLED | new frame kept probe (a range-class control at the previous head) |
| `lb-ge-start-minus1`: `>= start - 1` | KILLED | KILLED | new frame kept probe |
| `lb-drop`: the low term removed | KILLED | KILLED | new frame kept probe |
| `lb-plus4-sym-only`: widened for statics only | SURVIVED | KILLED | new static kept probe |
| `lb-plus4-frame-only`: widened for frame slots only | KILLED | KILLED | new frame kept probe |

Controls at the head that tie each kill to its probe:

- **The narrowing kills belong to the new stale probes.**
  - `lb-gt-without-new-stale` (the revert, with both new stale probes deleted) SURVIVES. This reproduces the R228-3 gap.
  - `lb-gt-static-stale-alone` and `lb-gt-frame-stale-alone` are each KILLED, by the remaining probe.
  - `lb-gt-sym-only-without-static-stale` and `lb-gt-frame-only-without-frame-stale` both SURVIVE. So each branch's narrowing is caught only by that branch's new probe.
- **The widening kills.**
  - `lb-plus4-static-kept-alone` and `lb-plus4-frame-kept-alone` are each KILLED by the remaining kept probe.
  - `lb-plus4-without-new-kept` is still KILLED, later, by the pre-existing range-class control (`:5383`). My recorded prediction was SURVIVED; the control set is stronger than I predicted. That control reaches frame slots only: `lb-plus4-sym-only` SURVIVED at `97aa1ec9`.
- **Null controls.** `null` and `null-drop-new-probes` both reach the stop hook. Deleting the four probes breaks nothing else.
- **The mutations-prev receipts.** Their `expected` field carries the head prediction, so `as_expected: false` there marks the differential, not an error.

**The compiled consequence each new probe guards.** Script `scripts/r228_4_gate_run.py` with `r228_4_gate_probes.py`. It is exec'd before gate 1b's mutation loop, with the SDK mapped.

| Tree | frame byte-3 plant | static byte-3 plant |
|---|---|---|
| head | REFUSED | REFUSED |
| head + `lb-gt`, both new stale probes deleted | ACCEPTED | ACCEPTED |
| head + statics-only narrowing, new static stale probe deleted | REFUSED | ACCEPTED |
| head + frame-only narrowing, new frame stale probe deleted | ACCEPTED | REFUSED |

"ACCEPTED" means that the whole boot contract passed a firmware that writes `ADP_CTRL` before the AEM verdict. Without the stop hook, the literal controls end every one of those mutated runs before the compiled census is reached.

**Earlier kills still hold.** I re-ran R228-3's 22 literal mutants plus its null control at this head (`receipts/prior-mutants-head/`). The results are 21 KILLED and 2 SURVIVED:

- `null-literal` SURVIVES, as a control should.
- `overlap-first-byte` (R228-S8) SURVIVES, as it is optional.
- `overlap-last-byte` has moved from SURVIVED to KILLED.

## Suggestions (optional; they do not affect coverage)

- **R228-S8 (Tests), retained: the companion high boundary.** `key[-1] <= start + width - 1` still has no failing control in either direction:
  - `hb-lt` (fail-open) SURVIVES. Only a misaligned `sh`, `sw` or `fsd` reaches it, and R228-3 found GCC 14.3.0 emitting packed members byte-wise.
  - `hb-plus1` (fail-closed: it over-forgets the next word) SURVIVES. It could only cause a loud false refusal.

  The author publicly declined this as optional (5794053679).
- **R227-3-S1 M17 (Tests), retained, measured at this head.** Computing a store's last written word one byte short (`footprint-last-word-short`) SURVIVES. Only a misaligned `sw` at an odd offset below the window reaches it, and the straddle probe uses offset -2. It is optional, like S8.
- **R228-S5 (Tests), retained: the census-ISA filter.** The census-ISA parse is byte-identical at this head (AST scope). I did not re-run its gate-1b mutant.
- **R228-S6 and R228-S7 (Docs), retained.** `BAREMETAL_FIRMWARE.md` is unchanged since `97aa1ec9`.
- **R228-S2 and R228-S3 (Robustness), retained.** `scripts/ci_rv32_sdk.py` is unchanged.

## Per-lens results at this head

```text
[R228] PASS Conformance - issue #504 acceptance 1-5; receipts/gate1b/null-gate1b.log, null-gate1b-absent.log; receipts/hosted/hosted-exact-head-extract.txt; receipts/scope.txt - the delta adds literal controls only and changes no acceptance-bearing behaviour; at this head the pinned SDK (fresh install via the head's installer, GCC 14.3.0, riscv32-buildroot-linux-gnu) drives gate 1b to 217/217, 17/17+4/4, 46/46, 0 NOT RUN, 235 compiles, and the absent run is 182/182 with 1 explicit NOT RUN and 0 compiles, the same counts as 97aa1ec9; exact-head hosted builder jobs 107161979789 and 107161980377 succeeded on "SDK cache hit: verified" and printed the 15/5 note; no text refusal, residual, firmware, RTL or pin changed; unchanged conformance artifacts (installer, workflows, fresh hosted acquisition at 3d90958f) carried from R228-3.
[R228] PASS RTL - receipts/scope.txt (git diff 574c29fa..4876423d -- hdl tb syn sw/firmware sw/litex configs and gitlinks: 0 paths; the four gitlinks identical at base and head); receipts/gate1b/null-gate1b.log and null-gate1b-absent.log - 46/46 RTL mutation variants elaborated as the real option-on top with scoped Verilator 5.050 (wrapper sha256 905795b9...e92f) in both modes at this head; receipts/final-integrity-clone.txt.
[R228] PASS Robustness - test_builder.py:1501-1509 (byte-identical to 97aa1ec9, receipts/ast-scope.txt); receipts/resolver-probes-head.json; receipts/gate-plants/head.json; receipts/sdk-*.log - 50/50 literal resolver soundness probes sound at this head, identical to R228-3 (5 documented limits unsound as the page states); both byte-3 boundary plants and the byte-0 plant refused by the whole boot contract; the head's installer fresh install from the pinned archive (digest verified), cache hit and verify-only all exit 0.
[R228] PASS Tests - test_builder.py:5274-5338 (stale 5281-5282, 5297-5298; kept 5328-5331) against :1508; receipts/mutation-summary.json - the F6 revert and 9 further boundary mutants, both directions and per caller, are KILLED at this head by the new arms, with 8 deletion/attribution variants and 2 null controls proving which arm kills; the revert is KILLED through the complete gate 1b in both modes; R228-3's 20 earlier literal kills all hold and overlap-last-byte is now KILLED (21/22); static and audit self-tests pass (receipts/static/); the only survivors are the controls and the optional boundaries (R228-S8 / R227-3-S1 M16, and M17).
[R228] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:452-541 and docs/testing/CI_WORKFLOWS.md (unchanged since 97aa1ec9, receipts/scope.txt); receipts/static/ - :494-496 "the rewrites above, each against a whole-word positive arm" stays true: every stale probe keeps its whole-word arm and the one-past arms are additional boundary pins the page does not deny; docs_check, check_em_dash --base 574c29fa (188 added lines, 0 findings), doc_style, doc_paths, gen_toc --check/--verify-anchors and feature_status all exit 0 at this head.
```

## Reviewer-owned lens ledger

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Acceptance 1-5 against my exact-head gate 1b runs in both modes (`receipts/gate1b/`) and the exact-head hosted builder logs (`receipts/hosted/`). Delta scope (`receipts/scope.txt`, `receipts/ast-scope.txt`). Unchanged installer, workflows and fresh-acquisition evidence carried from R228-3 | R228-4, with R228-3 for the unchanged scope | `4876423d4cf8e89b820c56f8339f230abefb4827`; R228-3 at `97aa1ec943ac740a27b942210a248f6512ae3ff6`, an ancestor, with nothing in the installer, workflows or docs changed since |
| RTL | CLEAN | Empty RTL-scope diff and identical gitlinks base..head. 46/46 variants elaborated with scoped 5.050 in both modes at this head. Clone integrity | R228-4; R228-3 carries the same scope | `4876423d4cf8e89b820c56f8339f230abefb4827` (R228-3: `97aa1ec943ac740a27b942210a248f6512ae3ff6`, RTL scope untouched since) |
| Robustness | CLEAN | Resolver code byte-identical (AST). 50/50 literal probes at the head. Compiled boundary plants at the head. Installer fresh install, cache hit and verify-only at the head. R228-3's tamper and relocation controls on the unchanged installer | R228-4; R228-3 for the tamper and relocation controls | `4876423d4cf8e89b820c56f8339f230abefb4827` (R228-3: `97aa1ec943ac740a27b942210a248f6512ae3ff6`, installer untouched since) |
| Tests | CLEAN | New stale and kept arms against 23 literal runs at the head (10 boundary mutants, 8 attribution variants, 3 optional-boundary mutants, 2 null controls) and 13 at `97aa1ec9`. 5 complete gate-1b runs. 4 compiled plant runs. R228-3's 23 literal runs re-run. Static and audit self-tests (`receipts/static/`) | R228-4 | `4876423d4cf8e89b820c56f8339f230abefb4827` |
| Docs | CLEAN | `BAREMETAL_FIRMWARE.md` and `CI_WORKFLOWS.md` unchanged since R228-3. The claim at `:494-496` re-read against the new arms. Docs gates at this head (`receipts/static/`) | R228-4; R228-3 for the page review | `4876423d4cf8e89b820c56f8339f230abefb4827` (R228-3: `97aa1ec943ac740a27b942210a248f6512ae3ff6`, docs untouched since) |

## Prior public review findings on this PR, at this head

I read these only after the verdict, the findings and the ledger above were written. I did not read the concurrent internal round R227-4.

| Finding | Status at `4876423d` | Evidence |
|---|---|---|
| R228-F6 MINOR (R228-3): overlap low boundary has no failing control | RESOLVED | See the F6 section: literal, complete gate 1b in both modes, and compiled plants |
| R227-3 MINOR Tests (5793809309): the same boundary, its mutant M15 | RESOLVED | M15 is the same edit as my `lb-gt`, which is KILLED in the literal controls and through the complete gate 1b in both modes. With the new probes present, the gate never reaches a census that would ACCEPT the plants |
| R227-3-S1 (Tests): M16 and M17 boundaries, redundant mirror term M4 | RETAINED, optional | M16 is my `hb-lt`, which SURVIVES. M17 is `footprint-last-word-short`, which SURVIVES. M4 is untouched by the delta. The author declined these as optional |
| R227-3-S2 (Docs): consequence of the sub-word-load bullet, memset-as-call example | RETAINED, optional | The same points as R228-S7. The page is unchanged |
| R227-3 O1 / R227-2 OBS-1: sub-word frame-slot load (pre-existing, not attributed to this PR) | RETAINED as out-of-scope, documented | `_rv32_step_load` is byte-identical (AST scope). The page names it at `BAREMETAL_FIRMWARE.md:538-539`. I found no dedicated public Issue; see the pending duties |
| R228-1 F1 MAJOR (FP stores), F2 MAJOR (download digest), F3 MINOR (receipt bindings), S1 | RESOLVED at `97aa1ec9`, still resolved | Resolver code is byte-identical, and `fp-classes`, `atomic-classes`, `footprint-first-byte`, `stores-first-word` and `unclassified-default` are KILLED at this head. The installer is unchanged and its self-test passes at this head (`receipts/static/sdk_installer_selftest.*`). The F2/F3 fix-removal mutants ran at `97aa1ec9` (R228-3) |
| R227-2-F1, R227-2-F2, R228-2-F4, R228-2-F5 (MINOR), R228-2-S4, R227-2-S1 | RESOLVED or TAKEN at `97aa1ec9`, still so | `value-subword`, `value-all-classes`, `value-amo-sc`, `stack-forget-frame`, `frame-overlap`, `sym-overlap`, `range-footprint`, both `*-overlap-width-4` mutants, `mirror-integer-only`, `mirror-no-memop`, `memop-displacement`, `atomic-rd` and `atomic-operand` are KILLED at this head. The page is unchanged |
| R228-S2, R228-S3 (Robustness), R228-S5 (Tests), R228-S6, R228-S7 (Docs) | RETAINED, optional | Their artifacts are unchanged since `97aa1ec9` |

## Executions at this head

All of these ran in disposable copies under `scratch/`. The review clone was only read.

**Toolchain** (`receipts/tool-identity.txt`)

- Pinned archive: 102,597,892 bytes, SHA256 `d42680e9…b78f`, equal to `scripts/ci_rv32_sdk.py:25`.
- The head's installer did a fresh install in 13.2 s, a cache hit in 0.8 s, and verify-only exits 0 (`receipts/sdk-*.log`).
- GCC 14.3.0, `riscv32-buildroot-linux-gnu`. The census arch is `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0` (`receipts/gate-plants/head.json`).
- Scoped Verilator 5.050 (wrapper SHA256 `905795b9…e92f`) was first on PATH for every gate 1b run. The host 5.052 was not used.

**Gate 1b** (`receipts/gate1b/`)

- Pristine, SDK mapped: exit 0 in 339 s.
- Pristine, compiler absent: exit 0 in 272 s.
- `lb-gt` (SDK and absent) and `lb-plus4` (SDK): KILLED.

**Literal mutants** (`receipts/mutations-head/`, `receipts/mutations-prev/`, `receipts/prior-mutants-head/`, summary `receipts/mutation-summary.json`)

- 23 at the head, 13 at `97aa1ec9`, and R228-3's 23 re-run at the head.
- Every mutated file was restored and its SHA-256 re-verified.

**Compiled plants** (`receipts/gate-plants/`)

- 4 whole-gate runs: the head and three attribution variants.

**Other checks**

- Resolver soundness probes: 50/50 at the head, identical to R228-3 (`receipts/resolver-probes-head.json`).
- Static and docs gates: 20/20 exit 0, and the copy is clean afterwards (`receipts/static/`).
- Scope: `receipts/scope.txt`. AST scope: `receipts/ast-scope.txt`.

**Exact-head hosted** (read-only; `receipts/hosted/`)

- Every check run on `4876423d` is `success` except "Physical gPTP (nightly and manual)", which is `skipped` and did not execute.
- Both builder jobs, docs-check `107161979789` and elaborate `107161980377`, restored the SDK on "SDK cache hit: verified" and printed the 15/5 control note.

**Clone integrity** (`receipts/initial-integrity-clone.txt`, `receipts/final-integrity-clone.txt`)

- HEAD and tree are exact. The index equals the HEAD tree, 860 blobs are byte- and mode-exact, and no index flags are set.
- Status is clean including ignored files.
- `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are at their gitlinks.

## Real limits

- I did not run the full parent, PP, gPTP, Yosys or builder banks, the local CI replica, or any hosted job.
- **The manager's source banks at this head.** The review assignment says they passed. I found no public receipt for `4876423d`: the `504-review-evidence` branch tip `ecf88577` carries only the A194 author packet, and no manager evidence comment for this head exists on #504 or #521. I claim nothing about those banks.
- **Hosted evidence** was read, not produced. At this head both hosted builder jobs used the verified-cache path. The fresh hosted acquisition evidence is from `3d90958f`, and the installer and workflows are byte-identical since then.
- The mapped-prefix gate runs are local compatibility evidence, not hosted selector adoption.
- **Compiled plants.** They are judged through an exec hook in disposable copies. "ACCEPTED" means the boot contract passed the firmware; it does not mean the product links.
- **My mutation set.** It is reviewer-chosen and not exhaustive. Branch-confined mutants use a `key[0] == "sym"` switch, which is a model of a per-caller regression and not a natural edit.
- Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Publish this report and its manifest-listed receipts.
- Publish the exact-head source static/builder and native bank receipts for `4876423d`.
- Trusted local replica and exact-head hosted acceptance.
- Obtain the internal R227-4 verdict. I have not read it.
- **At the merge turn**, with maintainer authorization:
  - build and validate the final current-dev candidate (source base `574c29fa`, live `dev` `ede8d48e` at review time);
  - then post-merge containment, the Issue close, and the Done readback.
- **A public Issue** is needed before #408/#409 retire any text rule onto the census, for the shapes the page lists as not observed:
  - a callee's store through a handed pointer (memset, memcpy, libatomic);
  - a callee's write into its caller's frame;
  - a numeric store that reaches the stack;
  - a sub-word frame-slot load (R227-2 OBS-1 / R227-3 O1).

  I found no dedicated Issue. #495 is the open review-leftover checklist.

## Reproduction

The paths are placeholders: `$PACKET` is this packet, `$CLONE` an exact-head clone, and `$PINNED_TOOLS` the directory holding the scoped Verilator 5.050 wrapper.

```sh
cp -a "$CLONE" "$PACKET/scratch/t0"          # one disposable copy per parallel job
python3 -B "$CLONE/scripts/ci_rv32_sdk.py" --destination "$PACKET/scratch/sdk/host" --archive <pinned archive>
python3 -B scripts/r228_4_mutate.py scratch/t0 lb-gt receipts/mutations-head        # any MUTANTS id
PATH="$PINNED_TOOLS:$PATH" python3 -B scripts/r228_4_mutate.py scratch/t1 null-gate1b receipts/gate1b --sdk "$PACKET/scratch/sdk/host"
PATH="$PINNED_TOOLS:$PATH" python3 -B scripts/r228_4_gate_run.py scratch/t6 "$PACKET/scratch/sdk/host" receipts/gate-plants/head.json [<mutant-id>]
python3 -B scripts/r228_mutate.py "$PACKET/scratch/t0" overlap-last-byte "$PACKET/receipts/prior-mutants-head"
python3 -B scripts/r228_resolver_probes.py scratch/t4 receipts/resolver-probes-head.json
bash scripts/r228_4_static_gates.sh "$PACKET/scratch/t3" "$PACKET/receipts/static"
python3 scripts/r228_4_ast_scope.py "$CLONE" 97aa1ec943ac740a27b942210a248f6512ae3ff6 4876423d4cf8e89b820c56f8339f230abefb4827
python3 scripts/r228_4_integrity.py "$CLONE" 4876423d4cf8e89b820c56f8339f230abefb4827
python3 scripts/r228_4_summary.py "$PACKET"
```

R228-4 FINISHED
