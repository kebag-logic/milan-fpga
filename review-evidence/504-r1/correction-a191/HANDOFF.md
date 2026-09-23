# A191 handoff: #504 / PR #521, second correction round (R227-2, R228-2)

Author: A191, the sole correction-round author. Public assignment: issue #504
comment 5790944031. TAKEN: issue #504 comment 5791069118. REVIEW READY: issue
#504 comment 5791630048, whose text is `REVIEW-READY.md`. Nothing was pushed, and the PR, its
metadata and the board were not edited. There was no merge, no Docker or act
run, and no delegation. Only one checkout was used, the lane checkout.

## Identity

| Item | Value |
|---|---|
| Corrected head | `97aa1ec943ac740a27b942210a248f6512ae3ff6` |
| Corrected tree | `4a12a545bdb478083d711a8f319d3c6d70c1b1d9` |
| Reviewed head (R227-2, R228-2) | `5081a25a451b4ac1c00f286ec59ab041c22fdde9`, tree `68a0628be2b55c1180a0e5751d2355cb8f987268` |
| PR base | `52711029f374650dc93830d5ea28e81cb5c8f410` |
| Previous source base | `483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| Live dev merged in | `574c29fa111c74e5e5ed63e4670aff1f492e28e2`, now an ancestor of the head |
| Dev merge commit | `4914eea5faac2e4816c38455584f259263ad8c20`, tree `fdf07c8588f8a242c2be626c51ed8072c863c191` |
| Branch | `504-hosted-rv32-compiler`, unpushed: 3 first-parent commits ahead of `origin/504-hosted-rv32-compiler` (merge + 2), 9 by `git rev-list --count` with the 6 dev commits the merge brings |

The merge tree equals `git merge-tree --write-tree 5081a25a 574c29fa`, which
exited 0 with no conflict (`receipts/01`, `02`). Dev and the branch both
changed two files, `docs/testing/CI_WORKFLOWS.md` and `scripts/ci_events.py`.
Both auto-merged. At the merge commit and at the head, `ci_events.py
--check` passes 1631 items and `--selftest` passes 2183 arms. The em-dash
gate against dev and `check_baremetal_only.py --check` also pass
(`receipts/merge-static/`).

Commits after the reviewed head. Each has a one-line subject and no trailer.

1. `4914eea5` Merge dev 574c29fa into 504-hosted-rv32-compiler
2. `3f7f083e` builder: forget rewritten frame slots in the store census and control each correction
3. `97aa1ec9` docs: state exactly which stores the RV32 store census observes

Change boundary (`receipts/11`). The two correction commits touch three files:
`sw/builder/test_builder.py`, `docs/integration/BAREMETAL_FIRMWARE.md` and
`docs/testing/CI_WORKFLOWS.md`. These are blob-identical to the reviewed head:

- the installer `scripts/ci_rv32_sdk.py` (SHA256 `ffcc5433...cb4`, so the
  cache key is unchanged);
- its self-test;
- both workflows;
- `sw/builder/test_firmware_compiler.py`;
- `scripts/check_baremetal_only.py`.

`scripts/ci_events.py` equals the merge-tree result. No path under `hdl/`,
`tb/`, `syn/`, `sw/firmware/`, `sw/litex/`, `configs/`, `constraints/` or
`.github/` changes in this round, and no budget, ratchet or pin changes. The
four gitlinks are identical at the head, the reviewed head and dev.

Final integrity (`receipts/13`): INTEGRITY PASS.

- 860 committed blobs match their bytes and modes.
- The index equals HEAD, with no assume-unchanged or skip-worktree flag.
- `git status --porcelain` is empty, and so is the ignored list: the
  `__pycache__` directories were removed.
- verilog-axis `48ff7a7e`, protocol-processor `424c688f` and gptp-processor
  `c1b61743` are checked out at their gitlinks, each with a clean status.

## Per-finding resolution

### R227-2-F1 MINOR (Robustness, Tests, Docs): route 1, the model fix

The root cause had two parts.

- **The frame branch stored the wrong value.** It set the slot to
  `_rv32_store_value()`, which returned the full source register for `sb` and
  `sh`, and the static branch filtered the same value separately. So a byte
  store at a slot's own offset left a whole, wrong word.
- **Stack-address stores touched no frame slot.** So `q = (T *)&v; q->w = x;`
  left `v`'s old value standing.

The fix, in `sw/builder/test_builder.py`:

- `_rv32_store_value()` is now the single source of "the whole word a store
  leaves at its own address". That is the source register for `sw`, `rs2` for
  `amoswap.w`, and "cannot say" for everything else. Both slot branches store
  exactly that value, so the two models cannot disagree about one store.
- A store through an `Rv32Stack` base calls the new `_rv32_forget_frame()`.
  Every frame slot is forgotten, because a stack address may be any of them.
- The `_rv32_forget_overlap()` docstring and the gate note now state what is
  modelled.

Pristine impact. Over all 120 census assemblies of a full mapped run
(`receipts/10`, summary `receipts/10-summary.txt`), the old and new resolvers
report identical store addresses in 116. The 4 that differ are exactly the new
rewrite mutants, where the `configure_fabric()` store goes from `0` to
`unplaced`. Call edges, handed arguments and seeds are identical in all 120.
Some values differ, and no rule reads them: the value field of `sb`/`sh`
observations, and some `nvm_*` helper return values. Gate 1b is green with the
same residual.

Controls. The literal-assembly controls run on every machine.

- Stale probes, which must leave the next store unplaced:
  - a byte store at a frame slot's own offset;
  - a half-word store at a frame slot's own offset;
  - a byte store at a static's own offset;
  - an integer store through a pointer to the slot;
  - an FP store through a pointer to the slot.
- A new positive arm: a whole-word store into a frame slot, a whole-word store
  into a static's second word, and an `amoswap.w` into a static. After each,
  the next store must be placed at the parked address.
- Four compiled whole-gate mutants, registered only where the census runs.
  Each is pinned on `... no declared residual accounts for: configure_fabric()
  through unplaced`:
  - a union byte store and a union half-word store at the word's own offset,
    which keep a parked `ADP_CTRL` address;
  - an integer rewrite, and a `float` rewrite computed at run time, of a local
    through a pointer to it.

Fix-removal evidence (`receipts/mutants/`). Each variant is applied in memory
to the committed builder.

| Variant | Result |
|---|---|
| sub-word stores carry their source register | KILLED in about 2 s by "after a byte store at a frame slot's own offset" |
| stack-address store keeps the frame slots | KILLED by "after an integer store through a pointer to a frame slot" |
| either of the two, with the literal stale control also removed | KILLED by the compiled mutant (`... mutation passed the boot-contract gate`) |

Reviewer plants at this head, whole gate, in memory:

- R227-2 byte-overwrite and half-overwrite, and R228-2 E12 and E12f: each
  REFUSED on the `configure_fabric()` unplaced store.
- R227-2 no-overwrite: still REFUSED on the store pin.
- R227-2 `resolver_controls.py` (`receipts/05`): F1 92/92.
  `X-stack-alias-overwrites-slot` and `X-subword-slot-store` now PASS.
  `X-subword-slot-load` is R227-2's OBS-1; it still fails and is now named on
  the page.

### R227-2-F2 MINOR (Tests, Docs): a failing control for each of the three changes

| Change | Control | Removal |
|---|---|---|
| ranged-store footprint (`hi + offset + width - 1`) | A `sw` and an `fsd` loop. Every first byte lies under the window, so each must be placed exactly to its footprint, ending at the window's first byte. | R5 (= RM8): KILLED by "a bltu-bounded `sw zero,0(a5)` loop from 0x8fffffbe came back as ..." |
| slot-mirror stop at every store class | An `fsw` over the slot, an `amoor.w` and an `amocas.w` through a pointer to it, between the slot's load and the `bltu`. Each must leave the body's store unplaced. A positive arm with nothing in between must be placed at `[0x40000000..0x40000042]`. | R6 (= RM1): KILLED by "with an fsw over the slot between the slot's load ..." |
| "cannot say" for non-swap AMO and SC | An `amoor.w` into a frame slot, and an `amoadd.w` and an `sc.w` into a static, each handed a placed address, must leave the word unknown. The `amoswap.w` positive arm must carry it. | R10: its published anchor line changed in this round. It is re-anchored on the new line (every AMO and SC writes `rs2`) and KILLED by "after an amoor.w into a frame slot, handed a placed address" |

The mirror block runs after the range block. That way the footprint mutant is
answered by the footprint control and not by the mirror's positive arm.

### R228-F4 MINOR (Tests)

- **RM8** (range width) is the R5 row above: KILLED.
- **RM11** (symbol overlap width 4) is KILLED by the new stale probe "an `fsd`
  over a static's first word, reloaded at its second".
- **RM12** is still KILLED, by "an fsd over a frame slot".
- R228-2's E10b and E11b plants stay REFUSED, on the store pin and on the
  unplaced pin.
- Optional R228-S4 was taken, as tests only:
  - RM1 is the R6 row;
  - RM5 (the memory operand needs a displacement) is KILLED by the new
    `cbo.zero (a4)` unclassified probe.

### R228-F5 MINOR (Docs)

On `docs/integration/BAREMETAL_FIRMWARE.md`:

- The class list says "RV32A: every `amo*.w` and `sc.w` instruction", and
  states that an atomic builtin compiled to a call is not one of them.
- A ranged store is judged over its footprint.
- A new paragraph, "What a store leaves behind", states the frame and static
  models exactly. It lists which stores keep a word, which forget it, the
  overlap rule per base, and the stack-address rule.
- The controls paragraph names the new controls and the four compiled
  mutants.
- The boundary paragraph names both unbound LR/SC edges (R227-2-S1). It
  makes no claim about their effect: the argument that the missing exit is
  harmless holds only for the template R227-2 measured.
- A new list, "What the census does NOT observe", has three entries:
  - stores made inside a called function: C-library and libatomic calls handed
    a window pointer, such as `memset` and a 64-bit atomic, and a callee's
    writes into its caller's frame through a pointer it was handed;
  - stores through a resolved number or a bounded range, which the frame and
    static models assume reach neither the stack nor the statics;
  - byte or half-word loads from a frame slot, which read the whole word
    (R227-2 OBS-1).
- The instrument-table cell is narrowed to FP and RV32A instruction classes
  plus the rewrites. It now says what the census does not see, with a link.
- The ISA sentence names FP stores and RV32A AMO and SC instructions.

Also changed:

- `docs/testing/CI_WORKFLOWS.md`: the same two wording corrections.
- The gate's printed resolver line says "store instruction", with RV32A AMO
  and SC.
- The gate's "NOT proved here" line now names called-function stores.

Evidence at this head: R228-2's E8 (64-bit `__atomic_exchange_n`) and E9b
(`__builtin_memset`) still PASS the complete gate, which is exactly what the
page now says. R228-2's `probe_resolver.py` is identical to their published
5081a25a receipt, 47/47: 43 caught, the one documented libatomic miss, and 3
loads (`receipts/12`).

## Suggestions

| Suggestion | Decision |
|---|---|
| R227-2-S1 | Taken (docs) |
| R228-S4 | Taken (tests only) |
| R228-S2, R228-S3 | Not taken. They change installer or workflow behaviour, and the installer bytes and cache key are unchanged. |

## Validation at the head

All runs used the scoped Verilator 5.050 and the SDK freshly installed from
the verified archive (102,597,892 bytes, SHA256 `d42680e9...78f`) into
`scratch/`.

| Check | Result |
|---|---|
| Fresh install / cache hit / verify-only | exit 0 in 12.96 s / 1.00 s / 0.74 s. GCC 14.3.0, target `riscv32-buildroot-linux-gnu`, realpath `bin/toolchain-wrapper`, relocated sysroot |
| Gate 1b, SDK mapped (`receipts/gate1b/pristine-sdk.*`) | exit 0 in 347 s. 217/217 mutations (213 plus 4 new), 17/17 and 4/4 positives, 46/46 RTL variants, 0 NOT RUN, 235 firmware compiles, census arch `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0` on all 120 census assemblies. Compiled classes: fsw, fsd, amoswap.w, amoor.w, sc.w. Residual unchanged (`parse_u64() through call(__errno_location) x1`); 66 pristine stores |
| Gate 1b, absent (`receipts/gate1b/pristine-absent.*`) | exit 0 in 282 s. 182/182, 17/17, 4/4, 46/46, exactly 1 NOT RUN, 0 compiles, all three cross candidates hidden. 35 registered skipped entries (31 plus the 4 new resolver-only ones) |
| Compiler audit (`receipts/14`) | 242 records. 239 map only argv[0], and every argument tail is preserved. The single non-zero return is the gate's deliberate 64-bit probe |
| Variants (`receipts/mutants/`) | 19/19 as expected: 10 fix-removal mutants KILLED on their own control's sentence, 7 plants REFUSED on the expected sentence, E8 and E9b PASSED |
| Static and focused gates (`receipts/static-head/`) | 22/22 exit 0; list below |

The 22 static and focused gates:

- `ci_rv32_sdk_selftest.py` (25 tests) and `test_firmware_compiler.py
  --selftest`.
- `check_baremetal_only.py`: `--check` finds 0 findings and `--selftest`
  passes 365 arms.
- `ci_events.py`: `--check` passes 1631 items and `--selftest` passes 2183
  arms.
- `docs_check.py`.
- `check_em_dash.py` against the PR base, dev and the previous source base
  (0 findings), plus its self-test.
- The doc path, TOC, anchor and doc style gates.
- The Python idiom, hygiene, fail-fast, test-evidence, naming, TODO and
  `py_compile` gates.

The "can be lowered" notes are ratchets this diff does not touch.

## Not done here (manager-owned or out of scope)

- By instruction, none of the following was run: pushes, PR or board edits,
  the full parent, PP and gPTP Verilator banks, Yosys, the full builder and
  behave banks, Docker or act, hosted runs, and hardware.
- The hosted compiled tally grows by the same 4 resolver-only entries.
  Hosted counts differ from local ones for the reasons earlier rounds recorded.
- For a public Issue before #408/#409 retire any text rule onto the census.
  These are the shapes the page now lists as not observed; none is new in
  this PR, and none is closed by it:
  1. stores inside a called function that is handed a window pointer, such as
     `memset`, `memcpy` or libatomic (R228-2 O1 class 1);
  2. a callee's write into its caller's frame through a pointer it was
     handed. This is the call-crossing half of R228-2 O1 class 2; this round
     closes the in-function half;
  3. a store through a numeric address that happens to be a stack location;
  4. sub-word frame-slot loads (R227-2 OBS-1).
- Receipts carry local absolute paths and must be neutralized before any
  public copy.
- `scratch/` was deleted: the SDK prefix, census captures, the old-builder
  copy and the probe copies.

## Files

- `TAKEN.md`: the posted TAKEN text.
- `REVIEW-READY.md`: the posted REVIEW READY text.
- `PR-BODY.md`: the proposed PR body for the manager.
- `COMMANDS.md`: the exact commands.
- `scripts/`: this round's scripts.
  - `gate_variants.py` runs the in-memory mutants and plants.
  - `run_pristine_gates.sh`, `run_static_receipts.sh`, `capture_census.py`,
    `resolver_compare.py` and `verify_integrity.py` are the other drivers.
  - `plants/` holds the reviewers' published plant diffs.
  - `r227-2/` and `r228-2/` hold unmodified copies of the reviewers' scripts.
- `receipts/`: the numbered receipts, plus `gate1b/`, `mutants/`,
  `static-head/` and `merge-static/`.
- `MANIFEST.sha256`: every file above.
