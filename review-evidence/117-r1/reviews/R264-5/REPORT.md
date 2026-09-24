[R264] POSITIVE - exact head b71061d7fbc1119b02eb430f293672ff8b3f85b8

Round R264-5: internal independent review of issue #117 / PR #531 in a cleared context. The exact head is `b71061d7fbc1119b02eb430f293672ff8b3f85b8` (tree `b39c840146a4d5ebee53c8633384017137ce896e`). The source base is `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The evidence pin is `bb8c690f8487c202f2f53dbcba2b84dc4c36df73` on `117-review-evidence` (tip `915d2faaba392ed43a878f39c9abbaa92d40f316`).

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head, and all five lenses are covered clean at this head. One new SUGGESTION (S1) and four retained earlier SUGGESTIONs are optional. Every BLOCKER, MAJOR and MINOR from earlier public rounds is closed at this head, and I re-derived each one independently from the raw packets. The sections below list the details.

The round focus was verified directly:

- **No bench identity at the pin, in its history or in the PR.** I derived 35 identity values from the four superseded archive commits, kept privately. I searched them in 9 encodings: ASCII, UTF-16LE/BE, hex, spaced hex, base64 at three alignments, percent and DNS-SD escaping. I searched every blob and commit of the pin tree, of the pin's history `ede8d48e..bb8c690f`, of the PR tree and history, and of the branch tip's additions. There were 0 identity hits. The 5 residual matches are adjudicated benign below.
- **The repository's own privacy rules agree.** The 10 `docs_check.py` scrub rules find 0 hits, applied to binary blobs too.
- **Host-name census.** An independent name census of all 22 captures (230,287 records) finds every capture-server and switch host name masked, in both DHCP option 12 and mDNS. So are the switch's DNS-SD fields.
- **Page hashes resolve.** All 74 raw-artifact table hashes (73 distinct) resolve through `MANIFEST.json` at the pin.
- **No superseded archive link in the PR.** No PR commit (`c3eb95fa`, `0abf147f`, `b71061d7`) links a superseded archive SHA; only `b71061d7` links the archive, at `bb8c690f`.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 - SUGGESTION - Docs

`[R264] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:540 - the "stays" list does not name the IP addresses the published captures carry`

- **Requirement/evidence.** CONTRIBUTING section 6 counts bench subnets as bench-identifying. The repository gate encodes that as the `192.168.` shape, and no such address is in the pin. The published captures do carry four kinds of address:
  - the switch's IPv4 link-local address (ARP probe and announcement, IGMP, mDNS);
  - a second, private-range IPv4 address of the switch, whose last two octets equal those of its link-local address, so it looks device-derived rather than a bench plan;
  - two IPv6 link-local addresses whose interface IDs are not MAC-derived;
  - the reverse-lookup owner name of one of those IPv6 addresses.
  
  Page line 540 lists what stays (MAC addresses, EUI-64 clock identities, entity IDs), but not addresses. Receipt: `receipts/pcap_name_census_pin.txt`. The address census itself stays in the private scratch area.
- **Impact.** None on any result. A cold reader cannot tell whether leaving the addresses was a decision.
- **Required change.** Optional. Name link-local and device self-assigned addresses under what stays, or mask them.
- **Verification.** Read line 540 at the next head.

### Earlier SUGGESTIONs still open at this head (optional, not re-filed)

- **R264-4 S3 = R265-4 S1, `:340`.** One `LINKG_STAT` delay (2.73 s) is stated for all six cycles. Re-derived per cycle, the first read with `[7]` clear comes 2.77, 2.77, 2.76, 2.69, 2.72 and 2.76 s after the last received frame. The reads are 0.1 s apart, and the RTL window is 2^27 cycles at 50 MHz, 2.68 s (`REGISTER_MAP.md:731`). "About 2.7 s" or the per-cycle range would be exact. Receipt: `receipts/verify_step3_details.txt`.
- **R264-4 S2 = R265-4 S3, `:129` against `:540`.** `:129` says a firmware version is not bench-identifying, while `:540` lists the peer's firmware string among masked bench-identifying strings. The rationale at `:129` resolves the earlier MINOR (R264-3 F2) as a decision, but the wording still disagrees.
- **R265-4 S2, `:177-179`.** The keep rule for the per-5 s minima of the tap clock fit is not stated. My own unfiltered fit reproduces every Step 3 table value within 0.01 s, so the rule does not affect any result (`receipts/verify_step3_cycles.txt`).
- **R265-2 S2, `:422`.** The Run B millisecond times (13:04:49.297 and 13:05:59.198) are the capture server's NTP host timestamps. They are not the build-box UTC that `:138` makes the page default, which is 1.08 s earlier. Re-derived: the first and last CRF PDU host times are exactly those values (`receipts/verify_step2_wire.txt`, tap-clock span 69.947 s).

