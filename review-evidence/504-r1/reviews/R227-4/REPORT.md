[R227] POSITIVE - exact head 4876423d4cf8e89b820c56f8339f230abefb4827

Round R227-4: cleared-context internal review of issue #504 / PR #521.
Tree `b2fb9e0516aa4ed9a17cdedfb1ae25460270d408`, parent `97aa1ec9`.
Source base and the base of every local run: `574c29fa111c74e5e5ed63e4670aff1f492e28e2`.

## Verdict in one paragraph

The one open finding from the previous round is resolved at this head. That
finding is R227-3 MINOR Tests, which R228-3 raised as R228-F6: the overlap
low boundary `key[-1] + 3 >= start` in `_rv32_forget_overlap` had no failing
control. The delta adds a stale-probe arm and a kept-probe arm. Together they
kill every low-boundary mutation I tried, in both directions:

- the under-forget mutants `>`, `+ 2` and `+ 1`;
- the over-forget mutants `+ 4`, `start - 1`, `+ 7`, and the low term dropped.

Each new probe kills the mutant on its own, and removing it brings the gap
back. The `>` and `+ 4` reverts are also KILLED through the complete gate 1b,
both with the SDK mapped and with the cross tools absent. The head passes both
modes with the same counts as the previous head.

The delta touches nothing outside the literal resolver control block of
`sw/builder/test_builder.py`. No finding of MINOR or higher is open, so the
verdict is POSITIVE. There are two optional suggestions: the untouched
companion high boundary, and a pre-existing symbol-addend aliasing gap for the
follow-up Issue. All five lenses are clean. Tests and Docs are covered at this
head. Conformance, RTL and Robustness are covered by R227-3 at `97aa1ec9`:
nothing in their scope has changed since, and this round re-checked each of
them at this head.

## Reconstruction

I read these in the contract's order:

1. `AGENTS.md` and `CONTRIBUTING.md`.
2. `docs/README.md`.
3. The #504 body and frozen acceptance items 1-5.
4. The #504 thread: decisions 5771447690, 5771915061 and 5778746031, the
   correction assignments 5789172582, 5790944031 and 5793839488, and the
   A194 REVIEW READY 5794053679.
5. `docs/integration/BAREMETAL_FIRMWARE.md:452-563`, the resolver code
   (`test_builder.py:1489-1649`) and the gate harness
   (`sw/builder/test_firmware_compiler.py`).
6. The diff `97aa1ec9..4876423d` and its commit, then the scope of
   `574c29fa..4876423d` (`receipts/scope.txt`, `receipts/delta_97aa1ec9_4876423d.diff`).
7. Exact-head hosted check runs and two job logs, read-only.

I read no private author material, lane scratchpad or management workspace.

**Independence.** I measured every probe, gate run and static gate below
before I read any review report on the PR (`receipts/independence_timeline.txt`).
My draft conclusions are in `receipts/independent-draft-findings.txt`. I wrote
that file after my measurements. I wrote it after reading R227-3 and before
reading R228-3. It states that the #504 thread I read during reconstruction
already names the finding and the optional boundary suggestions. The draft and
this report agree.

## The delta

- **One commit.** `4876423d`, one line, no trailers, parent `97aa1ec9`.
- **One file.** `sw/builder/test_builder.py`, +20/-7, in six hunks. All six are
  inside `test_baremetal_profile_contract()`, at lines 5263-5355. No resolver
  function changes, so `_rv32_forget_overlap` at `:1501-1509` is byte-identical.
  Nor do the installer, the workflows, the pages, RTL or the gitlinks
  (`receipts/scope.txt`).
- **The new stale probes.** Each parks 0x80001000, then writes a byte store at
  the word's LAST byte, reloads the word and stores through it. The store
  must be unplaced.
  - Frame slot: `sw a5,-20(s0)`, `sb zero,-17(s0)`, `lw a4,-20(s0)`
    (`:5281-5282`).
  - Static: `sw a5,0(a3)`, `sb zero,3(a3)`, `lw a4,0(a3)` (`:5297-5298`).

  For `start = K+3` and `width = 1`, the high term has 3 bytes of slack. Only
  the low term is tight, so these probes reach exactly the reported boundary.
