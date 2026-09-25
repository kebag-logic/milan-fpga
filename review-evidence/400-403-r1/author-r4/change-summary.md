## Changes

- `docs/ENDSTATION_BUILDER.md:1018`: Correct the declaration inventory to 71 rows.
- `docs/design/AREA_BUDGET.md:41`: State that supported configurations require MAAP.
- `docs/design/MAAP_FABRIC.md:83`: Document reset zero and exact declared-output allocation.
- `hdl/common/csr/milan_csr.sv:1542`: Describe neutral AAF/MAAP resets and the distinct lwSRP VID.
- `hdl/milan/milan_datapath.sv:274`: Correct MAAP requirement and independent RX-filter presence contracts.
- `sw/litex/milan_soc.py:3466`: Correct the MAAP prune help.
- `tb/common/gen_declaration_fixture.py:1`: Generate both fixture headers with the real builder; inject the nonshipping VID only after product validation.
- `tb/verilator/csr/Makefile:82`: Run the generated reset-bits-3 leg from the default target.
- `tb/verilator/csr/fixtures/reset_bits.yaml:1`: Commit both cold-reset admission bits as explicit fixture overrides.
- `tb/verilator/csr/sim_main.cpp:103`: Describe the committed fixture recipes accurately.
- `tb/verilator/milan_dp/README.md:683`: Name the generated per-output presentation default row.
- `tb/verilator/milan_dp/sim_main.cpp:652`: Correct neutral-reset and presentation-row commentary.
- `tb/verilator/nvm_cosim/run_cases.py:110`: Derive the host header from the generated overlay and SRP table through shared boot policy.
- `tb/verilator/pp_shadow/Makefile:106`: Run generated distinct-VID and CRF-on legs from the default target.
- `tb/verilator/pp_shadow/fixtures/crf_on.yaml:1`: Commit the second declared output fixture.
- `tb/verilator/pp_shadow/fixtures/vid73.yaml:1`: Commit the distinct emitter VID fixture.
- `tb/verilator/pp_shadow/sim_main.cpp:625`: Name the durable VID recipes in the harness comment.

