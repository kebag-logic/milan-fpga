Run these scripts from the published packet, supplying a pristine checkout of the exact reviewed head as REPO. All generated trees stay under packet scratch/.

Dependencies: Python 3.10+, Git, GCC/G++, Clang, CMake, GoogleTest/GMock, cppcheck, clang-tidy, an RV32 cross compiler and QEMU. The unchanged R556-4 probe expects riscv64-elf-gcc and riscv64-elf-objdump on PATH. No global installation is performed by the scripts.

```sh
python3 scripts/prepare_lexer.py
python3 scripts/run_review.py "$REPO"
python3 scripts/independent_probes.py "$REPO"
python3 scripts/preservation_and_probe.py "$REPO"
python3 scripts/replay_prior.py "$REPO"
python3 scripts/verify_checkout.py "$REPO"
```

The prepared lexer is Clang 18.1.3, extracted from the hash-pinned packages in receipts/clang18-download.json. The local full runner uses jobs=3 and RV32 jobs=2 concurrently to keep the combined maximum at 16. Reuse a fresh packet scratch directory for replay_prior.py; the earlier script deliberately refuses an existing work directory.

Expected results: native/RV32 gates pass; the macro-hash assembly prose control compiles and passes both gates (F1); the default-nearness fragment passes the audit while the default-only runtime match remains false (F2). The old full_comment_bypass.py exits 1 because its bypass is now false. Other required prior probes report zero gaps or zero accepted fragments.

scripts/audit_results.py regrades local and downloaded hosted receipts after execution. For the published reused campaign, receipts/mutation-xml, mutation-reused-results.json and message-markers-reused.json retain the per-binary evidence. Fresh and hosted compact summaries omit two earlier-arm messages, as explained in REPORT.md.

The report and manifest are the publication boundary. Scratch and unlisted files are not published.
