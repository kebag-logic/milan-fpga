# Handover — 2026-07-28

**UNCOMMITTED ON PURPOSE**, same as `HANDOVER_0727_NIGHT.md`: this carries bench
hosts, IPs and local paths that `scripts/docs_check.py` rejects in tracked
markdown. Scrub before committing any of it.

---

## 1. One-line state

**All 15 parallel lanes merged. 52 commits on `main-push`, nothing pushed.**
Desk gates green except four behave scenarios (§5), three of which are *true
findings* rather than test bugs. **Nothing has been built or flashed** — silicon
still runs `0x0001_0016` and the pre-session gateware.

---

## 2. What this session was actually about

One defect class, found five times:

| # | the declaration | what the fabric did |
|---|---|---|
| 1 | talkers advertised 8-channel AAF | framer emitted **2** |
| 2 | ADP stream counts from a boot script | gateware had 8, script said 1 |
| 3 | MSRP TSpec `MaxFrameSize 224` | wire frame is 90 B → MSDU **72** |
| 4 | `firmware_version: "0.1.0"` | gateware was **1.22** |
| 5 | `cfg_aaf_bypass` overrode ACMP+lwSRP | fabric already knew the answer |

**A declaration nobody checked against the thing it describes.** That is roadmap
item 00, and it is why `docs/testing/methodology.md` names **L1 (binding)** as
the missing test tier — six of its nine documented escapes live there.

The sharpest instance is self-referential: `cfg_aaf_bypass` existed because this
repo's own traceability flattened Milan v1.2 **5.3.7.3** into an unconditional
*"a Stream Output SHALL NOT be stopped"*. The real sentence conditions streaming
on **"…and receiving a Listener Ready or Listener Ready Failed attribute"**.
**The defect and its justification were the same sentence, mis-restated.**

---

## 3. Bench state — LEAVE IT ALONE UNLESS YOU READ §7

| | ALINX `.1` | Arty `.3` |
|---|---|---|
| VERSION `0x004` | `0x0001_0016` | `0x0001_0016` |
| `AAF_CTRL 0x654` | **`0x00020001`** | **`0x00020001`** |
| `CLKV_STAT 0x77C` | `0x4C2` (tu=0, leased) | `0x6A2` (tu=0, leased) |
| role | grandmaster | slave |

Both fixes above are **live but volatile**: `AAF_CTRL` reverts on reboot unless
the new `S50milan` is deployed, and `tu = 0` reverts unless `gptp2csr.sh` is
re-deployed. No ACMP binds are up. The bench is clean.

**Access** (unchanged from the 07-27 handover):
```bash
ssh amx-pw0                                  # peer, has the AVB iface enp6s0
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@192.168.127.1
ssh amx-ubuntu-server                        # ProfiShark capture host  <-- NEW
ssh amx-pi 'powerstrip status|on N|off N'    # OUT5 = "DN-1", unidentified
```

**The inline taps are on `amx-ubuntu-server`, and they are the best instrument
on this bench.** Identified empirically, not assumed:
- `enxe8eb1b37e2c0` → **ALINX ↔ switch**
- `enxe8eb1b39111a` → **Arty ↔ switch**

Tools deployed there: `/tmp/tapclass.py <if> <secs>` (tagged/VID/PCP/subtype/src)
and `/tmp/msrp.py` (MSRP declaration decoder). **Both handle the 28-byte
ProfiShark record header.** See §7 for their traps.

---

## 4. Gate status, exact

```
builder gates ............ ALL GATES PASS
check_entity_shape ....... 88 checks, 0 failures (--self-test)
lint_rtl ................. PASS, 150 <= ratchet 150   (never raised)
docs_check ............... 0 findings / 178 files
check_doc_paths / TOC / archive ... OK
check_soc_sources ........ OK, 36 modules, 84 sources
Verilator suites ......... 57/57 at the 12-lane point (2,101,084 checks)
                           aecp / csr / milan_dp / tsn_fuzz repaired since;
                           A FULL RE-SWEEP HAS NOT RUN ON THE FINAL TREE
behave ................... 245 passed / 4 failed  (see §5)
check_wire_accountability  RED BY DESIGN — see §6
```

**The check total is now trustworthy.** It was 2,062,389 for months and was
wrong twice over: the aggregator recognised one of five summary shapes (28 of
57 logs contributed zero) and read `N checks: P PASS` as `P`. It now **fails**
on any log it cannot account for, **refuses** concurrent sweeps, and reports
`timed out` separately from `failed`.

---

