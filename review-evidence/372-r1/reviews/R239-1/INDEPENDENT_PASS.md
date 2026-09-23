[R239] independent pass, written BEFORE reading any prior review finding - exact head 059c3a60b8290873ed9fd14673f9981e8af754ce

Independent verdict before prior-finding disposition: POSITIVE (no open BLOCKER, MAJOR or MINOR from this pass).

Candidate SUGGESTIONs from this pass (non-blocking):
- S1 Tests: campaign pins one defect per property; a bit-0-only TDATA stability weakening and an ai_payload
  weakening that drops the TDATA compare both survive every campaign row (probe weaken/v2_tdata_stable_bit0_only,
  weaken/payload_no_tdata). The unweakened properties do catch TDATA/TLAST defects (probe dut/*).
- S2 Tests, Robustness, Docs: the product mux instance inside ptp_ts_top is unbound (documented limit); a probe
  shows the unchanged bind reaches TOP.ptp_ts_top.axis_tx_rx_ts_switch_rr.u_sva with 21/21 pairs non-vacuous and
  no failure over the 92 original checks. Reuse needs an axis_sva_witness DPI definition (link-time, not silent).
- S3 Docs: the guide's reset/first-edge facts cite a commit on the unprotected, never-merging 372-review-evidence
  branch; the "measured on 5.050" framing also carries the upstream-changelog "before 5.038" clause.
- S4 Robustness: sva_campaign.py run directly grades clean/stimulus/unused-path rows on whatever
  obj_dir_mux_sva_w{8,64} binaries exist; `make` always rebuilds them first, so the suite gate is unaffected.

Ledger (independent pass):
| lens | state | covering round | exact head |
|---|---|---|---|
| Conformance | CLEAN | R239-1 | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| RTL | CLEAN | R239-1 | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Robustness | CLEAN | R239-1 | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Tests | CLEAN | R239-1 | 059c3a60b8290873ed9fd14673f9981e8af754ce |
| Docs | CLEAN | R239-1 | 059c3a60b8290873ed9fd14673f9981e8af754ce |

Prior public findings (F1/F2/F3 and any others) are read only after this file was written.
