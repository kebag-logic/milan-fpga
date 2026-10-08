[A560]

# Round 7 linked-size comparison

Candidate: `f74b9403b330ce316eeec6f724846f16def98443`. Lane base: `db9aa8c9b135b34ff3d070a979dee70440b37cc6`.
Round 5: `500b8f64443777685e6a54049d933476710d26f0`. All values are bytes. `1x1` means
`endstation_ax7101_1x1_tdm8`; `8x8` means `endstation_ax7101_8x8`.
All twelve links use the same CI-pinned RV32I/ILP32 build flags, SDK and verified
runtime archives. Data is zero in every fixture. The spans include alignment
and an 8192-byte stack reservation; the reservation is not a measured whole-call-chain
bound. These fixtures have not been booted. Largest span: 104720 bytes, below
128 KiB. `ROUND7-SIZES.json` retains section, symbol and artifact hash/size
measurements, plus the live text contribution of each object.

| Shape / IF | Text | Read-only | BSS | Stack | RAM span | Delta lane base | Delta Round 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1x1 / 1 | 33560 | 2846 | 18072 | 8192 | 62688 | +43936 | +8096 |
| 1x1 / 2 | 34792 | 2846 | 29424 | 8192 | 75264 | +56016 | +9424 |
| 8x8 / 1 | 33500 | 2846 | 32824 | 8192 | 77376 | +58624 | +8096 |
| 8x8 / 2 | 34744 | 2846 | 58928 | 8192 | 104720 | +85472 | +9424 |

## Attribution from Round 5

| Component | IF=1 | IF=2 | Evidence |
| --- | ---: | ---: | --- |
| MAAP core and mailbox text | +4520 | +4844 | `maap.o` plus `maap_mbx.o` live map sections |
| Application composition text | +516 | +524 | `ctrl_app.o`, `ctrl_app_srp.o`, `ctrl_image.o`, `mbx.o` deltas |
| Receive adapter text | +416 | +340 (1x1), +348 (8x8) | `srp_mbx.o` delta, including Round 6 and Round 7 |
| MAAP application state | +1104 | +2172 | `image_app` grows from 2096/2188 to 3200/4360 |
| Retained receive record | +1528 | +1528 | `image_srp` grows by one owned `mbx_frame` for both shapes |
| MAAP allocation fixture state | +8 | +16 | `image_allocation` |
| Total BSS | +2640 | +3716 | Sum of those three state changes |

Thus text grows by 5452 bytes at IF=1, 5708 bytes at 1x1/IF=2 and 5716 bytes at
8x8/IF=2. Read-only data and runtime text are unchanged from Round 5. The retained
receive record is one shared buffer, not one per interface. The entity-sized
arenas are already included in BSS and are unchanged from Round 5:
9920/19840 bytes for 1x1 and 24032/48064 for 8x8 at IF=1/2.

Against the Round 6 linked spans of 62560, 75152, 77264 and 104608 bytes, this
round adds 128, 112, 112 and 112 bytes respectively (alignment included).
Text adds 120 bytes at IF=1 or 116 at IF=2. BSS is unchanged: the new counter
uses existing trailing padding in the RV32 adapter layout.

## Reproduction

Use the environment in `ROUND7-GATES.md`, from the candidate checkout. Runtime
inputs and their source hashes are in `ROUND7-RUNTIME.json`; use the same
archives for all versions and supply a local `provenance.json` with its path
variables expanded. The lane-base firmware predates SRP. The historical helper
uses the Round 5 link fixture for the base and Round 5 source exports, while
current generators supply identical entity and mailbox contracts.
The Round 5 and current dependency pins have the identical `src` tree
`f46e01d3bf1c753009479d32e69d00263ee124ed`; only the checkout guard is set to
the current public pin. The historical firmware source is not modified.

```sh
git archive --format=tar --output "$SCRATCH/lane-base.tar" db9aa8c9b135b34ff3d070a979dee70440b37cc6 sw/firmware/ctrl
mkdir -p "$SCRATCH/lane-base"
tar -xf "$SCRATCH/lane-base.tar" -C "$SCRATCH/lane-base"
git archive --format=tar --output "$SCRATCH/round5.tar" 500b8f64443777685e6a54049d933476710d26f0
mkdir -p "$SCRATCH/round5"
tar -xf "$SCRATCH/round5.tar" -C "$SCRATCH/round5"
python3 "$PACKET/round7-helpers/images.py"
```

The helper issues twelve `ctrl_image.py` links with `--config`, `--interfaces`,
`--output`, `--libc` and `--compiler-runtime`; historical links additionally
supply `--ctrl-source`, and the base supplies `--without-srp`. Its outputs remain
in disk scratch. The unchanged runtime archives have these hashes:

| Input | Bytes | SHA256 |
| --- | ---: | --- |
| `libc.a` | 5542 | `488f3ee5be208e51fee0a5536fc2c7a690354627bdf0de41d3aa8e41d14fd294` |
| `libcompiler_rt.a` | 30036 | `ad58aefcca43955cf230f42fbc18d9352ec7caea57c68a0a3f7416c271604c97` |

## Full twelve-link section table

| Version | Shape / IF | Text | Read-only | BSS | Stack | RAM span |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| lane-base | 1x1 / 1 | 7264 | 144 | 3148 | 8192 | 18752 |
| lane-base | 1x1 / 2 | 7664 | 144 | 3240 | 8192 | 19248 |
| lane-base | 8x8 / 1 | 7264 | 144 | 3148 | 8192 | 18752 |
| lane-base | 8x8 / 2 | 7664 | 144 | 3240 | 8192 | 19248 |
| round5 | 1x1 / 1 | 28108 | 2846 | 15432 | 8192 | 54592 |
| round5 | 1x1 / 2 | 29084 | 2846 | 25708 | 8192 | 65840 |
| round5 | 8x8 / 1 | 28048 | 2846 | 30184 | 8192 | 69280 |
| round5 | 8x8 / 2 | 29028 | 2846 | 55212 | 8192 | 95296 |
| head | 1x1 / 1 | 33560 | 2846 | 18072 | 8192 | 62688 |
| head | 1x1 / 2 | 34792 | 2846 | 29424 | 8192 | 75264 |
| head | 8x8 / 1 | 33500 | 2846 | 32824 | 8192 | 77376 |
| head | 8x8 / 2 | 34744 | 2846 | 58928 | 8192 | 104720 |

