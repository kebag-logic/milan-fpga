[A692b] REVIEW READY
Commit: ca39dc1b0bd917e3e033df9d9db762514318377a (branch `799-adopt-processor-f65c8ff7`, 20 commits on dev `97aab1d0`, not pushed)

Changed, on [A692]'s `f67a4ca1`, per the ruling on its STOP (issuecomment-6460917634):
- (1) Mailbox contract 2.3 (`3b42bcf2`): a source entry per talker stream in the publication block, `SRC_SID_LO`/`SRC_SID_HI` at `0x80 + 8*s` (the hole below the sink entries, so a minor version), generated from `sw/mailbox/mailbox.yaml` by `gen_mailbox.py`, with `KL_mbx`'s `pub_src_sid_o`; host model, bench (P0 to P5 cover the sources; two new checks) and 4 new RTL arms on both adapters plus 2 model twins. The owner writes both words while the source's `DA_GATE` bit is clear (Milan v1.2 5.5.4.1). The split firmware's writer is #665's, recorded as "none yet" in `docs/design/MAILBOX_SPLIT.md`.
- (1) `8b76de69`: both stamps read `src_stream_id_o` through one per-source net, `tx_sid_w`, so the census sees one read in every shape, mapped to `SRC_SID_LO.SID`; `src_stream_id_o` in `CLASS_D_PORTS`; the GET_STREAM_INFO output read is a `processor` row. The synthesized logic is unchanged.
- (2) The twelfth resource record (`1efe31e2`, `ca39dc1b`), written by `pp_resource_gate.py record --write` under the owner decision: route-1x1 52,012 LUT / 53,707 FF / 15,780 slices (+753 / +499 / -55 against the eleventh), WNS +0.440 ns, WHS +0.036 ns; ooc-1x1 24,346 / 20,404; ooc-8x8 34,156 / 29,782. Every figure equals the `05b26476` measurement, so contract 2.3 and the census change moved none.
- (3) #800 opened for the 8x8 and 4x4 MAAP source-index width.

Validation (clean clones; each rc the command's own):
- `python3 sw/mailbox/publication_census.py --check --selftest`: RESULT: PASS, 6 shapes, 246 checks, 0 failures; selftest 0 of 120 arms failed, 0 of 31 rules unproven (`ca39dc1b`).
- Full sweep, 4 shard units: 64 / 64 suites, 2,191,647 checks, 0 failures, 0 timed out; `suite_tally.py` rc 0 (`41a78877`, RTL-final; later commits are docs, the record and two string-literal splits).
- milan_dp: 18 legs PASS (notify 499 with G11; sidmove 50, sidmove8 52); pp_shadow 651 / 691 / 651 / 317, 0 failures.
- milan_dp_gptp physical: PASS, 209 checks, 0 failures (`ca39dc1b`, `SUITE_TIMEOUT=14400`).
- `make -C tb/verilator/milan_dp gsi-mutants`: rc 0, 15 / 15 (clean 499 / 499, 14 / 14 arms by name).
- `tb/verilator/mbx`: `make`, `make run-if2` rc 0 (404 / 449 / 32, 406 / 451 / 391, 0 failures); `make mutants` 183 / 183 caught.
- `gen_mailbox.py --check --crosscheck` 0 findings; `--selftest` 0 arms failed.
- rtl-fast replica, all 12 `needs:` jobs: 12 / 12 jobs success (the six firmware jobs re-run with a freshly installed, verified RV32 SDK after the first run's relocated SDK copy failed the installer's provenance check); behave 14 features, 406 scenarios, 1,979 steps passed; lint PASS 89 <= 89.
- Firmware gate set: 8 / 8 rc 0 (523 / 523 ctrl mutants caught).
- Yosys `syn/yosys/run.sh`: 60 / 60 tops; tied-input and tap-purity PASS.
- Static and pin records, 22 commands (resource baseline check, ROM digests with no diff, diagrams, submodule and gPTP docs, port contracts, measures, integrator params, lint, xvlog, both idiom gates, source lists, `pp_srcs`, `test_builder.py`): 22 / 22 rc 0.
- Docs gates: 44 steps, 0 failed (2 skipped by rule); LiteX builder leg, markdown on CPython 3.12.3 and the no-git step rc 0.
- Resource gate: against the new record `check-baseline` PASS and `check` 0 at route-1x1, ooc-1x1 and ooc-8x8; route complete, 0 routing errors.

Acceptance criteria: all consumer gates rc 0 (above). #790's four cases, the planted pass-through and the restated ledger are in. Not met in this lane: the in-house qualification re-runs on the built image, with the gPTP adoption (they need the image and a bench), so the PR body says "Relates to #799, #790".

Open risks/questions: the split firmware has no `SRC_SID_*` writer yet (#665); #800 stays open (the shipping 1x1 is unaffected); the `--ctrl-mailbox` SoC's area with contract 2.3 (1,024 more bits per interface) was not measured.
