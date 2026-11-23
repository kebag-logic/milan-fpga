[A830] REVIEW READY

Commit: `677d605f37c3a80654df1dd2cde053b57242845b`, `pf-linuxprof-1` -> `dev-soft-core` (base `854bd723`). Local, not pushed.

Changed:
- `sw/builder/endstation_builder.py`: the descriptor-only host profile, `board.target: host`.
  - It has its own board, gPTP and interface loaders: `gptp_owner: host-phc`, `constraints.link_mbps`, every Announce field and `port_number` stated, the `usb_audio` family. It has no SoC, fabric blocks, render lane or framer cap.
  - Every other check is the FPGA path's, unchanged, and `build()` refuses the profile by name.
  - An FPGA target naming `board.gptp_owner` is refused instead of ignored.
- `configs/host/endstation_host_example.yaml`: the first user's inventory.
- `ctrl_loop.h`: a `(1, 1, 2)` row of THE SHAPES under `CTRL_HOST_PLATFORM` only. Its figures are 1x1/1if's, held as a stated host scheduling profile; the comment states what is not measured. The FPGA rows and the `#error` are untouched.
- `test_builder.py`: gate 41 covers the generators, the image, the shape row, and the section 6 key map held to the host loaders. Gate 42 plants 28 defects; 5 show an FPGA config still refuses a missing fabric gPTP owner.
- `docs/ENDSTATION_BUILDER.md`: section 6 and row 5d.

Validation:
- FPGA artifact identity at base and head: 5 configs at both placements, the builder outputs, the AEM image pair, the 4 firmware generator headers and the tracked generated files. 170/170 byte-identical; the tracked tree is clean after the builds.
- `test_builder.py --require-rv32`, run in 4 subsets: 114/115 gates passed once each. The one NOT RUN row is gate 11's calibration report, absent here.
- Gates 32, 41 and 42 pass: 116 == 116 keys, 28/28 defects refused.
- Docs and quality gates: 24/24, including `docs_check`, `check_em_dash --base 854bd723` and `check_baremetal_only --check` with `--selftest`.
- `ctrl_loop.h` preprocessed at base and head is identical for no shape header, 1x1 and 8x8. The three all-fabric Arty shapes are refused at both; their `#error` line moves from 397 to 424.
- The firmware gate's own arms on its tree pass: service bounds and every-shape SRP with RV32 (21), AECP (18), split platform (8).

Acceptance criteria: met. The profile generates a descriptor image and ADP fields through the AEM checks, the identity gate passes, and ENDSTATION_BUILDER describes the profile.

Open risks and questions:
- Gate 1b (builder leg 0) did not complete within the 10-minute bound on a command here; its builder arms printed PASS before the bound. `ci_builder_legs.py`'s own union and the firmware shards and mutation campaigns are owed to the hosted run.
- The host shape row is justified by a stated scheduling profile, not by a host or board measurement.
- The tree is bare-metal only (#259), so the profile uses the existing host-program vocabulary and carries no false `fabric_gptp`. Please confirm that a descriptor-only host profile in the generators is within #259's intent; this issue authorizes it.
