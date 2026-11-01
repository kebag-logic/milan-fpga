# D0 findings: design

Verified against dev `1e80128f`.
Source lines cite dev `1f29f189`.

## D0-001: docs/ARCHITECTURE_HW_SW_SPLIT.md:4

- Statement: Its default is bare-metal control through packet mailboxes.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-001: docs/design/MAAP_FABRIC.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-001: docs/fpga/DATAPLANE_WALKTHROUGH.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-001: docs/fpga/FPGA_DESIGN.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.

## D0-057: docs/fpga/FPGA_DESIGN.md:196

- Statement: presentation-time offset is pinned at the Milan 2 ms
- Contradicted by: Copy of the D0-057 statement on `docs/reference/REGISTER_MAP.md`. `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set
- Correction: Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply.

## D0-001: docs/litex/LITEX_SOC.md:5

- Statement: Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
- Contradicted by: Copy of the D0-001 statement on `README.md`. `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default
- Correction: Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric (`sw/litex/milan_soc.py` lines 2854-2856: `--ctrl-mailbox` is off by default and the default build carries no mailbox; line 4097: `store_true`). `REQUIREMENTS.md` is the normative page, so its copy goes to a maintainer decision on what "Mark II default" names, and every copy takes that one answer.
