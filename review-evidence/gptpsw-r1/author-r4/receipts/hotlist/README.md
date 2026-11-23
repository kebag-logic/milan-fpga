# The hot list relearned at `e81cecdb` with the gPTP ports in the image (#884's ruling of 2026-11-22)

The optimisation line's procedure (`scripts/opt-line-relearn.sh`, `opt-line-order.py`, `opt-line-filter.py`,
`opt-line-apply_hot5.py`, `opt-line-mapbuild.sh`, `opt-line-legs.py`). Copied for this lane with one change each:
- `relearn_gptp.sh` and `legs_gptp.py` build and run the image `--with-gptp` when `GPTP=1`;
- `mapbuild_full.sh` builds every arm at this head, without gPTP and with it;
- `filter_gptp.py` holds an entry of `gptp.c` or `gptp_mbx.c` to the images built with gPTP;
- `apply_gptp.py` records the gPTP image and that scope in the list's header.

- `gptp/`: the 1x1/1if split image, arm A, `--with-gptp`; the three windows (backlog, backlog-adp,
  aecp-largest-notice) traced as recorded. 1,960,622 committed PCs, 288 sections, 0 outside a function's section.
- `std/`: the same at the same head without gPTP, for comparison only. 1,906,685 PCs, 268 sections.
- `mapbuild.log`: 48 full builds (3 points, 8 arms, plain and gPTP), 144 link maps, each image as itself and as the
  SoC plan's stand-in and mapped images. 24 are gPTP images; the stand-in and mapped images of a gPTP build are
  the shape's one-interface image without gPTP, and link no gPTP section.
- `gptp/filter.txt`: 286 kept, 2 dropped, the same two the shipped list dropped (`aecp owe`, `aecp owed_drain`, which
  every arm's 8x8/2if image lacks, with gPTP and without).
- The list applied (`631dc544`): the 266 entries of the shipped list and 20 more, 15 of `gptp.c` and `gptp_mbx.c`, and
  5 that the gPTP image alone runs (`avb` of `aecp_commands`, `aecp_face`, `aecp_mbx` and `ctrl_app_aecp`, and
  `ctrl_mem memcmp`), all in the order the windows first ran them.
- The standard relearn's 266 kept entries are the shipped list's set in another order, from the first entry (126 at
  the same position). So a
  relearn at this head reorders the images without gPTP too, with or without the ports in it.

The traces are in LARGE.txt by size and sha256; the list's header names the gPTP traces' sha256.
