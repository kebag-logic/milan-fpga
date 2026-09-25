[A293]

Closes #55
Closes #56
Closes #77
Relates to kebag-logic/milan-fpga#510

## Round 2

Re-measured the merged baseline and both mutations; the README scopes its
historical counts to `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`, before M4L.
The waiver now quotes the full recommendation note and adds a trigger for a
targeted Milan revision that makes support mandatory. Section 11 uses the registered microcode constant. M4L adds response
checks for both waived SETs under another controller's lock.

## Change and validation

The October profile deliberately leaves the recommended SYSTEM_UNIQUE_ID and
MEDIA_CLOCK_REFERENCE_INFO command pairs unsupported. Record the
[owner decision](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089)
in section 6.9, F06.14, GAP-03 and REQ-MVU-003/004. Milan v1.2 sections
5.4.4.2–5.4.4.5 (printed pp. 58–61) and 7.6 (printed p. 115) introduce support as a recommendation. Implementation
returns at P4 if the conformance lab requires it or a targeted Milan revision
makes it mandatory.

F01.5 marks both phantom enable names reserved with no RTL consumer. Related
interface and storage descriptions are marked deferred. GET_MILAN_INFO remains
implemented; features_flags is zero and Table 5.20 has no flag for either pair.

M4 sends complete commands 0x0001–0x0004 and reserved type 0x0005. It verifies
the response type, NOT_IMPLEMENTED status, length and exact echo, including
nonzero SET data. The four cdl values are 28/20/92/20.
M4L also grades byte-exact lock/unlock, both refusals under a foreign lock,
and absence of extra AECP responses during each 20 ms observation. No RTL changes.

Processor head: `490e4309749c83f92d794a8ff10d3043e0f5f080` on `510-mvu-waiver`,
from `265d6762a58d9d9e545624d6d3f1a34e7006d171`, including the manager's
merge of main at `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`.
All round-2 counts below were measured on the content of this processor head;
they are snapshots and must be re-measured after a later change.

Mutation evidence: changing only generated ROM word 560 from NOT_IMPLEMENTED
to SUCCESS is rejected with exit 1: 199 failures out of 7,646 default-build
checks. Every waived command fails both its M4 status and byte-exact response
check; lengths remain correct. Both M4L refusal checks also fail. Changing
features_flags from 0 to 3 is rejected with exit 1 and 3 failures out of 7,646
(M1, M2, M5b). Disposable copies leave the original ROM unchanged. The normal
top-level suite passes 7,666 checks: 7,646 default plus 20 fixture.

All required local validation returned **0**:

- `make check`: 41 diagram blocks, 18 waveform blocks, 872 links, 115 requirement rows, 92 module/test rows and zero untested modules.
- Every `.github/workflows/hdl.yml` gate: links, compliance matrix, waveform freshness, `make stale`, lint, the full suite bank, generated matrix, historical NVM figures and portability including memory-mapping assertions.
- Full suite bank: **33 suites, 1,014,637 checks, zero failing suites**.
- Parent consumer at local commit `d1d1fbba98563524a46cc825e4cf9936603ef1bb`, based on `35f0695815c202392b6b4806bb9f59dd110687ed`, with only the processor gitlink changed: all requested checks pass; integration suite **371 checks, 0 failures**.

Parent commands:

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

Existing parent ratchet findings remain within their recorded budgets; no
budget was changed. The parent validation commit remains local; no parent
branch was pushed.

REQ-MVU-005 timing remains tracked by #57. This waiver claims no successful
command behavior, state storage, persistence or notifications for either pair.
