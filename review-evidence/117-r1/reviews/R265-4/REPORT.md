[R265] NEGATIVE - exact head dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba

Round R265-4: external independent review of issue #117 / PR #531, run with cleared context.

- Head `dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba`, tree `9c80255cbc74dfa1a57eb5979fd4e150c964cc14`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- PR commits: `c3eb95fa`, `0abf147f` and `dfe6a587`, each a one-line message with no trailers.
- Diff: three Markdown files and nothing else. `docs/findings/117_GPTP_SILICON_EVIDENCE.md` is added; `docs/design/GM_LOSS_RECOVERY.md` and `docs/findings/README.md` are modified. There is no HDL, firmware, configuration or gitlink change.
- Evidence pin `db842315015dda3d68c9687973c4803bb25ceefb`; branch `117-review-evidence` tip `7626fb2b850e1e9c707ea247cab211b1e6833e0e` (10 commits on `ede8d48e`).
- All five lenses applied: Conformance, RTL, Robustness, Tests and Docs.
- I wrote the verdict, findings and ledger before reading any prior review report. Reading R264-3 and R265-3 afterwards changed none of them (see "Prior public findings").

## Reconstruction order (public state only)

1. AGENTS.md; CONTRIBUTING.md, sections 2, 3 and 6 (the section 6 privacy rule and the `scripts/docs_check.py` deny-list); `docs/README.md`.
2. Issue #117 body and frozen acceptance, and the public decisions: 5561827955 (one DUT), 5565246390, 5789767491, 5794146393 and 5794354283; the build, flash and bench records 5794274143, 5794859125 and 5794950660; the operator records 5795658105 and 5796668867; decision 5795898094 (switch power cycling and the 5 s bound); 5798470752 (follow-up routing). The manager's PR notes 5800264651 and 5802093720 (the round-4 changes and the firmware-version decision).
3. Authorities: `docs/reference/REGISTER_MAP.md`, `docs/design/GM_LOSS_RECOVERY.md`, `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv` and `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv`. Follow-up issues #495, #529 and #530.
4. `git diff ede8d48e..dfe6a587`, the full correction diff `0abf147f..dfe6a587`, and the per-commit trees.
5. The evidence at the pin and over the whole branch history, re-derived with my own decoder (no packet analysis script is reused), plus the exact-head hosted check-run metadata.
6. Only after the verdict: R265-3 (5801972860) and R264-3 (5802037583), then the finding headings of rounds 1 and 2.

## Verdict in brief

**NEGATIVE, on one MINOR finding.**

- **F1.** The pinned archive still publishes the capture server's own machine host name, 83 times in six captures. The redaction statement on the page neither masks it nor lists it under what stays.

F1 leaves `Docs` and `Conformance` unclean. `RTL`, `Robustness` and `Tests` are clean at this head. Three SUGGESTIONs do not affect coverage.

Everything the round was asked to verify holds, apart from F1:

- **R264-3 F1/F2/S1/S2 and R265-3 F1/F2/S1 are closed** with no new defect in the corrected passages. See the resolution table.
- **Identity.** The pin, all 10 branch commits and the PR tree carry none of the identities that the three redactions targeted. That was checked in raw, hex (with and without separators), base64 at three alignments, UTF-16LE/BE and percent encodings, capture bytes included. Positive controls on two superseded publications fire, 2,022 hits in all. The only residual found is F1, a name no redaction pass targeted.
- **Page hashes.** All 74 raw-artifact hashes resolve through `MANIFEST.json` at the pin, and all 236 published files hash to their manifest values. The 8 page hashes outside the archive are exactly the ones the page says are.
- **Archive facts.**
  - B1 and B3 match the captures in all six cycles, on both capture points.
  - Both holdover episodes match the transcripts.
  - Every step 2, step 3 and step 4 figure I re-derived matches, within the tap clock-fit uncertainty of at most about 0.01 s.
- **Superseded links.** No PR commit links a superseded archive SHA. The only link is the pin.

## Findings

### F1 - MINOR - Docs, Conformance

`[R265] MINOR Docs, Conformance - review-evidence/117-r1 at db842315 (6 captures) with docs/findings/117_GPTP_SILICON_EVIDENCE.md:540 - the pinned archive still publishes the capture server's own machine host name`

