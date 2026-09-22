<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# desc_store — KL_aecp_desc_store suite

Proves the [07 §3.3](../../docs/architecture/07_memory_maps.md) entity-model
store: `make` = build + run, exit 0 = PASS, **584 checks**.

The store keeps the descriptor image in the integrator's **main memory** (DDR3
on the reference board) and serves the µCPU's `st_*` face from an on-chip line
buffer, so the harness is two independent models — never DUT logic:

1. **A latency-injecting memory BFM.** Its first-word latency is **24 clocks by
   default and never zero**: the reference SoC measures ~1424 ns on a miss to
   main memory, and a store that only ever sees zero-latency answers is
   untested against the thing that makes this hard. The BFM also plays a bridge
   that **never accepts a request**, one that answers a beat with `rsp_err`, and
   one with inter-beat gaps at a longer latency.
2. **An independent parser *and* builder of the documented image format**
   (`hdl/aecp/desc/gen_desc_image.py` header + index map). Every expectation is
   computed from the parsed image, never from anything the DUT produced. The
   suite additionally loads the generator's own worked example
   (`example_milan_8.json` → `image.bin`), so generator and RTL are proven to
   agree on the *format* rather than merely on each other.

   That worked example is a **test vector, not a compliance reference**. Its
   stream descriptors deliberately use the Milan v1.2 Annex C Table C.1 layout
   (`formats_offset` = 136), which is *not* what ships: shipping descriptors
   come from the consuming repository's `avdecc/gen_aem_store.py` in the IEEE
   1722.1-2021 Table 7-8 layout (`formats_offset` = 138), as Milan v1.2
   §5.3.3.4 requires. The disagreement is the point. The store takes every
   length from the index map and never reads a descriptor's interior, so this
   is the one image here whose `formats_offset` contradicts the length its
   index map declares. See the header of `example_milan_8.json`.

## What it proves

| Group | Checks |
|---|---|
| **G1–G2** | boot walk out of DRAM; then every descriptor of the 07 §3.1 eight-descriptor example located and served **byte-exact**, lane by lane, with its length and `name_base`; a lane past the descriptor reads 0, never the next descriptor |
| **G3** | index-map **boundaries**: the first and the last entry are both found (a scan that stops one early, or runs one past, fails exactly here); a type past the last entry and a type in a hole between entries both MISS |
| **G4** | locate misses: unknown type, `descriptor_index` past `count`, unknown configuration — each `st_err`, each counted, and the store is not wedged afterwards |
| **G5** | the 07 §3.4 **name region** via `st_name`: every entry read back against the image, semantic index 0/1 validation, then full-lane and byte-strobed writes; each write is immediately visible in the unaligned inline field served by READ_DESCRIPTOR |
| **G5b** | an 80-entry name table crosses the 511-beat request limit, loads through multiple whole-name chunks, and preserves the final entry at its absolute overlay address |
| **G6** | the image is **read-only at run time** (07 §2): a non-name write is dropped, counted, and does not reach the served bytes |
| **G7** | **back-to-back reads with `st_req` held high** — the µCPU never drops the request between two consecutive state ops, so a store that latched the request edge would deadlock here |
| **G8** | a longer memory latency with inter-beat gaps changes nothing |
| **U1–U2** | **software has not loaded the image**: a 0xA5 region and an all-zero region are both refused on the magic/version/checksum header, every locate misses, and no length, no descriptor byte and no `configurations_count` comes back — an unloaded region cannot produce a plausible-looking descriptor |
| **U3–U4** | a corrupted (stale-checksum) image and a future layout version are refused |
| **U5–U7** | more index entries than the on-chip cache, more names than the overlay, and a descriptor longer than the line buffer are each refused **up front** with a distinct fault code |
| **U8** | **self-heal**: after a garbage boot, a late software load is picked up by the re-probe a locate arms — no reset needed, and nothing wrong served in between |
| **M1** | a bridge that **never accepts** degrades to a clean TIMEOUT fault and a `NO_SUCH_DESCRIPTOR`-shaped miss; it never hangs the µCPU |
| **M2** | a `rsp_err` on the descriptor fetch becomes a locate miss, and the store recovers |
| **S1** | two descriptors of one type with a length that is **not a multiple of 8** — without the padded `elem_stride` of the index entry, index 1 starts mid-beat and the whole line buffer comes back byte-shifted |
| **S2–S3** | an index entry whose stride is shorter than the length or not 8-aligned, and one with a zero length, are refused rather than served — and one bad entry does not poison the rest of the model |

`MEM_TIMEOUT_CYC_P` is compressed to 64 clocks here (`-G` in the Makefile) so
the "no bridge at all" arm runs in a few hundred clocks instead of tens of
thousands; the default is 4096 (41 µs at P-CLK-HZ), far inside `T-AECP-RESP`.

## Mutation-proven 2026-08-13

| Break | Went red |
|---|---|
| the whole header gate removed (`hdr_ok_w` forced true) — garbage accepted as a model | **18** of 375 |
| index-map scan stops one entry early (last-entry test `+1` → `+2`) | **21** of 375 |
| `elem_stride` replaced by `elem_len` in the locate address (index > 0 byte-shifted) | **12** of 375 |
| locate ignores `descriptor_index` vs `count` (out-of-range served) | **3** of 375 |
| checksum compare alone removed | **3** of 375 |
| magic compare alone forced true | **1** of 375 |

The last two are recorded because of what they say rather than how loud they
are: magic, version and checksum are *three* independent guards, so disabling
any one of them still leaves an unloaded region refused — only the fault CODE
changes. That is the intent (an accidental magic match must not be enough), and
it is why the honest mutation for "the store refuses what software has not
loaded" is the whole-gate one above.
