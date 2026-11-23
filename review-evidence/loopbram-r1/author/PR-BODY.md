Target: `pf-loopbram-1` into `dev-soft-core`. Closes #979.

**Depends on #975** (input port clusters), which rides in the post-flip composition: until that merges into `dev-soft-core`, this PR's diff also shows #975's commits.

Adds optional loopback controlled by the input map. At 8x8, 63 independent mono loopback destinations share the existing 64-key space with an independent physical destination: port 0 has physical plus eight loopback destinations, and port 7 has seven. The 1x1 shape has eight physical and eight loopback destinations.

`INPUT_LOOPBACK_P` defaults to zero. Received samples are copied from the presentation queue into a separate block RAM and read synchronously by the capture mapper, adding one media frame. Missing, expired and invalidated data produces silence. Disabled builder artifacts, descriptor images and firmware ROM bytes match the baseline at both sizes.

Sample-exact wire tests pass at both sizes, all seven planted copy/scheduling/invalidation defects are detected, affected render and capture regressions pass, and the 114-gate builder union passes. Selected routes meet the unchanged setup and hold floors at every required corner. The 8x8 route uses 49097 LUTs, 54663 FFs and 111 BRAM tiles; the new leaf increment is 650 LUTs, 259 FFs and one RAMB18.

The enabled 8x8 control-memory allocation is 70.5 tiles, 11.5 above its existing ledger entry. This remains S14 debt: the normal allocation guard still refuses that image, and owner bounds remain unchanged. Resource measurements use a separate measurement export. The builder union records one existing historical calibration row as unrun because its external report is absent.
