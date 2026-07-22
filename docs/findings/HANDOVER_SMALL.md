# Small handover — 2026-07-22 night (item-4 done, item-5 in flight)

Full history: `HANDOVER.md` + `BENCH_TOPOLOGY.md` + `MILAN_COMPLIANCE_GAPS.md`
(§5b/5c/5d + the USER-reordered 12-item attack order). NxN design:
`docs/NXN_ARCHITECTURE.md` (normative). Builder: `docs/ENDSTATION_BUILDER.md`
+ `sw/builder/` (16+ test gates). Traceability: `docs/SPEC_TRACEABILITY.md`
(162✅/18🟡/7❌ after the coverage round).

## Consoles — `/home/alex/bench-console/` (unchanged)
TRAP: (re)opening the ARTY serial port RESETS the board (DTR). AX port safe.
`strings` on console logs DROPS <4-char lines — prefix reads (`echo X=$(...)`).

## Boards (QSPI self-boot, milan CSR 0x90000000, both VERSION 0x0007)
- **ARTY** = `eto_milanfinal48` (+0.349): RMON latch WORKING (first silicon
  ever — the event bus was tied off in milan_soc.py since forever; TX_GOOD
  0x21C / RX_GOOD 0x230, latch 0x200=1, invalidate-on-reinit proven).
  Music locked (rebind = one acmp_bind connect, no set_fmt).
- **ALINX** = `eppo_milanfinal38` (+0.063, **e2 port** — `--eth-port e2`,
  sweep default): e1's "death" was the ROTTED DTB dma-ts window (0x3064 =
  rx_rsc_en; images-flash poison, NOT hardware — e1 retest with fixed
  images pending, needs a cable move). RTL8211E at MDIO addr 0 via
  AB21/AB22. **DOCTRINE: diff the dtb reg windows vs the build csr.csv
  before EVERY images flash.**
- Rootfs (both): kl-eth **mdio2** (MII ioctls silicon-proven incl.
  SIOCSMIIREG real renegotiation), mii-tool on-board, linkmon back-off
  (one "reinit #N (guard gw vX)" per outage, exponential, capped 600 s;
  `/tmp/linkmon.pause` = full MDIO quiet — all bench-drilled).
  linkmon logs to /dev/console NOT dmesg.

## CERT — ★ 63/63 scenarios, 321/321 steps ★ (final pair, one clean run)
Harness: pw0 home `aets_recreate/` (runners run_arty.sh/run_alinx.sh; flap
cmds need `sudo -u alex ssh` — root has no dropbear key; dropbear host keys
REGENERATE on reflash → ssh-keygen -R). Tap helpers: redeploy from the
private snapshot tools-tap/ after every tap-host /tmp wipe. es-4.7 carries
a scratch-name pre-step (the DUT rightly suppresses no-change SET replays).

## Item 4 (software-defined End-Station): DONE
Builder = working generator: config-selectable clusters, one STREAM_PORT
per stream, talker clusters = config, sweep.sh single-source (generated
opts fragments; inline tables = fallback), hash-derived entity_model_id
(sha256 of model-shaping fields under 0x001BC5, arty_current PINNED),
CRF output per Milan 7.2.3 (>=2 AAF inputs => mandatory, enforced),
resource estimator (calibrated ±0.21% vs real mf48; **replication for
NxN = 142%/107% LUT = DEAD; shared-engine ≈87.7% projected**).
No-regression gates: arty_current ROM byte-identical + sweep flags
byte-match.

## Item 5 (NxN, shared engines + context RAM): IN FLIGHT
Merged: architecture (LCTX/TCTX/ACTX/SCTX records, indexed CSR 0x800
window spec, P0-P12 phasing), CRF-output model, ACMP N-contexts (~764
cells/ctx), lwSRP N-attributes (~1.9k cells/attr, CRF reservation
registrar closed), coverage round (+tied-input check
scripts/check_tied_inputs.sh — 3 real constant ties incl. the historic
i_mac_events). In flight: dataplane core (stream table/LCTX monitor/PCM
routing/shared packetizer), walker dom_a_evt_r fix, indexed CSR window
(VERSION→0x0008). Then: P12 integration → mf49/AX39 sweeps → drills →
CERT. AX budget watch: 8x8 ≈ 87.7% LUT (levers: L2 32K authorized,
crf_rx ts-ring→BRAM, pruning).

## Standing rules burned in this round
Every round grows the TB suite (USER directive; matrix 🟡/❌ = backlog) ·
pkill/pgrep self-match: bracket patterns · busybox has killall not pkill ·
worktree agents: verify base first (stale-fork trap), cp -r third_party ·
one-line commits, hackerman-kl, both repos, push --force on USER ask.
