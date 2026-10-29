[A695b]

Closes #94

## What changes

IEEE 802.1AS-2011 (+Cor1/Cor2), the edition Milan v1.2 profiles, defines portEnabled (10.2.4.11) as MAC_Operational and the port administratively enabled. Figure 11-8 (MDPdelayReq, as corrected by Cor1 and Cor2) enters NOT_ENABLED at BEGIN and whenever portEnabled is FALSE. NOT_ENABLED takes no Pdelay_Resp or Pdelay_Resp_Follow_Up. It is left only through INITIAL_SEND_PDELAY_REQ, which sends a Pdelay_Req at once with `lostResponses = 0` and `asCapable = FALSE`. Milan v1.2 4.2.6.2.5 ends the multiple-responder Pdelay_Req cease when the link state or portEnabled toggles, or after 5 minutes.

Before this change the engine had no such input. Only the 5-minute countdown ended the cease, and a link loss dropped asCapable only at the fifth lost response.

- **New port.** `KL_gptp_engine` takes `port_enabled_i`, a level synchronous to `clk_i` and registered once. The parent drives its effective link, which is already on that clock, so no synchroniser is added. This is the only port, parameter or register-map change. `KL_gptp_tx_slot`, an internal block, gains `cancel_i`.
- **Each edge: NOT_ENABLED.** The first sample after reset is the reference level, so a port enabled at release raises nothing and the boot cadence serves it, as before. Every later change of level is an edge, so the rise of a port that was disabled at a warm reset's release is one too. Each edge raises the NOTEN leg (timer slot 6):
  - it clears the cease, its countdown and its streak, the asCapable ladder and asCapable, and commits;
  - it disarms the outstanding exchange: `S_RSPSEQ` zero refuses its Follow_Up, and `S_PDGOT` set refuses a later response's arm until the next request;
  - it dispatches ahead of the result and the queue, and does not wait for the serializer, since it builds and sends nothing. So a frame stalled on the byte face cannot hold asCapable up, and no event dispatched after the edge runs before it.
- **While disabled, the port starts no gPTP frame.**
  - the transmit credit word reads 0, so the Pdelay_Req, Sync and Announce beats skip (for Announce and Sync, a disabled port is a DisabledPort, 10.3);
  - the serializer withdraws every frame whose first byte is still unaccepted, a frame SENT while disabled included. Valid falls in the cycle the port is seen low, with no transfer. A frame whose first byte was accepted before the fall runs to its last byte, since the byte face has no abort;
  - both egress claims read empty, so no stamp the down link never returns can block a later beat, and a frozen pair's late t1 completes nothing.
- **Rising edge: INITIAL_SEND_PDELAY_REQ.** NOTEN runs again, then the 1 s beat queued behind it. One Pdelay_Req goes out at once and the cadence runs from it. NOTEN set `S_PDGOT`, so that beat counts no lost response. asCapable stays FALSE until two good exchanges (Milan v1.2 4.2.6.2.4).
- **Unchanged.** The 5-minute countdown exit and every other state are as on main. With the port up from reset, boot is unchanged, and a warm reset taken with the port up keeps a cease, as on main.
- **ROM.** The cease entry ends in NOTEN's tail, which writes the same cells and commits the same flags. NOTEN's disarm is one word: 1,022 words shipping and 1,023 seeded, one more than main. A 3,000-configuration packing sweep against main finds exactly one more word in every configuration and no packing failure.
- **Docs.** "Port enable" sections in the integration and HDL guides, the transmit-face exception for a disabled port, eleven test-guide lines, and re-pointed source-evidence anchors.

Not done, recorded:

- Cor2's `neighborRateRatio = 1.0` and `pdelayReqSequenceId = random()` at INITIAL_SEND_PDELAY_REQ. The rate window and the sequence counter carry over the toggle. After a long outage the stale-window guard skips that window as before. The ladder still needs two good exchanges, so asCapable still rises inside 4.2.6.2.4's 2 to 5.
- A portEnabled change made entirely while `rst_n` is held is not seen: the engine samples the level only out of reset. The parent does not reset the engine on a link toggle.

### Review fixes (PR #95 reviews R729-1 and R730-1)

| Finding | Fix |
|---|---|
| R730-F1: a stalled serializer delayed disable and could start a frame while disabled | The serializer withdraws an unstarted frame while the port is disabled; NOT_ENABLED dispatches without waiting for it |
| R730-F2 = R729-F2: a Follow_Up after the fall paired with the armed response | NOT_ENABLED disarms the outstanding exchange, and runs ahead of every queued event |
| R730-F3 = R729-F1: after a warm reset with the port disabled, the first rise kept the cease | The first sample after reset is the reference level, so that rise is an edge |

Each reviewer probe now passes: R729's probes A, B1, B3, C and D, and R730's 24 adversarial checks and its 32 focused ones.

## Tests

