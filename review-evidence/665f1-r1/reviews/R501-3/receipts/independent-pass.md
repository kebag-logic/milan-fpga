[R501] NEGATIVE - exact head 9412006bd58c002835bb06d46045c53098cc59a5

Independent pass recorded before reading prior review findings. Public-finding reconciliation and final packet verification are pending.

R501-3-F1, MAJOR; Conformance, RTL, Robustness, Tests, Docs.
Artifact: sw/firmware/ctrl_nvm/nvm_store.c:203; test/nvm_checks_write.py:516; README.md:391; PR #669 stated readings.

The refusal confirmation compares verdict codes, not the bytes read. Two different corruptions of a valid slot produce the same refusal and permit a generation restart. The disposable flash model returned two different bytes (XOR 8, then XOR 16); production store, codec and port bytes were unchanged. Across both slots, four sequence boundaries, header/body faults and two shapes, all 32 cases lost previously saved values after a successful commit and a clean reboot. This exceeds the documented limitation of identical corruption repeated on every read.

Authority: #665 decision 2, comment 5997929153; the round-3 stated reading that disagreeing reads are media faults, comment 5998087724; FASTCONNECT sections 6.2 and 7.
Required outcome: confirm refusal with evidence that the relevant returned bytes agree, or keep authority unknown; never use unvalidated sequence metadata. Add differing-corruption regression cases and a control that removes the agreement check.
Verification: scripts/probe_read_agreement.py; receipts/read-agreement/*.results.json and *.runs.jsonl. Probe rc 1 is a demonstrated contract failure.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | nvm_store.c:191, FASTCONNECT sections 6.2/7, #665 decisions | R501-3, F1 open | 9412006bd58c002835bb06d46045c53098cc59a5 |
| RTL | UNCLEAN | nvm_store.c boot/write FSM, nvm_klj2.c, plat/nvm_flash_litespi.c, state/flash interfaces | R501-3, F1 open | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Robustness | UNCLEAN | receipts/read-agreement; boundary, read-fault and power-cut checks | R501-3, F1 open | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Tests | UNCLEAN | test/nvm_checks.py, nvm_checks_write.py, nvm_mutants.py; five shapes and 80 controls | R501-3, F1 open | 9412006bd58c002835bb06d46045c53098cc59a5 |
| Docs | UNCLEAN | README.md Boot/limits, nvm_state.h, FASTCONNECT tie edit, PR #669 | R501-3, F1 open | 9412006bd58c002835bb06d46045c53098cc59a5 |

The checked-in 40 checks passed for each of five shapes; all 80 controls were caught. Permanent signalled read failures reached HELD with six failed reads, one AECP release, dirty status, 100,000 completed service calls and no erase/program. Healing without reset retained HELD. CPU/board calibration was not executed; generated-header integration and physical power cuts remain outside this review.

R501-3 FINISHED