**Where**

At `db842315015dda3d68c9687973c4803bb25ceefb`, and unchanged at the tip `7626fb2b`, six captures carry the name:

- `bench-a200/bench/runA/tap-runA.pcap`;
- `bench-a202/bench/cycle1/tap-c1.pcap`, `cycle3/tap-c3.pcap`, `cycle4/tap-c4.pcap` and `cycle6/tap-c6.pcap`;
- `bench-a202/bench/final/tap-final.pcap`.

**Evidence** (`receipts/hostname_census_pin.txt`; the value is withheld everywhere in this packet)

- The envelope-less records of those captures are the capture host's own traffic on its tap interface. They carry the capture server's machine host name, a 16-octet single-label name, 83 times:
  - 59 times in DHCP option 12 (Host Name) of its DISCOVER and REQUEST frames;
  - 24 times as mDNS AAAA owner names.
- It is not the bench-prefixed host name the redaction masks. It is not one of the short role names the archive itself keeps (`pi`, `pw1`, `ubuntu-server`, from its own `<bench-host-prefix>` placeholders). The repository's role names (`pw1`, `pw0`, "Ubuntu server", "build box") do not include it, and the name appears nowhere in the repository.
- The equivalent fields of the other devices are handled consistently:
  - the switch's DHCP option 12 and mDNS host names are masked, 162 occurrences;
  - the controller host's DHCP option 12 is its role name `pw1`, 198 occurrences.
- The multi-encoding sweep finds 83 occurrences at the pin, the same 83 in the branch history (the same blobs) and in the first publication, and 0 in the PR tree. The receipts count 166 pattern hits per set, because the class has two patterns, the full name and its distinctive part. See the class "capture server machine host name" in `receipts/identity_sweep_targets.txt` and `receipts/identity_sweep_controls.txt`.
- It was present unchanged in the first publication and survived all three redactions. No redaction pass targeted it.

**Authority**

- CONTRIBUTING section 6: "No bench-identifying information: hostnames, home paths, bench subnets, USB serials, interface names."
- Page `:540` publishes the archive "redacted under CONTRIBUTING section 6". It lists what is masked ("bench host names with the bench prefix") and what stays ("Short host role names, ... as elsewhere in the repository"). This name fits neither.
- The round brief: no bench identity may remain in any encoding at the pin.

**Lenses**

- Docs: the page's redaction statement at `:540` is incomplete, and the evidence it pins breaks the section 6 privacy rule.
- Conformance: the box 5 PASS (`:58`) rests on raw artifacts published under section 6, and their published form does not conform.

**Impact**

- A bench host name is public in the archive that the merged page would pin permanently.
- The repository scrub cannot catch this class. A planted copy of the name in the page leaves `scripts/docs_check.py` at rc 0 (`receipts/gate_probes.txt`, probe P8). Only a field census or a value sweep finds it.

**Required outcome** (one of the two)

- (a) Mask the name, length-preserving, in DHCP option 12 and in the mDNS owner names of the six captures. All six are already in the redacted set, so the counts 77, 71 and 29 stay. Then republish, re-pin the page, and keep `MANIFEST.json` consistent.
- (b) A recorded owner or manager decision that this name is not bench-identifying, with the class named in the page's "what stays" sentence at `:540`. This is how the peer firmware version was handled.

Either way, the superseded commits that carry it are already covered by the pending purge request.

**Verification**

- `scripts/hostname_census.py` at the new pin reports no `OTHER` class, only `MASKED` and `ROLE`. Under (b), the named class is the only `OTHER`.
- `scripts/identity_sweep.py` with the private token reports 0 at the new pin and at every commit reachable from the new tip. Under (a), `scripts/page_hashes_vs_manifest.py` still resolves every page hash.
- The documentation gates pass at the new head.

**Relation to R265-3.** R265-3 reported "Capture DHCP host names: the switch's is masked; two short role names stay, as stated". I read the page's "short host role names ... as elsewhere in the repository" as the role names the archive and the repository actually use. By that reading, only `pw1` qualifies and this name does not. R265-3's check covered DHCP option 12; its mDNS review (R265-3 S1) concerned the switch's self-advertisement, not the capture server's own AAAA answers. The owner or manager may take reading (b); the finding asks that the decision be recorded and the page say so.

