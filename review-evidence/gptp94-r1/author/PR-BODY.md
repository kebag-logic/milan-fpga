[A695]

Closes #94

## What changes

IEEE 802.1AS-2011 (+Cor1/Cor2), the edition Milan v1.2 profiles, defines portEnabled (10.2.4.11) as MAC_Operational and the port administratively enabled. Figure 11-8 (MDPdelayReq, as corrected by Cor1 and Cor2) enters NOT_ENABLED whenever portEnabled is FALSE. It leaves that state only through INITIAL_SEND_PDELAY_REQ, which sends a Pdelay_Req at once with `lostResponses = 0` and `asCapable = FALSE`. Milan v1.2 4.2.6.2.5 ends the multiple-responder Pdelay_Req cease when the link state or portEnabled toggles, or after 5 minutes.

Before this change the engine had no such input. Only the 5-minute countdown ended the cease, and a link loss dropped asCapable only at the fifth lost response.

- **New port.** `KL_gptp_engine` takes `port_enabled_i`, a level synchronous to `clk_i` and registered once. The parent drives its effective link, which is already on that clock, so no synchroniser is added. This is the only port, parameter or register-map change.
- **Falling edge: NOT_ENABLED.** The engine queues a timer-slot-6 event, and the slot dispatch, which ended there before, now runs the new NOTEN leg.
  - NOTEN clears the cease, its countdown and its streak (`S_CEASE`, `S_CEASECNT`, `S_MULTI`, `S_IVMULTI`, `S_RSP1`). It then clears the asCapable ladder and asCapable, and commits.
  - So asCapable falls one handler after the edge, not at the fifth lost response. The existing asCapable-fall hook then drops an elected peer, as for any other loss of asCapable.
- **While disabled, the port sends no gPTP frame.** This was small and local, so it is implemented, not only recorded:
  - the transmit credit word reads 0, so the Pdelay_Req, Sync and Announce beats skip (for Announce and Sync, a disabled port is a DisabledPort, 10.3);
  - every SEND is dropped, so a frame built across the fall, or a reply to a frame heard while disabled, does not leave;
  - both egress claims read empty: a stamp the down link never returns cannot block a later beat, and a late stamp builds no Follow_Up.
- **Rising edge: INITIAL_SEND_PDELAY_REQ.** NOTEN runs again, then the 1 s beat queued right behind it. One Pdelay_Req goes out at once and the cadence runs from it. NOTEN set `S_PDGOT`, so that beat counts no lost response. asCapable stays FALSE until two good exchanges (Milan v1.2 4.2.6.2.4).
- **Unchanged.** The first enable since reset raises no event; the boot cadence serves it, as before. On a board whose link comes up after reset, nothing is sent until it does. The 5-minute countdown exit and every other state are as on main: with the port up throughout, the parent's physical gPTP leg prints every Pdelay timestamp and verdict line exactly as on main.
- **ROM.** The cease entry now ends in NOTEN's tail, which writes the same cells and commits the same flags. That pays for the new leg word for word: 1,021 words shipping and 1,022 seeded, as on main. A 3,000-configuration packing sweep against main finds the same used count everywhere and no packing failure.
- **Docs.** A "Port enable" section in the integration and HDL guides, six test-guide lines, and re-pointed source-evidence anchors.

Not done, recorded: Cor2's `neighborRateRatio = 1.0` and `pdelayReqSequenceId = random()` at INITIAL_SEND_PDELAY_REQ. The rate window and the sequence counter carry over the toggle. After a long outage the stale-window guard skips that window as before. The ladder still needs two good exchanges, so asCapable still rises inside 4.2.6.2.4's 2 to 5.

Four commits on main `f97c1803`:

- the port, the gates and the NOTEN leg, with every tracked image regenerated;
- the four new engine phases and twelve planted controls;
- the docs;
- three more controls, and a toggle phase whose disabled span always holds a beat, so a control kills every new check.

## Tests

- Engine suite: 2,002 checks per shipping pass (1,977 on main); the priority1 255 pass is unchanged at 60. Four new phases run after phase 43:
  - **44, the toggle exit.** Three requests answered by two identities cease Pdelay_Req. 1.3 s into the countdown the port falls for 1.2 s, which spans a beat. Nothing is sent while it is down. On the rise a Pdelay_Req goes out at once, within one interval, then one every interval. Unanswered, only the fifth loss after the rise commits asCapable FALSE again, so the count restarted at zero. Answered, asCapable takes two exchanges.
  - **45, the link loss.** A capable master's port falls for 6.5 s while the peer sends a Pdelay_Req, an Announce and a Sync pair. asCapable falls with a commit within 2 ms. Nothing is sent and nothing commits while the port is down. On the rise a request goes out at once, and asCapable takes two exchanges.
  - **46.** A Pdelay_Resp built after the fall is not sent, and its claim does not hold the next request after the rise.
  - **47, the countdown exit.** Without a toggle the first request after the cease follows the last before it by the countdown and two beats: 5 s with this image's 3 s countdown, 302 s at the 5-minute default, as on main.