- **The new kept probes.** The same shapes with the byte store one past the
  word: `sb zero,-16(s0)` and `sb zero,4(a3)` (`:5328-5331`). The word must be
  kept and the next store placed at 0x80001000. These pin the same boundary
  from the other side.
- **Comments and the printed note.** They are updated. The counts are computed
  with `len(...)`, and at this head they are 15 stale probes and 5 kept probes.

## Mutation evidence

### Literal controls, in isolation

Script: `scripts/overlap_probe.py`. Results: `receipts/overlap_probe_results.jsonl`.

The script copies the head's `sw/builder`. It applies exact-string edits, each
asserted to occur exactly once. It then executes the literal control segment
verbatim from the mutated file: the `rv32_probe` helper, then the source from
`outside = 0x8000_1000` up to `store_classes_note = (`. A deleted probe is
therefore deleted from what runs. The verdict is the gate's own first
assertion sentence, or SURVIVED.

| Probe | Edit | Result |
|---|---|---|
| P0 | none | passes: 15 stale, 5 kept |
| M1 | `+ 3 >= start` to `+ 3 > start` | **KILLED**: "after a byte store at a frame slot's last byte the RV32 resolver still placed the next store ([2147487744])" |
| M1, frame stale probe deleted | same | **KILLED** on "after a byte store at a static word's last byte ..." |
| M1, both new stale probes deleted | same | SURVIVED: the pre-delta gap, reproduced |
| M1b / M1c | `+ 2 >= start` / `+ 1 >= start` | **KILLED** on the frame last-byte sentence |
| M1b, both new stale probes deleted | same | SURVIVED |
| M2 | `+ 4 >= start` (over-forget) | **KILLED**: "after a byte store one past a frame slot's last byte ... [unplaced(None)], not at the 0x80001000 it wrote" |
| M2, frame kept probe deleted | same | **KILLED** on the static one-past sentence |
| M2, both new kept probes deleted | same | SURVIVED |
| M2b / M2c | `+ 3 >= start - 1` / `+ 7 >= start` | **KILLED** on the frame one-past sentence |
| M3 | low term dropped | **KILLED** on the frame one-past sentence. It SURVIVES with both new kept probes deleted |
| U1 | high term `<=` to `<` | SURVIVED (S1 below; not in this delta) |
| U2 | high term `<= start + width` | SURVIVED (S1) |
| U3 | high term dropped | SURVIVED in the literal controls (S1) |

### The complete gate 1b

Scripts: `scripts/gate_trees.sh` and `scripts/run_gate.sh`. Logs: `receipts/gate/`.

The runs use disposable full-tree copies of the exact head, with the three
required submodules copied in. The head's own harness,
`sw/builder/test_firmware_compiler.py`, runs each one with scoped Verilator
5.050 first on `PATH`.

The SDK is a fresh install of the pinned archive into scratch, using the
head's installer: 102,597,892 bytes with the pinned SHA256, and
`--verify-only` exit 0. It reports GCC 14.3.0 and target
`riscv32-buildroot-linux-gnu` (`receipts/sdk_*`).

| Tree | Mode | Exit | Result |
|---|---|---|---|
| head | SDK mapped | 0 (336 s) | GATE 1b PASS: 217/217 mutations, 17/17 firmware and 4/4 Makefile positives, 46/46 RTL variants, 0 NOT RUN, 235 compiles, 120 census assemblies all `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`, 0 argv tails changed (`receipts/compiler-audit-summary.txt`). The store-class mutants reached the resolver as `fsw`, `fsd`, `amoswap.w`, `amoor.w` and `sc.w`, and each was refused on its resolved address. It prints "15 rewrites of a parked word ... while 5 stores that write the word whole or miss it by one byte left exactly theirs" |
| head | absent | 0 (272 s) | GATE 1b PASS: 182/182, 17/17, 4/4, 46/46, exactly 1 NOT RUN (the compiled census), 0 compiles, 3 deliberately absent cross candidates |
| M1 (`>`) | SDK mapped / absent | 1 / 1 | **KILLED** in both modes, on the frame last-byte sentence |
| M2 (`+ 4`) | SDK mapped / absent | 1 / 1 | **KILLED** in both modes, on the frame one-past sentence |
| U1 (high `<`) | SDK mapped | 0 (339 s) | SURVIVES the complete gate: 217/217 (S1) |
| U3 (high term dropped) | SDK mapped | 1 | KILLED only by the pristine census: several stores in the pristine firmware become unplaced |