### S1 - SUGGESTION - Docs, RTL

`[R265] SUGGESTION Docs, RTL - docs/findings/117_GPTP_SILICON_EVIDENCE.md:340 - LINKG_STAT RX-activity delay stated as one value, 2.73 s`

- Under the page's own later-sample convention, the `0x83` to `0x03` edge follows the switch's last frame by:
  - 2.65 to 2.73 s, timed at the status sample;
  - 2.69 to 2.78 s, timed at the `mem_read` send time.
- 2.73 s is cycle 1's value. It lies outside cycle 4's edge window of 2.59 to 2.69 s.
- The six edge windows intersect at 2.68 to 2.69 s. That is the documented `act_recent` window: 2^27 guard-clock cycles, 2.684 s at 50 MHz (`docs/reference/REGISTER_MAP.md:731`).
- Receipt: `receipts/step3_rederive.json`, fields `linkg_transitions*`.
- Optional change: give the range, or write "about 2.7 s, the 2^27-cycle `act_recent` window". The difference is inside the page's stated 0.1 s resolution.

### S2 - SUGGESTION - Docs, Robustness

`[R265] SUGGESTION Docs, Robustness - docs/findings/117_GPTP_SILICON_EVIDENCE.md:177-179 - the tap clock fit's keep rule is not stated (R265-1 S2, still not taken)`

- The page reports "the residual of the kept minima is at most 2.02 ms" but does not say which minima are kept. The packet's own analysis keeps 10 of 28 windows in cycle 1, 7 of 21 in cycle 2 and 13 of 20 in cycle 3.
- Cycle 3's per-window minima form two clusters about 8.5 ms apart.
- My consensus fit (the line with the most minima within 2.5 ms) reproduces the page. A naive fit that rejects only upper outliers shifts cycle 3's tap times by about 15 ms.
- No page result depends on the choice, given the 0.1 s console resolution and the 5 s bound.
- Optional change: add one clause naming the keep rule and the resulting uncertainty.

### S3 - SUGGESTION - Docs

`[R265] SUGGESTION Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:540 vs :129 - the peer firmware string is called bench-identifying at :540 and not bench-identifying at :129`

- Line 540 lists the peer's "firmware string" among the "bench-identifying strings masked".
- Line 129, following decision 5802093720, says a firmware version "is not bench-identifying".
- The facts are right: the archive masks the string, and the digest identifies it. Only the classification is inconsistent.
- The switch's firmware version (B3, `:529`) is masked "under CONTRIBUTING section 6" on the opposite premise.
- Optional change: at `:540`, say the peer firmware string is "masked with them", or name the two decisions separately.

## Prior public findings at this head

