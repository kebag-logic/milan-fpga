[R662] NEGATIVE - exact head 53ac2e9d75ceb381c2d2b04854e760304d9ae43f

One open MINOR finding leaves Docs unclean: the current ROM-budget figures still describe the base revision. No functional defect was found in the scoped mastership or path-publication changes. The focused controls pass and the planted defects fail their intended checks.

Reviewed tree: `69618d639b4019c0c27d6b03cfae8f9d36830d8b`. Base: `43acfbcc098f5af1be20a4a5458770ead3717622`. The two commits are `4d6288e82ebf40d10d7521a7a675feacd502b847` (#84) and the reviewed head (#85).

The independent verdict and five-lens ledger were written in [INDEPENDENT-PASS.md](INDEPENDENT-PASS.md) before prior-review reconciliation. No other reviewer's report was read during the independent pass.

**R662-1-F01 — MINOR — Docs — OPEN**

- **Location:** `docs/MANAGER.md:103` and `docs/MANAGER.md:107`; causal change at `hdl/ucode/gen_gptp_ucode.py:1990` (`prog_leg_srto`).
- **Authority/evidence:** The guide labels these figures “Current ROM budget.” It claims 1,013 of 1,024 words (98.9%) and eleven free words. Regeneration at the reviewed head reports **1,015 words (99.1%)**, leaving **nine**. [Base receipt](base-rom-budget.log) reports 1,013; [head receipt](focused/image-0.log) reports 1,015. The receipt-timeout leg grows from five to seven instructions. All four regenerated images match the committed images byte for byte; see [focused summary](focused/summary.json).
- **Impact:** The current capacity statement overstates the remaining ROM space by two words in an already tightly packed image. This delta makes a previously correct figure stale. It does not demonstrate a packing or runtime failure.
- **Required outcome:** Update the current usage to “1,015 of 1,024 words (99.1%)” and the free-space statement to nine words, preserving the warning that fragmented gaps constrain placement.
- **Verification:** Regenerate the default shipping image and the other three tracked image configurations; confirm the current occupancy and matching bytes, then run the documentation checks. The existing documentation checks pass at this head but do not validate this number.
- **Classification:** This changes a measurement/capacity figure, so the owner's wording-only RESIDUE exception does not apply. Docs remains UNCLEAN until corrected.

**Scope and authority reconstruction**

The supplied AGENTS instruction and its referenced command policy were read first. No repository AGENTS.md or CONTRIBUTING.md, or ancestor AGENTS.md, was present. `docs/README.md`, the root README and the current integration, HDL, test, source-evidence and manager guides were read before the diff.

The frozen [#84 acceptance and assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/84#issuecomment-6257168490), [#85 acceptance](https://github.com/Mister-M-alt/FPGA-gPTP/issues/85), and newest [STOP ruling](https://github.com/Mister-M-alt/FPGA-gPTP/issues/84#issuecomment-6259159680) govern this review. The ruling explicitly authorizes both changes with the four-expectation parent companion and requires the full 11-command consumer list. It does not authorize a parent-visible port or parameter change. #82's reset, winning-peer and departed-peer publication contract remains binding.

The applicable requirements are IEEE 1722-2016 4.4.4.7 and 10.4, Milan v1.2 4.3.5.2 and Annex B.1.1, IEEE 802.1AS-2020 10.3.9.23 and 10.3.13.2.4 f) 5), and the GET_AS_PATH consumer references in #85. Conformance here is assessed against the frozen public clause requirements and the implementation authorities; this is not a separate full-text standards audit or certification.

Parent authorities were read at `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`: the [integration contract](authority-GPTP_PLANE.md), [publication wrapper](authority-KL_gptp_shadow.sv), and [clock-validity implementation](authority-KL_ptp_clock_validity.sv). The wrapper samples the complete tuple at commit and raises a pre-commit discontinuity on a GM change or sync loss. Clock validity combines sync health, live discontinuity and retained holdover. Raising master sync-ok therefore does not bypass GM-change holdover.

**Five-lens evidence**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen #84/#85 acceptance and STOP ruling; #82 transitions; parent publication/validity authorities; generator mastership policy; engine path staging | R662-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| RTL | CLEAN | `hdl/top/KL_gptp_engine.sv:718–993`; `prog_btca`, `prog_become`, `prog_self`, `prog_leg_srto`; four ROM images; module-interface comparison | R662-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Robustness | CLEAN | `tb/verilator/engine/sim_main.cpp:2433`, `:3781`, `:5198`, `:5221`; frozen Announce ownership; reset, loss and reacquisition checks; `holdover/control.log` | R662-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Tests | CLEAN | `tb/verilator/engine/mutants.py`; `focused/summary.json`; `holdover/summary.json`; `evidence-audit.json`; parent companion and consumer receipts | R662-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |
| Docs | UNCLEAN | Current guides, PR body, source-evidence anchors, source-comment delta, public receipt index; F01 current ROM-budget mismatch | R662-1 | 53ac2e9d75ceb381c2d2b04854e760304d9ae43f |

For #84, BECOME sets bits 1 and 3 together. The branch-free SRTO mask preserves sync-ok while master and clears it while slave. The stalled serializer test queues receipt expiry behind takeover and grades the later commit. Handover to a peer still clears the verdict. The existing distinction between self publication before mastership and an active master role is explicitly described in the PR and guide; this review does not extend that behavior beyond the assigned change.

