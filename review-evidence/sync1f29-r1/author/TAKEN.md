[A723c] TAKEN

Resuming the dev `1f29f189` -> dev-soft-core sync after the [A723] and [A723b] STOPs, under rulings (B) and (C) above.

Branch: `sync-dev-1f29f189-into-dev-soft-core`, at the merge commit `97e9a3d3` over dev-soft-core `5b5f4336`. Local only; the merge commit stays as made.
Authoritative references: the owner branch policy (2026-10-26); rulings (B) and (C) on this issue; `docs/design/MAILBOX_SPLIT.md`; `sw/mailbox/census_ports.py`; `sw/mailbox/mailbox.yaml`.
Interpreted scope: one commit each after the merge. (1) The port census: `src_stream_id_o` in class C; `reboot_req_o` in class G with one exclusion that stops its cone at `reboot_ctrl.reboot_req_i`, named as a placement-switch acceptance item next to the `amr_fsm` exclusion, with its own self-test arm (a planted net past the terminal still fails `g-on-wire`); the counts. (2) The 11 living "2.3" citations of the source entries become 2.4; the dated records of the #799 measurement at dev `97aab1d0` keep 2.3. (3) The split service-budget harness stages its LiteSPI PHY as the SoC does, with the flash-window, refill and XIP arms re-measured and the "same access cost" claim corrected. (4) The `MAILBOX_SPLIT.md` verification figures re-measured on the head. No REBOOT carrier: that is switch-over work.
Validation plan: mailbox generator check and self-tests; publication census check and self-test; ctrl firmware host tests and the mutant campaign; LiteX simulation gates and the builder bank legs (run 0 and run 1); rtl-fast bdd; every docs workflow step; the native suite sweep in 4 shards; `git diff --check` against the merge base.
Blockers: none