## Earlier public findings on this PR: status at this head

| Earlier finding | Severity | Status at b71061d7 | Evidence (this round) |
|---|---|---|---|
| R264-1 F1 = R265-1 F1: bare-metal-only gate red | BLOCKER | CLOSED | `check_baremetal_only.py --check` rc 0, 0 findings over 839 files; hosted `docs-check` succeeded at this head (`receipts/docs_gates_head.txt`, `receipts/hosted_check_runs_head.tsv`) |
| R264-1 F2 = R265-1 F4: follow-ups not filed | MINOR | CLOSED | `:473-501` link #530 (items 1-3, 9) and #495 (items 4-6); #495 comment 5798471063 carries items 4-6; #529 and #530 are open with matching subjects; items 8 and 10 give reasons |
| R264-1 F3 = R265-1 F2: descriptive statements against raw packets | MINOR | CLOSED | Dark window: last record 1.03-1.76 s, always DUT-sent; first after return 37.56-38.58 s. Loss-edge holdover 3-5 samples, 0.30-0.50 s. Console: 38,954 commands in 14 transcripts, only `milan_status`, `mem_read`, `mem_list`, `crc`. Envelope-less records 76 / 38, 0, 38, 45, 0, 37 / 18. Census 18 of 18 identical. Daemon check covers both bench hosts |
| R265-1 F3: stale "reaches asCapable" row | MINOR | CLOSED | `CLKV_STAT[16]` rises 0.016-0.094 s after the DUT's second completed Pdelay exchange, and 1.03-1.64 s after the switch's first frame; `PDELAY_NS` 377-389 at the rise |
| R264-1 F4: box 5 traceability | MINOR | CLOSED | 74 of 74 table hashes resolve; 29 name redacted-only files, as `:542` says (`receipts/archive_manifest_pin.txt`) |
| R265-2 F1 = R264-2 F1: peer identity hex-encoded in the archive | MAJOR | CLOSED | Peer product, vendor, serial, firmware and entity strings: 0 hits in every encoding, hex and spaced hex included, at the pin, in its history and in the PR (`receipts/identity_census_pin_pr.txt`) |
| R265-2 F2 = R264-2 F2: tool redaction statement | MINOR | CLOSED | 7 redacted tool files at the pin = 4 quoted hashes (`8c9f2885`, `45889a7d`, `c4ef8c9a`, `bdd228a1`) + 3 unquoted `run_a/b/c.sh`, as `:220-225` says (`receipts/redacted_tools_pin.txt`) |
| R265-3 F1: owner-blocker switch facts against captures | MINOR | CLOSED | `:527` matches the captures: ARP probe and announcement for the link-local address; IGMP from it and from a second IPv4 address; DNS-SD control service; DHCP every 15.0 s from the switch's OUI (`receipts/verify_switch_dhcp.txt`) |
| R265-3 F2: holdover while the grandmaster is absent | MINOR | CLOSED | No holdover sample while GM = the DUT outside the 3-5 sample episode at the identity change (0.31-0.52 s), as `:339` says |
| R264-3 F1: console adapter USB serial | MAJOR | CLOSED | USB serial and by-id tokens: 0 hits in any encoding; the scripts read `/dev/<adapter>`; the repository rule "USB serial path" has 0 hits |
| R264-3 F2: firmware digest | MINOR | CLOSED as a decision (`:129` rationale); the wording remainder is retained as a SUGGESTION above | digest prefix `33f0e7f9e86fe482` equals the `sha256_8` of comment 5670665596 |
| R265-4 F1 = R264-4 S1: capture server host name in 6 captures | MINOR | CLOSED | Both DHCP option-12 host names and both mDNS host names are masked, length-preserving. The fourth redaction changed only 83 capture-host records in exactly those 6 captures, with 0 tap records, and every changed byte is `#`. `:540` names the class (`receipts/redaction_delta_db842315_bb8c690f.txt`, `receipts/pcap_name_census_pin.txt`) |
| R264-1 F5, F6; R265-1 S1, S2; R264-2 S1, S2; R265-2 S1; R265-3 S1; R264-3 S1, S2 | SUGGESTION | taken, in effect taken, or optional | F6: `GM_LOSS_RECOVERY.md:96` defines the start. R265-1 S1: pinned locator. R264-2 S2: `:541`, and `sha256sum -c` gives 20 and 57 FAILED by design. R265-3 S1: DNS-SD named. R264-3 S1, S2: taken |

## Lens results (clean lines with evidence)