- Engine suite: 2,048 checks per shipping pass (1,977 on main); the priority1 255 pass is unchanged at 60. Eight phases run after phase 43:
  - **44, the toggle exit.** Three requests answered by two identities cease Pdelay_Req. 1.3 s into the countdown the port falls for 1.2 s. Nothing is sent while it is down. On the rise a Pdelay_Req goes out at once, then one every interval. Unanswered, only the fifth loss after the rise commits asCapable FALSE again. Answered, asCapable takes two exchanges.
  - **45, the link loss.** A capable master's port falls for 6.5 s while the peer talks. asCapable falls with a commit within 2 ms; nothing is sent or committed while it is down; the rise sends a request at once.
  - **46.** A Pdelay_Resp built after the fall is not sent, and its claim does not hold the next request.
  - **47, the countdown exit.** Without a toggle the first request after the cease follows the last by the countdown and two beats: 5 s here, 302 s at the 5-minute default, as on main.
  - **48, no exchange across the fall.** A Pdelay_Resp arrives before the fall, then its Follow_Up 2 ms after it, or its late t1, or a Follow_Up queued before the fall behind a stalled frame. None publishes or commits while the port is disabled, and asCapable takes two fresh exchanges after the rise.
  - **49, a stall at the first byte.** The frame is withdrawn at the fall, asCapable falls within 2 ms, and when ready returns, a beat included, no frame starts. The rise sends a request at once, so no claim is stranded.
  - **50, a stall after the first byte.** After 1, 34 or 67 of 68 bytes, the stall held across the fall and a beat: the started frame keeps its place and completes whole, nothing else starts, and asCapable still falls within 2 ms.
  - **51, a disabled warm reset.** Inside a cease the port falls with a warm reset and stays down 1.3 s past release. Its first rise sends a request at once, and asCapable takes two fresh exchanges.
  - Every "nothing starts" check now counts each accepted first byte, so a torn start counts too.
- 25 engine controls planted for #94, each caught on every check it names. Every one of the 71 #94 checks is failed by at least one. The new ones: an unstarted frame not withdrawn; withdrawal off and credit kept; the request claim surviving the fall; valid left up for the withdrawing cycle; a started frame torn; NOT_ENABLED waiting for the serializer; that wait with no withdrawal; NOTEN keeping the armed response; NOT_ENABLED queued behind earlier events; and the first rise after a disabled release raising nothing.
- The new checks, run against the round-1 RTL and microcode, fail exactly where the findings stood: 12 FAIL.
- Every other repository suite keeps its tallies.

## milan-fpga companion

This lands with the gPTP pin adoption (milan-fpga #806), as a patch, not committed. It applies to #805's head.

- `KL_gptp_shadow` takes `port_enabled_i` and passes it to the engine.
- `milan_datapath` drives it from `eff_link_w`: the PHY link, already synchronised into `axis_clk`, gated by `LINK_CTRL[0]` and the link guard's estimate. There is no register-map or contract change.
- The parent boundary: the shadow's gearbox and its timestamp ticket take accepted bytes only, so a withdrawn first byte leaves nothing behind. A started frame completes into the shadow's frame FIFO.
- The three gPTP test wrappers tie the port high.
- The `milan_dp` gptp legs gain three checks, each killed by a planted control: asCapable falls at a link loss; a link loss inside the cease ends it, with a Pdelay_Req within one interval of the link's return; and without a link loss the countdown exit is unchanged.
- `docs/design/GPTP_PLANE.md` and the `milan_dp` README describe the seam.

The adoption still owes the parent area re-measure (route-1x1, ooc-1x1 and ooc-8x8) and the in-house link-toggle scenario on the built image.

## Area

Engine, out of context, with the repository's 10 ns clock, synthesized and then placed for slices:

| | LUTs (synth) | FFs | LUTs (placed) | Slices | WNS placed |
|---|---:|---:|---:|---:|---:|
| main `f97c1803` | 4,990 | 3,455 | 4,943 | 1,663 | +0.524 ns |
| this head | 4,926 | 3,459 | 4,876 | 1,634 | +0.506 ns |
| delta | −64 | +4 | −67 | −29 | −0.018 ns |

The four FFs are the port level, the reference mark and the two owed events. Each RTL gives its own figures with the other's ROM image. BRAM, DSP and the standalone microCPU are unchanged.

## How to validate

```sh
make
make diagrams-check
make ooc
```

## Results

All rc 0, every command run alone with its own log, in fresh clones.

| Gate | main `f97c1803` | this head |
|---|---|---|
| `make contract`, `make lint`, `make docs`, `make diagrams-check` | rc 0 (evidence 20 exact) | rc 0 (evidence 20 exact) |
| `make -C tb/verilator/ucpu` | 768/768 | 768/768 |
| `make -C tb/verilator/parser` | 378/378; arm 16/16 | 378/378; arm 16/16 |
| `make -C tb/verilator/engine run` | 1,977 ×3 + 60 | 2,048 ×3 + 60 |
| `make -C tb/verilator/engine mutants` | 113/113 | 136/136 |
| `make -C tb/verilator/gaskets` | 81/81; arm 5/5 | 81/81; arm 5/5 |
| `make -C tb/tsngen` | 288/288; arm 4/4 | 288/288; arm 4/4 |
| `make -C bench/arty test` | PASS | PASS |
| `syn/ooc/check_ooc_clock.py --selftest`, `make ooc` | rc 0 | rc 0 |
| `git diff --exit-code` after the run | clean | clean |

milan-fpga, on a local snapshot of #805's head (base) and of #805's head plus the companion with this head as the gitlink: every command of the parent consumer list is rc 0.

- Both idiom gates hold every ratchet.
- `milan_dp` `gptp` and `gptp-lat` go from 202/202 to 205/205.
- The physical gPTP leg passes with every Pdelay event, progress and verdict line identical to base.
- The four parent-side controls are each caught on every check they name.
- The extra suites gptp_plane (with its generator-text step campaign), gptp_txts, gptp_tables and the `tsn_fuzz` `ptp` field campaign (675 pass) are rc 0 on both sides.