| Prior finding | Severity | State at `dfe6a587` | Evidence |
|---|---|---|---|
| R264-3 F1: the pin published the console adapter's USB serial; only the detector-matched prefix was masked | MAJOR | CLOSED | At the pin, `bench-a200/tools/run_a.sh:9`, `run_b.sh:8` and `bench-a202/tools/cycle_locked.sh:9` read `P=/dev/<adapter>`, the whole by-id name masked. The adapter serial and by-id name classes get 0 hits at the pin and in all 10 branch commits, in every encoding. The only `serial/by-id` text left on the branch is a generic path phrase in an archived review record (`identity_sweep_targets.txt`). Page `:540` now says "whole USB by-id names". |
| R264-3 F2: the digest at `:129` recovers the firmware string the page called withheld | MINOR | CLOSED, via the "not private" branch of its required outcome | Decision 5802093720 rules the peer firmware version not bench-identifying. `:129` now says "this digest identifies the value by design". I confirmed the page value is the SHA-256 of the zero-padded 64-octet field; the 7 octets alone do not give it (`line129_check.txt`). The raw string is absent from the pin in every encoding. See S3 for the residual wording. |
| R264-3 S1: say "first 8 octets match the prefix recorded on 2026-09-14" and link the record | SUGGESTION | TAKEN | `:129` links 5670665596. Its `sha256_8` is `33f0e7f9e86fe482`, which is the page digest's first 8 octets. |
| R264-3 S2: name protocol identifiers under what stays | SUGGESTION | TAKEN | `:540`: "protocol identifiers (MAC addresses, EUI-64 clock identities, entity IDs and entity model IDs, whose OUI names a manufacturer) stay". |
| R265-3 F1: B1 and B3 contradicted the captures | MINOR | CLOSED | B1 (`:527`) and B3 (`:529`) now match `b1_b3_check.txt` in all six cycles, on both the tap and the controller-host captures. After power-on the switch sends 3 ARP probes and 2 ARP announcements for a 169.254 address. It sends IGMP from that address and from a second IPv4 address (and from 0.0.0.0). It sends one DNS-SD response with an SRV record for a `_tcp` service and a TXT record. No TCP flow exists on either link. The TXT firmware key is present in every original cycle capture (12 of 12) and masked in every published one (0 of 12). DHCP repeats every 15.0 s in the steady state. |
| R265-3 F2: "holdover clear" while the grandmaster is absent | MINOR | CLOSED | `:339` and the Step 4 row `:440` record the second episode. Re-derived per cycle: 4, 4, 4, 5, 3 and 4 samples; 0.40, 0.40, 0.40, 0.52, 0.31 and 0.41 s. Each starts at the sample where GM first reads `020000fffe000001`, and bit 3 stays clear for the rest of the interval. The RTL arms it on `gm_id_i != gm_r` (`KL_ptp_clock_validity.sv:186-198`). |
| R265-3 S1: switch DNS-SD fields not named or masked | SUGGESTION | TAKEN (masked and named) | At the pin, all six vendor-namespaced TXT strings are fully masked. Two short generic `key=digit` strings remain. The SRV instance words, the SRV target and the A owner are masked; the MAC in the instance name stays, as policy allows. `:540` names the "DNS-SD self-advertisement (vendor-namespaced keys, unit and remote identifiers, firmware version)". |
| R264-2 F1 = R265-2 F1 (peer identity hex-encoded); R264-2 F2 = R265-2 F2 (tool redaction paragraph) | MAJOR / MINOR | still CLOSED | The peer's product, serial, firmware and vendor classes get 0 hits in every encoding, and the positive controls fire. `:218-230` names exactly the four redacted quoted tools; `run_a/b/c.sh` are identity-redacted (`page_hashes_vs_manifest.txt`, `archive_claims.txt`). |
| R264-1 F1 = R265-1 F1: bare-metal-only gate red | BLOCKER | still CLOSED | `check_baremetal_only.py --check` returns rc 0, and probe P3 shows it still fires on the retired phrase. Hosted `docs-check` succeeded at this head. |
| R264-1 F2-F4 = R265-1 F2-F4: dark window, holdover span, read-only commands, envelope-less records, census, daemon scope, reach-asCapable row, follow-ups, box 5 traceability | MINOR | still CLOSED | All re-derived independently at this head (next section). #495 carries items 4 to 6; #529 and #530 cover items 1 to 3 and 9. |
| R264-2 S1; R265-2 S1, S2; R264-1 F5, F6 | SUGGESTION | not taken | Optional. |
| R265-1 S2: state the clock-fit quality | SUGGESTION | taken in part (the 2.02 ms figure) | Carried as S2 with new evidence (cycle 3 is bimodal). |

## Independent re-derivation at this head (page against the pinned raw artifacts)

