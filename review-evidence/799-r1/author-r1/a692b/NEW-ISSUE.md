### Objective / problem

On the shapes whose AAF stream count is a power of two above one (`endstation_ax7101_8x8`, `endstation_arty_4x4`, `endstation_arty_8ch`), `milan_datapath`'s MAAP request face carries a source index one bit narrower than the processor's. The CRF Media Clock Output is source `N_STREAMS`, so its index loses its top bit. Its `ALLOC_DA` request and a conflict on its address both arrive as source 0's. Each Stream Output must get its own destination address (Milan v1.2 Table 5.3), and the processor must be told which source a conflict hits. The shipping AX7101 1x1 shape is unaffected.

### Evidence / motivation

Observed (at milan-fpga `8b76de69`, processor `f65c8ff7`):

- `hdl/milan/milan_datapath.sv:2580`: `PP_SRC_IDX_W_C = (N_STREAMS > 1) ? $clog2(N_STREAMS) : 1`. It sizes `pp_maap_req_src_w` (`:2587`) and `pp_maap_confl_src_w` (`:2592`).
- The processor wrapper is elaborated with `.N_STREAM_OUT_P (ACMP_SRC_C)` (`:9359`), and `ACMP_SRC_C` is `N_STREAMS + 1` on a shape with a CRF output (`:1768`, `:1785`).
- `hdl/milan/KL_pp_shadow.sv:254-255`: its `SRC_IDX_W_C` is `$clog2(N_STREAM_OUT_P)`, which sizes `maap_req_src_o` (`:608`) and `maap_conflict_src_i` (`:613`). protocol-processor `hdl/top/protocol_processor_top.sv:248` clamps the same way.
- `KL_pp_maap_shim` is elaborated with `.N_SRC_P (ACMP_SRC_C)` (`milan_datapath.sv:9705`). Its `req_src_i` and `conflict_src_o` are `$clog2(N_SRC_P)` wide (`hdl/milan/KL_pp_maap_shim.sv:148`, `:163`, `:168`), and its block offset is `blk_addr_i[15:0] + req_src_i` (`:193`).

| Shape | `N_STREAMS` | `ACMP_SRC_C` | processor and shim index | datapath wire | CRF output's index |
|---|---:|---:|---:|---:|---|
| `endstation_ax7101_8x8` | 8 | 9 | 4 bits | 3 bits | 8 arrives as 0 |
| `endstation_arty_4x4`, `endstation_arty_8ch` | 4 | 5 | 3 bits | 2 bits | 4 arrives as 0 |
| `endstation_ax7101_1x1_tdm8` | 1 | 2 | 1 bit | 1 bit | 1, unaffected |
| `endstation_arty_current` | 1 | 1 | 1 bit | 1 bit | no CRF output |

Expected: the CRF output's `ALLOC_DA` is answered with block offset `N_STREAMS`, and a conflict on that address names source `N_STREAMS`.

Evidence: protocol-processor PR #204 recorded it for the pin adoption ("on parent shapes whose AAF stream count is a power of two above one (8x8, 4x4), the datapath's maap-face source index is one bit narrower than the processor's"). #799 found it again and left it out of scope. The ruling on #799's STOP (issuecomment-6460917634, item 3) moved it to this issue.

### Authoritative references

- Milan v1.2 5.3.7.5, Table 5.3: "The PAAD uses MAAP to allocate a unique Destination MAC Address for each of its Stream Outputs".
- IEEE 1722-2016 Annex B (B.3.6.4 `compare_MAC`; the conflict a MAAP claim reports).
- protocol-processor `docs/guides/integrator.md`, the `maap_*` face: the request and conflict source index.
- `hdl/milan/KL_pp_maap_shim.sv` banner.

### Context entry points

Read first:
- `hdl/milan/milan_datapath.sv` around `PP_SRC_IDX_W_C`, the `pp_shadow` instance and `pp_maap_shim`.
- `hdl/milan/KL_pp_shadow.sv` (`SRC_IDX_W_C`, the `maap_*` ports).
- `hdl/milan/KL_pp_maap_shim.sv`.
- `tb/verilator/milan_dp/` (the `sidmove8` leg runs the 8x8 shape) and `tb/verilator/pp_shadow/`.

### Scope

In scope:
- the MAAP face's source index width on every shape the builder builds, so the CRF output's request and conflict keep their source;
- a self-checking test on a shape with a CRF output and a power-of-two stream count that fails on the narrow index (the CRF output's allocated address, and a conflict on it reaching the CRF source);
- the lint or elaboration evidence that no port of the face is width-mismatched.

Out of scope:
- the shipping 1x1 shape's behaviour, which is already correct;
- the mailbox publication block and the split placement (#665).

### Executor

Unassigned

### Independent reviewer

Unassigned

### Acceptance criteria

- On `endstation_ax7101_8x8` and `endstation_arty_4x4`, the CRF output's `ALLOC_DA` is answered at block offset `N_STREAMS`, distinct from every AAF talker's.
- A conflict on the CRF output's address reaches the processor as source `N_STREAMS`.
- A test fails with the old width and passes with the fix.
- Every consumer gate that reads the datapath stays rc 0.

### Validation

The new test's leg, the full sweep, Yosys (`syn/yosys/run.sh`), lint and the publication census, all rc 0. The planted narrow width fails the new test by name.

### Dependencies / lane conflicts

Touches `milan_datapath.sv`, which #799 also edits. Start after #799 merges.

### Open design/specification decision?

No

### Discovered from

#799 (the ruling on its STOP, issuecomment-6460917634, item 3); protocol-processor PR #204.