For #85, region 3 word 7 stages the frozen selected Announce. Counts 1–7 gain one entry; the appended identity comes from the configured ROM, not the announcing source. Received tails are copied, the next slot receives thisClock, and inactive slots clear. Count zero stays empty. Eight or more received entries retain the existing eight-entry prefix. This preserves the interface limit and agrees with the documented scope. The BTCA take/resolution paths keep the committed GM/path pair coherent; reset, peer loss and return still publish `{thisClock}`. No new prohibited source-comment identifiers were found in the reviewed delta.

**Execution and public evidence**

Independent executions used the verified pinned simulator identity 5.050. Disposable builds and mutation sources stayed under `scratch/`; the reviewed source was not patched. Independent cases ran concurrently under one foreground driver, with no more than 16 compilation jobs. No full parent, protocol-processor, gPTP, synthesis or builder bank was run by this reviewer.

| Reviewer execution | Result | Receipt |
|---|---|---|
| Ordinary, request-seeded, Sync-seeded engine passes | Each 1,703/1,703 | `focused/{control,request-seed,sync-seed}.log` |
| Priority1 255 pass | 53/53 | `focused/priority255.log` |
| Clear sync-ok on becoming master | Caught; 4 failed checks | `focused/mutant-0.log` |
| Clear master sync-ok on queued receipt timeout | Caught; 2 failed checks | `focused/mutant-1.log` |
| Omit thisClock from received path | Caught; 31 failed checks | `focused/mutant-2.log` |
| Append announcing source instead of thisClock | Caught; 18 failed checks | `focused/mutant-3.log` |
| Parent GM-change holdover, all eight scaled prescaler phases | 104/104; one-quarter-tick fault fails 35 checks | `holdover/{control,one-tick-fault}.log` |
| Documentation, diagram and PHC-contract checks | Pass | `focused/docs-contract.log` |
| Four regenerated ROM images | All byte-identical | `focused/summary.json` |
| Parent companion applicability at e9cbb676 | Pass | `companion-apply-check.log` |

The holdover probe scales one quarter-second to eight cycles and exercises the unchanged parent module. It confirms immediate uncertainty at the identity edge, retention through at least a quarter-second, and later return to tu=0 with sync health asserted. It is a focused module probe, not an end-to-end physical timing measurement.

The [pinned public packet](https://github.com/kebag-logic/milan-fpga/tree/948261dfc94d7da73dac5cdb80621b4cbaaaf4e2/review-evidence/gptp84-r1) is the author's source validation. [Download audit](public-download-audit.json) binds 197 fetched files to their pinned Git blobs. [Evidence audit](evidence-audit.json) verifies all 194 receipt-index entries, including file sizes and hash prefixes, and 196 downloaded entries against the publication manifest's full hashes. It also checks all 72 source mutants, 24 positive controls and the required named failures.

The parent companion changes exactly the four specified expectations, includes a clause citation for every row, and adds the direct-path tail identity assertion. It applies cleanly to the public parent file. The author's committed adoption snapshot `28e1085fb57ac95ec660f3f6a4449e08657e956c` reports all 11 consumer gates passing: ten return-code rows plus the builder union. The shadow suite passes 310/310; the companion's new identity assertion fails both published omission and wrong-identity mutants. The builder union covers 103 gates exactly once, with verdict digest `8800c441e33bfdedbc0a2b41321ebc75251b43c1a36b0e11362b5df8d0367e84`.

The parent adoption is an author-run local committed snapshot described by public receipts. It is not a manager source bank or a current-dev merge-candidate result. Physical calibration is explicitly NOT RUN in the builder receipt; field skips are not hardware proof.

**Prior findings, checkout integrity and remaining duties**

After the independent verdict and ledger were written, the public PR conversation, submitted reviews and inline review comments were queried. No prior public FINDINGS were present: the conversation contained only the two review-start notices; submitted reviews and inline comments were empty. Therefore no prior finding remains to resolve or retain. The issue's earlier parent-test STOP is resolved by the explicit ruling and the published companion rerun, not by ignoring the four original failures.

The exact-head hosted queries returned zero workflow runs, zero check runs and zero status contexts. No executed hosted job or skipped context is counted as evidence here. The empty combined-status response is not a passing hosted gate. Hosted and local acceptance remain the manager's responsibility.

[Checkout verification](checkout-verification.json) independently hashes all 107 tracked entries, verifies executable modes and the full index against the named tree, and compares module ports/parameters with the base after stripping comments. All match. This donor repository has no nested submodule gitlinks. The published parent environment records the required dependency pins and the head adoption; no other checkout was edited.

The manager still needs to arrange correction and review of F01, obtain the required independent positive reviews, adopt the parent companion with the donor pin, and validate the final current-dev merge candidate with builder and native banks at the merge turn. Those receipts must be linked on the PR when published. Source validation uses base 43acfbcc; the stated live parent dev is e9cbb676. Physical calibration and field acceptance remain outstanding. No source fix, commit, push, GitHub write, merge, author contact or hardware operation was performed.

Reproduction scripts are `run_focused.py SOURCE_ROOT --jobs 16`, `run_holdover.py`, `fetch_evidence.py`, `audit_evidence.py SOURCE_ROOT`, and `verify_checkout.py SOURCE_ROOT`. The focused runner accepts `--simulator`; the holdover runner accepts `REVIEW_SIMULATOR`. Fetch public evidence before auditing it. `MANIFEST.sha256` lists every publishable receipt; `scratch/` is excluded.

R662-1 FINISHED
