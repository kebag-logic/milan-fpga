[R551] NEGATIVE - exact head d6b6ca899ae4c248a1342867bb89060e24febcd5

External independent review R551-1 of issue #654 / PR #694.
Tree: `4080c70435bc8dc06e157eb3e46671aab9f83912`.
Source base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
All five lenses were applied. One MINOR finding remains open.
The CPU measurements and both product artifact comparisons reproduce.
The remaining defect is a fractional-input boundary in CLI validation.

## Authority and scope

Reconstruction followed the requested order: operating and contribution rules,
documentation index, issue and public decisions, requirements and interfaces,
exact diff/history, then public executable evidence. No private author material
or another reviewer's report informed this verdict.

- [Issue #654](https://github.com/kebag-logic/milan-fpga/issues/654) freezes the three acceptance criteria.
- [Assignment 6045462105](https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6045462105) requires per-path measurements, early reasoned refusals, planted controls and unchanged product outputs.
- [Ruling 6045774790](https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6045774790) restricts comparisons to the two AX7101 configurations. Arty remains outside this lane under #583.
- `REQUIREMENTS.md`, REQ-VER-03/04, `docs/litex/LITEX_SOC.md:10`, its CPU/default contract, and `docs/integration/BUILDING.md:136` govern the option and build behavior. No wire-protocol clause changes.
- [Public evidence](https://github.com/kebag-logic/milan-fpga/tree/672394110780ae01de682b7ca8360d50dcdca633/review-evidence/654-r1) was checked against all 18 published manifest digests. See `receipts/public-hashes.json`.

The exact diff has one commit and four files: the recipe, focused option
tests, builder-bank registration and build documentation. Defaults, CPU
generator sources, configurations, RTL, registers and gitlinks do not change.

## Finding

**R551-1-F1 | MINOR | Conformance, Robustness, Tests, Docs**

**Artifact:** `sw/litex/milan_soc.py:3483`, `sw/litex/milan_soc.py:2575`,
`sw/builder/test_soc_options.py:143`, `docs/integration/BUILDING.md:147`.

**Title:** Nonzero fractional byte counts underflow to accepted zero before validation.

**Authority/evidence:** Issue acceptance 1 requires refusing ineffective L2
requests. The added validator and build guide require finite, nonnegative,
whole-byte counts. CLI `type=float` converts `1e-400` to `0.0` and `-1e-400`
to `-0.0` before the validator sees either token. Both then pass the new
whole-byte check, the cacheless-L2 refusal and the existing product-profile
gate. The independent probe intercepts the first board-routing/setup call;
both invalid tokens reach it. Literal zero correctly reaches setup, while
`1e-12` exits 2 with the whole-byte reason.
`receipts/byte-count-underflow.log` records all four cases; the regression
probe returns 1 at the reviewed head.

**Impact:** Invalid fractional requests, including a negative request, are
silently treated as zero. This leaves a narrow instance of the issue's
ignored-option behavior and makes the documented whole-byte contract incomplete.
The normal product recipes and their generated outputs are unaffected.
The float parser predates this change; the new validation does not close this boundary.

**Required outcome:** Validate the byte-count input before a lossy conversion
can turn a nonzero fraction into zero. Preserve omission and genuine zero,
and retain existing reasoned refusals and supported constructor effects.
Add the underflowing positive and negative tokens to the CLI regression bank.
The documentation's whole-byte promise must hold for these inputs too.

**Verification:** Run `scripts/byte_count_underflow.py <source-root>` using
the pinned dependency interpreter. It must return 0, with both underflow
cases exiting 2 before the setup sentinel and naming the invalid count.
Re-run the focused option bank, planted controls and both AX7101 comparisons
at the fix head.

No other BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is recorded.

## Examined behavior and executable evidence

| Check | Result and receipt |
|---|---|
| Sixteen baseline exports | All returned 0. Raw hashes, normalized hashes and sizes reproduce all sixteen published rows. `receipts/cpu-measurements.json`, `receipts/cpu-campaign.log` |
| VexiiRiscv, RV32 and RV64 | FPU and explicit zero retain raw bytes. L2=8192 changes the generated name/comments only. Refusing FPU and nonzero L2 follows those measurements. |
| NaxRiscv, RV32 and RV64 | FPU adds instantiated `FpuCore`, `FpuDiv` and `FpuSqrt`. L2=8192 changes the actual 64-bit data-bank depth from 16384 to 1024 words, or 128 KiB to 8 KiB. Zero retains the default netlist. `receipts/hardware-effects.json` |
| Candidate focused bank | 36 constructor cases, 11 CLI cases, six killed refusal controls, four real netlist effects and four killed forwarding controls; rc 0. `receipts/cpu-campaign.log` |
| Builder registration | Invoked only `test_soc_option_refusals` through the real builder module; rc 0, no skip. Registration at `sw/builder/test_builder.py:29036` and invocation at line 28727 inspected. `receipts/builder-registration.log` |
| Additional early-boundary probes | 25 cases pass, including negative infinity, small fractions, fractional positive sizes, negative zero on NaxRiscv, malformed CLI input and an alternate board. Constructor probes stop at CPU `args_fill`; CLI probes stop before platform construction. Child execution failure propagates rather than counting as a killed control. `receipts/additional-probes.log` |
| Fraction underflow regression | Fails as R551-1-F1 describes. `receipts/byte-count-underflow.log` |
| AX7101 8x8 | 32 generated artifacts match base/head byte for byte. `receipts/ax-equivalence.json` |
| Shipping AX7101 1x1 TDM8 | 32 generated artifacts match base/head byte for byte. `receipts/ax-equivalence.json` |
| Dependency patch reconstruction | The four declared patches reproduce all four installed files on disposable copies; rc 0. `receipts/dependency-patches.log` |
| Documentation and Python checks | Documentation style, solution documentation and Python idiom checks return 0. Corresponding logs and rc files are in `receipts/`. |

The baseline campaign removed the ten distinct measured CPU netlists from
disposable data copies before exporting. First uses regenerated them from
existing generator sources; identical-option cases then reused those outputs.
Each export used a fresh process. Candidate netlist tests used these real
generated files, including the forwarding-removal controls. No stubbed
netlist, CPU source patch or new shared installation supplied the evidence.

The AX7101 comparison executes public `export_compare.py` on a disposable
source clone. The baseline recipe comes from the exact source-base blob;
other production inputs are unchanged by this four-file diff. Both phases
receive identical timestamps and deterministic diagnostic instance ordering
before generation. Every artifact is compared as raw bytes afterward.
Diagnostic logs are excluded, as the published harness states. The 32-file
populations match the public populations. Absolute source locations change
three files relative to the author's manifests, so cross-environment digests
are not claimed equal; base/head equality within this reproduction is exact.
No software compilation, synthesis, placement, timing or hardware proof is implied.

The six named refusal controls remove the FPU, cacheless-L2, explicit-zero,
byte-size, constructor-call and CLI-call checks. The four effect controls
remove FPU or L2 forwarding at each width. Every control fails its intended
assertion. The additional failing underflow case is absent from the shipped bank.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | Issue #654 and decisions; `milan_soc.py:2573`, `:2612`, `:3483`, `:3790`; sixteen exports; both AX comparisons | R551-1 applied, open F1 | d6b6ca899ae4c248a1342867bb89060e24febcd5 |
| RTL | CLEAN | Four-file exact diff; unchanged CPU forwarding at `milan_soc.py:2651`, `:2686` and `:2694`; real FPU/L2 netlists; `receipts/hardware-effects.json`; both 32-artifact comparisons | R551-1 | d6b6ca899ae4c248a1342867bb89060e24febcd5 |
| Robustness | UNCLEAN: F1 | `_validate_cpu_options`; real constructor/CLI refusal bank; 25 additional setup-boundary probes; `receipts/byte-count-underflow.log` | R551-1 applied, open F1 | d6b6ca899ae4c248a1342867bb89060e24febcd5 |
| Tests | UNCLEAN: F1 | `test_soc_options.py:23`, `:119`, `:143`, `:158`, `:197`; actual builder registration; all ten planted controls; missing underflow case | R551-1 applied, open F1 | d6b6ca899ae4c248a1342867bb89060e24febcd5 |
| Docs | UNCLEAN: F1 | `BUILDING.md:136` option table and whole-byte claim; CLI help; public issue/PR scope and evidence; documentation gate receipts | R551-1 applied, open F1 | d6b6ca899ae4c248a1342867bb89060e24febcd5 |

[R551] PASS RTL - `receipts/ax-equivalence.json` and `receipts/hardware-effects.json` - CPU forwarding, cache geometry and both product outputs checked against the exact source base and CPU contract. No changed RTL, clock/reset, CDC, register or default artifact was found.

## Limits and manager duties

Prior public findings were checked only after this verdict and ledger were
written. The PR had zero formal reviews, zero inline comments and two
review-start notices, with no prior findings to resolve or retain.
`receipts/prior-findings.json` records that read-only snapshot.

This is a source-head review, not merge approval. The source base differs
from assigned live `dev` tip `d8b355fe0f41d49dca6cae1cd8b3826e2edde364`.
The manager owns validation of the final current-dev candidate, hosted and
local-replica acceptance, independent review completion, merge authorization,
containment, issue closure and project state.

Full parent, processor, portability and builder banks were not rerun.
Their reported source-head results remain separate from these focused receipts
and from final-candidate evidence. Historical Arty report calibration is NOT RUN.
Physical calibration and field skips are not hardware proof. No hardware ran.
Hosted checks were observed as execution/skips individually; unfinished or
skipped contexts are not promoted into executed passing suites.
The recorded snapshot has fourteen successful jobs, six unfinished jobs and
one skipped physical job; see `receipts/hosted-snapshot.json`. Hosted and
local-replica acceptance remain the manager's responsibility. At this read,
the public issue and PR carried the author review-ready evidence and manager
assignment/ruling/start notices, without a separate manager gate-evidence comment.

No tracked source was edited. Before/after raw blob, executable-mode, index
and required-submodule checks agree: 1165 superproject blobs, 104 gPTP blobs,
558 protocol-processor blobs and 214 stream-library blobs. The optional
`external` submodule remains uninitialized and is outside these exports.
See `receipts/tree-before.json` and `receipts/tree-after.json` for exact pins.
All owned campaigns finished. Peak unit memory was 5,448,843,264 bytes under
the 12 GiB cap, with no OOM event. Disposable trees remain under scratch.
Publishable logs have location-only redactions, with both hashes recorded
in `receipts/log-provenance.json`. `REPRODUCE.md` describes the scripts.

F1 requires correction and a new review verdict at the corrected head.
Any later artifact change requires reassessing applicable ledger rows.

R551-1 FINISHED
