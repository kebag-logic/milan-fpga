[R339] POSITIVE - exact head 7c63e453142deb4d848c41594b2246afe32a792a

External independent review R339-3 of issue #565 / PR #581. Head `7c63e453142deb4d848c41594b2246afe32a792a`, tree `4233e1b99eb6e3120aba74ac671749e3092c12e1`. This round is a delta review of `054e59b4..7c63e453`: one text-only commit, two Markdown files, 14 insertions and 7 deletions. Source base `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.

Verdict basis: no BLOCKER, MAJOR or MINOR finding is open. R339-2 F1 (MINOR) and F2 are closed at this head. Three SUGGESTIONs are recorded; they do not affect coverage. All five lenses were applied at this head and are CLEAN.

## Reconstruction order

1. AGENTS.md, then CONTRIBUTING.md by reference, then the build contract at `docs/integration/BAREMETAL_FIRMWARE.md#build-contract`.
2. Issue #565: the body and its frozen acceptance, the assignment and decision (5848231174), TAKEN (5848248804), REVIEW READY for round 1 (5848792439), the round-2 assignment (5853405428) and REVIEW READY for round 2 (5853449568). Issue #582 was read as the declared destination of the deferred items.
3. PR #581: the body, and the manager's comments 5853095668 and 5853457567.
4. `git diff 054e59b4..7c63e453` in full, `831f94f4..7c63e453` by stat, and the commit metadata.
5. Public evidence at `8322c6de:review-evidence/565-r1`. It holds only round-1 author evidence at `054e59b4` (`author/commit.json`). See the limits section.
6. My own verdict and ledger were written before I read any prior review (`receipts/draft_verdict_before_prior_findings.md`, identical in verdict and ledger). After that I read the prior public findings (R339-2 at 5853297338, R338-2 at 5853401533) and resolved each one below.

## Delta identity (`receipts/delta_identity.txt`, `receipts/rtl_delta_and_derivation.txt`)

- Changed: `docs/integration/BAREMETAL_FIRMWARE.md` (13+/6-) and `hdl/ieee1722/aaf/README-parameters.md` (1+/1-). Both keep mode 100644. No non-Markdown path changed.
- These blobs are identical at `054e59b4` and `7c63e453`: `measurements.json` (894e9f5a), `check_nvm_capture.py` (5d763f85), the 8x8 yaml (7743b130), `endstation_builder.py` (97617b4e) and `milan_soc.py` (1e03d094).

## Focus item 1: the build-contract paragraph against the code

`BAREMETAL_FIRMWARE.md:33-44` makes six claims. I checked each against the source and then against the running tool. The builder was probed on scratch copies of the 8x8 yaml (`scripts/probe_builder_clock_and_profile.sh`, `receipts/builder_probe_summary.txt`, per-case logs in `receipts/builder_probe_logs/`). The `milan_soc.py` argument checks were probed by running its `main()` prefix up to the last profile refusal, with LiteX stubbed (`scripts/probe_milan_soc_args.py`, `receipts/milan_soc_args_probe.txt`).

| Doc claim | Builder | `milan_soc.py` | Holds? |
|---|---|---|---|
| `:36` CPU is VexiiRiscv, XLEN 32, `cpu_count` 1 (both tools) | `endstation_builder.py:4224-4226`. naxriscv, xlen 64 and cpu_count 2 are each refused | `milan_soc.py:3683-3685`. The same three are refused | yes |
| `:37` `l2_bytes` is zero (both) | `:4227-4228`. 4096 is refused | `:3686-3688`. `--l2-bytes 4096` is refused | yes |
| `:37` "no Scala overrides" (both), replacing "no cache or prefetch Scala arguments" | `:4227` tests `soc["scala_args"]` for any non-empty list. A non-cache `alu-count=1` is refused, and so is a cache one | `:3686` tests `args.scala_args`, and the message reads "no --scala-args overrides". `alu-count=1` is refused | yes. The new wording matches the code, and the old "cache or prefetch" wording was narrower than the code. Gate 1b's own case label is "scala override" (`test_builder.py:3019`) |
| `:39` builder restricts `flashboot` to `baremetal`/`none` | `:3757-3759` (unconditional) and `:4229-4230`. `linux` is refused and `none` is accepted | argparse `choices` at `:3623-3624` restrict it the same way (see S1) | yes |
| `:40` `milan_soc.py` additionally refuses an FPU | no FPU key exists: `soc.with_fpu` is refused as an unknown key (`:4209-4211`), and the argv emitter never passes `--with-fpu` (`:4768-4787`) | `:3686`. `--with-fpu` is refused | yes |
| `:42-43` the 50 MHz target is checked by neither tool; the builder's only clock check is `milan_clk_hz <= sys_clk_hz` | `:3772-3773` is the only clock refusal. 1, 12.345678, 33, 62.5, 75 and 100 MHz all exit rc 0. At 75 MHz the output carries `--milan-clk-freq 75e6` (`receipts/builder_probe_75MHz_propagation.txt`). 150 MHz is refused with "must not exceed sys_clk_hz" | no clock check at argument level. 75e6, 100e6, 200e6 (above sys) and an absent Milan clock are all accepted | yes |
| `:44` enforcement is tracked in #582 | #582 is open and its acceptance 1 is exactly this enforcement | - | yes |

