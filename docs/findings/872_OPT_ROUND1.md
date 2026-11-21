# Execution and fabric for 64x64 streams on two interfaces: round 1, measured, modelled and planned (#872)

Status: **measurement and design only**, for the owner's decisions (#872). **Nothing in the product changed.** Measured at `opt-exec-1` =
`origin/dev-soft-core-optimisation` `15168e14` (the flip train's reviewed final head; its firmware and RTL are the
train's measured `8c5e2b4f`'s, the difference being comments and message strings). The decisions marked **OWNER
DECIDES** change the CPU the owner chose (NFR-SCOUT-01) or the mailbox contract, and wait for the owner. Every figure
names its receipt in the round packet (the packet's `INDEX.md` lists them).

## Contents

- **[1. The target](#1-the-target)** -- 64x64/2if, its two readings, the line-rate limit, and the target model.
- **[2. The execution baseline](#2-the-execution-baseline)** -- each source's cost at each shape, the fitted model, the load, every path that grows faster than its streams, and what must fit one pass.
- **[3. The execution levers, ranked](#3-the-execution-levers-ranked)** -- the load each removes at 32x32/2if and 64x64/2if, with its cost and risk.
- **[4. Resources and the restructure](#4-resources-and-the-restructure)** -- where today's LUTs and block RAM go, and the shape of design that fits 64x64/2if (section 4).
- **[5. Silicon on the Arty](#5-silicon-on-the-arty)** -- the same firmware in simulation and on the board, and what disagrees.
- **[6. The plan](#6-the-plan)** -- the lever set, the expected load and area per shape, the work order from round 2, and the owner's decisions.
- **[7. Limits of round 1](#7-limits-of-round-1)**

## 1. The target

**Shapes.** The split places stream n on interface n mod 2 (`ctrl_plat.c` compose; `acmp.sink_interface[n] = n %
MBX_N_IF`). Each shape's sources and sinks include the CRF stream:

| Point | Interfaces | Sources / sinks on the entity | Streams on the busiest interface | Where measured |
|---|---:|---:|---:|---|
| 1x1/1if | 1 | 2 / 2 | 4 | the train's full re-measure at `8c5e2b4f` (every arm, every group) |
| 8x8/1if | 1 | 9 / 9 | 18 | the train's full re-measure at `92de01f7` (byte-identical images to `8c5e2b4f`'s) |
| 8x8/2if | 2 | 9 / 9 | 9 | this lane at `15168e14`: arm A's 12 non-save groups, valid-destinations, answering-later, answering-every-port |
| 16x16/2if | 2 | 17 / 17 | 17 | this lane: a 16x16 simulation shape (half of #859's 32x32) on a scratch port of #859 onto `15168e14`, 8 arm A groups and valid-destinations' 2 |
| 32x32/2if | 2 | 33 / 33 | 33 | this lane: #859's 32x32 shape on the same scratch port, arm A's 19 groups and valid-destinations' 2 (no saved state, as #859 builds it) |
| 64x64/2if (A) | 2 | 65 / 65 | 65 | modelled: #640's naming, as 32x32 is 16x16 logical streams each redundant: 32 a direction on each interface |
| 64x64/2if (B) | 2 | 129 / 129 | 129 | modelled: 64 streams a direction on **each** interface |

**The definition is the owner's (OWNER DECIDES, D1).** Reading B with eight-channel streams cannot be carried on a
1 Gb/s interface: 64 x 16.5 Mb/s is 105.7 % of the line and SRP admits 75 % to classes A and B; it needs at most four
channels a stream (66.4 %). Reading A at eight channels is 52.8 % (section 4.4). This plan targets A and
reports B beside it.

**The target model** (what round 2 onwards must reach, each held by the existing gates):

- **64x64/2if (A):** the long-window load at or under **0.70** by `load_grade.py`'s arithmetic, at the row bounds the
  flip states (tier 1 at 20 ms, SRP 90 ms, the last queued notice 125-140 ms) and the per-pass share of 2.0 ms; room
  for firmware gPTP on both ports (NFR-SCOUT-02, #665 F6), stated as a labelled reservation of 0.10 until F6 measures it;
  the image placed and routed on the xc7a100t with #818's floor (+0.030 ns setup, 0 hold, every corner).
- **32x32/2if, milestone one:** the same, on the way.
- **1x1/1if and 8x8/1if do not regress:** 1x1/1if at or under 0.70 (today 0.511 at the pin), 8x8/1if at or under 0.75
  (today 0.744), their bounds unchanged (the last notice 140 ms, ACMP 30 ms, txL 49 ms at 1x1/1if), and the 1x1 image
  does not grow (#872's acceptance item 3).

## 2. The execution baseline

### 2.1 What was run

The CPU service budget harness, arm A and the arms named below, the formal measurement's options
(`--record-budget-findings --record-share-findings`), the CPU on `sys` at 100 MHz with the split's 16 KiB
instruction cache. Each cost is the most CPU cycles over every instance, extracted by #665 round 28's tools
(`costs24.py`, `parts.py`, `eventcost.py`, `aecp_kinds.py`, unchanged but for reading a simulation shape's own
transmit rings). Receipts: the round packet\'s `exec/`.

- **16x16/2if and 32x32/2if are a scratch port, not a product image.** #859's 32x32 shape (`665-s15-32x32`
  `936e0a56`, 1,224 commits behind this head) was merged into a clone of `15168e14`, 50 conflict hunks resolved
  keeping this head's behaviour (the round packet\'s `port/port32.py`), and the shape made to build at this head: a THE SHAPES
  block, the per-source masks of SRP and MAAP widened to 64 bits (33 sources), SRC_SID and the DA gate mapped to each
  interface's entries (`MBX_ENTRY_ORDINAL`), and four harness fixes (the round packet\'s `port/*.diff`). **Its overhead is in its
  figures**: libgcc's 64-bit shift (`__lshrdi3`) is 2.8 to 3.7 % of the 32x32 service cycles, and the port's two
  entry-to-source loops sit inside MAAP's `declaring` and `srp_mbx_gate`. The shape has no saved state (#859), so its
  save, aged and held-talker groups cannot run; each cost's ratio of all groups to the matched groups at 8x8/2if
  stands in for them (section 2.3).
- **Grading** at 16x16 and 32x32 uses 8x8/2if's stated polls (the shape has none of its own), as S2b round 24 graded
  32x32; its `STATED` lines are those, not findings.

| Point | Groups measured at this head's code | 
|---|---|
| 1x1/1if, 8x8/1if | every arm, every group (the train's re-measure; `8c5e2b4f`, `92de01f7`) |
| 8x8/2if | arm A's 12 non-save groups, valid-destinations (`srp-talker-held`, `srp-talker-loss`), answering-later (`notice-retried-0`), answering-every-port (`notice-every-0`, `notice-burst-0`) |
| 16x16/2if | arm A's `srp`, `backlog-owed`, `backlog-adp-refill`, `control`, `adp-link`, `acmp-noresp`, `maap`, `aecp`; valid-destinations' `srp-talker`, `srp-talker-loss` |
| 32x32/2if | arm A's 19 groups (its saves owed to #823); valid-destinations' `srp-talker`, `srp-talker-loss` |

### 2.2 The load at each point, this head

The gate's own arithmetic (`load_grade.load`), each cost stated by its rule from this head's measurement
(the round packet\'s `exec/load-terms.md`); the points no image is built at are the model's (section 2.3):

| Term | 1x1/1if | 8x8/1if | 8x8/2if | 16x16/2if | 32x32/2if | 64x64/2if (A) * | 64x64/2if (B) * |
|---|---:|---:|---:|---:|---:|---:|---:|
| `srp` | 0.156 | 0.222 | 0.195 | 0.228 | 0.321 | 0.702 | 2.259 |
| `item.mrpdu` | 0.012 | 0.027 | 0.033 | 0.058 | 0.116 | 0.304 | 0.976 |
| `ticks` | 0.047 | 0.046 | 0.046 | 0.060 | 0.112 | 0.213 | 0.416 |
| `timers` | 0.015 | 0.022 | 0.049 | 0.056 | 0.092 | 0.212 | 0.618 |
| `rec.acmp` | 0.041 | 0.045 | 0.043 | 0.053 | 0.069 | 0.100 | 0.162 |
| `item.acmp` | 0.015 | 0.024 | 0.021 | 0.032 | 0.060 | 0.133 | 0.367 |
| `builds` | 0.006 | 0.014 | 0.017 | 0.029 | 0.058 | 0.152 | 0.488 |
| `item.aecp` | 0.032 | 0.031 | 0.060 | 0.050 | 0.055 | 0.054 | 0.060 |
| `rec.aecp` | 0.050 | 0.043 | 0.039 | 0.042 | 0.042 | 0.042 | 0.042 |
| `notices` | 0.002 | 0.008 | 0.011 | 0.020 | 0.037 | 0.073 | 0.143 |
| `steps` | 0.029 | 0.028 | 0.028 | 0.034 | 0.034 | 0.034 | 0.034 |
| `item.reclaim` | 0.020 | 0.015 | 0.026 | 0.021 | 0.031 | 0.031 | 0.047 |
| `rec.adp` | 0.011 | 0.013 | 0.013 | 0.017 | 0.025 | 0.039 | 0.070 |
| `item.acmp_declined` | 0.012 | 0.017 | 0.011 | 0.019 | 0.023 | 0.037 | 0.066 |
| `rec.maap` | 0.005 | 0.009 | 0.008 | 0.012 | 0.019 | 0.033 | 0.061 |
| `item.walk` | 0.003 | 0.004 | 0.005 | 0.010 | 0.017 | 0.029 | 0.054 |
| `gm` | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| **load** | **0.456** | **0.568** | **0.605** | **0.741** | **1.111** | **2.189** | **5.863** |
| compute for 0.70 | 1.00x | 1.00x | 1.00x | 1.06x | 1.59x | 3.13x | 8.38x |
| a pass's own cost (events' fixed part + the polls' base), us | 240 | 330 | 330 | 495 | 855 | 1,570 | 3,005 |

\* modelled: the fit of section 2.3 at the point's streams. 1x1/1if, 8x8/1if and 8x8/2if are measured at this head; 16x16/2if and 32x32/2if are measured, each cost raised to the model where the model, with the held groups' ratio, is higher (the groups a store-less shape cannot run).

**Against the gate as it stands** (`load_grade.py --check` at this head): 1x1/1if 0.511 (0.508 with tsn-c-stack#32),
8x8/1if 0.744, 8x8/2if 0.799, 32x32/2if 2.175. The gate's statements keep the most any image measured since S2b, and
its 32x32/2if column is `a30c9986`'s and `3a1d14c2`'s image: the train's cuts took this head's 32x32/2if SRP record
from the 865 us stated to 390 us measured (535 with the held groups' ratio), and a build of one MRPDU from 7,485 us
to 2,045 us measured (valid-destinations' `srp-talker-loss`; 845 in arm A). **So 32x32/2if at this head is about 1.1,
not 2.2**: 1.59 times the compute for 0.70, not 2.41.

### 2.3 The cost model

Each cost's maxima over the groups every point ran (matched) are fitted against the streams the code walks: P, the
streams on the busiest interface (SRP and lwSRP's costs, which walk one interface's participants), or E, the entity's
(every other). A line, except where the code has a named quadratic path (an SRP record and its retained retry, and a
build of one MRPDU, section 2.4). Each
cost is then multiplied by its ratio, all groups to matched, at 8x8/2if, for the groups a store-less shape cannot run
(the held talker raises an SRP record 1.38 times, a build of one 1.34, an AECP notice 4.0: 32 recipients against 2).
Fits and residuals: the round packet\'s `exec/costs-fit.md`, `model2-out.json`.

| Cost (CPU cycles) | X | fit | 1x1/1if | 8x8/1if | 8x8/2if | 16x16/2if | 32x32/2if | 64x64/2if (A) | 64x64/2if (B) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `record.srp` | P | 23,260 - 80 X + 14.8 X^2 | 24,662 | 34,803 | 30,582 | *36,109* | *50,713* | *111,359* | *358,407* |
| `build_one` | P | 40,300 + 2,010 X + 81.1 X^2 | 53,827 | 123,076 | 75,018 | *131,086* | *261,004* | *687,619* | *2,207,970* |
| `base` | E | 7,133 + 991 X | 19,359 | 27,896 | 26,841 | *43,995* | *78,164* | *146,504* | *283,182* |
| `centisecond` | E | 1,571 + 796 X | 15,672 | 26,692 | 30,778 | *54,465* | *102,912* | *199,806* | *393,594* |
| `record.acmp` | E | 16,926 + 228 X | 19,427 | 21,368 | 20,264 | *25,034* | 32,445 | *47,257* | *76,889* |
| `record.adp` | E | 7,560 + 227 X | 9,585 | 11,937 | 11,433 | *15,271* | 22,863 | *37,043* | *66,072* |
| `record.aecp` | E | 14,662 + 0 X | 23,726 | 20,202 | 18,391 | *19,808* | *19,808* | *19,808* | *19,808* |
| `record.maap` | E | 8,282 + 415 X | 10,411 | 16,176 | 15,526 | *22,378* | 35,808 | *62,177* | *115,244* |
| `event.ACMP` | E | 11,612 + 226 X | 13,859 | 16,373 | 16,805 | *19,827* | 27,400 | *42,139* | *71,887* |
| `event.MAAP` | E | 11,413 + 409 X | 12,637 | 19,007 | 20,221 | *26,065* | *39,544* | *66,501* | *120,416* |
| `event.ADP` | E | 6,872 + 6 X | 7,257 | 6,981 | 7,296 | 8,170 | *7,258* | *7,632* | *8,381* |
| `item.acmp` | E | 3,365 + 130 X | 4,739 | 6,217 | 5,118 | *7,793* | 12,239 | *20,296* | *36,967* |
| `item.aecp.notice` | E | 4,992 + 5 X | 14,084 | 13,414 | 25,605 | *20,775* | 22,974 | *22,841* | *25,595* |
| `item.reclaim` | P | 1,429 + 21 X | 1,767 | 995 | 2,205 | *1,779* | 2,662 | *2,768* | *4,086* |
| `item.walk` | P | 939 + 170 X | 2,105 | 3,300 | 2,072 | 4,214 | 6,797 | *12,008* | *22,908* |

Italic: the model (the fit at the point, times the held groups' ratio where the point cannot run them); plain: measured, all groups.

### 2.4 Where the CPU goes, and what grows faster than its streams

**A pass's polls dominate at scale.** The polls' base, a pass with nothing to do, fits 7,133 + 991 cycles a stream
of the entity over the matched groups: 13,430 cycles at 1x1/1if, 72,331 at 32x32/2if, about 147,000 projected at
64x64/2if (A), 1.5 ms of THE SHARE's 2.0 ms, and 2.8 ms at (B), past it. It is not a load term (the gate reports it
beside the load) but every pass of every row pays it. By function (the round packet\'s `exec/func-*.md`, the harness's committed pcs attributed to the linked
functions, service only):

| Function (source) | 1x1/1if, `control` | 8x8/2if, `control` | 32x32/2if, `control` |
|---|---:|---:|---:|
| `deliver` (`ctrl_app_srp.c:50`: every source's Listener presence, every sink's request, each interface's gate, every pass) | 4.1 % | 7.5 % | 15.4 % |
| `declaring` and `refresh_demand` (`maap_mbx.c:60`, `:42`: every source, every interface, every pass) | under 2.5 % | 7.2 % | 12.5 % + |
| `acmp_declaring` (`acmp.c:1340`: `enter`, `now`, a `memset` and three `source` callbacks, a source a call) | 2.3 % | 4.9 % | 10.7 % |
| `memset` (mostly `acmp_declaring`'s) | 2.7 % | 5.2 % | 9.8 % |
| `source` callbacks (`ctrl_app_srp.c:17`, `ctrl_app_aecp.c:17`, the image's) | under 2.5 % | 5.5 % | 6.6 % |
| the `poll`s (`srp_mbx.c:1272`, its `snapshot` and licence scan of every source each pass; `maap_mbx.c:222`; `aecp_mbx.c:185`), and `snapshot` | 8.2 % | 10.7 % | 15.1 % |
| `srp_mbx_gate` (`srp_mbx.c:785`, called a pass an interface) | under 2.5 % | under 2.5 % | 4.0 % |
| **the per-stream polling above, together** | **about 20 %** | **about 41 %** | **about 74 %** |

(The profile attributes cycles to functions by name, so the static functions of one name are added: the `deliver`
row is `ctrl_app_srp.c`'s, the larger of the two; `ctrl_app_aecp.c`'s is 2.6 to 3.1 %. The 32x32 column carries the
port's overhead in `declaring` and `srp_mbx_gate`; `__lshrdi3`, 2.8 %, is not in it. 1x1/1if and 8x8/2if are this
head's own code.)

**Every path that grows faster than its streams, by code location:**

| Path | Code | Growth | Measured |
|---|---|---|---|
| a received SRP attribute scans every sink (`interested_msrp`), every source (`sources_of`), and lwSRP scans every attribute twice (`find_attr`, the replace loop) | `srp_mbx.c:430`, `:96`, `:205` `listener`, `:487` `listener_moved`; `third_party/lwSRP/src/core/mrp_mad.c:442`, `:1032` | k attributes x (A + S + K): quadratic | record.srp 23,260 - 80 P + 14.8 P^2 (residuals in `costs-fit.md`): 36,819 at 32x32, 81k at P = 65 and 260k at P = 129 before the held groups' ratio (1.38) |
| a build's post-send loop calls each attribute's observer, `listener_moved` and so `sources_of` over every source; the build sorts each type's vectors by swapping them backwards | `mrp_mad.c:1504` (the post-send loop), `srp_mbx.c:487`, `:96`; `mrp_mad.c:1379` (`tx_message`) | attributes x sources, and n^2 a type | build_one 40,300 + 2,010 P + 81 P^2: 194,669 measured at 32x32/2if (2.05 ms, over THE SHARE), 688k modelled at 64x64/2if (A) |
| the per-port audio map capacity is the entity's channel count | `AECP_ENTITY_MAP_ROWS` = ports x `AECP_ENTITY_MAP_MAX` (`aecp_entity_gen.h`) | quadratic memory | 4.6 / 17.4 / 67.6 KB at 8x8 / 16x16 / 32x32 |
| every armed lwSRP timer is visited each centisecond | `third_party/lwSRP/src/ports/timer.c:25` (`shlan_timer_tick`) | timers a centisecond | inside the centisecond (1,571 + 796 E; 56,748 measured at 32x32/2if) |
| every source and sink polled every pass (the table above) | `ctrl_app_srp.c:50`, `maap_mbx.c:42`, `:60`, `acmp.c:1340`, `srp_mbx.c:1346-1364` | streams x passes | the polls' base, 991 cycles a stream |
| lwSRP's pool sized for every entity stream on each interface | `image_arena` (`SRP_POOL_ARENA_BYTES`) | streams x interfaces memory | 48 / 80 / 145 KB at 8x8/2if / 16x16 / 32x32 |

Everything else is linear in its streams (record.acmp 16,926 + 228 E, record.adp 7,560 + 227 E, record.maap 8,282 +
415 E, event.ACMP 11,612 + 226 E, event.MAAP 11,413 + 409 E, item.acmp 3,365 + 130 E) or flat (an AECP record, a
notice by its recipients, a TICK, a GM event, a response).

### 2.5 What must fit one pass

THE SHARE (2.0 ms, 200,000 CPU cycles) binds three costs before the load does, because each runs inside one pass:

| Cost (CPU cycles) | 8x8/2if measured | 32x32/2if measured | 32x32/2if with the held groups' ratio | 64x64/2if (A), modelled |
|---|---:|---:|---:|---:|
| a build of one MRPDU (THE TRANSMIT, a pass given whole) | 75,018 | **194,669** | 261,000 | 688,000 |
| a centisecond's consumers | 30,778 | 56,748 | 103,000 | 200,000 |
| the polls' base (every pass) | 26,841 | 72,331 | 78,000 | 147,000 |

**At 32x32/2if a build already runs past THE SHARE**: `srp-talker-loss` counts 2 of its 14,088 work passes over it
(the round packet\'s `exec/costs-32x32/`). A build costs about 5,900 cycles a stream on the interface at 32x32/2if (194,669 over
33: the encode, the backwards insertion sort, the post-send loop whose observer calls `listener_moved` and so
`sources_of` over every source). For 64x64/2if (A)'s 65 streams an interface to build inside a slice (at most THE SHARE less its margin, 1,935 us),
with the held groups' ratio of 1.34, the cuts L3 and L4 must bring it under about 2,200 cycles a stream, or THE
TRANSMIT must build in slices across passes, which sends more MRPDUs and needs a ruling. L2 and L5 take the polls' base and the centisecond out of
the way.

**#928's CPU levers at 32x32/2if, re-measured at this head** (four arm A groups, every work pass's cycles,
the round packet\'s `exec/cmp-32x32.txt`): **the 32 KiB instruction cache -0.3 % CPU time** (median; -1.9 to +0.2 %), 64 KiB
-0.7 % (-2.2 to 0), **RV32IMC +1.6 %** (+1.1 to +1.7 %), against #928's -6 to -14 % and -3 to -7 % at 1x1/1if and
8x8/1if. The 16 KiB cache already misses 0.9 to 1.6 times a thousand instructions at 32x32/2if: the per-stream loops
keep the code hot. RV32IMC halves those refills but its aligner costs more than they save. **Neither is an execution
lever at scale.** RV32IMC keeps its memory value (-29 KB of rom at 32x32/2if, about 7 RAMB36).

## 3. The execution levers, ranked

Each lever's load is the model's: this head's measured costs (section 2) with the lever's factors on the costs it
moves, through the gate's arithmetic (the round packet\'s `exec/levers-out.json`, `levers.py`). **The firmware cuts' factors
are estimates** from the measured scaling and the code (each lever's basis below); round 2 measures each cut it
builds. The CPU levers' factors are round 1's measurements at 32x32/2if, or the clock's ratio.

### 3.1 Each lever alone, against this head (load removed)

| Lever | 32x32/2if | 64x64/2if (A) | 64x64/2if (B) |
|---|---:|---:|---:|
| L3 SRP stream_id and attribute indexes: hashed lookups in place of per-attribute scans | +0.102 | +0.482 | +2.106 |
| L9 the CPU and bus at 125 MHz (OWNER DECIDES; #818 grades it) | +0.205 | +0.409 | +1.127 |
| L5 timers: lwSRP's timer list (ports/timer.c:25 walks every armed timer a centisecond) and the per-sink timer scans as a wheel | +0.091 | +0.239 | +0.613 |
| L1 statement: an owed MRPDU measured, resent from lwSRP's prepared PDU (mrp_transmit keeps it), not stated at a build of one | +0.076 | +0.197 | +0.634 |
| L6 ACMP and ADP sink indexes (the record finds its sink by stream or entity, not by a walk) | +0.039 | +0.070 | +0.149 |
| L4 lwSRP's build: a stable merge sort of an index in place of tx_message's byte-swapping insertion sort | +0.012 | +0.030 | +0.097 |
| L8 32 KiB instruction cache (#928; OWNER DECIDES, NFR-SCOUT-01) | +0.003 | +0.004 | +0.013 |
| L2 event-driven polls: dirty masks in place of every-pass scans of every source and sink | +0.001 | +0.001 | +0.002 |
| L7 RV32IMC (#928; OWNER DECIDES, NFR-SCOUT-01) | -0.017 | -0.034 | -0.089 |

(Load removed: a positive figure is a saving, a negative one adds load.)

### 3.2 The levers in order (the load after each, cumulative)

| After | 1x1/1if | 8x8/1if | 8x8/2if | 16x16/2if | 32x32/2if | 64x64/2if (A) | 64x64/2if (B) |
|---|---:|---:|---:|---:|---:|---:|---:|
| L0 this head, measured and modelled | 0.456 | 0.568 | 0.605 | 0.741 | 1.111 | 2.189 | 5.863 |
| L1 statement | 0.448 | 0.550 | 0.584 | 0.704 | 1.035 | 1.992 | 5.229 |
| L2 event-driven polls | 0.448 | 0.550 | 0.583 | 0.703 | 1.035 | 1.990 | 5.226 |
| L3 SRP stream_id and attribute indexes | 0.447 | 0.540 | 0.579 | 0.693 | 0.945 | 1.538 | 3.215 |
| L4 lwSRP's build | 0.446 | 0.540 | 0.578 | 0.691 | 0.935 | 1.512 | 3.132 |
| L5 timers | 0.445 | 0.536 | 0.569 | 0.667 | 0.844 | 1.272 | 2.519 |
| L6 ACMP and ADP sink indexes (the record finds its sink by stream or entity, not by a walk) | 0.429 | 0.514 | 0.550 | 0.641 | 0.806 | 1.201 | 2.369 |
| L7 RV32IMC (#928; OWNER DECIDES, NFR-SCOUT-01) | 0.436 | 0.521 | 0.563 | 0.648 | 0.818 | 1.219 | 2.402 |
| L8 32 KiB instruction cache (#928; OWNER DECIDES, NFR-SCOUT-01) | 0.434 | 0.520 | 0.562 | 0.647 | 0.813 | 1.215 | 2.391 |
| L9 the CPU and bus at 125 MHz (OWNER DECIDES; #818 grades it) | 0.360 | 0.423 | 0.461 | 0.543 | 0.678 | 1.004 | 1.964 |
| a pass's own cost after L1-L6, us | 170 | 130 | 135 | 130 | 145 | 170 | 230 |

- **L1 statement**: an owed MRPDU measured, resent from lwSRP's prepared PDU (mrp_transmit keeps it), not stated at a build of one. Basis: mrp_transmit skips the build while prepared_pdu is set (mrp_mad.c:1426); the resend is the ring copy and the post-send loop over the attributes: 0.35 of a build, an estimate to be measured by a group that fills the SRP ring at a build.
- **L2 event-driven polls**: dirty masks in place of every-pass scans of every source and sink. Basis: ctrl_app_srp.c deliver (every source's presence, every sink's request), maap_mbx.c refresh_demand and declaring (acmp_declaring a source a pass, its memset and three source callbacks), srp_mbx.c poll's snapshot and licence scan: about 74 % of the service cycles at 32x32/2if in arm A's groups (FUNC profile); the polls' base from section 2.3's a + b E to a + 40 E cycles.
- **L3 SRP stream_id and attribute indexes**: hashed lookups in place of per-attribute scans. Basis: interested_msrp (srp_mbx.c:430) scans every sink, sources_of (:96) every source, a received attribute each, and lwSRP's find_attr (mrp_mad.c:442) and the replace loop (:1032) every attribute: the record's fitted c P^2 term; indexed, a + 150 P (estimate); the build's post-send observer calls (listener_moved, sources_of) the same: 0.85 (estimate).
- **L4 lwSRP's build**: a stable merge sort of an index in place of tx_message's byte-swapping insertion sort. Basis: tx_message (mrp_mad.c:1379) inserts each value by swapping whole vectors backwards: O(n^2) compares and byte swaps a type; 5 % below 20 streams an interface, 20 % above (estimate).
- **L5 timers**: lwSRP's timer list (ports/timer.c:25 walks every armed timer a centisecond) and the per-sink timer scans as a wheel. Basis: the centisecond fits a + b E (x the held groups' ratio); a wheel visits only what expires; an ACMP timer event finds its sink by the slot, not by a walk of every sink: 0.5 (estimate).
- **L6 ACMP and ADP sink indexes (the record finds its sink by stream or entity, not by a walk)**. Basis: record.acmp fits 16,926 + 228 E and record.adp 7,560 + 227 E (section 2.3): the slope is a record's walk over the sinks; indexed, 0.75 and 0.7 (estimate).
- **L7 RV32IMC (#928; OWNER DECIDES, NFR-SCOUT-01)**. Basis: measured at 32x32/2if round 1: +1.1 to +1.7 % CPU time (median +1.6 %) over four groups; -29 KB rom (-7 RAMB36).
- **L8 32 KiB instruction cache (#928; OWNER DECIDES, NFR-SCOUT-01)**. Basis: measured at 32x32/2if round 1: -1.9 to +0.2 % (median -0.3 %), +4 RAMB36.
- **L9 the CPU and bus at 125 MHz (OWNER DECIDES; #818 grades it)**. Basis: every stated cost is CPU cycles at 100 MHz: x 100/125; the mailbox and datapath paths are placement-thin at 8x8/1if (#928), so the route is the risk.

### 3.3 Each lever, what it costs and what it changes

| Lever | Kind; proof of equivalence | Fabric | Firmware memory | Timing risk | Mailbox contract; firmware |
|---|---|---|---|---|---|
| **L1** an owed MRPDU measured, not stated | harness and statement; nothing in the product moves. `mrp_transmit` resends `prepared_pdu` without a build (`mrp_mad.c:1426`), so the gate's rule (an owed MRPDU at a build of one's) overstates it. Needs a group that fills the SRP ring at a build, and the manager's ruling to restate | none | none | none | none; the harness gains a group |
| **L2** event-driven polls | firmware, exact equivalent: each producer sets a dirty bit (SRP's presence change, a request, MAAP's DA validity, ACMP's answered flag with its `da_fresh_ms` deadline, a licence input), the poll visits the set bits (count-trailing-zeros) instead of every stream. Proof: the pass's outputs (every mailbox write, every callback, in order) identical to the scan's over the harness's arms, and a host differential test that runs both on random event sequences; a planted mutant that drops one producer's dirty bit must fail it | none | about 1 KB (masks) | none | none; `ctrl_app_srp.c`, `maap_mbx.c`, `acmp.c` (tsn-c-stack), `srp_mbx.c` |
| **L3** SRP stream_id and lwSRP attribute indexes | firmware and lwSRP, exact equivalent: a hash of stream_id to the source mask and sink index per interface (rebuilt at bind, declare and gate changes), and per participant a hash of (type, value) to the attribute, kept beside the list (insert, free and reclaim update both). Proof: every MRPDU byte and every observer call identical (differential test over the lwSRP suite's sequences and the harness's), mutants: a stale index entry after a reclaim, a hash collision path | none | about 2 to 4 KB | none | none; `srp_mbx.c`, `third_party/lwSRP` |
| **L4** lwSRP's build sorts an index | lwSRP, exact equivalent: a stable merge sort of an index of the selected attributes, then one encode pass; insertion sort and this sort give the same order for every input (both stable on equal keys). Proof: the MRPDU bytes identical; mutant: an unstable sort | none | under 1 KB | none | none; `mrp_mad.c` `tx_message` |
| **L5** timer wheel | lwSRP and firmware, exact equivalent: `shlan_timer_tick` visits only the timers that expire this centisecond (a wheel of 256 slots and a far list), the ACMP timer event finds its sink by the slot. Proof: every callback at the same centisecond in the same order; mutant: a timer re-armed inside its own callback | none | about 1 KB | none | none; `third_party/lwSRP/src/ports/timer.c`, `acmp_mbx.c` |
| **L6** ACMP and ADP sink indexes | firmware and tsn-c-stack, exact equivalent: a record finds its sink by stream or by entity through an index, not a walk | none | about 1 KB | none | none; tsn-c-stack ACMP and ADP cores |
| **L7** RV32IMC | CPU (OWNER DECIDES, NFR-SCOUT-01) | CPU about +200 LUT, +90 FF (#928) | -29 KB rom at 32x32/2if | none measured (#928) | none |
| **L8** 32 KiB instruction cache | CPU (OWNER DECIDES, NFR-SCOUT-01) | +4 RAMB36 | none | none measured (#928) | none |
| **L9** the CPU and bus at 125 MHz | clock (OWNER DECIDES); #818's floor grades it | none | none | **high**: today's 8x8/1if routes keep +0.001 to +0.433 ns at 10 ns (#928) on the mailbox and datapath paths; at 8 ns they fail unless the restructure (section 4) removes the per-stream multiplexers | none |
| **L10** a second hart (#872 option a) | CPU (OWNER DECIDES, NFR-SCOUT-01/03: one control hart is a requirement) | about +3.8k LUT, +4.4k FF, +6 RAMB36 and 9 RAMB18 with its caches (this head's CPU subtree, the round packet\'s `res/hier-8x8.rpt`); built at 32x32 and above only, so 1x1 does not grow | its own stack and data | low (a second instance of a core that closes with +0.08 to +0.97 ns) | **changes the contract**: each hart owns its channels (SRP and ACMP on one; AECP, ADP, MAAP and the store on the other), and five cross-hart queues (ADP to ACMP availability, MAAP to SRP's gate, SRP to AECP's notices, ACMP to AECP's stream state, AECP to ACMP's start and stop) |
| **L11** a faster core at 100 MHz (#872 option b: dual issue, branch prediction) | CPU (OWNER DECIDES) | not measured: about +1.5 to +3k LUT (estimate) | none | medium | none; round 2 measures it (the harness builds any generator configuration) |

**The second hart, after the firmware cuts** (L1 to L6), each hart's share of the load:

| Point | SRP / the rest | SRP + ACMP / AECP + ADP + MAAP + store |
|---|---:|---:|
| 1x1/1if | 0.188 / 0.241 | 0.243 / 0.185 |
| 8x8/1if | 0.254 / 0.260 | 0.322 / 0.192 |
| 8x8/2if | 0.250 / 0.300 | 0.310 / 0.240 |
| 16x16/2if | 0.296 / 0.344 | 0.380 / 0.261 |
| 32x32/2if | 0.368 / 0.438 | 0.489 / 0.317 |
| 64x64/2if (A) | 0.542 / 0.659 | 0.753 / 0.448 |
| 64x64/2if (B) | 1.095 / 1.274 | 1.561 / 0.808 |

## 4. Resources and the restructure

### 4.1 Why today's shape cannot scale

The 1x1/1if and 8x8/1if images at this head were routed on the AX7101's xc7a100t-2 (the train's gate at `8c5e2b4f`,
whose RTL is this head's). Their hierarchical utilization (the round packet\'s `res/hier*.rpt`):

| Image | LUT | FF | RAMB36 / RAMB18 | DSP | Slices |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 32,714 | 42,628 | 62 / 36 | 11 | (see util-1x1.rpt) |
| 8x8/1if | 42,988 | 50,993 | 78 / 33 | 11 | 98.6 % (the train's figure) |

The seven extra streams of each direction cost +10,274 LUT and +8,365 FF, after the 8x8 build drops the 1x1's
latency taps and TDM render (-2,256 LUT, -2,117 FF). So one stream pair costs about **1,790 LUT and 1,500 FF**, almost
all in flip-flops and multiplexers that hold or select per-stream state:

| Block (8x8/1if) | LUT 1x1 -> 8x8 | FF 1x1 -> 8x8 | What grows |
|---|---:|---:|---|
| `KL_mbx_cdc/u_edit` | 514 -> 3,743 | 424 -> 451 | the EDIT window's per-stream map selection (multiplexers) |
| `milan_datapath` (own logic) | 1,592 -> 4,175 | 2,884 -> 7,052 | per-stream gates, registers and their selection |
| `milan_datapath/csr` | 2,421 -> 4,104 | 1,718 -> 1,836 | the CSR read multiplexer over per-stream registers |
| `avtp_rx_monitor` | 737 -> 2,071 | 743 -> 1,674 | already one engine over a context RAM; its per-stream seen flags and walker state are flops |
| `talker_diag` | 208 -> 771 | 357 -> 1,512 | per-stream talker counters in flops |
| `stream_table` | 59 -> 564 | 69 -> 552 | per-stream comparators |
| `aaf_packetizer` | 663 -> 1,100 | 1,332 -> 1,469 | per-stream header state |
| `KL_mbx_cdc/u_gsi`, `u_pub` | 373 -> 1,066 | 1,209 -> 3,085 | the publication block's per-stream words crossed in flops |
| `chan_map_capture`, `render_queue` | 1,271 -> 1,980 | 1,417 -> 1,920 | per-stream map and queue state |

The shape-independent part is large too: the CPU 3.8-4.0k LUT, the mailbox `KL_mbx` 5.5k LUT and 8.8k FF, the gPTP
plane 5.9k LUT, the MMCM servo 1.3k, the CSR base 2.4k.

**Today's structure at the target**, scaled at 1,790 LUT a stream pair: 32x32/2if about 88k LUT and 64x64/2if about
145k LUT against the device's 63,400. It cannot fit, at any packing. (An estimate by linear scaling: the routed
figure would be worse, since 8x8/1if already binds on slices at 98.6 %.)

**The firmware's memory binds as well**, and grows faster than linearly. The split image's largest objects, measured
on the harness's images at this head (the round packet\'s `exec/symbols.md`):

| Object | 1x1/1if | 8x8/1if | 8x8/2if | 16x16/2if | 32x32/2if | Growth |
|---|---:|---:|---:|---:|---:|---|
| `image_arena` (lwSRP's attribute pool) | 9,920 | 24,032 | 48,064 | 80,320 | 144,832 | per stream, on **each** interface |
| `aecp_entity_image` (descriptor image, rom) | 7,512 | 19,520 | 19,520 | 36,176 | 69,488 | about 1 KB a stream |
| `image_maps` (audio maps) | 0 | 4,608 | 4,608 | 17,408 | 67,584 | **quadratic**: ports x entity channels |
| `image_values` (names and values) | 4,527 | 11,753 | 11,753 | 21,657 | 41,465 | about 600 B a stream |
| plan, RAMB36 (rom + sram) | 43.0 | 56.0 | 60.5 | 72.5 | 118.5 | against the 56 budget (each image build's own plan at this head) |

At 64x64/2if (A) the same rules give about 920 KB, 200 to 240 RAMB36 of firmware memory alone (the maps x 3.9, the pool and the descriptors x 2, before the banks' power-of-two rounding), against the device's 135.

### 4.2 The shape of the design: one engine, many contexts

Every per-stream function the datapath runs at packet rate is a small state machine over a few hundred bits of
state. At 1 Gb/s the packet rates are low against the clock (section 4): one engine has time to serve every stream
of both interfaces if the state lives in block RAM and the engine is time-multiplexed over it. So the target design is:

1. **Stream state in block RAM, never in flops.** Each STREAM_INPUT and STREAM_OUTPUT is a row of a context RAM; the
   CPU writes the configuration words in place through the RAM's second port, which is also the clock-domain crossing
   (a dual-clock RAMB36 replaces the per-bit handshakes of `KL_mbx_cdc/u_pub` and `u_gsi`).
2. **One listener engine for both interfaces** (prototype `KL_opt_rx_ctx`): a frame's context is read, updated and
   written in four clocks; counters live in a block RAM incremented by a read-modify-write queue; the 100 ms silence
   rule is a walker over each context's last-seen time, not a timer per stream.
3. **Redundancy as shared work**: the two copies of a logical stream share one dedupe word (the last sequence number
   accepted from either interface); the first copy is rendered, the other is counted and dropped, so the render and
   the media clock path run once per logical stream.
4. **A hashed stream_id lookup in block RAM** (prototype `KL_opt_sid_cuckoo`): two tables in one true-dual-port RAM,
   one read of each per lookup, one lookup a clock; the CPU places keys at bind time (the cuckoo insert), so the
   datapath never searches and holds no comparator a stream.
5. **One talker engine for both interfaces** (prototype `KL_opt_tx_engine`): each observation interval it walks the
   contexts, builds each header once and emits it to each interface the stream is declared on, with the per-interface
   fields (DA, VID, stream_id, SA) from the context, and a zero-copy payload descriptor: the samples are read in place
   from the capture ring, so nothing copies them.
6. **Shared sample memory**: one capture ring and one render memory in block RAM, indexed by (stream, channel,
   slot); the maps become a table the render and the packetizer read, sized by the physical channels.
7. **Counters and diagnostics in block RAM** (talker and listener), read in place by the CPU.
8. **The CSR file as a block RAM** behind a small decoder for the few live registers, in place of a read
   multiplexer over every register.

What stays per interface: the MAC and PHY, the gPTP port, the receive parser (one byte a clock at GMII) and the
transmit FIFO. What stays shared and unchanged: the CPU, the mailbox's rings, the gPTP shadow and the media clock
servo.

### 4.3 The prototypes, measured

Out-of-context synthesis, placement and routing on xc7a100t-2 (the round packet\'s `proto/ooc/`), sized for 64 logical streams
a direction, each on both interfaces (128 STREAM_INPUT contexts): reading B of section 1, twice reading A.
Fmax is 1 / (period - WNS) of a route at a 4.0 ns constraint.

| Block | Serves | LUT | FF | Slices | RAMB36 + RAMB18 | DSP | WNS at 125 MHz | Fmax |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `KL_opt_sid_cuckoo` | 512 entries (128 keys at 25 % load) | 88 | 151 | 48 | 2 + 0 | 0 | +3.889 ns | 281 MHz |
| `KL_opt_rx_ctx` | 128 STREAM_INPUT contexts, 16 counters each, 64 dedupe words | 226 | 132 | 80 | 2 + 2 | 0 | +1.168 ns | 146-161 MHz |
| `KL_opt_tx_engine` | 64 logical STREAM_OUTPUTs, both interfaces | 278 | 439 | 141 | 1 + 0 | 0 | +3.011 ns | 200-269 MHz |
| **all three** | | **592** | **722** | **269** | **5 + 2** | 0 | | |

For comparison, today's design spends about 1,790 LUT and 1,500 FF on **each** stream pair.

**Behaviour, tested** (the round packet\'s `proto/tb/`, Verilator, self-checking): 128 random keys placed by the software cuckoo
insert are all found with their values, and 4,000 absent keys all miss; on a redundant pair each sequence number is
accepted once and its copy dropped and counted; a run lost on one interface is filled from the other; a late copy is
dropped; the 8-PDU settle locks at the ninth in-order PDU and not before; one lost PDU is a mismatch and no
interruption, two lost are both, and a stopped input counts no interruption; 100 ms of silence unlocks both copies
once; an unbound context counts nothing. Measured throughput: 8.44 clocks a frame, 14.8 Mframes/s at 125 MHz, 14.5
times the 1.02 Mframes/s that 64 streams on each of two interfaces bring. **Seven planted defects each fail the test**
(dedupe off, the window off by one, the silence doubled, lock at seven, one lost counted as an interruption, a hash
the writer does not share, one slot compared): `mutants.txt`.

Not yet prototyped: the payload mover and the shared sample memory, the CSR block RAM and the mailbox's rings in
block RAM. Their figures below are estimates.

### 4.4 Throughput at 1 Gb/s

Class A, an observation interval of 125 us, AAF at 48 kHz (6 samples a frame, 32-bit containers), 802.1Q tagged:

| Channels a stream | Frame, B | On the wire, B | A stream | 32 streams | 64 streams |
|---:|---:|---:|---:|---:|---:|
| 1 | 70 | 90 | 5.8 Mb/s | 18.4 % | 36.9 % |
| 2 | 94 | 114 | 7.3 Mb/s | 23.3 % | 46.7 % |
| 4 | 142 | 162 | 10.4 Mb/s | 33.2 % | 66.4 % |
| 8 | 238 | 258 | 16.5 Mb/s | 52.8 % | **105.7 %** |

SRP admits at most 75 % of a port to classes A and B. So **64 eight-channel streams a direction on one 1 Gb/s
interface cannot be carried**: the reading "64 streams a direction on each interface" needs at most four channels a
stream. The reading that follows #640's naming of 32x32 (16x16 logical streams, each redundant on both networks) puts
32 streams a direction on each interface, 52.8 % at eight channels.

Packet rates: 64 streams a direction on an interface are 512 kframes/s; both interfaces' listeners are 1.02 Mframes/s,
122 clocks a frame at 125 MHz for one shared engine, which needs 8.44 (measured). The talker engine emits 12 words a
stream an interface an interval: 1,536 of the 15,625 clocks of a 125 us interval at 125 MHz for 64 streams on both
interfaces (9.8 %). The stream_id lookup takes one clock a frame.

### 4.5 Budget for 64x64/2if (estimate, anchored on the measured blocks)

| Part | Today, 8x8/1if, LUT | 64x64/2if restructured, LUT | Basis |
|---|---:|---:|---|
| CPU (VexiiRiscv, 16 KiB I-cache) | 3,775 | 3,800 | measured; unchanged |
| mailbox `KL_mbx` + `KL_mbx_dma` | 6,259 | 4,500 | estimate: rings and publication words in block RAM |
| `KL_mbx_cdc` | 5,553 | 800 | estimate: dual-clock RAM tables in place of per-bit crossings |
| gPTP plane (one port today) | 5,860 | 8,800 | estimate: a second port for the second interface, 1.5x |
| MMCM servo, media grid, ts, ptp_sync | 2,093 | 2,100 | measured; unchanged |
| CSR | 4,104 | 1,000 | estimate: a block RAM register file |
| stream engines (lookup, listener, talker) | 4,505 (monitor, packetizer, diag, table) | 600 | **measured prototypes** |
| sample memory, maps, depacketizer, payload mover | 2,189 | 1,500 | estimate |
| datapath own logic, CRF, top, MACs | 6,800 | 7,000 | estimate: a second MAC, the rest unchanged |
| **total** | **42,988** | **about 30,100** | |

So the restructured 64x64/2if sits near today's 1x1/1if (32,714 LUT), well under the device, with the stream count
moving block RAM bits rather than slices: about 7 RAMB36-equivalents for every stream context, counter and lookup of
64x64/2if (measured prototypes), plus the sample memory (6 RAMB36 for 64 mapped channels with 2 ms of buffering at
32 bits; estimate).

**The firmware memory is the harder half.** Four changes, each an exact equivalent to be proven by the firmware's
tests, bring 64x64/2if's estimated 200 to 240 RAMB36 of firmware memory to about 70 to 90:

| Change | Today | After | 64x64/2if saving, estimate |
|---|---|---|---:|
| lwSRP's pool sized per interface by the placement (stream n on interface n mod 2), not for every entity stream on each | 2 x (S+K) attributes | its own streams | about 140 KB (35 RAMB36) |
| the audio maps' rows from one pool bounded by the entity's channels, not ports x channels | quadratic | linear | about 250 KB (62 RAMB36) |
| the descriptor image generated from a template a descriptor kind plus each index's fields (precomputed response templates) | 1 KB a stream | a few KB | about 125 KB rom (31 RAMB36) |
| an attribute instance's 48-byte pending-flush copy pooled, its timer in a shared wheel | about 150 B | about 80 B | about 70 KB (17 RAMB36) |
| RV32IMC (#928, OWNER DECIDES) | | | 33 KB rom (8 RAMB36) |

### 4.6 Risks

- Timing: `KL_opt_rx_ctx` closes 125 MHz with +1.168 ns but not 200 MHz (Fmax 146-161 MHz); its combinational update
  is the path. A pipelined update (two stages) is the remedy if the datapath clock rises.
- The cuckoo writer must keep the load factor low (two tables of 256 for 128 keys); an insert that loops (64 kicks) is
  a bind refusal the firmware has to report. At 25 % load two-way cuckoo inserts do not fail in practice; a stash
  entry would make it certain.
- Redundancy semantics: the dedupe window is a prototype's (1..127 ahead accepted). Milan's redundancy rules
  (clause 8) are out of #859's scope and owed to #394; the window must be checked against them before RTL.
- The design keeps today's mailbox contract's meaning but changes its layout: the publication block and the CSR become
  RAMs. That is a contract change (OWNER DECIDES) and #665's mailbox rules apply.

## 5. Silicon on the Arty

The Arty A7-100T carries the same xc7a100t as the AX7101. Access was JTAG and the console only, under
the Arty's lock, `-hupcl` set before every open; no flash write, no power action, no network action
(the round packet\'s `arty/`).

- **As found** (09:03): a split image answering `milan_status` (AEM loaded, no gPTP peer: `SYNC=0 ASCAPABLE=0`).
- **The image measured**: the #878 lane's head `bafaed8b` (its Arty split configuration is not on this head), with a
  scratch instrumentation patch (`instrumentation.diff`): the time CSR (0xC01, read as `.insn`) around every pass by
  class, every event by type and timer slot, every loop sink and poll, every centisecond; at boot an I-cache probe
  (4 KiB of straight-line code after `fence.i`, cold then warm) and a flash probe (uncached word and byte reads of the
  flash window); a console command `milan_cyc` printing six pages. Built by S9's recipe (WNS +0.164 ns, WHS +0.008 ns,
  30,229 LUT, 36,892 FF, 66.5 BRAM), loaded into the FPGA's configuration memory over JTAG (volatile; the flash keeps
  its image), booted to `ready`, read twice. The same image ran in the split boot simulation
  (`tb/verilator/ctrl_split_boot`, the platform image on the same CPU and memory, the datapath's registers stood in).
- **Agreement, same firmware** (`agreement.md`; counts of the 100 MHz time CSR):

| Probe | Boot simulation | Silicon | Silicon / simulation |
|---|---:|---:|---:|
| I-cache probe, cold / warm | 6,216 / 2,424 | 6,216 / 2,424 | 1.000 / 1.000 |
| flash: first uncached word / next word | 640 / 304 | 568 / 296 | 0.887 / 0.974 |
| flash: a 64-byte line as 16 word loads | 5,160 | 5,072 | 0.983 |
| flash: 64 bytes as byte loads (the store's `ls_read`) | 35,624 | 32,648 | 0.916 |
| polls, least a pass: MAAP, ADP, ACMP, AECP delivery, console, SRP, SRP delivery | | | 0.946 to 1.061 |
| poll: AECP's (`aecp_mbx` poll), least a pass | 26,920 | 181,800 | **6.753** |

- **The CPU and its memory are cycle-exact in simulation**: the I-cache probe agrees to the tick, and every poll whose
  inputs are the same agrees within 6 %. The flash is 3 to 11 % faster on silicon than the simulation's 12.5 MHz model.
  For #928: a 64-byte line read as words is 5,072 ticks, 50.7 us (the model 51.6 us; #928's computed burst 44.2 us),
  and a block RAM refill on the I-cache probe is (6,216 - 2,424) / 64 = 59 ticks a line: the flash is about 86 times
  slower a line. The saved-state store's flash port reads **byte by byte**: 510 ticks a byte against 79 a byte as words,
  6.4 times dearer (`nvm_flash_litespi.c` `ls_read`), a cut for the store.
- **What disagrees is driven by inputs the simulation does not have.** On silicon the loop is never idle: 3,099 work
  passes in about 45 s, 13.7 ms each on average. AECP's timer slot fires **22,379 times in about 45 s (about 500 a
  second) at a mean of 1.6 ms each**, all in AECP's event handler, and AECP's poll costs 1.8 to 4.1 ms a pass, while
  the board has no controller and no gPTP peer; 37 AVB_INFO_CHANGED events arrived, none in the simulation. At that rate
  AECP's timer path takes most of the CPU of an idle board. **This is the #878 lane's older firmware, not this head's**:
  whether the path survives the train's AECP changes is unknown. **Finding F1, owed to round 2**: rebuild the Arty
  image at this head (the #878 configuration ported), rerun the same instrumentation, and if the rate persists,
  instrument AECP's retry (rounds, recipients, the port's answers) and open an issue. The CPU budget harness answers
  the face block's windows at the contract's bound and posts no datapath event unless a group stages it, so this path
  is outside what it measures.
- **Not done on silicon** (the board has a 100 Mb/s PHY and unknown wiring; network action is not allowed): the
  harness's per-record costs, which need peers; at-scale streaming.

## 6. The plan

### 6.1 The lever set and what it is expected to reach

| Point | This head | After L1-L6 (firmware) | + gPTP 0.10 | Two harts after L1-L6, gPTP on the lighter, the better split | L1-L6 and 125 MHz (+ gPTP x 0.8) | Expected to meet 0.70 with |
|---|---:|---:|---:|---:|---:|---|
| 1x1/1if | 0.456 | 0.429 | 0.529 | 0.243 / 0.285 (SRP+ACMP / the rest) | 0.435 | one hart, the firmware cuts |
| 8x8/1if | 0.568 | 0.514 | 0.614 | 0.322 / 0.292 (SRP+ACMP / the rest) | 0.498 | one hart, the firmware cuts |
| 8x8/2if | 0.605 | 0.550 | 0.650 | 0.310 / 0.340 (SRP+ACMP / the rest) | 0.535 | one hart, the firmware cuts |
| 16x16/2if | 0.741 | 0.641 | 0.741 | 0.380 / 0.361 (SRP+ACMP / the rest) | 0.616 | one hart at 125 MHz |
| 32x32/2if | 1.111 | 0.806 | 0.906 | 0.468 / 0.438 (SRP / the rest) | 0.749 | two harts |
| 64x64/2if (A) | 2.189 | 1.201 | 1.301 | 0.642 / 0.659 (SRP / the rest) | 1.071 | two harts |
| 64x64/2if (B) | 5.863 | 2.369 | 2.469 | 1.195 / 1.274 (SRP / the rest) | 2.019 | not reached by these levers |

The chosen set is L1 to L6 (firmware and harness, exact equivalents, no owner decision), then the CPU lever the re-measured load still needs (D4, D6). L7 and L8 are no execution levers (section 2.4). 1x1/1if and 8x8/1if only fall: every cut removes work and the 1x1 image does not grow (no hart, no cache, no clock).

### 6.2 Work order, execution first

**Round 2 (firmware and harness; no CPU or contract change; each item its own Issue under #872):**

1. **Measure what the gate states by rule** (L1): a harness group that fills the SRP ring at a build, so an owed
   MRPDU is measured; one that stages a retained record's retry. The manager rules on restating `item.mrpdu` and
   `item.retained` from them.
2. **The polls, event-driven** (L2): `ctrl_app_srp.c deliver`, `maap_mbx.c refresh_demand` and `declaring` with
   `acmp_declaring`, `srp_mbx.c poll`'s snapshot and licence scan. The pass's outputs held identical by a differential
   run over every harness arm, a host differential test, and a mutant per dirty bit. This is the largest cut of CPU
   time at scale (about 74 % of the 32x32/2if service cycles in arm A's idle-heavy groups) and of a pass's own cost.
3. **SRP's indexes** (L3) in `srp_mbx.c` and lwSRP (`find_attr`, the replace loop, `sources_of`,
   `interested_msrp`): the one quadratic load term. Upstream in lwSRP with its suite.
4. **lwSRP's sort and timers** (L4, L5), and **ACMP's and ADP's sink indexes** (L6) in tsn-c-stack; then
   **THE TRANSMIT's build under THE SHARE** at 32x32/2if (section 2.5), measured, or a sliced build put to the
   manager for a ruling.
5. **The firmware's memory at scale** (section 4.5): lwSRP's pool per interface by placement, the maps'
   rows from one pool, the descriptor image from templates, the attribute instance compacted. Each an exact equivalent
   held by the firmware suites and the harness, measured in planned RAMB36 at every point.
6. **Re-measure** every point (1x1/1if, 8x8/1if and 8x8/2if formally; 16x16/2if and 32x32/2if on the port), and
   restate the gate's columns at the measurement by its rule. **Milestone one is met when 32x32/2if's load is at or
   under 0.70 with the gPTP reservation**, or the plan says by how much it is not.
7. **Silicon**: the Arty image at this head (the #878 configuration ported), the same instrumentation, finding F1
   (section 5) answered.

**Round 3 (the datapath restructure, staged; each stage keeps 1x1/1if and 8x8/1if behaviour, held by the twin
co-simulation and the existing suites, and moves its shape's slices measurably):** counters and diagnostics into
block RAM; the CSR file and the publication block as dual-clock RAMs (a contract change, OWNER DECIDES, D5); the
listener engine with its stream_id lookup and the redundant pair's dedupe (after #394 rules on Milan redundancy); the
talker engine; the shared sample memory and maps. Then 32x32/2if is routed on the xc7a100t for the first time.

**Round 4 (only what the measurements still need):** a second hart (L10) or a faster core (L11) for 64x64/2if, the
clock (L9) graded by #818 on the restructured fabric.

### 6.3 What the owner decides

| # | Decision | Recommendation | Evidence |
|---|---|---|---|
| D1 | What 64x64/2if means: (A) 64 stream instances a direction, 32 on each interface (#640's naming of 32x32), or (B) 64 on each interface | (A). (B) cannot carry eight-channel streams on 1 Gb/s (105.7 % of the line; SRP admits 75 %) and needs far more compute (section 2.2) | sections 1, 2.2; section 4.4 |
| D2 | RV32IMC (NFR-SCOUT-01) | take it for memory only, where block RAM binds; it is no execution lever at scale (+1.6 % CPU time at 32x32/2if) | section 2.4; #928 |
| D3 | A larger instruction cache (NFR-SCOUT-01) | do not take it: -0.3 % at 32x32/2if for +4 RAMB36 | section 2.4 |
| D4 | A second hart (NFR-SCOUT-01/03), or a faster core | decide after round 2's measurement. The model needs one of them for 32x32/2if (0.806 after the cuts, 0.906 with the gPTP reservation, 0.749 at 125 MHz; two harts 0.468 / 0.438) and a second hart for 64x64/2if (A) (0.642 / 0.659, gPTP on the SRP hart) | sections 3.2, 3.3 |
| D5 | The mailbox contract's publication block and CSR as dual-clock RAMs (the restructure) | yes, staged in round 3, under #665's mailbox rules | section 4 |
| D6 | The CPU and bus clock above 100 MHz | not before the restructure; then graded by #818 | section 3.3 |
| D7 | The gPTP reservation in the target (firmware gPTP on both ports, NFR-SCOUT-02, #665 F6) | 0.10 until F6 measures it | section 1 |

## 7. Limits of round 1

- **16x16/2if and 32x32/2if are a scratch port**, not a product image: their figures include the port's 64-bit masks
  (section 2.1) and lack every save, aged and held-talker group; the held groups' ratio at 8x8/2if stands in for them.
- **64x64/2if is modelled**, a line or (for the SRP record and a build of one) a quadratic, fitted over five points and projected
  two to four times past the largest. The fits' residuals are in `costs-fit.md`; the projection's error is not bounded.
- **The firmware cuts' factors are estimates** (section 3); only L7 to L9's are measured or exact.
- **The load is the gate's long-window load**, not the rows: the rows by every source were not re-graded at the new
  points, and the per-pass share was only read (no work pass over the share at 16x16/2if or 32x32/2if in the groups
  measured but `srp-talker-loss` at 32x32/2if, which counts 2 of 14,088: section 2.5).
- **The 8x8/2if formal measurement was a subset** (section 2.1); the gate's 8x8/2if column was not restated.
- **Silicon**: the #878 lane's older firmware, two reads of one image, no network action (section 5).
- **Nothing changed in the product**: no default, no RTL, no firmware, no bound, no contract.