### The compiled shape, asked of the resolver alone

Source: `scripts/top_byte_compiled.c`. Assembly: `receipts/top_byte_compiled.s.txt`.
Results: `receipts/top_byte_resolve.{head,M1-gt,M2-plus4}.jsonl`.

A union byte store into byte 3 of a parked `0x12000600` is compiled with the
census flags (`-std=gnu99 -O0 -fno-inline`, SDK default ISA). In the frame it
compiles to `sw a5,-28(s0)`, `sb a5,-25(s0)`, `lw a5,-28(s0)`. In a static it
compiles to `lla a5,g`, `sb a4,3(a5)`, `lw a5,0(a5)`. Those are the exact
shapes of the new literal probes.

| Function | head | M1 | M2 |
|---|---|---|---|
| frame, top byte rewritten | unplaced (refused) | placed at 0x12000600, which is the bypass | unplaced |
| static, top byte rewritten | unplaced (refused) | placed at 0x12000600 | unplaced |
| frame, next word's byte 0 | placed at 0x12000600 (kept) | placed | unplaced (over-forget) |
| static, next word's byte 0 | placed at 0x12000600 (kept) | placed | unplaced |

This is the resolver alone. The R227-3 and R228-3 firmware plants are their
own tooling, and I did not re-run them. The resolver code they exercised is
byte-identical at this head.

## Findings

No BLOCKER, MAJOR or MINOR finding is open at this head.

### Suggestions (optional; no effect on coverage)

**R227-4-S1 (Tests): the companion high boundary.** This retains R227-3-S1 and
matches R228-S8.

- The high term `key[-1] <= start + width - 1` at `test_builder.py:1508`
  still has no failing control.
- U1 (`<`) survives the literal controls and the complete SDK-mapped gate
  (217/217).
- U2 survives the literal controls. U3 is killed only by the pristine census.
- A literal control that kills U1 exists:
  - `sh zero,-21(s0)` over a slot parked at -20;
  - `addi a2,a3,1` then `sw zero,0(a2)` over a static word parked at +4.

  The head leaves both unplaced, and U1 places them at 0x80001000. A
  `sh zero,-22(s0)`, one byte short, is kept (`receipts/extra_probes.*.jsonl`).
- **Why this is not load-bearing today.** Only a misaligned multi-byte store
  reaches that boundary. The census compile stores packed members byte by byte
  (`receipts/align_probe_stores.txt`). A misaligned cast store through a static
  is spelled `lla a5,g+1` (`receipts/align_static_probe.s.txt`), which S2
  covers.
- **R227-3-S1 M17 is retained and re-measured.** It computes the footprint's
  last word one byte short. The shipped `sw` probe at X-2 cannot tell the
  difference, and a probe at X-3 would (`receipts/footprint_m17.jsonl`).

**R227-4-S2 (Robustness, Docs): symbol-addend spelling.** This is pre-existing
and is not attributed to this PR. It is information for the follow-up Issue.

- **The mechanism.** `lla`/`la` models its whole operand as the symbol name
  (`test_builder.py:1382-1384`), and dev `574c29fa` does the same at `:1336-1337`.
  So `lla a5,g+4` is the object `g+4` at displacement 0, not `g` at
  displacement 4.
- **At this head.** A whole-word store through `lla a2,probe_static+4` neither
  sets nor forgets the word keyed `probe_static`/4. After it, `lla` of
  `probe_static` and `lw 4(...)` read the stale parked 0x80001000, and the next
  store is PLACED there. The misaligned `+1` spelling behaves the same way
  (`receipts/extra_probes.head.jsonl`).
- **Where GCC emits the spelling.** The census compile folds only
  address-taken expressions into it, such as `&nested.in.parked` becoming
  `lla a0,nested+8`. Direct member, array and union accesses are spelled
  `lla sym` plus a displacement (`receipts/sym_spelling_probe.s.txt`). A
  displacement too large for an immediate is spelled `lla`, `li`, `add`, which
  resolves to unplaced (`receipts/sym_addend_probe.s.txt`). The shipping
  firmware takes only `&nvm_blocks[i]`, with a variable index.
