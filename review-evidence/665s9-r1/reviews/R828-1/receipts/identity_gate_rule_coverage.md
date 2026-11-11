# Identity gate: rule against planted control (static, head a91fb27d)

Source: `sw/litex/check_image_identity.py` (rules) and `sw/builder/test_builder.py:23618-23705`
(gate 23p's twelve plants), read at a91fb27dd39483e4694e193504da1dbe06208807. No LiteX
interpreter that imports migen + litex + litex_boards was available to this round, so gate 23p
was not re-executed; the author's receipt is `r3/gates/test-builder.log` in the evidence archive.

| Gate rule (`check_image_identity.py`) | Line | Plant that fires it (gate 23p) |
|---|---|---|
| manifest fields are exactly the schema's seven | 168-170 | none |
| schema 1 and placement `split` | 172-174 | "the manifest's placement renamed" |
| **manifest ident equals the image's csr.csv `config_identifier`** | **175-176** | **none** |
| manifest VERSION equals the image's milan_csr.sv | 177-179 | "the manifest records another VERSION" |
| manifest mailbox (major, minor) equals KL_mbx_pkg.sv | 180-183 | "the manifest records another mailbox minor" |
| firmware sha256 equals the manifest's | 195-197 | "the firmware relinked after the build" |
| rom banks hold the ELF's rom words | 203-205 | "the manifest forged to the relinked firmware" |
| ident's last word names the placement | 238-240 | "the split ident names no placement"; "the manifest removed" also fires placement |
| bitstream bound / unbound / other | 208-229 | "a bitstream the manifest does not bind"; "a bitstream other than the one the manifest binds" |
| split image: CTRL_SPLIT_P = 1 and a mailbox | 242-244 | "the split datapath built without CTRL_SPLIT_P"; "the manifest removed" (all-fabric branch) |
| all-fabric image: no mailbox, no split datapath | 245-247 | "an all-fabric image with the mailbox"; "the manifest removed" |
| split image: no DDR3 | 248-249 | "a split image with DDR3 left in" |

Why the ident-equality rule has no control: the "split ident names no placement" plant edits
`soc_ident`, whose single result `soc._ident` is both the SoC ident (csr.csv) and the manifest's
`ident` (`milan_soc.py:3014`), so the two still agree and only the last-word rule fires. No file
plant edits the manifest's `ident`. Deleting lines 175-176 therefore leaves every arm of gate 23p
and every other test in the tree green (no other test imports or runs the gate:
`grep -rn check_image_identity --include=*.py` finds only milan_soc.py and test_builder.py).