| Page statement | Re-derived | Receipt |
|---|---|---|
| Step 2 cadence (`:239-242`): 4,556 / 565 / 564 / 566 intervals; Sync mean 124.99-125.02 ms, min 100.6, max 149.4; Announce max 1010.6; Pdelay_Req max 1029.6; DUT 1000.002 ms; `logMessageInterval` -3 / 0 | identical; 0 intervals outside 30 %; 569.6 s tapped | `step2_rederive.txt` |
| Turnaround (`:249-250`): 568/568, 10,984-11,009 ns, 7,552-7,569, claimed 10,608-10,629, tap-minus-claimed median 383-391 (371-400); 570/570, 0.68-0.88 ms plus 18.33 / 18.36 ms, medians 393-394 (385-524) | identical | `step2_rederive.txt` |
| Announce fields (`:127`) and "all 569" (`:410`) | 569 Announces (315 + 115 + 100 + 39), each prio1 246, class 248, accuracy 0x20, variance 0x436A, prio2 248, timeSource 0xA0, steps 0, PathTrace itself | `step2_rederive.txt` |
| Run B CRF (`:419-422`, `:479`): 34,061 PDUs, `tu=0`, continuous; bursts 19.67 / 18.45 / 15.00 / 15.00 s; pauses 1,106 / 578 / 148 ms; 500 PDU/s; PCP 3, VID 2; destination `91:e0:f0:00:8d:6f` | identical | `step2_rederive.txt`, `archive_claims.txt` |
| Step 3 table (`:312-317`): every column | each cell within 0.01 s. Recovery 0.509 / 0.512 / 1.507 / 0.426 / 1.463 / 1.601 s, against the page's 0.51 / 0.52 / 1.51 / 0.43 / 1.46 / 1.60. Cycle 2 differs by 0.008 s through the fit choice | `step3_rederive.txt/.json` |
| Loss offsets (`:325-327`): 0.40-0.46 s after the last Sync (edge 0.30-0.46), 3.01-3.08 s after the last Announce, 5.0-5.1 s after the last Pdelay_Resp | 0.403-0.464 (edge 0.303-0.464); 3.009-3.077; 5.015-5.091 | same |
| Holdover at loss (`:325`): 3-5 samples, 0.30-0.50 s | 3/3/5/3/4/4; 0.30/0.30/0.50/0.31/0.41/0.41 | same |
| Dark window (`:341`): switch's last frame 0.63-0.73 s; last record DUT-sent (cycle 2 a Pdelay_Req at 1.75 s); nothing from 1.03-1.75 until 37.55-38.57 s | 0.626-0.730; all DUT-sent (cycle 2 Pdelay_Req 1.752); 1.031-1.752 until 37.555-38.573 | same |
| Master window (`:342`): 0.1-0.6 s; 1-4 Sync; self-Announce, prio1 248, in cycles 3 and 5 | 0.10-0.60; 3/2/4/1/3/4; cycles 3 and 5 only, prio1 248 | same |
| Return (`:346-351`): carrier 13.6-13.8 s after "on"; first frame 3.7-4.5 s later; first Announce 1.0-1.7 s after that, Sync 0-18 ms behind; which-Announce split; `tu` clear 0.41-0.52 s after adoption | 13.63-13.80; 3.70-4.48; 1.00-1.72, 0-16 ms; cycles 1, 2, 4 and 3, 5, 6 as stated; next Announce 1.007 s; 0.414-0.52 | same |
| Reach asCapable (`:41`, `:442`): within one sample of the DUT's second completed Pdelay; 1.03-1.64 s after the first frame; 377-389 ns | 0.014-0.094 s after the second completion (pairing includes the request sent just before the link returned); 1.02-1.64 s; 385/377/385/385/389/382 | same |
| `CLKV_TUCNT` +40/+39/+41/+40/+40/+41; span 38.5-39.7 s; path generation +1 per edge, count 1; `RST_EPOCH` 1 | identical; spans 39.3/38.5/39.5/39.26/39.44/39.66 | same |
| Cycles 4-6 CRF and ACMP (`:385-399`) | all as stated: first `tu=1` 1.08/1.07/1.00, inside 1.06-1.17 / 0.99-1.09 / 0.96-1.06; 316/293/243 `tu=1` PDUs; end 1.71/1.65/1.49; licence drop 2.21/5.23/1.89; relicence 41.25/42.92/41.45 (0.83/2.38/0.72 after all-good); no CONNECT_TX between off and all-good; first after return 41.28/42.96/41.46, first PDU right after, all `tu=0`; bind -28.2 to -28.4 s, unbind 109.8 s, first attempt; AECP codes to the DUT only 0x27/0x28/0x29 | `step3_rederive.json`, `archive_claims.txt` |
| DUT ADPDU (`:443`, `:497`): none during absence; first after adoption 0.54-2.56 s, naming the switch | none; 0.544-2.555, switch | `step3_rederive.json` |
| Observation 7: PHC steps -128.5 / -355.9 / -163.3 / -154.5 / -180.3 / -154.1 s, equal to the "on" interval within 0.04 s | identical; residuals 0.036 / -0.011 / -0.003 / -0.004 / -0.001 / 0.007 (cycle 1 against attempt 1's guard "on") | `archive_claims.txt` |
| Attempt 1 (`:290-299`): guard "on" after 5.95 s; carrier lost 1.14 s, back 13.7 s after the early "on"; first poll about 4 s later names the DUT, asCapable clear; the switch 2 s after | 5.95; 1.14; 13.69; 23.75 s (DUT, 0); 25.75 s (switch, 1) | `archive_claims.txt` |
| Reference-peer table (`:358-365`) and observation 11 | identical: first poll 38.23/38.16/38.15/38.80/38.15/38.64; switch named 38.23/46.66/46.65/38.80/38.15/38.64; ADP self 39.84 and 41.65 | `peer_view.txt` |
| Archive (`:134`, `:397`, `:505`, `:540-542`): envelope-less 76; 38, 0, 38, 45, 0, 37; 18; 0 elsewhere; 19 tcpdump logs with 0 dropped; 14 transcripts with 38,954 read commands; 18 ACMP states with one `stream_dest_mac` difference; two hosts daemon-free; 77 / 71 / 6; 20 / 57 `sha256sum -c` FAILED; 29 redacted table hashes | identical | `archive_claims.txt`, `page_hashes_vs_manifest.txt` |
| Build hashes (`:84-91`), grader and tool hashes (`:203-230`) | `.bit`, payload and AEM are in the CRC table of both packets; `bios.bin`, `csr.csv` and `flashboot_layout.json` are not. The grader equals the `ede8d48e` blob. `95d64fd5`, `ad579e18` and `0e9faf30` are full on 5584039577; `8ef4b008` is nowhere | `archive_claims.txt`, `page_hashes_vs_manifest.txt` |
| Register decodes | `CRFT_CTRL` `0x3002E3` = enable, class A, tagged, reservation, licensed, VID 2, PCP 3; `GPTP_LAT` 656 / 219 ns; `CLKV_STAT` bits 0/1/3/16 | `REGISTER_MAP.md:731,770,875,1392` |

## Per-lens results at this head

- `[R265] MINOR Docs, Conformance - see F1.` Conformance was otherwise applied clean:
  - page rows `:38-58` against the frozen acceptance and the owner decisions of 2026-09-06 and 2026-09-23. The asCapable partner is the switch; the page states this and ties it to the one-DUT decision;
  - `docs/design/GM_LOSS_RECOVERY.md:88-118` against 5795898094: 5 s = 3 s + 0.375 s + 1.625 s. The announce and sync receipt timeouts are at the Milan 1 s and 125 ms intervals. The start (first Announce or Sync) and end (asCapable and sync) are consistent with the page's stricter all-good end point;
  - every figure in the re-derivation table.
- `[R265] PASS RTL - hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:174-200, hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:648, docs/reference/REGISTER_MAP.md:731,770,875,1392 - the diff touches no RTL, and every RTL-behaviour claim on the page matches the RTL and the register map.` Checked:
  - holdover armed on any `gm_id_i` change, on `pub_disc` and on PHC steps, for 2 quarter-ticks (0.25-0.5 s), which matches the observed 0.30-0.52 s;
  - the `LINKG_STAT` `act_recent` window;
  - the CSR decodes.

  S1 is a SUGGESTION.
- `[R265] PASS Robustness - review-evidence/117-r1 at db842315: attempt1-aborted/*, all 22 pcaps, 14 console transcripts, clock-*.jsonl - the evidence handles its failure and edge paths honestly and reproducibly.` Checked:
  - the aborted attempt;
  - envelope-less exclusion;
  - 2^32 ns unwrap across the 36-37 s dark windows;
  - Pdelay pairing across the link return;
  - NOT RUN rows where the peer link is untapped;
  - the later-sample edge convention;
  - clock-fit sensitivity, at most about 0.015 s, S2 only;
  - length-preserving masks: all 22 captures parse to their last record.
- `[R265] PASS Tests - receipts/docs_gates_at_head.txt, receipts/gate_probes.txt, receipts/page_links.txt - no test file changes, and the gates the PR relies on pass at this head and can fail on this page.`
  - The gates: 14 commands rc 0, including `docs_check`, `check_baremetal_only --check`, `check_em_dash --base ede8d48e` (0 findings over 670 added lines, arms 57/57), `gen_toc --check` and `--verify-anchors`, and `check_doc_paths`.
  - Mutation probes, each restored to the exact HEAD blob: `docs_check` fires on a planted bench-host line, a peer-product line and a home-path line; `check_baremetal_only` fires on the retired phrase; `--verify-anchors` fires on a broken cross-page anchor.
  - `docs_check` also fires on a broken relative-link target (P6b). No gate checks in-page anchors: P5 stays silent under all four gates tried. So I resolved all 75 relative links and anchors directly: 0 broken.
- `[R265] MINOR Docs - see F1.` Docs was otherwise applied clean:
  - every statement the correction commit changes, re-derived above;
  - all 74 raw-artifact hashes resolved at the pin, with published bytes matching;
  - `MANIFEST.json` pin entries identical at the tip;
  - the design page and the index row;
  - #495, #529 and #530 carry what the page says they do;
  - PR commits one-line, with no trailers and no superseded link.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MINOR) | issue #117 acceptance and decisions 5561827955, 5789767491, 5795898094, 5802093720; page `:34-64`, `:261-452`, `:540`; `GM_LOSS_RECOVERY.md:88-118`; raw captures, transcripts and watcher logs at `db842315` | R265-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| RTL | CLEAN | diff `ede8d48e..dfe6a587` (no RTL or gitlink change); `KL_ptp_clock_validity.sv:174-200`; `KL_gptp_shadow.sv:648`; `REGISTER_MAP.md:731,770,875,1392`; page `:403-452` | R265-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Robustness | CLEAN | `attempt1-aborted/*`, 22 pcaps (envelope, unwrap, pairing, fit), 14 transcripts, NOT RUN rows `:49`, `:54-57`, `:401` | R265-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Tests | CLEAN | 14 documentation gate commands at head; 17 mutation probes, each restored (17 of 17 as expected); the 75-link check | R265-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |
| Docs | UNCLEAN (F1 MINOR) | the three changed pages (all 629 lines of the findings page); `MANIFEST.json` and both `MANIFEST.sha256` at `db842315`; the 10 branch commits to `7626fb2b`; the three PR commit trees | R265-4 | dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba |

SUGGESTIONs do not affect coverage.

Answering F1 either way changes page `:540`, and under outcome (a) also `:535-536` and the archive. That un-covers Docs and Conformance, which must be re-covered at the new head. Robustness and Tests read the same page and must be re-applied to whatever changes. RTL stays banked while nothing in its scope changes.

## Real limits

- **Evidence, not the product.**
  - Physical calibration was NOT RUN, and field or hosted skips are not hardware proof.
  - As the page states, these are NOT RUN too: the reference peer's own recovery time, the first reach after the flash, Hive, behave, latency and audio.
  - I had no bench access.
- **Build artifacts are not public.** Image identity rests on the CRC32 readbacks. The `bios.bin` and `csr.csv` hashes exist only on the page. The la_avdecc library and probe hashes were checked only against the public record, not against binaries.
- **Identity tokens.** They come from three sources:
  - what the redactions changed, found by diffing the superseded public publications against their successors;
  - the repository's scrub rules;
  - field censuses of DHCP option 12, mDNS owner names, TXT strings and IPv4 source addresses, which is how F1 was found.

  An identifier that no redaction touched and that sits outside these fields would be missed. The derived values are kept private and the derivation step is withheld while the purge is pending. Without the private token file, `scripts/identity_sweep.py` applies the repository rules only.
