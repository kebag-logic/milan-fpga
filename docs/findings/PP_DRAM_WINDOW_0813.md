# The processor's DRAM window was never reserved — 2026-08-13

**Status: FIXED before any board ran it.** Found while building the descriptor-image
supply chain, by reading the generated device tree rather than the comment that
described it.

## What was wrong

`KL_aecp_desc_store` READS the AEM descriptor image from main memory and
`KL_aecp_resp_buf` WRITES the AECP response buffer to main memory, both at bases
compiled into the bitstream (the processor holds no base register — see
`docs/findings/PP_SHADOW_AREA_0812.md` for why those regions are not on-die).

`sw/litex/milan_soc.py` derived those bases as *the top 1 MiB of `main_ram`*:

```python
_desc_base = _ram.origin + _ram.size - _PP_WINDOW   # 0x7FF00000 on a 1 GiB AX7101
_resp_base = _ram.origin + _ram.size - 0x1000       # 0x7FFFF000
```

with a comment stating that the Linux device tree reserved that megabyte. It did
not. The only `reserved-memory` node `endstation_builder.py` emitted was
`pcmring`, and every AX7101 config places it at `0x7F800000`:

| shape | PCM ring | processor window | result |
|---|---|---|---|
| `ax7101_1x1_tdm8` | `0x7F800000 + 0x100000` | `0x7FF00000 + 0x100000` | window is **ordinary kernel System RAM** |
| `ax7101_8x8` | `0x7F800000 + 0x800000` | `0x7FF00000 + 0x100000` | window sits **inside the PCM ring** |

At the 1x1 shape the response buffer would have written 592 bytes into whatever
the page allocator had handed out. At the 8x8 shape the processor and the audio
capture ring would have shared the same megabyte — each corrupting the other.

Neither failure raises anything. There is no counter on either side that reports
a write to the wrong physical address, and the entity keeps answering.

## Root cause

Two independent derivations of the same fact. The builder decided where the
reserved band was; the SoC decided again, differently, from a different input.
The comment recorded the *intent* of the first and was never checked against it.

This is the failure mode `derive-never-mirror-constants` names: a copied value
diverges in silence. Here it was not even copied — it was independently
recomputed, which is worse, because the two agree for exactly as long as the
memory map does not move.

## The fix

The config already owns the one address both sides need. `platform.pcm_ring_phys`
is now the single authority:

* `sw/builder/endstation_builder.py` derives `pp_mem_phys = pcm_ring_phys -
  PP_MEM_BYTES`, emits a second `no-map` reservation `ppmem@...` beside
  `pcmring`, and publishes the pair as `pp_mem` in `platform_shape.json`;
* `sw/litex/milan_soc.py` READS `pp_mem` and only CHECKS it — inside `main_ram`,
  no overlap with the ring — raising rather than building a bitstream that
  writes where it must not.

Both shapes now place the window at `0x7F700000`, immediately below the ring:

```
0x7F700000  ppmem    1 MiB   no-map   descriptor image (grows up) + response buffer (last 4 KiB)
0x7F800000  pcmring  1 / 8 MiB  no-map
```

`no-map` does double duty: it keeps the kernel out, and it is what allows
`scripts/load_entity_model.sh` to reach the window through `/dev/mem` on a
`CONFIG_STRICT_DEVMEM` kernel — a region the kernel still owns is refused.

## What this costs operationally

**The DTB must be rebuilt, not just the gateware.** A board booting a DTB
generated before this change has no `ppmem` node, so the kernel will allocate
that megabyte regardless of what the bitstream was built to use. Rebuild the
device tree from the regenerated `milan-nic.dtsi` and reflash it with the
bitstream.

The bitstream built earlier on 2026-08-13 (`TAG=drammem`, which placed and routed
at 84.80% LUT / 125 BRAM, post-route WNS +0.095 ns) was compiled against the OLD
base and must not be used with the new device tree.

## The rebuild that ships

`TAG=ppmemsw ./build.sh ax7101 --sweep` — three place directives, one closed,
which is the usual rate for this design (`rv32-fit-campaign-0731`: closure above
the area cliff is roughly a one-in-three lottery, so a single build failing
timing is not evidence of a regression).

| directive | WNS | TNS | failing | verdict |
|---|---|---|---|---|
| `ExtraPostPlacementOpt` | −0.063 ns | −1.055 | 20 | missed |
| **`AltSpreadLogic_high`** | **+0.008 ns** | **0.000** | **0** | **MET** (WHS +0.036) |
| `ExtraTimingOpt` | −0.063 ns | −0.383 | 8 | missed |

**Ship `build_ax7101_asl_ppmemsw`**: 50,040 Slice LUTs post-place (78.9%),
125/135 Block RAM, `alinx_ax7101.bit` 3,825,992 B, and `aem_desc.bin` (5,520 B,
base `0x7f700000`) beside it — byte-identical to the copy the builder wrote into
the rootfs overlay, which is the copy the board actually loads.

The margin is +8 ps. That is met, not comfortable: re-sweep rather than assume
closure survives an unrelated edit.
