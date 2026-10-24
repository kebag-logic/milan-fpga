# Superseded receipts (round 1b)

Evidence taken at heads before the final one, kept as the record of what each showed.

- `derived_constants_8a599554_041b7922/`: the derived constants first with the transmit-arbiter term (`8a599554`;
  1x1 late 27,811 ns, 8x8 26,715 ns, CRF 25,564 and 9,908 ns, the same periods), then without it at `041b7922`
  (the shipping shapes' files were overwritten by that run; the two test shapes are `041b7922`'s).
- `precommit_8a599554/`: the capture_coherence dp leg (847 checks, 0 failures) and the arm subset (9/9) on the tree
  committed as `da079f3d`, and milan_dp nxn / nxn8 excerpts on the tree committed as `8a599554`.
- `head_041b7922/`: the arm subset (9/9), lint (89 <= 89) and Yosys (60/60) at `041b7922`.
- `head_9f9161d3/`: milan_dp nxn (4x4) and nxn8 excerpts with the 125 us step, on the tree committed as `9f9161d3`.

Every gate was run again at the final head `bf2d96f9`: see `../final/`.