- **Where it reaches.** A store through such an address is a new pointer store.
  The retained pointer-store text set pins that store, except behind a
  brace-less `if`. That is the #495 hole the resolver covers.
- **Not measured.** I built no whole-gate plant, so whether a complete bypass
  can be built on this shape is not measured.
- **The page.** `BAREMETAL_FIRMWARE.md:482-484` says a store through "a
  static's address" invalidates the words of "that static" it overlaps. That
  holds per symbol spelling. It is the same precision point as R228-S6, which
  is per frame register. The "does NOT observe" list at `:520-542` does not
  name this shape.
- **The suggestion.** Name it in that list, or split `sym+N` operands in the
  resolver, before #408/#409 retire any text rule onto the census.

## Prior public review findings on this PR, at this head

The delta changes only the literal control block. The resolver, the installer,
both workflows, the pages and every compiled mutant are byte-identical to
`97aa1ec9`. So each disposition that R227-3 and R228-3 recorded there carries
forward. I re-checked the ones in the table below.

| Prior finding | Disposition at `4876423d` | Evidence this round |
|---|---|---|
| **R227-3 MINOR Tests**, the overlap low boundary has no failing control | **RESOLVED** | The required control exists at `:5281-5282,5297-5298`. M1 (the R227-3 M15 edit) is KILLED on the new control's sentence, in the literal controls and through the complete gate in both modes. P0 passes. The compiled top-byte shapes are refused at the head and placed under M1. The resolver is byte-identical, so the R227-3 plant verdicts stand. Also resolved: the reverse direction (M2, M3), which R227-3 did not require |
| **R228-3 F6 MINOR Tests**, the same finding | **RESOLVED** | Same evidence. The literal and complete-gate equivalents of `overlap-last-byte` are KILLED. The byte-3 frame and static compiled shapes are refused at the head, measured by the resolver alone |
| R227-3-S1 (M16, M17) and R228-S8 | RETAINED, optional | S1 above. U1 is re-measured through the complete gate, and M17 is re-measured |
| R227-3-S2 and R228-S7 (Docs precision), R228-S6 (per-register overlap) | RETAINED, optional | The page is unchanged since `97aa1ec9` |
| R228-S5 (census-ISA filter) | RETAINED, optional | Its code is unchanged. I did not re-measure it |
| R228-S2 and S3 (installer relocation proof, download retry and deadline) | RETAINED, optional | `scripts/ci_rv32_sdk.py` and both workflows are unchanged since `3d90958f` (`git diff` is empty). The installer reports its own digest as `ffcc5433...` (`receipts/sdk_verify.log`) |
| R228-1 F1 MAJOR, F2 MAJOR, F3 MINOR | RESOLVED, retained | Their artifacts are unchanged. The head's mapped gate 1b refuses 217/217, and its log reports the five store-class mutants refused on their resolved addresses. That re-run is the only new evidence this round |
| R227-2-F1, R227-2-F2, R228-2-F4, R228-2-F5 (all MINOR) | RESOLVED, retained | Their artifacts are unchanged. Per A191 and R227-3, the 217 registered mutations at this head include the four compiled rewrite mutants, and the head refuses 217/217. I did not isolate those four |
| R227-3 O1, R227-2 OBS-1 (sub-word frame load) and R228-2 O1 (called-function and call-crossing halves) | Out of scope, pre-existing, still in the tree | Unchanged. No tracking Issue was found by R227-3. See the pending duties |

## Per-lens results at this head