- Fifteen new engine controls, each caught on every check it names:
  - the toggle keeps `S_CEASE`, and the falling edge raises no event (the issue's two named mutants);
  - slot 6 runs no leg; the edge keeps the ladder; the edge leaves the interval unanswered;
  - the countdown loads one beat less; the cease entry ends the cease at once; the cease entry keeps asCapable;
  - the ladder raises asCapable at the first exchange;
  - a rise sends no request at once; a disabled port keeps its credit; a frame built across the fall is sent; a disabled port keeps both its credit and its SEND; the claims survive the fall;
  - the first enable since reset raises events, caught by the existing one-commit-at-reset checks.
- A coverage run kept every failure of every control: each of the 25 new checks is failed by at least one.
- Every other repository suite keeps its tallies.

## milan-fpga companion

This lands with the gPTP pin adoption (milan-fpga #806), as a patch, not committed. It applies to #805's head.

- `KL_gptp_shadow` takes `port_enabled_i` and passes it to the engine.
- `milan_datapath` drives it from `eff_link_w`: the PHY link, already synchronised into `axis_clk`, gated by `LINK_CTRL[0]` and the link guard's estimate. There is no register-map or contract change.
- The three gPTP test wrappers tie it high.
- The `milan_dp` gptp legs gain three checks, each killed by a planted control (the shadow ignoring the port, the edge keeping the cease, the falling edge raising no event, the countdown one beat short):
  - asCapable falls at a link loss;
  - a link loss inside the cease ends it, with a Pdelay_Req within one interval of the link's return;
  - without a link loss, the countdown exit is unchanged.
- The leg's existing `LINK_CTRL[0]` toggle now really takes the port down. So after it the leg re-earns asCapable and re-selects its peer before the Sync phase.
- `docs/design/GPTP_PLANE.md` and the `milan_dp` README describe the new seam.

The adoption still owes the parent area re-measure (route-1x1, ooc-1x1 and ooc-8x8) and the in-house link-toggle scenario on the built image.

## Area

Engine, out of context, with the repository's 10 ns clock, synthesized and then placed for slices:

| | LUTs (synth) | FFs | LUTs (placed) | Slices | WNS placed |
|---|---:|---:|---:|---:|---:|
| main `f97c1803` | 4,990 | 3,455 | 4,943 | 1,663 | +0.524 ns |
| this head | 4,922 | 3,459 | 4,874 | 1,659 | +0.513 ns |
| delta | −68 | +4 | −69 | −4 | −0.011 ns |

The four FFs are the port level, the first-enable mark and the two owed events. The LUT fall is restructuring around the new terms; running each RTL with the other's ROM image reproduces its own figures. BRAM, DSP and the standalone microCPU are unchanged.

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
| `make -C tb/verilator/engine run` | 1,977 ×3 + 60 | 2,002 ×3 + 60 |
| `make -C tb/verilator/engine mutants` | 113/113 | 128/128 |
| `make -C tb/verilator/gaskets` | 81/81; arm 5/5 | 81/81; arm 5/5 |
| `make -C tb/tsngen` | 288/288; arm 4/4 | 288/288; arm 4/4 |
| `make -C bench/arty test` | PASS | PASS |
| `syn/ooc/check_ooc_clock.py --selftest`, `make ooc` | rc 0 | rc 0 |
| `git diff --exit-code` after the run | clean | clean |

milan-fpga, on a local snapshot of #805's head (base) and of #805's head plus the companion with this head as the gitlink: every command of the parent consumer list is rc 0.

- Both idiom gates hold every ratchet.
- `milan_dp` `gptp` and `gptp-lat` go from 202/202 to 205/205.
- The physical gPTP leg passes with every Pdelay timestamp and verdict line identical to base.
- The extra suites gptp_plane (with its generator-text step campaign), gptp_txts, gptp_tables and the `tsn_fuzz` `ptp` field campaign (675 pass) are rc 0 on both sides.
