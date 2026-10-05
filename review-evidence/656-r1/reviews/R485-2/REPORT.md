[R485] POSITIVE - exact head d0e29f6dda6f04f3ace1dbb395f57379e58cacaf

R485-2 external independent review of issue #656 / PR #662.

The body correction resolves R485-1 F2 = R484-1 M1. No BLOCKER, MAJOR or MINOR remains open. All five lenses are CLEAN. This verdict covers the source head and corrected body; remaining merge and release obligations are listed below.

The public and local head remain `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf`, tree `289f09d8c7151617ffb019f49b5c972924e4fedd`. Source base: `c0280fc008ef9c5c1650402a58bab3e47a92127b`. Observed live dev: `e617275074e370cec342af99b929e2588fc8d43f`.

The contract, documentation map, frozen issue scope and authorities were read before the diff and history. The independent diff pass preceded reading prior public findings. No private author material was read. The four non-Docs lenses retain R485-1 coverage at the identical head, with their unchanged scope verified here. Docs is applied anew. The physical leg was not rerun.

## Delta verification

`receipts/body.diff` contains one hunk wholly inside the Known limitations bullet "INTERNAL against an asynchronous talker". All prefix and suffix bytes, including the final newline, match the original public author file. That file is `review-evidence/656-r1/author/PR-BODY.md` at evidence commit `e5cae5f54a7efc54eb1b22095e310bb8324ace4e`. Its published manifest records identical original/published hashes and no redaction, proving the comparison without reading its private location.

- Original body SHA-256: `19d959618430f119f1313173309c578fee09efddd68597c808200014201b5c4d`.
- Live body SHA-256: `2ab688eaaf2e8d06d22dfa90503fa1a337932d31e3254b1a8e4957fc29cf38a3`.
- `48000 * 10 / 1000000 = 0.48` events/s per fed pair.
- `48000 * 10.64 / 1000000 = 0.51072`, correctly rounded to `0.51` events/s per fed pair.
- The exact plan gives `47999.489314896` Hz, `10.639272994` ppm below nominal, `0.510685104` excess events/s per fed pair and a `1.958153846` s slip period.

The pre-A2-a TDM-junction clause now explicitly names this leg's old axis-paced talker. That talker matched the old nominal packet grid. The next clause correctly preserves loopback slipping against another clock before A2-a. The #396 qualification still requires the two media clocks to follow one another.

Authority: `hdl/ieee1722/aaf/KL_chan_map_capture.sv:173` and `:211` define the elastic queue and counted repeat/drop behavior; `docs/reference/REGISTER_MAP.md:1867` defines the per-pair counter unit and `:2003` identifies upstream clock mismatch. `hdl/milan/milan_datapath.sv:5905` engages INTERNAL alignment. `docs/design/MEDIA_CLOCK_FOLLOWING.md:1133` records A2-a and `:1504` limits its accuracy claim. The arithmetic makes no physical-calibration claim.

## Findings and dispositions

### F2 / M1 - MINOR, RESOLVED - Docs

- Artifact: PR #662 body, corrected bullet at `receipts/PR-BODY.live.md:190`; [manager correction 5986948467](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986948467).
- Authority/evidence: queue/counter contracts above; `receipts/delta-audit.txt` and `receipts/body.diff`.
- Former impact: an overstated coefficient and an overgeneralized pre-A2-a claim.
- Required outcome: 0.48 events/s per fed pair per 10 ppm, 0.51/s at 10.64 ppm, and a TDM clause limited to the old axis-paced talker.
- Verification: all three corrections are present; all other body bytes are unchanged. F2 is resolved at this head and the live-body hash above.
- The frozen issue REVIEW READY comment retains the old coefficient. The manager explicitly superseded it in correction 5986948467; it is not outstanding conflicting guidance.

### F1 / S1 - SUGGESTION, retained and not taken - Tests, Robustness

- Artifact: `tb/verilator/milan_dp_gptp/verify_abort.py:76`; PR body "The exact 160-PDU pin"; [R485-1](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986909374).
- Authority/evidence: R485-1 measured 160 RX completions in each deterministic 20 ms control window, with a 299-313 cycle margin from the exceptional phase band. Approximately 0.17% of arbitrary start phases would contain 159 at the new cadence.
- Impact: no failure at this head; a future phase change could cause a false failure, never a false pass. The body discloses it.
- Optional outcome: accept 159-160 or derive the RX expectation from cadence, retaining exact zero TX and samples.
- Verification if adopted: preserve accounting controls and test a shifted window phase. The manager declined this optional change. No lens remains unclean.

### RES-1 / R2 - RESIDUE, retained - Docs