```text
[R227] PASS Tests - sw/builder/test_builder.py:5263-5355 at 4876423d (receipts/delta_97aa1ec9_4876423d.diff); receipts/overlap_probe_results.jsonl; receipts/gate/{head,M1-gt,M2-plus4}.{mapped,absent}.log; receipts/top_byte_resolve.*.jsonl; receipts/static/selftest_fwc.log - the new stale and kept arms were checked against R227-3/R228-F6's required outcome and AGENTS.md section 6: every low-boundary mutant tried, in both directions, is KILLED on the new controls' own sentences, each new probe kills alone, deleting both reproduces the gap, M1 and M2 are KILLED through the complete gate in both modes, the head passes both modes, counts are computed, and the probes model the compiled top-byte shape exactly. S1 is optional.
[R227] PASS Docs - test_builder.py:5263-5269,5315-5320,5340-5354 (the changed comments and printed note, printed at this head in receipts/gate/head.mapped.log and in both exact-head hosted builder logs, receipts/hosted_log_observations.txt); BAREMETAL_FIRMWARE.md:475-506 (unchanged); receipts/static/{docs_check,em_dash_574c}.log - the changed printed gate claim matches the controls (15 stale, 5 kept, the named shapes); the note that only the low boundary reaches the last-byte shape is exact; the page's "each against a whole-word positive arm" still holds; docs_check 0 findings and em-dash 0 findings over 188 added lines against 574c29fa. S2 is optional.
[R227] PASS Conformance - receipts/gate/head.{mapped,absent}.log, receipts/compiler-audit-summary.txt, receipts/sdk_{install,verify}.log, receipts/hosted_check_runs.tsv, test_builder.py:4158-4165 (RESOLVER_STORE_RESIDUAL, outside the delta) - re-check at this head against acceptance 1-5: item 2 counts 217/217, 17/17, 4/4, 46/46 with 0 NOT RUN; item 3 182/182 with exactly one explicit NOT RUN and 0 compiles; item 5 residual unchanged; no text refusal, firmware, RTL or pin change; items 1 and 4 hosted parts read-only (all seven required contexts succeeded at the exact head; docs-check and elaborate report a verified SDK cache hit with GCC 14.3.0) and owned by the manager. Covering round: R227-3.
[R227] PASS RTL - receipts/scope.txt (no hdl/, tb/, syn/, sw/firmware/, sw/litex/ or configs/ path in 574c29fa..4876423d; four gitlinks identical at base and head); receipts/gate/head.*.log (46/46 RTL variants elaborated with scoped Verilator 5.050 in both modes); receipts/final-integrity*.txt - no RTL, CDC, reset or interface change exists to review. Covering round: R227-3.
[R227] PASS Robustness - test_builder.py:1489-1649 (byte-identical to 97aa1ec9); receipts/extra_probes.*.jsonl; receipts/top_byte_resolve.*.jsonl - the delta changes no product, installer or resolver path; the resolver's boundary behaviour at this head is correct on both sides of the low boundary for frame and static words, literal and compiled. S2 is a pre-existing, optional observation. Covering round: R227-3.
```

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | R227-3: acceptance items 1-5 against the installer, both workflows, `--require-rv32`, the residual table, both gate 1b modes, the compiler audit and exact-head hosted logs. Nothing in this lens's scope changed in `97aa1ec9..4876423d` (`receipts/scope.txt`). R227-4 re-check at this head: both gate 1b modes, the audit summary, a fresh SDK install and verify, and exact-head hosted contexts | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| RTL | CLEAN | R227-3: the changed-path list, gitlinks, 46/46 RTL variants, integrity, and hosted Verilator and Yosys. R227-4 re-check at this head: no RTL path in `574c29fa..4876423d`, gitlinks identical, 46/46 with scoped 5.050 in both modes, and integrity of the parent and all three submodules | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Robustness | CLEAN | R227-3: the installer under 16 faults, the resolver under 22 literal mutants, and compiled plants and mutants. The resolver and installer are byte-identical at this head. R227-4 re-check at this head: boundary probes on both sides and compiled top-byte shapes. S2 is optional | R227-3 | 97aa1ec943ac740a27b942210a248f6512ae3ff6 |
| Tests | CLEAN | The delta `test_builder.py:5263-5355`. 17 literal-segment probes. 8 complete gate 1b runs: head and M1 and M2 in both modes, plus U1 and U3 mapped. Compiled top-byte shapes under head, M1 and M2. `test_firmware_compiler.py --selftest`. S1 is optional | R227-4 | 4876423d4cf8e89b820c56f8339f230abefb4827 |
| Docs | CLEAN | The changed comments and printed gate note (`test_builder.py:5263-5269,5315-5320,5340-5354`), as printed locally and in the exact-head hosted logs. `BAREMETAL_FIRMWARE.md:452-563`, unchanged. `docs_check`, and `check_em_dash --base 574c29fa`. S2 is optional | R227-4 | 4876423d4cf8e89b820c56f8339f230abefb4827 |