## 5. The four behave failures, with verdicts

| step | verdict |
|---|---|
| `serving 8 mappings … would read past its descriptor` | **Stale scenario.** Asserts the pre-fix over-read; the fix landed and the geometry changed. Rewrite. |
| `entity advertises 24 AUDIO_CLUSTER descriptors` | **Legitimate change.** `arty_4x4` moved `tdm8 → i2s_philips`; count is 16. Update. |
| `arty_4x4: fabric emits 2ch, talkers declare 4ch` | **TRUE FINDING** — item-00 in `arty_4x4`. Owner: item 5. |
| `arty_4x4: front-end supplies 1 pair slot` | **TRUE FINDING** — same cause. |

The last two assert a property that is knowingly false today, so they belong
under the repo's `@rtl-defect` tag (a scenario deliberately asserting current
non-compliant behaviour, flipped when the RTL lands) rather than in the green
gate. **Do not "fix" them by down-declaring `arty_4x4` to 2ch** — that is the
reverted `dade536` mistake.

---

## 6. `check_wire_accountability` is SUPPOSED to be red

It reports **W3**: 16 pair slots back **four** 8-channel talkers, not eight.
That is a *different* defect from the one item 00 closed (an unfed talker is
**silent**, not mis-framed) and it is correctly owned by item 5. Do not read it
as a regression.

---

## 7. Traps burned today — read before touching the bench

1. **`/tmp/floodclass.py` on the peer masks the AVTP subtype with `0x7F`**, so
   ADP/AECP/MAAP (`0xfa/0xfb/0xfe`) misreport as `0x7a/0x7b/0x7e`. AAF (`0x02`)
   is unaffected. `tapclass.py` reads the full byte.
2. **`/tmp/msrp.py`'s first version stopped after the first Message in an
   MRPDU.** Our serializer packs every attribute into ONE PDU, so Domain-first
   hid the TalkerAdvertise and produced a confident wrong answer. Its vector
   arithmetic still misses some Listener attributes — **cross-check at byte
   level**: scan for a byte in {1,2,3,4} followed by its mandated
   AttributeLength {25,34,8,4}.
3. **The standards ARE on this box**: `/home/alex/standards/` (1722.1-2021,
   1722-2016, Milan v1.2 Final, the media-clocking spec, the end-station
   validation test plan). `$STANDARDS_DIR` is merely **unset**, which made
   several lanes conclude they were paywalled and fall back to the repo's
   paraphrase — producing the 5.3.7.3 error above. **Quote the clause.**
4. **`pdftotext` mangles Table 7-1's hex *value* column** (reads `D16` where
   the value is `0xC`). Take type codes from the intact *clause* column.
5. **Concurrent sweeps corrupt each other** (shared `obj_*`) and spuriously trip
   `timeout 1800`, manufacturing FAKE failing suites. A lock now refuses them.
6. **Never `pkill -f verilator_bin`** unscoped on this shared box, and never
   `pgrep -f` a pattern your own waiter command line contains.
7. **`cp -r` third_party into a worktree, never `ln -s`** — then DELETE the
   copied `.git` pointer or every git command in that worktree fails.
8. **`scp` to a board fails** (busybox has no sftp-server) and silently wrote an
   EMPTY `gptp2csr.sh`, killing the daemon. Use `ssh host "cat > f" < f`.

---

## 8. Roadmap — do these in order

### 8.1 Before any flash (blocking)
- [ ] **Re-sweep the final tree.** Four suites were repaired after the last
      full run; only per-suite runs have been done since.
- [ ] Fix / re-tag the four behave scenarios (§5).
- [ ] Deploy the new **`S50milan`** (`milan-tests-avb` `2998e06`) into the
      buildroot image, or the `AAF_CTRL` fix dies at first boot.

### 8.2 Build and flash
- [ ] 3-seed sweep per board, keep best WNS. **Verify `N_STREAMS` before
      flashing** (the sweep downgrade trap).
- [ ] **New this round: timing closure on the 98.304 MHz `cd_audio_tdm`
      domain is UNPROVEN.** The TDM32 master added it.
- [ ] Cable discipline: ALINX = FT232H serial `210512180081`; Arty = FT2232
      `210319AFEED0`. **IDCODE cannot tell them apart** — both `0x3631093`.
      The flash chips can: Micron N25Q = ALINX, Spansion S25FL = Arty.
- [ ] `--fpga-part`: ALINX `xc7a100tfgg484`, Arty `xc7a100tcsg324`.
- [ ] After flashing: **re-deploy `gptp2csr.sh`** or `tu = 1` returns silently.
      Check `devmem 0x9000077C` — expect bit 1 SET, not `0x5`.
