### Fresh shipping 1x1 OOC, main versus final

Both measurements use the same 50 MHz clock, shipping parameters, images and
two-thread recipe. All synthesis, resource, path and cone commands complete
rc 0. The resource comparison uses the freshly measured new-main reference;
all policy limits are unchanged.

| Measurement | Main `c9f74b68` | Final `c4539ff1` |
|---|---:|---:|
| WNS (ns) | -3.562 | 3.337 |
| TNS (ns) | -37.519 | 0.0 |
| Failing setup endpoints | 16 | 0 |
| WHS (ns) | 0.159 | 0.159 |
| Failing hold endpoints | 0 | 0 |
| Arbiter startpoints queried | 1631 | 328 |
| Arbiter endpoint pins queried | 561 | 561 |
| Arbiter pairs reported | 263154 | 17990 |
| Pairs above 20 logic levels | 146535 | 0 |
| Maximum logic levels | 51 | 16 |
| Worst arbiter slack (ns) | -3.562 | 11.912 |
| Pairs with no slack annotation | 12219 | 187 |

Pairs without a slack annotation are included in the level census.
The survey asks for every startpoint against all non-clock input pins of the
arbiter sequential cells, one worst path per endpoint, with a path limit above
the endpoint count. Raw pair tables remain in scratch; the artifact manifests
record their byte sizes and hashes.

| Area scope | Main LUT | Final LUT | Delta | Main FF | Final FF | Delta |
|---|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 23179 | 23160 | -19 | 19779 | 19787 | +8 |
| `u_pp` | 22517 | 22478 | -39 | 18941 | 18951 | +10 |
| `(u_pp)` | 939 | 780 | -159 | 2033 | 2039 | +6 |
| `u_tx_arbiter` | 185 | 234 | +49 | 187 | 187 | +0 |
| `u_originator` | 697 | 676 | -21 | 885 | 885 | +0 |
| `u_notify` | 2125 | 2157 | +32 | 1256 | 1258 | +2 |

Own logic (top's own scope plus arbiter): -110 LUT, +6 FF; within the 60 LUT / 120 FF STOP limits.

| Rank | Before: source -> endpoint; levels; slack (ns) | After: source -> endpoint; levels; slack (ns) |
|---|---|---|
| 1 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[0]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[0]/D`; 16; +11.912 |
| 2 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[1]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[1]/D`; 16; +11.912 |
| 3 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[2]/D`; 47; -3.562 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/slot_r_reg[2]/D`; 16; +11.912 |
| 4 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[0]/D`; 46; -3.417 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[1]/D`; 15; +12.057 |
| 5 | `u_pp/u_notify/pend_r_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[1]/D`; 45; -2.930 | `u_pp/u_ca_builder/cancel_release_slot_o_reg[2]/C` -> `u_pp/u_tx_arbiter/owner_r_reg[0]/D`; 14; +12.296 |

Source-group census (maximum level and minimum slack may be different pairs):

| Source group | Main pairs; max levels; minimum slack (ns) | Final pairs; max levels; minimum slack (ns) |
|---|---|---|
| notification wr_ix_r | 752; 51; -2.981 | no direct combinational path |
| RX header fields | 40044; 50; -1.795 | no direct combinational path |
| registered withdraw mask | no direct combinational path | 1504; 12; +13.512 |
