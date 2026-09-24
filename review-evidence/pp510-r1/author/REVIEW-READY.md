[A290] REVIEW READY

Head: `05fd9e1b2390e7cb0c704c07cd3d9ec47ecd0a19` on local branch `510-mvu-waiver`, from `265d6762a58d9d9e545624d6d3f1a34e7006d171`.

Assignment items 1–4 complete:
- Record the October waiver in section 6.9, F06.14, REQ-MVU-003/004 and GAP-03, citing the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089). Independently checked Milan v1.2 sections 5.4.4.2–5.4.4.5 (printed pp. 58–61) and 7.6 (printed p. 115): support is a recommendation. P4 revisit if the conformance lab requires it.
- F01.5 marks P-EN-MVU-SUID and P-EN-MVU-MCR reserved, with no RTL consumer. Related interface, hazard and storage descriptions are marked deferred.
- M4 pins VENDOR_UNIQUE_RESPONSE / NOT_IMPLEMENTED for complete command types 0x0001–0x0004, with exact echo and cdl 28/20/92/20, plus reserved type 0x0005. M1/M2 pin features_flags to zero; Table 5.20 has no support bit for either pair.
- No RTL or microcode source changes.

Mutation evidence: changing generated ROM word 560 to SET_STATUS SUCCESS is rejected with exit 1. Every 0x0001–0x0005 response fails both its status and byte-exact check while all length checks pass. A features_flags=3 mutant is also rejected, by M1/M2/M5b. Original ROM restored before the full bank; reproduction and counts are in tb/pp_top/README.md.

All repository gates returned 0: every gate in `.github/workflows/hdl.yml`, `make check`, lint, full suite bank, historical NVM figures and portability. Full bank: **33 suites, 1,008,937 checks, zero failing**; pp_top: **1,966 PASS, 0 FAIL**.

Parent consumer local commit: `65bc81ed7cd1ffc9c24226a5d81850e10f5cc241`, based on `35f0695815c202392b6b4806bb9f59dd110687ed`. Only the processor gitlink changed, to the head above. Every requested command returned 0:

```text
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
make -C tb/verilator/pp_shadow -j8
```

Parent integration: **371 checks, 0 failures**. Existing ratchet findings remain within their recorded budgets; no budgets changed. REQ-MVU-005 timing remains in #57.

HANDOFF.md and PR-BODY.md are complete in the requested output directory. Both commits are local; nothing pushed, no PR created or edited, no merge or hardware work.