- [ ] Diff the flashed DTB windows against the build's `csr.csv` (the CSR-rot
      trap). At the last check they matched: `dma-ts 0xf0003100`, `pcm 0xf0003120`.

### 8.3 Silicon validation (the goal)
Run in this order; each lane handed back a procedure in its commit message.

1. **R7 first** — `devmem 0x90000004` on BOTH boards, refuse if they differ.
   Expect `0x0001_0018` after this build.
2. **Calibrate against the reference device BEFORE trusting any new check.**
   `hive_compliance.py` C10, C11 and the revived C9 cluster bound have **never**
   been run against a device. If one fails there, **the check is wrong** until a
   clause says otherwise (the C1 precedent). C11 asserts a *refusal*, so it can
   be right about the clause and vacuous about a device — it prints the port
   count so you can tell.
3. **AECP D1/D2**: `hive_compliance` on our entity must go **40 failures → 1**
   while the reference stays clean. Hive's 15× "Incorrect payload size" and the
   8×+7× no-such-descriptor lines must disappear.
4. **Entity version**: read the ENTITY descriptor with Hive; `firmware_version`
   must equal `devmem 0x90000004` through the documented mapping → **`1.24.0`**.
5. **The framer** (item-00 acceptance oracle): `A_AAF_PAIRS 0x664` delta should
   go from ~48,000/s to ~768,000/s (16 pairs = TDM32). Then bind talker 0 to a
   reference sink whose channel count MATCHES and confirm `UNSUPPORTED_FORMAT`
   = 0 with `FRAMES_RX` advancing. **Baseline: 8ch sink = 296,294/296,294
   failures; 2ch sink = 0 over 1,491,239.**
6. **The streaming licence**: with nothing bound, the taps must show **zero**
   tagged AAF from either board. Bound, they must show ~8000/s. `LWSRP_STATUS
   0x694` = `0x30` unbound, `0x37E` bound.
7. **The flood**: `tapclass.py` on the Arty link must no longer show the ALINX's
   CRF once the CRF class-A path is enabled (`CRFT_CTRL[1]`). **Success looks
   like ABSENT, not tagged** — a registered stream with no listener is pruned.
8. **gPTP under load**: `iperf3 -u -b 950M` at the grandmaster. With
   `rx_queues: 1` the GM is deposed within seconds (conformant BMCA, 802.1AS
   10.3). `rx_queues: 2` is the fix and is **reflash-gated** (moves `dma-ts`
   and `pcm-dma` by `0x74`; builder gate 19c refuses until re-pinned).
9. **Frame analysis** — verify against the standard, on the tap:
   - AAF frame length ↔ declared `channels_per_frame` (`42 + 24·C`).
   - MSRP `MaxFrameSize` ↔ the measured MSDU (**currently 224 vs 72 — open**).
   - VLAN tag: TPID `0x8100`, PCP 3, VID 2 (802.1Q 9.5/9.6, 34.5 Table 34-1).
   - `tu` bit = 0 while the lease holds (1722-2016 4.4.4.7, PICS AAF-10).

### 8.3b ARTY AUDIO SHAPE — USER DECISION 2026-07-28, supersedes Lane 10

**The Arty gets ONE I2S lane, on Pmod 1 (where the Pmod I2S2 already sits), and
the rest becomes TDM8 as MASTER.**

This reverses Lane 10's conclusion, and correctly: that lane refused a TDM
front-end because the board routed no `tdm` resource and the bench had no TDM
device, so declaring one would have framed digital silence and moved
`i2s_mclk` off the Pmod. With real pins and a real master that reasoning no
longer applies — a master needs nobody to drive it. **The refusal machinery
stays; it just starts answering "backed" once the pads are declared**, which is
how `board_audio_routing.py` was built to behave: it READS routing, it does not
hardcode a verdict.

**THE CLOCKING IS FREE — this is the good news.** TDM8 x 32-bit slots @ 48 kHz
needs bclk = 8 x 32 x 48000 = **12.288 MHz**, and `KL_tdm_capture_master`
generates bclk as `clk_audio / (2 x BCLK_HALF_P)`. At the existing **24.576 MHz**
audio MMCM with `BCLK_HALF_P = 1` that is 12.288 MHz **exactly**. Unlike the
AX7101 — where TDM32 forced a second 98.304 MHz MMCM output and a new clock
domain whose timing closure is still UNPROVEN — **the Arty needs no clocking
change at all**: no new output, no new domain, no new closure risk.