The paragraph now claims no clock enforcement. The remaining contract properties at `:46-60`, the ISA, the 50 MHz clock and fabric gPTP, are introduced as "The product contract also requires these properties". They are no longer presented as tool refusals.

## Focus item 2: README-parameters row

`hdl/ieee1722/aaf/README-parameters.md:37` now reads "derive it from the selected shape's clock to avoid incorrect sampling with a fixed divider". It names no board clock. The row's derivation matches the RTL: `milan_datapath.sv:656` is `MCLK_DIV_LOG2_C = $clog2(MILAN_CLK_FREQ_HZ / 12_500_000)`, fed by the shape's `milan_clk_hz`. That gives 2 at 50 MHz and 3 at 100 MHz (`receipts/rtl_delta_and_derivation.txt`), which agrees with the PR table's "MCLK divider exponent 3 -> 2". All five tracked configurations now declare 50 MHz.

## Focus item 3: nothing else changed; the capture gate still passes

- No config, gate, measurement or code blob changed (see Delta identity).
- `python3 -B scripts/check_nvm_capture.py` returns rc 0 with every control detected: "PASS: capture census, clocks, both timing arms and receipt agree" (`receipts/check_nvm_capture.log`).

## Focus item 4: docs gates and the PR body

All gates return rc 0 (`receipts/gates_rc.txt`):

- `docs_check.py` in Git mode (0 findings over 166 md files) and in `GIT_DIR=/dev/null` mode (0 findings; the Git-parity arm is skipped and supplies no evidence).
- `check_em_dash.py --base 831f94f4`: 0 findings over 32 added lines, arms 339/339.
- `check_doc_style.py`.
- `gen_toc.py --check` and `--verify-anchors` (176 reproduced).
- `check_doc_paths.py` (847 paths).
- `check_feature_status.py`: 0 findings. It reads the marked blocks on the edited page.
- `git diff --check` over `054e59b4..7c63e453` and over `831f94f4..7c63e453`.

The default interpreter lacks the pinned Markdown renderer, so the renderer gates first refused (rc 2, "cannot judge"; logs kept as `*.default_python_no_renderer.log`). I re-ran them under an existing interpreter whose `cmarkgfm`, `cffi`, `pycparser`, `html5lib`, `six` and `webencodings` versions equal `tools/markdown/requirements.txt`. Nothing was installed.

No builder gate pins the rewritten sentences. Gate 1b reads this page only for the boot-order and paste-ban claims (`test_builder.py:12100-12103` against page `:111-114`; `:14857-14861` against page `:440-443`), and neither is in the edited span. A repository search finds no script or workflow that quotes the removed text.

PR body: the "Round 2" section and its validation table describe this head accurately. One stale word remains: the `Status` line says the corrections are "committed locally" (S2).

## Findings

```text
[R339] SUGGESTION Docs — docs/integration/BAREMETAL_FIRMWARE.md:39 — flashboot restriction attributed to the builder only
Requirement/evidence: the paragraph sets out to say what each tool enforces. :39 reads "The builder also restricts `flashboot` to `baremetal` or `none`". sw/litex/milan_soc.py:3623-3624 restricts --flashboot to the same two values through argparse choices; `linux` is refused with rc 2 (receipts/milan_soc_args_probe.txt). The sentence does not say milan_soc.py lacks the check, so nothing false is stated.
Impact: understatement only. A reader could conclude that milan_soc.py accepts other manifests.
Required change: optional. For example, "Both tools also restrict flashboot to baremetal or none (the builder in its loader, milan_soc.py by argument choices)".
Verification: re-read :39 against milan_soc.py:3623-3624.
```

```text
[R339] SUGGESTION Docs — PR #581 body, "Status" section — "committed locally" is stale
Requirement/evidence: the Status line reads "Round 2 text corrections are committed locally and ready for independent re-review". The PR head is 7c63e453, so the commit is published. The DoD line "Independent re-review ... remains pending" is true until this verdict is published.
Impact: cosmetic. A cold reader could doubt that the published head is the reviewed one.
Required change: optional. When the manager next edits the body, state the published head and the review results.
Verification: read the PR body.
```