- **IPv4 addresses.** The only unicast IPv4 sources in any capture are the switch's self-assigned link-local address and its second address. No management or bench-subnet address appears. I did not treat the switch's second address as a bench subnet; the page does not address it.
- **Base64.** Base64 is matched by stable core. Tokens shorter than 4 octets are covered at alignment 0 only.
- **Tap clock line.** Mine is a consensus line through the per-5 s minima (see S2). It agrees with the page within about 0.01 s in every cycle.
- **Not run.** The scoped Verilator was not used, because the diff has no RTL. No full parent, PP, gPTP, Yosys or builder bank was run, by instruction. The manager's bank results for this head were not re-verified. The evidence link in the round brief points at a superseded archive tree.
- **Hosted checks, metadata only** (`receipts/hosted_check_runs_dfe6a587.tsv`; I read no logs):
  - executed and successful: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, `changes` and `bdd-conformance`;
  - completed as skipped, not executed: `verilator-suites`, `yosys-portability`, both shard matrices, `verilator-lint`, `yosys-elaboration` and the physical gPTP job.
- **Reports not read.** The archived review records on the evidence branch were swept mechanically for identity and for superseded-SHA mentions, and not otherwise read. The parallel round-4 internal review was not read.

## Pending manager duties

1. **F1.** Either re-redact the six captures (outcome a), re-pin, and correct `:540` and `:535-536`, or record a decision and name the class at `:540` (outcome b). Then re-review at the new head.
2. **Purge of superseded evidence objects** (decision 5800264651). This round fetched the four superseded commits named in the manager's archive note by full SHA from the public remote, and all four resolved. None is an ancestor of the current tip, and the positive controls show two of them carry the identities later removed (`receipts/superseded_objects.txt`).
3. **Superseded SHAs in archived review records.** They are named 163 times in 82 files under `reviews/` on the evidence branch, and nowhere else on it. The R264-3 question, whether these fall under the "history link" decision, is still open. No PR commit links any of them.
4. **Merge-turn duties.**
   - Build the final current-dev candidate against live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a` (source base `ede8d48e`). That is distinct from this source-head review.
   - Complete hosted and act acceptance, candidate validation and post-merge containment.
   - Merge only with explicit maintainer authorization.
5. **Issue #117 boxes** stay the owner's call:
   - box 1's partner is the switch, under the one-DUT decision;
   - box 4 carries FAIL and NOT RUN rows;
   - audio is deferred to 2026-12-31;
   - the PR only relates to the issue.

## Receipts and reproduction

`scripts/run_all.sh CLONE EVID_GITDIR OUT [TOKENS_JSON] [ORIGINAL_ROOT]` regenerates every receipt except these five:

- `baseline_before.txt`, `restore_verify.txt`, `hosted_check_runs_dfe6a587.tsv` and `identity_sweep_controls.txt` (the controls need the superseded objects);
- `line129_check.txt` and `superseded_objects.txt`, which are withheld-value summaries.

A second full run reproduced the other receipts byte for byte. The token file and the original archive root are private inputs and are not published. Receipts name tokens by class label only and never print a withheld value.

- **Page against archive:**
  - `receipts/page_hashes_vs_manifest.txt`
  - `receipts/archive_claims.txt`
  - `receipts/step2_rederive.txt`
  - `receipts/step3_rederive.txt`
  - `receipts/step3_rederive.json`
  - `receipts/peer_view.txt`
  - `receipts/b1_b3_check.txt`
  - `receipts/line129_check.txt`
- **Identity and links:**
  - `receipts/hostname_census_pin.txt`
  - `receipts/identity_sweep_targets.txt`
  - `receipts/identity_sweep_controls.txt`
  - `receipts/pr_commits_archive_links.txt`
  - `receipts/superseded_objects.txt`
- **Gates and state:**
  - `receipts/docs_gates_at_head.txt`
  - `receipts/gate_probes.txt`
  - `receipts/page_links.txt`
  - `receipts/hosted_check_runs_dfe6a587.tsv`
  - `receipts/baseline_before.txt`
  - `receipts/restore_verify.txt`: the clone restored exactly. HEAD, tree and index are exact; all 865 tracked blobs match in bytes and mode; there are no hidden index flags and no untracked or ignored file; the four gitlinks are at stage 0 at their pins, with the two initialized processor submodules clean.
- **Scripts:** `scripts/tapdec.py`, `step2_rederive.py`, `step3_rederive.py`, `b1_b3_check.py`, `hostname_census.py`, `identity_sweep.py`, `page_hashes_vs_manifest.py`, `peer_view.py`, `archive_claims.py`, `gate_probes.py`, `page_links.py`, `pr_links.sh` and `run_all.sh`.

R265-4 FINISHED