```text
[R264] PASS Conformance - docs/findings/117_GPTP_SILICON_EVIDENCE.md:34-64, :261-401; docs/design/GM_LOSS_RECOVERY.md:88-118 - every PASS/FAIL/NOT RUN row checked against #117's acceptance boxes, owner decisions 5561827955, 5789767491 and 5795898094, and my own re-derivation from the pinned raw packets. Step 2: 4,556 Sync, 565 Announce and 564/566 Pdelay_Req intervals, all within 30 %; 568/568 and 570/570 exchanges; turnaround 10,984-11,009 ns; Announce fields as stated. Step 3: all six cycles' table columns within 0.01 s, recovery 0.42-1.60 s against 5 s; the bound's 3 + 0.375 + 1.625 derivation matches decision 5795898094. Step 4: the CSR words and the 34,061 CRF PDUs, all tu=0. The 15 ms limit is row 4.2.6.2.6 (MILAN_COMPLIANCE_MATRIX.md:83). Counters-probe parity is the TESTING.md:665 bar. Box 4's FAIL and NOT RUN rows are honest, and the PR says "Relates to", so #117 stays open.
[R264] PASS RTL - git diff ede8d48e..b71061d7 touches only 3 Markdown files, and the gitlinks equal the base. The page's RTL and register claims hold against hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:70-78,122,188-199: holdover arms on any published-GM change (gm_id_i != gm_r) for 0.25-0.5 s, against 0.30-0.52 s measured. REGISTER_MAP.md decodes hold: CRFT_CTRL 0x3002E3 is enable, class A, tagged, reservation, licensed, VID 2, PCP 3 (:875); GPTP_LAT 0x029000DB is 656/219 ns (:1392); CLKV_STAT 0x00010002 (:770); LINKG_STAT act_recent 2.7 s at 50 MHz (:731); RST_EPOCH (:730).
[R264] PASS Robustness - pin bb8c690f archive and page :136-197, :288-299. The aborted attempt 1 is disclosed and excluded. The capture-host record exclusion, 0 drops in 19 tcpdump logs, RST_EPOCH=1 in 7,736 reads, console gaps of at most 0.113 s and the read-only command census are re-derived. Redaction integrity holds: all 22 captures still parse. Against the as-recorded originals (225 of 236 files are byte-equal to MANIFEST.json original_sha256 at superseded 160debeb), every differing capture record is DHCP or mDNS, with 0 gPTP, AVTP or MSRP frames altered. Changes are '#'-only and length-preserving.
[R264] PASS Tests - receipts/verify_step2_wire.txt, verify_step3_cycles.txt, verify_step3_details.txt, verify_step4_csr.txt, docs_gates_head.txt, hosted_check_runs_head.tsv. Independent decoders that do not import the packets' tools reproduce the Step 2, 3 and 4 numbers. The docs gates at the exact head all return 0: docs_check, check_em_dash --base ede8d48e (670 added lines), doc style, gPTP docs with and without the submodule, bare-metal-only, DOC_MAP, feature status self-test, TOC, anchors. Hosted at the exact head: 8 executed contexts succeeded (rtl-fast, docs-check, docs-check-no-git, wire-accountability, elaborate, bdd-conformance, full-ci-gate, changes); 7 skipped, including verilator-suites and yosys-portability, as a docs-only change emits them. No test code changed.
[R264] PASS Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:1-628, docs/design/GM_LOSS_RECOVERY.md:18-27,88-118,171, docs/findings/README.md:11. The redaction statement :540-542 matches the pin: 77 = 71 identity + 6 path-only; 20/57 per packet; 29 redacted-only table rows; the masked classes are the masks actually present. The tool redaction statement :218-230 matches. The 52 relative links and anchors resolve. The cited comments 5584039577, 5670665596, 5794859125 and 5795898094 carry what the page says, and 8ef4b008 indeed has no published full value. #495, #529 and #530 match. The em-dash rule holds. The index row and PR body agree with the page. Commits are one line with no trailers. Only S1 and the retained optional SUGGESTIONs remain.
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #117 body and owner decisions; page `:34-64`, `:118-134`, `:232-452`; `GM_LOSS_RECOVERY.md:88-118`; compliance matrix `:83`; `TESTING.md:665`; raw captures, transcripts and logs at `bb8c690f` through my decoders | R264-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| RTL | CLEAN | diff `ede8d48e..b71061d7` (3 docs files, gitlinks unchanged); `KL_ptp_clock_validity.sv:60-90,115-125,170-200`; `REGISTER_MAP.md:730-731,770-771,875,1161,1363-1364,1392` | R264-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Robustness | CLEAN | attempt 1; host-record exclusion; 19 tcpdump logs; console gaps and RST_EPOCH; redaction integrity across `160debeb`, `db842315` and `bb8c690f`; identity census in 9 encodings | R264-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Tests | CLEAN | independent re-derivation receipts; 10 docs gates at the head; hosted check runs at the head; `MANIFEST.sha256` FAILED-by-design counts | R264-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Docs | CLEAN (S1 and retained SUGGESTIONs optional) | the three changed pages, all lines; `MANIFEST.json` and both packet `MANIFEST.sha256` at the pin; external references; PR body; commit messages | R264-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |

## Adjudicated census residue

The five non-zero census tokens at the pin, in the PR tree and in the tip additions are all benign. They carry opaque IDs in `receipts/identity_census_pin_pr.txt`.

- **T04** matches only inside longer decimal timestamps in analysis and receipt files. It never appears on its own.
- **T05** is the DUT's own serial string from the repository's `configs/endstation_ax7101_*.yaml`. It is product-owned and already public.
- **T06 and T11** are the DUT board's USB-UART bridge chip names. They appear only in pre-existing dev files (`docs/integration/BOARD_PORTING_AX7101.md`, `docs/integration/BUILDING.md`, `sw/litex/deploy.sh`), not in the archive, and this PR does not introduce them.
- **T45** is a short host role name, which the page's policy keeps.

The name census of the captures leaves 125 unreviewed runs, all binary noise:

- 113 five-octet runs inside CRF timestamps;
- 12 runs of 6 or more octets in binary records.

## Real limits

- The as-recorded originals are private. I proved redaction integrity against superseded `160debeb`, whose 225 files are byte-equal to `MANIFEST.json` `original_sha256`. That includes all 22 captures. The 11 files that were path-only-redacted even there could not be compared.
- My identity token list comes from what some round masked. Values no round ever masked are covered by independent checks instead:
  - the repository scrub rules;
  - shape scans for user@host, home paths, private IPv4, uname lines, host-name keywords, serial keywords, MAC-derived interface names and by-id paths, all 0 hits;
  - the full name-field census of the captures.
- The bench hardware was not observed. All physical claims rest on the published packets.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- I did not run the full parent, protocol-processor, gPTP, Yosys or builder banks, Docker/act or `act_ci`. The manager's statement that its source static/builder and native banks passed at this head was not checked from a public receipt. The evidence link in this round's brief (`32aec661`) is a superseded bench archive commit, not bank receipts.
- The Step 3 timebase uses my unfiltered least-squares fit, with residuals up to 74 ms against the page's filtered 2.02 ms. It reproduces the table within 0.01 s.

## Pending manager duties

1. **M1: superseded archive commits still served by SHA.** GitHub still serves these superseded evidence commits by SHA, and public comments on #531 and #117 link them.

   | Superseded commit | What it still carries (classes only) |
   |---|---|
   | `160debeb` | the as-recorded bench identity: host names with the bench prefix, the capture server host name, the switch's vendor, model, serial and DNS-SD fields, the peer's product, vendor, serial and firmware (text and hex), the console adapter's USB serial path and a MAC-derived interface name |
   | `32aec661` | switch DNS-SD fields, the USB serial tail, the capture server host name, peer identity in hex |
   | `74ac94e8`, `4165beb8` | switch DNS-SD fields, the USB serial tail, the capture server host name |
   | `db842315`, `7626fb2b` | the capture server host name |

   Totals only: `receipts/identity_census_superseded_summary.txt` and `receipts/repo_scrub_superseded_summary.txt`. Rewriting branch history does not remove these objects from the hosting service. A purge of the dangling objects and cached views is a hosting-service request. Relinking them from new comments or briefs should stop; this round's brief linked `32aec661`. None of this affects the head or the pin.
2. **M2.** Publish the source static/builder and native bank receipts for this head where a reviewer can read them.
3. **M3.** Build and validate the final current-dev candidate at the merge turn: source base `ede8d48e`, live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a`. Then run post-merge containment.
4. **M4.** Own hosted/act acceptance at the exact head. Two independent positive reviews are required at this head, one of them external.
5. **M5.** #117 stays open. Box 4 has FAIL and NOT RUN rows, and audio continuity is deferred to 2026-12-31.

## Clone state after probes

`receipts/clone_state_final.txt` records the review clone at the exact head after the round:

- HEAD `b71061d7`; tree and `write-tree` `b39c8401`;
- index hash unchanged, porcelain empty (ignored files included), no assume-unchanged or skip-worktree entries;
- 865 tracked files byte- and mode-equal to their index blobs;
- all four gitlinks equal to the base's, and the two initialised processor submodules clean at them.

A bytecode cache directory my import created was removed.

## Receipts and scripts

Everything publishable is listed in `MANIFEST.sha256`. The scripts run from the packet directory against a bare fetch of the evidence branch and the review clone. Private token lists and disposable trees stay in `scratch/` and are not published.

R264-5 FINISHED