```text
[R339] SUGGESTION Docs — sw/builder/endstation_builder.py:4228 — refusal message narrower than the check
Requirement/evidence: the message says "no cache/prefetch scala_args", but :4227 refuses any non-empty scala_args (receipts/builder_probe_logs/soc_scala_noncache.log: `alu-count=1` is refused with that message). This is pre-existing code outside this text-only delta. The page is now more accurate than the message.
Impact: a misleading diagnostic only. The behaviour is correct.
Required change: none for this PR. #582 edits this function, so it can align the message there.
Verification: the refusal text names scala_args overrides generally.
```

## Prior public findings: resolved or retained at this head

| Finding | State at 7c63e453 | Evidence |
|---|---|---|
| R339-2 F1 (MINOR, Docs): the contract claimed both tools reject a non-50 MHz bare-metal profile | **CLOSED** | `:33-44` lists only the enforced checks, says the 50 MHz target is checked by neither tool, states the builder's only clock check and links #582. Every claim was confirmed by source reading and by probes (focus item 1). |
| R339-2 F2 (SUGGESTION, Docs): README-parameters `:37` named the 100 MHz AX build | **CLOSED** | Focus item 2 |
| R339-2 F3 (SUGGESTION, Robustness): builder should enforce the contract clock | **RETAINED as SUGGESTION, routed to #582** (acceptance 1) | The builder still accepts 75/100 MHz (probe). The page now says so, so no false assurance remains. It does not affect coverage. |
| R338-2 S1 (SUGGESTION, Docs/Conformance): the same enforcement overclaim | **CLOSED** by the rewording | Same evidence as F1 |
| R338-2 S2 (SUGGESTION, Tests/Docs): hand-written AX clock pairs in `test_pp_mem_bridge.py:382-392` and `sweep_extra.sh:13` | **RETAINED as SUGGESTION, routed to #582** (acceptance 2) | Both files are unchanged in `831f94f4..7c63e453`. The item is pre-existing and does not affect coverage. |
| R339-2 observation (not a finding): `docs/AAF_LATENCY_TAPS.md:15` | Unchanged, routed to #582 (acceptance 3) | - |

## Clean lens results