Docs is re-covered at this head, not cited from R227-3. The delta changed a
printed gate claim, and R227-3 examined the printed gate claims under Docs.

## Execution evidence (all at exact head 4876423d)

| Execution | Result | Receipt |
|---|---|---|
| Tool identity | The scoped Verilator wrapper reports 5.050 rev v5.050. The system's 5.052 was not used for gate runs | `receipts/gate/*.log` (first line) |
| Archive | 102,597,892 bytes, SHA256 `d42680e9...b78f`, equal to the pinned `ARCHIVE_SHA256` | `receipts/sdk_archive.sha256.txt` |
| Fresh SDK install, then verify-only, with the head's installer | exit 0 (13.3 s) and exit 0 | `receipts/sdk_install.log`, `receipts/sdk_verify.log` |
| Literal-segment probes | 17 probes: 9 KILLED. 8 passed as designed: the P0 no-edit control, the 4 deletion controls and the 3 high-boundary mutants | `receipts/overlap_probe_results.jsonl` |
| Complete gate 1b | 8 runs, table above | `receipts/gate/`, `receipts/compiler-audit-summary.txt`, `receipts/audit/head.*.jsonl` |
| Compiled shapes | top-byte and one-past shapes under head, M1 and M2. Alignment and spelling probes | `receipts/top_byte_*`, `receipts/align_*`, `receipts/sym_*` |
| Supplementary literal probes | the high boundary, and the addend spelling | `receipts/extra_probes.*.jsonl`, `receipts/footprint_m17.jsonl` |
| Focused static gates in the review clone | all exit 0: py_idiom (0 over-long lines), fail-fast ratchet, hygiene ratchet, TODO ownership, parse, em-dash (0 findings, 57 arms), baremetal-only (0 findings), docs_check (0 findings), firmware-compiler self-test | `receipts/static/` |
| Exact-head hosted, read-only | All seven required contexts succeeded. So did Verilator shards 0-4 and Yosys shards 0-3. `Physical gPTP` is a skipped context. docs-check and elaborate each report `SDK cache hit: verified` and GCC 14.3.0, run TEXT RULES + INSTRUMENTS, and print the new "15 rewrites ... 5 stores" note. docs-check also ran the TEXT RULES ONLY (absent) mode | `receipts/hosted_check_runs.tsv`, `receipts/hosted_log_observations.txt` |
| Final integrity of the review clone | PASS. HEAD and tree are as reviewed. The index equals HEAD at stage 0, with no assume-unchanged or skip-worktree flag. 860 parent blobs are byte- and mode-exact. Status is clean, including ignored files. The initialised submodules are at their gitlinks, clean and byte-exact: gptp-processor 103 blobs, protocol-processor 222 and verilog-axis 214. `external` is uninitialised and empty at its pin | `receipts/final-integrity.txt`, `receipts/final-integrity-submodules.txt` |

## Real limits

- **Not run, by instruction.**
  - The full parent, PP, gPTP, Yosys and builder banks. Only gate 1b ran,
    through the head's `test_firmware_compiler.py`.
  - Docker/act, and host `act_ci` or its self-test.
  - Hardware. Physical calibration is NOT RUN, and field skips are not
    hardware proof.
  - The manager's static/builder and native banks for this head are neither
    claimed nor inferred.
- **Local mapping.** The mapped runs substitute only the absolute selector's
  argv[0] with the scratch SDK. That is local compatibility evidence, not
  hosted adoption. The hosted observations are read-only greps of public job
  logs. At this head both hosted builder jobs were cache hits, and I observed
  no fresh hosted acquisition at this head.
- **Probe trees.**
  - Mutants and gate runs used disposable `git archive` copies of the exact
    head under unpublished scratch, with the submodules copied in.
  - The copied `protocol-processor` was given a disposable index of its own
    bytes, because `scripts/pp_srcs.py` derives its list with `git ls-files`.
    The list equals the clone's 42 `.sv` files.
  - A first head run without that index failed in the environment, at RTL
    source derivation, and was discarded.
  - The review clone ran only the focused static gates and the
    firmware-compiler self-test, with `-B`. Integrity afterwards is clean.
