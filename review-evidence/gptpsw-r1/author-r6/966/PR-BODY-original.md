[A814] gPTP in split firmware on the optimisation line (#884, #665 F6)

Targets `dev-soft-core-optimisation`. Refs #884, #665, #872 and #962. Implements the owner's firmware-gPTP
choice and #884's admission, latency, memory-debt and buildable-plane rulings. The product line on
`dev-soft-core` is unchanged. This does not close #884: bench qualification remains owed.

### Behavior and integration

Firmware owns BMCA, Announce, Sync/Follow_Up, Pdelay, asCapable and the servo under `--sw-gptp`, one end-station
port per interface. The fixed-point implementation has no heap and uses a three-call HAL: send, adjust rate,
step time. Fabric retains the PHC, rate/offset controls, launch observer and timestamp unit, with the existing
stamp points and corrections. The fabric gPTP plane remains buildable and remains the default.

Mailbox contract 2.5 is additive: channel `gptp`, credit-flowed uncoalesced `TIMESTAMP` events, and three publication
words per interface. It assumes no hart number; the second-hart lane adds its 2.6 routing on top. The derived
admission burst is seven message kinds per interface per 10 ms refill window, hence 7 at one interface and 14
at two. It comes from the worst legitimate coincidence of message kinds and their minimum intervals, not from
a service-budget fit.

The ingress timestamp accompanies its delivered frame in an eight-byte trailer; the stamp FIFO follows the
frame FIFO. The committed publication crosses as a bank, isolated from subsequent uncommitted writes.
Under `--sw-gptp`, the status block narrows and firmware answers AVB_INFO and AS_PATH from the same published
snapshot. The register map is updated in the same change.

**One physical MAC remains.** The product build has one PHC and one timestamp unit. Two interfaces, two peers
and one PHC/timestamp unit per interface are exercised in the closed loop. Physical second-MAC work is #962.

### Review corrections

- A generation committed while an earlier crossing is busy now captures the committed bank; later live writes
  cannot tear it. The crossing bench and host model exercise the reviewed ordering.
- Raw Sync alone cannot postpone sync receipt expiry. Only a consumed Sync/Follow_Up pair restarts it.
- A second Pdelay response clears asCapable and its publication immediately, including on an already-capable
  port with a missing or late Follow_Up. Three requests with different responders trigger the cease; same-clock
  duplicates invalidate capability without counting toward that cease. Resume behavior is retained.
- Follow_Up without the mandatory information TLV is refused, including truncated and wrong-type variants.
- Peer delay uses LocalClock time, the PHC less all applied servo steps, for local and reported peer timestamps.
  A slave step within or beyond the rate-envelope span therefore cannot corrupt the far port's rate estimate.
  The overflow-safe envelope remains for peers that timestamp on a stepped PHC.
- The engine's PHC tie-offs are defined once for every build without the plane. Builder checks retain their
  sole-driver assertions, count the timestamp unit's reads and retain firmware ownership as an explicit opt-in.
- The service hot list was relearned using the optimisation line's three recorded windows with gPTP in the
  traced image. Its 286 sections include 15 gPTP sections. The link check exempts a whole object only when it
  is compiled out and rejects an exemption if that object actually links. The held-row ledger did not move.

Every reviewer probe is a regression that fails on the head where its defect was reported. The multiple-response
cases cover completed and in-flight exchanges, missing/late Follow_Up and duplicate clock identities. The step
checks cover both signs and the full requested turnaround matrix.

### Measurements and validation

At `631dc544`, with the executable sources and layout of final head
`165476c755e4728a044c12ea6bc33ce0a0a9d28f`:

| Measurement | 8x8/1if | 8x8/2if |
|---|---:|---:|
| Pdelay turnaround, bound 10 ms | 0.309 ms | 0.292 ms |
| Last admitted gPTP record, bound 10 ms | 6.115 ms | 7.750 ms |
| Composed pass maximum, share 2.0 ms | 1.675 ms | 1.657 ms |
| Work passes over the share | 0/5,139 | 0/5,217 |
| Maximum measured gPTP CPU load after link-up | 0.212 % | 0.269 % |

All seven held 8x8/1if rows pass their unchanged ledger, including ACMP at 62.45305 ms against 62.62 ms and AECP
at 62.12258 ms against 62.16 ms. The plain image also passes. The seven known held rows still exceed their nominal
20 ms budgets; the separate egress ledger governs them. No 2if ledger exists: applying the 1if figures to 2if
fails, with five owed rows 0.05 to 0.10 ms past those figures and the last AECP instance on interface 1.

Memory remains within its recorded debt entries: the gPTP fixtures use 59/64 RAMB36 and the platform 8x8/1if
image 62 RAMB36, 152,072 B ROM and 99,392 B SRAM. Their identifying symbols are `image_gptp` 1,104/2,152 B
and `ctrl_plat` 20,160 B, including the eight-byte LocalClock offset per port. The documentation now matches
those executable ledger keys. No CPU bound or allocated memory-tile limit changed.

An image without the flag excludes the firmware gPTP owner. The shared hot-list relearn changes code layout in
both variants. Between `a6323318` and `631dc544`, plain platform ROM grows from 126,632 to 126,640 B at 1x1/1if
and from 140,952 to 140,960 B at 8x8/2if; SRAM and allocated tiles are unchanged. The design page records these
measurements in place of the earlier byte-identity claim.

Completed local evidence, each attached to its actual head in the handoff:

- Port tests: 63 cases, also clean under undefined-behavior checks; 41/41 planted defects caught.
- Four firmware-gate shards after relearn at `631dc544`: pass, with all 826 mutation controls caught;
  hot-list checks include the two new compiled-out-object plants.
- Full RTL simulation sweep at `e81cecdb`: 67/67 suites pass, plus field campaigns of 164 and 675 cases.
  RTL and host simulation sources have not changed since that run; rebuilt split-CPU boot tests cover the layout.
- Synthesis portability at `a6323318`: 64 tops pass; publication census and its controls pass.
- Documentation, idiom and light gates at `334ca4b7`: 73/73 pass, no skipped syntax check; the vendor front end
  analysed 142 files. The four requested documentation gates pass on the tree committed as `165476c7`.
- Focused memory-ledger tests on that tree pass 150 assertions, including all 16 ledger plants and three mapper
  mutants. Regrading the original `631dc544` platform images passes five points and all nine controls;
  no new image build or full memory/simulation bank is claimed for this documentation-only correction.
- Fresh closed loop at `334ca4b7`: 48/48 checks, all 14 planted defects caught. The flood retains all 490 delivered
  stamps, loses no egress timestamp record, locks by 2.9 s and stays within 95 ns afterward. The final commit
  changes documentation only.
- Full builder suite at `8267b895`, with RV32 and elaboration required: rc=0; the two reviewed assertions
  pass. Two arms are explicitly NOT RUN: a build-flags mutation that has no effect in this environment, and a
  calibration report absent from this host. Neither is counted as a pass.

The status narrowing saves 3,049 flip-flops in synthesis. The routed 8x8/1if software-gPTP image at `a6323318`
meets #818's floor under all three directives: setup/hold +0.292/+0.036, +0.281/+0.036 and +0.173/+0.067 ns.
It uses about 38.1k LUT, 45.9k FF, 95.5 memory tiles and five DSPs. Against the plane build at `40bd7738` with the
same best directive, this is about 5.1k fewer LUTs, 5.4k fewer FFs and six fewer DSPs, with equal block RAM.
These are measurements of those routed images. The hot-list relearn changes the firmware image; no RTL changed
after the route, so no post-relearn route is claimed.

### Owed before onward integration or qualification

The census owner must rule the software-gPTP shape. This lane supplies these rows:

- `o_ctl_avb_chg_p`, `o_ctl_asp_chg_p`: tied zero; firmware raises the changes.
- `i_ctl_gptp_pub`, `i_ctl_gptp_pub_p`, `i_ctl_ts_take`: consumed only in the software build; publication GEN is
  consumed in the crossing and state bits 11–15 remain reserved.
- `o_ctl_ts_valid`, `o_ctl_ts_data`: zero with the plane, driven by the timestamp unit with software gPTP.
- Plane parent, peer-delay and path-publication nets: zero in the software build.
- Control tap with `GPTP_P`: frame-associated timestamp FIFO and ingress trailer.

The second MAC is #962. Bench qualification of accuracy, lock time and the retained plane A/B comparison remains
owed under #884. No bench access occurred in this round.

