# The gating bitstreams' firmware is the head's product firmware, by every loaded byte (R866-4-F1)

At both points, 1x1/1if and 8x8/1if, these receipts join each gating bench bitstream to the product image of the head
(`8c5e2b4f`, whose firmware and gateware inputs are those of the final head `8dc85884`). The product image is the one
the ROM ledger links (`plat_ledger.py --self-test`, points `1x1-if1` and `8x8-if1`). Each link of the chain below is a
check that can fail, run here with its output and exit status.

```
bitstream .bit (sha256, ../<point>/artifacts.sha256)
  -> payload sha256 and part, recomputed from the .bit (bitstream_binding) = image_manifest.json's "bitstream"
image_manifest.json (sha256 = artifacts.sha256's) -> "ctrl_firmware" sha256 and bytes = the gating ELF
gating ELF -> its rom words = the build's rom bank init files = the product ELF's rom words
gating ELF <-> product ELF: every program header and PT_LOAD's bytes, and every SHF_ALLOC section's
  name, type, flags, VMA, LMA, size and bytes, equal
product ELF sha256 = ../../images/product-images.txt's for the head (1x1-if1 fe12a3f1..., 8x8-if1 c6355962...)
```

| File | What it is |
|---|---|
| `1x1.txt`, `8x8.txt` | `loaded_identity.py` at each point. Covers the ELF headers, the program headers and PT_LOAD bytes, the loaded sections (name, VMA, LMA, length, full sha256 of each side), the other sections, the symbol tables, the rom words against the build's init files, the manifest and the bitstream binding, the identity gate re-run, and the input objects. Each ends with `RESULT <point>: PASS` |
| `loaded-identity.log`, `.rc` | `tools/loaded_identity.sh`: both points, two planted controls, the toolchains; rc 0 |
| `plants/` | The planted controls' full outputs: the product ELF with one `.rodata` byte flipped (refused by `segments`, `loaded`, `not-loaded`, `rom-words`), and the artifact list with the bitstream's digest zeroed (refused by `manifest`) |
| `toolchains.txt` | The SDK each link used |
| `verify-published.log`, `.rc` | `tools/verify_published.py .`, run from `receipts/step16/gating` on the receipts alone. Each published manifest file matches its artifact-list digest, and the manifest binds the compared gating ELF. The bitstream digest is the bench list's and the binding's, the product ELF is the product-images receipt's, and the identity gate passes. rc 0 |
| `verify-published-plant.log` | The same check on a copy of the receipts whose 8x8/1if manifest names another firmware: refused |
| `../<point>/build/` | The gating build's listed outputs: `image_manifest.json`, `flashboot_layout.json`, `csr.csv`, `aem_desc.bin`. Each matches its digest in `../<point>/artifacts.sha256`. The 3.8 MB `.bit` is bound by its sha256 there and by the payload binding the manifest records |
| `../bench-images-8c5e2b4f.txt` | The bench list's section for these two bitstreams |

**Why the whole ELF files differ** (1x1/1if `c873a0aa…` / `fe12a3f1…`, 8x8/1if `d67fd049…` / `c6355962…`). The gating
chain links with the gating lane's pinned SDK (Buildroot 2021.11-18033, GCC 14.3.0, binutils 2.43.1). The ledger links
with the lane's SDK (Buildroot 2026.05, GCC 14.3.0, binutils 2.45.1). See `toolchains.txt`.
- **The whole files:** same size, and their section header tables are equal. All 2,474 differing bytes at each point
  lie in `.symtab`, which is not loaded.
- **The symbol tables:** both hold the same 1,267 entries. 612 positions hold another entry, and each such entry sits
  at the same address as the one it replaces: a named local and the RISC-V mapping symbol `$x…` at one address are
  listed in the other order.
- **The input objects:** none of the 43 differs in a loaded section. They differ only in `.comment` (each SDK's
  compiler identification), in the order of `.symtab` and `.strtab`, and in the relocation indices that follow from
  that order.

**Re-running:** `bash tools/loaded_identity.sh OUT > OUT/loaded-identity.log 2>&1; echo $? > OUT/loaded-identity.log.rc`.
- It needs the scratch trees: `SCRATCH` (the gating chains' `gate15/` and the gates' `r9gates/`) and `PYTHON` (the
  product venv's `python3`). The script defaults are host paths, shown here as placeholders.
- `tools/verify_published.py` needs only these receipts.