- **Plants not re-run.** The R227-3 and R228-3 whole-firmware plants are other
  rounds' tooling. Their verdicts at this head rest on the resolver being
  byte-identical, and on my resolver-alone compiled check. For S2 I built no
  whole-gate plant.
- **Classification method.** Literal verdicts are the gate's own assertion
  sentences from the verbatim control segment, not a stop marker. Whole-gate
  verdicts are the harness exit and its assertion sentence.
- **Receipt paths.** Published receipts and scripts substitute `$REVIEW_OUT`,
  `$CLONE`, `$HOME`, `$ARCHIVE_DIR` and `$PINNED_TOOL_BIN` for local paths.
  `scripts/run_gate.sh` therefore expects `PINNED_TOOL_BIN` in the
  environment. The raw copies stay in unpublished scratch.

## Pending manager duties

- Publish this report. R228-4 is in flight separately. The merge bar still
  needs both independent positive reviews and the full completion bar.
- The full source static/builder and native banks for this head, trusted act,
  and exact-head hosted acceptance for items 1 and 4. That acceptance includes
  fresh-acquisition evidence for the installer revision in use.
- The final current-dev candidate at the merge turn. The source base is
  `574c29fa`, and live dev is `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
  Then post-merge containment.
- Record or file the public follow-up Issue for the documented resolver gaps
  before #408/#409 retire any text rule onto the census:
  - stores inside a called function;
  - a callee's write into its caller's frame;
  - numeric stores that alias a model;
  - sub-word frame-slot loads (O1);
  - per-register frame keys (R228-S6);
  - the symbol-addend spelling (S2 here).

## Reproduction

From an exact-head clone, with `PINNED_TOOL_BIN` pointing at the scoped
Verilator 5.050 directory and the archive verified as above:

```sh
python3 scripts/ci_rv32_sdk.py --destination "$REVIEW_OUT/scratch/sdk" --archive "$ARCHIVE_DIR/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz"
python3 scripts/ci_rv32_sdk.py --destination "$REVIEW_OUT/scratch/sdk" --verify-only
git archive 4876423d4cf8e89b820c56f8339f230abefb4827 | tar -x -C "$REVIEW_OUT/scratch/base"
python3 -B "$REVIEW_OUT/scripts/overlap_probe.py" "$REVIEW_OUT/scratch/base" "$REVIEW_OUT/scratch/probes"
bash "$REVIEW_OUT/scripts/gate_trees.sh" "$CLONE" "$REVIEW_OUT/scratch"
printf '%s\n' "head absent" "head mapped" "M1-gt absent" "M1-gt mapped" "M2-plus4 absent" "M2-plus4 mapped" | xargs -P 6 -L 1 bash "$REVIEW_OUT/scripts/run_gate.sh" "$REVIEW_OUT"
printf '%s\n' "U1-high-lt mapped" "U3-high-term-dropped mapped" | xargs -P 2 -L 1 bash "$REVIEW_OUT/scripts/run_gate.sh" "$REVIEW_OUT"
"$REVIEW_OUT/scratch/sdk/bin/riscv32-linux-gcc" -std=gnu99 -O0 -fno-inline -S -o top_byte.s "$REVIEW_OUT/scripts/top_byte_compiled.c"
python3 -B "$REVIEW_OUT/scripts/top_byte_resolve.py" "$REVIEW_OUT/scratch/gate/<tree>/sw/builder" top_byte.s
python3 -B "$REVIEW_OUT/scripts/extra_probes.py" "$REVIEW_OUT/scratch/gate/<tree>/sw/builder"
python3 -B "$REVIEW_OUT/scripts/footprint_m17.py" "$REVIEW_OUT/scratch/gate/head/sw/builder" [--m17]
python3 -B "$REVIEW_OUT/scripts/verify_integrity.py" "$CLONE" 4876423d4cf8e89b820c56f8339f230abefb4827 b2fb9e0516aa4ed9a17cdedfb1ae25460270d408
```

R227-4 FINISHED
