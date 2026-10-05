[R488] round R488-2, exact head 9050c4bbd25556929a0f24fb98258bc98e3bcfbe: own verdict and ledger, written
BEFORE the prior public review findings on PR #160 were read.

Own verdict: NEGATIVE (one open MINOR).

Own finding:
- R488-2-F1 MINOR (Tests, Docs): tb/srp_top/README.md:539-541 says "Neither arm fails any
  other check of the suite" for lv-second-lv-ends and lv-never-ends. At the head the complete
  default srp_top suite (8656 checks) includes lvcoll, and lv-never-ends fails 3016 SC2 checks
  in it beside its 16 S2/S3 failures (receipts/fault-lv-never-ends-full.log). lv-second-lv-ends
  fails only its 16 S1/S2 checks (receipts/patch-lv-second-lv-ends-full.log).

Own ledger:
| lens | state | examined |
|---|---|---|
| Conformance | CLEAN | RTL branch order against 802.1Q-2014 Table 10-4 (LV / leavetimer!, then each received event), Δ13, F08.1 T-MRP-LEAVE vs Milan Table 4.3 |
| RTL | CLEAN | KL_srp_talker_fsm.sv:720-744, KL_srp_listener_fsm.sv:747-784 and ind_unreg_w 449-454, timer service cancel-after-fire, lint, focused Yosys |
| Robustness | CLEAN | same-clock JoinIn integration probe 6432/6432, stale-expiry guard after cancel, per-plane restore faults |
| Tests | UNCLEAN | F1 |
| Docs | UNCLEAN | F1 |
