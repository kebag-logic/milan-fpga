# milan-fpga #983 receipts

Head `677d605f37c3a80654df1dd2cde053b57242845b`, base `854bd7236792ce1adbd10c43b13a6a5002ad3bb6`, branch `pf-linuxprof-1` (local, not pushed).

| Receipt | What it shows |
|---|---|
| [identity-gate.txt](identity-gate.txt) | 170/170 FPGA artifacts byte-identical base -> head; tracked tree clean after the builds |
| [identity-base-854bd723.json](identity-base-854bd723.json), [identity-head-677d605f.json](identity-head-677d605f.json) | the per-artifact sha256 manifests compared |
| [identity_gate.py](identity_gate.py) | the lane-local capture script (not committed to the repository) |
| [builder-union.json](builder-union.json) | 115-gate inventory; 114 ran once and passed; `test_baremetal_profile_contract` not executed to completion; 1 NOT RUN row |
| [sub-0.json](sub-0.json) to [sub-3.json](sub-3.json), [sub-0.log](sub-0.log) to [sub-3.log](sub-3.log) | the four `test_builder.py --require-rv32 --gates` subset receipts and logs |
| [builder-leg-0.log](builder-leg-0.log) | gate 1b's output up to the 590 s bound: its builder arms PASS |
| [docs-gates.log](docs-gates.log) | 24 docs and quality gates, each rc=0 |
| [ctrl_loop-token-identity.txt](ctrl_loop-token-identity.txt) | `ctrl_loop.h` expansion identical at base and head for every tracked shape |
| [fw-arms-shapes.log](fw-arms-shapes.log), [fw-arms-aecp.log](fw-arms-aecp.log), [fw-arms-plat.log](fw-arms-plat.log) | the firmware gate's own arms, run by [fw_arms.py](fw_arms.py): 21, 18 and 8 PASS |
| [comment-milan-fpga-983.md](comment-milan-fpga-983.md) | the posted [A830] REVIEW READY on #983: https://github.com/kebag-logic/milan-fpga/issues/983#issuecomment-7099191077 |

Not run: gate 1b to completion; `ci_builder_legs.py`'s leg union; firmware gate shards 0 to 3 as shards; the mutation campaigns. Each needs more than the ten-minute command bound of this session.
