# The release (all-fabric) image: byte-identical where loaded at every head from step 11's record to the final head (R865-4-F2)

The AX7101 1x1 shipping image is the `route-1x1` record since `73272666` (step 11). These receipts compare its export
(`tools/release_export.sh`: the launcher's dry run and its `milan_soc.py` command without `--build`, no Vivado) at
each pair of consecutive heads.

The chain runs `b1f1161b` (the record's docs-only successor), `967b1ca9`, `7650a02d`, `0839453f`, `01765bb0`,
`c1e95dc1`, `92de01f7`, `8c5e2b4f` and `15168e14`, the final head. `fb083864` adds two test files to `92de01f7`, and
`8dc85884` adds one doc to `8c5e2b4f`. Neither is a release input.

| File | What it is |
|---|---|
| `release-identity.log`, `.rc` | `tools/release_identity.sh` over the eight pairs; rc 0 |
| `release-identity-plant.log` | the planted control: the final head's export with one `bios.bin` byte flipped, refused |
| `tools/` | `release_identity.sh`, the `cmp_export.py` it calls, and the `release_export.sh` that made each export |

For each pair, the log gives:
- the source diff's size and the release recipe's inputs it touches (`hdl/`, `syn/`, `sw/litex/`, `configs/`);
- `cmp_export.py` over all 3,876 files, each export's absolute roots replaced first;
- the sha256 of every file the image loads, on both sides.

**The result at every pair:**
- **Loaded files:** `software/bios/bios.bin` `603b9ca3…`, `aem_desc.bin` `bdfde7cf…`, `gateware/alinx_ax7101_rom.init`
  `621133bb…`, `_sram.init` `e3b0c442…` (empty) and `_mem.init` `d1657b93…` are equal. That is 40 of 40 comparisons.
- **Gateware:** the only differing file is the top Verilog, and it is equal outside its comments.
- **The other differences:** `litex.log` and the BIOS build's object files differ. The object files carry the export
  directory in their names (the 21 files only on one side).
