# The all-fabric datapath's elaboration, base 70f4056f against the head

`sw/mailbox/placement_identity.py`'s dump of the recipe shape (shape 0), through `pi_try.py` (one shape, the tree's
own census_elab, the pinned sv2v v0.0.12 and Yosys 0.66):

| Tree | Digest | Cells | Nets |
|---|---|---:|---:|
| base 70f4056f | `72214352fc1f3014e23da18a2b22464c561fd86afa099a7436a094e55ff2d750` | 113,558 | 1,339 |
| head (the cut, a4a0c7dc's datapath) | `7f56b4556dd408ea628858dcac2d198e3ab5a793d85792682cc41eb5115521a8` | 113,572 | 1,339 |

The digests differ: the all-fabric datapath's elaboration changes. The canonical forms (`pi_keep.py`, 48 MB each,
kept in scratch) differ only in `made_cells`: 14 more cells, and 1,188 against 1,202 relabelled ones. The function
`amap_edit_out_encode` is now called in a continuous assignment in `g_af_amap_enc` rather than inside the
`amap_edit_validate` process, so the validator reads the named net `amap_edit_out_enc_w` where it read the
function's internal result, and the structural labels downstream of it change. The named cells, nets, ports,
memories and parameters are equal. The logic is the same function of the same nets; the all-fabric suites that
exercise it (milan_dp dynmap, maprec8, maprec4 and dynmap-mutants, the twin's all-fabric half) pass.
`KL_aaf_clock_meter` (every shape) changes too, and the census reads it as a blackbox. So the release netlist
changes, and that is stated: the release image is owed a route.