- Artifact: pre-existing text at `tb/verilator/milan_dp/README.md:287`, `:297`, and `tb/verilator/milan_dp_gptp/README.md:7`, `:9`.
- Authority/evidence: R485-1's head run and the public driver give 139 physical plus 40 accounting checks, 179 total. This lane neither introduced nor relies on the old descriptive counts.
- Impact: stale prose, with no change to measurements, executed tests, code or verdict. Retained under the explicit residue disposition, not downgraded from a new numeric defect.
- Required outcome: carry the exact fixes to #495 at merge. At `milan_dp/README.md:297`: "The physical harness contributes 139 checks." At `milan_dp_gptp/README.md:7`: "The normal total is 179 checks: 139 physical, 40 accounting." At `:9`: "Extended mode runs the physical harness alone, with 139 checks." Confirm the extended count when that mode is next run. The optional duration correction at `milan_dp/README.md:287` is "16.992510280 simulated seconds over 849625514 cycles"; the dated historical measurement at `:359` stays unchanged.
- Verification: compare the prose correction with the corresponding execution receipt. The residue is not marked fixed by moving its paperwork.

After this round's own verdict and ledger were written, the [other prior public review](https://github.com/kebag-logic/milan-fpga/pull/662#issuecomment-5986945006) was read. Its M1 is resolved as F2 above; S1 is retained as the optional F1; R2 is retained as RES-1, including its optional duration correction. These account for every prior public finding on the PR. Formal reviews and inline review-comment lists were empty. No additional open finding was discovered.

## Reviewer-owned coverage ledger

Each row is an artifact-specific PASS. Unchanged source coverage retains its actual covering round; Docs is covered against the corrected body hash above.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #656 acceptance and scope comment 5985174558; R485-1 bisect/mechanism and controls; `KL_chan_map_capture.sv:173`; unchanged lane diff. Local acceptance 3 has evidence; its hosted half remains pending. | R485-1; unchanged scope confirmed R485-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| RTL | CLEAN | No RTL in the diff; `hdl/milan/milan_datapath.sv:5905`, `:5932`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:173`; R485-1 grid/NCO/queue analysis; exact tree and gitlinks. | R485-1; unchanged scope confirmed R485-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Robustness | CLEAN | `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:483` preserves deferred cadence, `:743` reset re-arm, `:839` windows; R485-1 loss/recovery/stall/reset and pin probe. F1 remains optional. | R485-1; unchanged scope confirmed R485-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Tests | CLEAN | R485-1 head/C1/C2 runs; public head/control log excerpts and hashes; `receipts/lane.diff` leaves check code, deadlines and counts unchanged. F1 remains optional. | R485-1; unchanged scope confirmed R485-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |
| Docs | CLEAN | PR body lines 190-196; body diff and arithmetic receipt; `tb/verilator/milan_dp/README.md:173`, `:200`; `docs/reference/REGISTER_MAP.md:1867`, `:2003`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:1133`, `:1504`. F2 resolved; RES-1 retained. | R485-2 | d0e29f6dda6f04f3ace1dbb395f57379e58cacaf |

## Evidence and real limits

R485-1 independently ran head 139/0 plus 6/0, 20/0 and 14/0; C1 139/5 with 8 cumulative ordering errors; C2 139/3 with 5 cumulative ordering errors. This round re-read the unchanged public execution excerpts and verified their published hashes. These are earlier executions, not new runs.

All seven required hosted contexts report success at the exact head; the native shards also report success. The "Physical gPTP (nightly and manual)" job is SKIPPED and supplies no execution evidence for acceptance 3. `receipts/hosted-checks.json` records job status, conclusion, head and URL. Hosted and local-replica acceptance remain manager-owned.

The assignment reports that the manager's full source static/builder and native banks passed at this head. That source validation is distinct from the final current-dev candidate. This round did not rerun those banks or build that candidate. The PR's recorded base `506d91dbeeba585d72d2e80d92fca799c719f8ee` is not the live validation base.

Physical calibration: NOT RUN. Field skips are not hardware proof. No hardware, physical-leg rerun, full-bank builds, new mutations, source fixes, commits, pushes, hosted writes or merge occurred. All commands completed in the foreground. The `external` gitlink remains uninitialized and is unused by this leg.

`receipts/clone-integrity.txt` proves the tracked blob bytes and executable/symlink modes against the exact committed tree, stage-zero index equality, zero hidden index flags and untracked files, and all three required submodule gitlinks and tracked contents. No restoration was needed.

## Pending manager duties

1. Publish the report and manifest-listed receipts; reconcile the internal delta verdict and ensure no review remains in flight.
2. Retain F1/S1 as optional and not taken; carry RES-1/R2, including the duration correction, to #495 at merge.
3. Obtain executed hosted Physical gPTP evidence for acceptance 3. Keep "Relates to #656" until it is satisfied, then update acceptance evidence and closure wording.
4. Complete manager-owned hosted/local-replica acceptance and build/gate the final candidate from the reviewed head and current live dev. Source passes alone do not establish the candidate result.
5. Obtain explicit merge authorization and complete post-merge containment before issue closure and Done.

`MANIFEST.sha256` lists publishable receipts and scripts using packet-relative paths; scratch is excluded. Reproduce the focused checks with `python3 scripts/audit_delta.py` and, from the exact-head checkout, `python3 <packet>/scripts/verify_clone.py`.

R485-2 FINISHED