**Pins are available and already surveyed.** Lane 10 verified against the stock
`litex_boards` platform: `pmoda` is fully consumed by the I2S2 Pmod
(`G13 B11 A11 D12 D13 B18 A18 K16`, with `i2s_rx_mclk` = pmoda:4 = ball **D13**
— the pin that must not move), and **pmodb/pmodc/pmodd carry 24 unclaimed
LVCMOS33 pins**, verified free by grep across `sw/`, `scripts/`, `configs/` and
`constraints/`. A TDM8 master needs mclk + bclk + fsync + data-in (+ dout if the
render side is wanted): four or five pins out of 24.

**Channel budget, stated honestly:**

| source | pairs | channels |
|---|---|---|
| I2S on Pmod 1 | 1 | 2 |
| TDM8 master | 4 | 8 |
| **total** | **5** | **10** |

`endstation_arty_4x4` declares **4 channels per talker** across 4 talkers = 8
pairs required against 5 available, so **two of its four talkers would be fully
backed**. That is the same W3 shape as the AX (section 6) and it must be
REPORTED, not hidden — a source-coverage gap owned by item 5, and a different
defect from the mis-framing item 00 closed.

**Work items, in order:**
1. Declare the Arty TDM pads in the platform (pmodb/c/d), leaving `pmoda`
   untouched. **Assert that `o_i2s_mclk_o` still binds to `i2s_pads[0]`** —
   Lane 10's mutation #4 exists precisely to catch that regression.
2. Point `board_audio_routing.py` at the new resource; gate 24c should flip to
   `tdm routed {'arty': True, 'ax7101': True}` with NO edit to the gate itself.
3. `endstation_arty_4x4.yaml` -> `kind: tdm8` + master. Its hash-derived
   `entity_model_id` WILL move again (`interface.kind` is a model-shaping
   field) — that is the mechanism working. `arty_current`'s **pinned**
   `0x001BC5AB73EC9D1D` must NOT move.
4. `BCLK_HALF_P = 1` off the existing 24.576 MHz clock, and **assert the
   frequency in the TB** rather than assuming it — the elaboration guard
   already refuses a `clk_tdm_i` that is not an exact even multiple of
   `SLOTS x 32 x fs`.
5. Silicon acceptance: scope bclk **12.288 MHz** and fsync **48.000 kHz**
   (period 20.833 us) on the new header, and `A_AAF_PAIRS 0x664` delta
   ~= **240,000/s** (5 pairs x 48 kHz) against ~48,000/s on the I2S-only build.

### 8.4 Known-open, owned
| item | owner |
|---|---|
| W3: 16 pair slots back 4 of 8 talkers | item 5 |
| TSpec `MaxFrameSize` follows the declaration, not the wire | provisioning |
| `TIMESTAMP_UNCERTAIN` computed (`0x780`) but not served by `GET_COUNTERS` | AECP |
| Re-add Lane 1's `hive_compliance` C5/C6 as C12/C13 (numbering collision at merge; they live in `e076647`) | compliance |
| `arty_4x4` declares 4ch on a 2ch front-end | item 5 |
| SR class B never exercised, engine or bench | — |

---

## 9. Documentation written this session

- **`docs/testing/methodology.md`** — NORMATIVE. Six levels, seven rules
  (R1–R7), what a lane owes, and the "a bug found outside your subject gets a
  new lane with fresh context" rule. Read this first.
- `docs/findings/GPTP_GM_LOSS_UNDER_RX_LOAD.md` — D7, reproduced 2/2.
- `docs/MILAN_COMPLIANCE_GAPS.md` — item 00 updated with what landed.
- `docs/findings/BENCH_TOPOLOGY.md` — the boot provisioning value corrected.
- `docs/reference/REGISTER_MAP.md` — `AAF_CTRL` reset, `CHMAP_SNAP/LOOP`,
  VERSION-as-ATDECC-version.
- Traceability rows across `ieee1722-2016.md`, `ieee1722_1-2021.md`,
  `milan-v12.md`, `ieee8021as.md`, `ieee8021q.md`.

**Memory** (`~/.claude/projects/.../memory/`) carries the durable facts:
`standards-pdfs-are-on-this-box`, `d7-gm-loss-rx-queues-rootcause`,
`tu-bit-lease-fixed-in-software`, `framer-emits-2ch-proven-both-ways`,
`shared-box-parallel-lane-hazards`, the peer AES3 loopback note,
`check-standard-for-expected-behavior`.