```text
[R339] PASS Conformance — docs/integration/BAREMETAL_FIRMWARE.md:33-44 against sw/builder/endstation_builder.py:3757-3773,4209-4230 and sw/litex/milan_soc.py:3370-3371,3623-3624,3683-3688; receipts/builder_probe_summary.txt; receipts/milan_soc_args_probe.txt — round-2 assignment 5853405428 items 1-2 met: enforced checks are separated from the declared 50 MHz target, cited by file, with no enforcement claimed that the tools lack (probes: 1-100 MHz accepted by the builder, 200 MHz accepted by milan_soc.py, each listed profile violation refused); issue #565 acceptance 1-2 remains met, since the config line and every consumer are byte-unchanged from 054e59b4, which R339-2 covered.
[R339] PASS RTL — hdl/ieee1722/aaf/README-parameters.md:37 against hdl/milan/milan_datapath.sv:656; receipts/rtl_delta_and_derivation.txt — no RTL, constraint or generator file changed in 054e59b4..7c63e453; the only RTL-facing text restates MCLK_DIV_LOG2_C's derivation from MILAN_CLK_FREQ_HZ correctly (exponent 2 at 50 MHz, 3 at 100 MHz) and names no board clock.
[R339] PASS Robustness — receipts/builder_probe_summary.txt; receipts/milan_soc_args_probe.txt — the configuration-dependent behaviour the page now documents was driven at its boundaries: Milan = sys (100 MHz) accepted, Milan > sys (150 MHz) refused by the builder, off-contract clocks (1, 12.345678, 33, 62.5, 75 MHz) accepted, flashboot none/baremetal accepted and linux refused, an absent Milan clock accepted by milan_soc.py; the page states exactly this. Retained F3/S2 are SUGGESTIONs tracked in #582.
[R339] PASS Tests — scripts/check_nvm_capture.py with tb/verilator/nvm_capture_cpu/measurements.json (blobs unchanged since 054e59b4); receipts/check_nvm_capture.log; receipts/check_feature_status.log; sw/builder/test_builder.py:3013-3037 — the capture gate passes on the unchanged receipt with all controls detected; no test or gate changed; gate 1b's refusal arms (RV64, two harts, alternate CPU, cache, scala override, unknown flash manifest) are exactly the refusals the page lists, and gate 1b has no clock arm, consistent with ":42 not checked"; the page text gate 1b pins (the boot-order claim at :111-114 and the paste-ban claim at :440-443) is outside the edited span (:33-44).
[R339] PASS Docs — docs/integration/BAREMETAL_FIRMWARE.md:29-64; hdl/ieee1722/aaf/README-parameters.md:37; PR #581 body; receipts/gates_rc.txt — the rewritten paragraph is accurate claim by claim; #582 exists and matches the pointer; no other current document claims clock enforcement (regex search over docs/, sw/builder/*.md, sw/litex/*.md and configs/); all docs gates rc 0; the PR body describes round 2 accurately, with one stale word recorded as S2 (SUGGESTION).
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | BAREMETAL_FIRMWARE.md:33-44; endstation_builder.py:3757-3773, 4209-4230; milan_soc.py:3370-3371, 3623-3624, 3683-3688; builder and milan_soc argument probes; issue #565 acceptance, assignment 5853405428, #582 | R339-3 | 7c63e453142deb4d848c41594b2246afe32a792a |
| RTL | CLEAN | README-parameters.md:37; milan_datapath.sv:656; delta file list (no RTL, constraint or generator change) | R339-3 | 7c63e453142deb4d848c41594b2246afe32a792a |
| Robustness | CLEAN | clock and profile boundary probes (builder 17 cases, milan_soc.py 15 cases) | R339-3 | 7c63e453142deb4d848c41594b2246afe32a792a |
| Tests | CLEAN | check_nvm_capture.py on the unchanged receipt; check_feature_status.py; test_builder.py gate 1b refusal table and doc anchors | R339-3 | 7c63e453142deb4d848c41594b2246afe32a792a |
| Docs | CLEAN | BAREMETAL_FIRMWARE.md build contract; README-parameters.md; PR body; docs gates in both modes with the pinned renderer; tree search for enforcement claims | R339-3 | 7c63e453142deb4d848c41594b2246afe32a792a |

Scope note for section 7: R339-2 covered Conformance, RTL, Robustness and Tests at `054e59b4`, an ancestor of this head. This delta touches only two Markdown files. Even so, each lens was re-applied here and is banked at the exact head above.

## Real limits

- **Delta review.** I re-derived nothing from the round-1 consumer audit or the capture reproduction. Those rest on R339-2 and R338-2 at `054e59b4`, and every file in their scope is byte-identical at this head.
- **`milan_soc.py` probe method.** LiteX and migen are not installed on this host. The probe runs `main()`'s own source only up to the last profile refusal (`milan_soc.py:3686`), with top-level constants loaded and `builder_args` stubbed. Refusals later in elaboration, such as PLL feasibility or bridge-timeout checks, were not exercised. The page makes no claim about them.
- **Simulator.** The scoped Verilator path named in the assignment does not exist on this host. No simulation was needed for a text-only delta, and none was run.
- **Evidence tree.** `8322c6de:review-evidence/565-r1` holds only round-1 author evidence at `054e59b4`. I found no public artifact of the manager's source bank at `7c63e453`. I did not rely on one.
- **Hosted checks.** In a snapshot taken during this round (`receipts/hosted_checkruns_snapshot.txt`), several exact-head jobs were still in progress: docs-check, elaborate, the five Verilator shards and yosys-elaboration. The completed ones succeeded, and "Physical gPTP" was skipped, which is not evidence. Hosted acceptance is the manager's.
- **Not run:** the full builder bank, suite shards, PP/gPTP/Yosys banks, synthesis, place and route, Docker/act and hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Clone restore.** The builder writes `configs/generated/<stem>/gen` regardless of `-o`, and its subprocesses create `__pycache__` directories. I removed both. `scripts/verify_clone.sh` then confirmed that HEAD, tree and index equal the reviewed head, all 908 tracked blobs match in bytes and mode, there are no hidden index flags and no untracked or ignored files, and the four gitlinks are at their recorded commits. `external` is not checked out, and its index gitlink is at efeb541a (`receipts/restore-verification.txt`).

## Pending manager duties

- Hosted and act acceptance at the exact head, keeping executed jobs separate from skipped contexts.
- Publish or cite the source-bank evidence at `7c63e453`.
- Build and validate the final candidate merge result on live dev `8c8e7bb05aa50d840a84394e44659dc9c46b9639` (source base `831f94f4`).
- Optionally refresh the PR body Status line (S2).
- Carry #582, which holds F3, S2 and the latency-tap observation, and optionally S1 and S3. A merge needs explicit maintainer authorization.

R339-3 FINISHED
