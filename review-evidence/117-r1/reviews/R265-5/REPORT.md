[R265] POSITIVE - exact head b71061d7fbc1119b02eb430f293672ff8b3f85b8

Round R265-5, external independent review of kebag-logic/milan-fpga issue #117 / PR #531. Exact head `b71061d7fbc1119b02eb430f293672ff8b3f85b8`, tree `b39c840146a4d5ebee53c8633384017137ce896e`, source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The diff is docs-only: three Markdown pages, 670 added lines, no HDL, script, config or gitlink change.

**Verdict: POSITIVE.** All five lenses are covered clean at this head. No BLOCKER, MAJOR or MINOR finding is open. The one finding open at the previous head, R265-4 F1 (the capture server's machine host name in six captures), is closed. I verified that from my own census of the new pin, its history, the PR range and the later archive commits. Two new SUGGESTIONs are optional.

The verdict and ledger were written to this file after my independent pass and before I read any prior review round. The reconciliation of prior findings was added afterwards and changed neither.

## 1. What was reconstructed, and from where

- Contract: AGENTS.md, CONTRIBUTING.md (sections 2, 3, 6 and 6.1) and docs/README.md.
- Scope: the #117 body and acceptance boxes, plus these owner and manager decisions:
  - 5561827955 and 5565246390: the one-DUT contract;
  - 5789767491: unattended steps 2 to 5;
  - 5795898094: the switch power cycle and the 5 s bound;
  - 5802093720: the peer firmware version is not bench-identifying;
  - 5800264651: superseded archive commits are not acceptable, and a purge is requested.
- Build and bench records on #117: 5794859125 (A198), 5795658105 (A200) and 5796668867 (A202).
- Authorities:
  - REQUIREMENTS.md REQ-VER-05 and docs/integration/BUILDING.md 4.1 (the one-DUT contract);
  - docs/reference/MILAN_COMPLIANCE_MATRIX.md rows 4.2.6.1.1 (800 ns) and 4.2.6.2.6 (15 ms);
  - docs/reference/REGISTER_MAP.md;
  - `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv` and `hdl/milan/milan_datapath.sv`.
- Diff and history: `git diff ede8d48e..b71061d7` and the three linear, one-line PR commits `c3eb95fa`, `0abf147f` and `b71061d7`.
- Executable evidence: the pinned archive `bb8c690f8487c202f2f53dbcba2b84dc4c36df73` (branch `117-review-evidence`, tip `915d2faaba392ed43a878f39c9abbaa92d40f316`), extracted and checked byte by byte.
  - The round brief linked the archive tree at `32aec661`. That is a superseded, pre-redaction generation of the same archive.
  - I used it only as the positive control for the identity census, and quote no value from it. See section 7.

## 2. Findings

No finding at BLOCKER, MAJOR or MINOR.

### R265-5-S1 - SUGGESTION - Robustness, Docs

`[R265] SUGGESTION Robustness, Docs - docs/findings/117_GPTP_SILICON_EVIDENCE.md:534-537 - the page's only raw-artifact locator pins a commit reachable solely through an unprotected branch that has been rewritten four times`

- **Evidence.**
  - `receipts/evidence_branch_protection.txt`: `117-review-evidence` reports `protected: false` and no branch rules, and no tag points at `bb8c690f`.
  - The manager's archive note (appended to 5799413596 and later) records four whole-history rewrites.
  - `receipts/superseded_archive_reachability.txt`: the four superseded pins survive only as unreachable objects, and those are slated for purge.
- **Impact.**
  - After merge, box 5's PASS (`:58`) and every hash table (`:544-628`) depend on `bb8c690f` staying reachable.
  - A fifth rewrite of the branch would leave `bb8c690f` unreachable. A purge or garbage collection would then make the merged page's locator dangle.
  - Nothing fails today.
- **Suggested outcome (optional).** Choose one:
  - an immutable ref at `bb8c690f` (a tag);
  - branch protection that forbids force-pushes on `117-review-evidence`;
  - a sentence on the page saying that any re-pin must update this page in the same change.
- **Verification.** `git ls-remote --tags origin` lists a tag at `bb8c690f`, or the branch API reports `protected: true`.

### R265-5-S2 - SUGGESTION - Docs

`[R265] SUGGESTION Docs - docs/findings/README.md:11 - the index State cell headlines only the GM loss and return pass`

- **Evidence.**
  - The State cell reads "Current; GM loss and return inside the 5 s bound (worst 1.60 s)".
  - The page records a FAIL at `:53` (la_avdecc Milan compatibility, #529) and NOT RUN rows at `:54-57`.
- **Impact.** None on correctness. A reader who stops at the index could take the entry for an overall pass.
- **Suggested outcome (optional).** Add "Milan enumeration FAIL (#529); Hive, latency and audio NOT RUN" to the State cell.
- **Verification.** Re-read the row.

## 3. Per-lens results at this head

```text
[R265] PASS Conformance - docs/findings/117_GPTP_SILICON_EVIDENCE.md:34-64,261-452 and docs/design/GM_LOSS_RECOVERY.md:88-118 against the raw files at bb8c690f and decision 5795898094 - every numeric claim I re-derived matches (receipts/recompute_step3.txt, recheck_stream.txt, recheck_counts.txt, recheck_prior_items.txt, recheck_census_a200.txt, external_hashes.txt)
[R265] PASS RTL - no HDL, testbench or gitlink change (receipts/clone_integrity.txt); page CSR decodes :408-420,437-445 against REGISTER_MAP.md rows 0x624/0x628/0x62C/0x730/0x734/0x750/0x764/0x774/0x77C/0x780/0x7E4/0x7F0 and KL_ptp_clock_validity.sv:70-78,185-200 with milan_datapath.sv:1927-1945 - consistent
[R265] PASS Robustness - pin bb8c690f, its history ede8d48e..bb8c690f, PR range ede8d48e..b71061d7 and later archive range bb8c690f..915d2faa - 0 identity-token hits in 20 to 23 encodings per token, captures structurally intact, no superseded archive SHA in PR text (receipts/census_*.txt, pr_sha_references.txt, verify_manifest_pin.txt)
[R265] PASS Tests - documentation gates at b71061d7 all rc 0 (receipts/docs_gates_head.txt, docs_gates_head_extra.txt); planted probes on the page fire for the bare-metal term, home path, dead file link and dead cross-page anchor (receipts/mutation_probes.txt); independent re-derivation of the page's numbers with separate code
[R265] PASS Docs - the three changed pages, every fragment link (receipts/fragments_head.txt), all 82 full hashes and 35 abbreviated hashes on the page against MANIFEST.json and the external records, both MANIFEST.sha256, redaction statement :540-542, commit format - consistent and accurate
```

### Conformance: what was checked

- **Step 3 per-cycle table** (`:310-317`), recomputed by `scripts/recompute_step3.py` from the raw files.
  - Inputs: power-strip command times, clock offsets, console transcripts and the tap captures, placed with my own clock fit (median-slope start, 2 ms inliers).
  - It does not read the packet's analysis files.
  - Result: every column matches within 0.01 s. Worst recovery is 1.60 s against the 5 s bound, and the recovery measured from the first Sync is the same or up to 0.02 s shorter.
  - Loss side: sync lost 0.40 to 0.46 s after the last Sync; own grandmaster 3.00 to 3.08 s after the last Announce; asCapable cleared 5.01 to 5.09 s after the last Pdelay response.
  - Return side: asCapable came within 0.01 to 0.09 s of the DUT's second completed Pdelay exchange, at peer delay 377 to 389 ns. The DUT sent 1 to 4 Syncs as master, and a self-naming Announce in cycles 3 and 5 only. The CSR followed the adopted Announce by 0 to 74 ms.
- **Stream rows, cycles 4 to 6** (`:385-387`). The first `tu=1` PDUs came at 1.08, 1.07 and 1.00 s, with 316, 293 and 243 `tu=1` PDUs. The first PDUs after return came at 41.28, 42.96 and 41.46 s, and every one after the return had `tu=0`. No ACMP CONNECT_TX reached the DUT between the loss and all-good.
  - The console licence times match under the page's stated convention: a sample carries its `milan_status` send time.
- **Step 2** (`:237-258`). 4,556 Sync intervals (100.6 to 149.4 ms), 565 Announce, 564 and 566 Pdelay_Req. 568 of 568 and 570 of 570 exchanges completed. DUT turnaround 10.984 to 11.009 us; the switch took 18.33 and 18.36 ms twice.
- **Run B.** 34,061 CRF PDUs, all `tu=0`, with no sequence discontinuity.
- **Countable claims.**
  - Envelope-less records: 76; then 38, 0, 38, 45, 0 and 37; then 18; 0 elsewhere.
  - 38,954 console commands in the 14 transcripts, only `milan_status`, `mem_read`, `mem_list` and `crc`.
  - 19 tcpdump logs, each with 0 dropped.
  - `CLKV_TUCNT` deltas: +40, +39, +41, +40, +40 and +41.
  - Observation 7: on-command intervals of 355.93, 163.28, 154.51, 180.29 and 154.08 s. Cycle 1's 128.5 s is measured from attempt 1's guard "on"; the packet's `attempt1-aborted/NOTE.md` records that the sequence's own later "on" found OUT4 already on.
  - A200 census: 18 ACMP states, all unbound. Only DUT Stream Output 1's `stream_dest_mac` differs, as `:505` says.
- **External anchors.**
  - The grader's SHA-256 at `ede8d48e` is `bc41ab03...`.
  - `95d64fd5`, `ad579e18` and `0e9faf30` resolve in full on 5584039577. `8ef4b008` has no full value there, as the page says.
  - `33f0e7f9e86fe482` is the 8-octet prefix on 5670665596. I recomputed the full digest over the 64-octet firmware field, and the pin masks the raw string.
  - The `.bit`, payload and AEM hashes appear in both byte-identical `identity/expected-crc.txt` files, and `.bit`, AEM and layout in 5794859125.
- **Design page.**
  - `GM_LOSS_RECOVERY.md:88-118` reproduces the owner's decision: start, end, 5 s, and the media clause.
  - The sum 3 + 0.375 + 1.625 = 5 is right, and the Milan intervals are cited correctly.
- **Acceptance framing.** Box 1's asCapable partner is the bench switch (`:60-64`). BUILDING.md 4.1 and REQ-VER-05 name the reference peer and the bench AVB switch but not the DUT's link partner.
  - asCapable is a per-link property, so a bridged bench can satisfy "against the reference peer" only through the switch.
  - The page publishes that reading and its basis rather than hiding it, and the PR says "Relates to #117", not "Closes".
  - I judge the reading acceptable for a findings record. Ticking the boxes remains the maintainer's call.

### RTL: what was checked

These decodes all match REGISTER_MAP.md:

- `CLKV_STAT` bits [0] `tu`, [1] sync, [3] holdover and [16] asCapable, so `0x00010002`, `0x00010009` and `0x00000001` read as the page says.
- `ASP_CMD` `0x11` is generation 1, count 1.
- `GPTP_LAT` `0x029000DB` is 656 ns in and 219 ns out.
- `CRFT_CTRL` `0x3002E3` means enabled, class A, tagged, reservation active, licensed, VID 2 and PCP 3.
- `LINKG_STAT` `0x83` and `0x03` differ only in `act_recent`, whose 2^27-cycle window is 2.68 s at 50 MHz.

The holdover claims at `:339` and `:351` match the RTL. It arms on any change of `gm_id_i`, with `HOLD_QTICK_P` = 2, giving 0.25 to 0.5 s; `milan_datapath.sv` does not override the parameter.

### Robustness: what was checked

- **Identity census.** `scripts/identity_census.py` reads tokens from a private list that is not published, and reports only class labels.
  - It searches 20 to 23 encodings per token: raw (case-insensitive), ASCII hex in 8 forms (lower or upper case, bare or separated by `:`, space or `-`), base64 and URL-safe base64 in 3 alignments each, UTF-16LE/BE, NetBIOS, DNS label, reversed, and URL/JSON/HTML escapes for tokens containing `&`.
  - Positive control: the superseded `32aec661` generation fires 528 times across the capture-host, switch DNS-SD, product and peer-firmware classes.
  - At the pin, its history, the PR range and the later review-archive range, the only hits are numeric or binary coincidences, which I inspected: a relative time value in two analysis files, epoch timestamps in one watcher log, and random capture bytes.
- **Protocol-field extraction.** `scripts/pcap_identity_fields.py` covers DHCP, mDNS, LLMNR, NetBIOS, SSDP, DHCPv6 and LLDP. Every name field is masked except `pw1`, the controller host's role name, which BUILDING.md:511 already uses.
- **Printable strings.** `scripts/printable_strings_census.py` scans every capture frame and every decoded hex or base64 payload. The only readable names are the DUT's own descriptor strings. The switch's RSTP padding carries stale bytes, none of identity length.
- **Pattern scans.** No home path, `user@host`, USB by-id, MAC-derived interface name or `.local` host name remains in text. Placeholders are consistent.
- **Captures.** All 22 walk to exact EOF.
- **PR text.** The only commit SHAs referenced are the pin, the base and `f6b31625`. No superseded archive SHA appears.

### Tests: what was checked

- **Gates.** These all return rc 0 at the head:
  - `docs_check.py`, `check_doc_style.py`;
  - `gen_toc.py --check` and `--verify-anchors`;
  - `check_em_dash.py --base ede8d48e` (670 added lines, 57/57 arms);
  - `check_gptp_docs.py`, `check_feature_status.py` and its self-test (46/46);
  - `check_solution_docs.py`, `check_baremetal_only.py --check`, `check_submodule_docs.py`;
  - `DOC_MAP.gen.py --check` and `gen_module_matrix.py --check`.
- **Probes that fire.** Each probe was planted on the page and then restored: a retired-stack term fails the bare-metal gate, a home path and a dead relative file link fail `docs_check`, and a dead cross-page anchor fails `--verify-anchors`.
- **Probes that show gate scope.**
  - A dead same-page anchor is not gated. `scripts/check_fragments.py` resolves all 38 fragment links on the three pages.
  - The added-line em-dash gate judges commits, not the worktree.

### Docs: what was checked

- **Manifests** (`scripts/verify_manifest.py`).
  - MANIFEST.json covers exactly the 236 archive files, and every published hash matches the bytes.
  - 77 files are redacted: 71 identity-redacted and 6 path-only. No file is flagged but unchanged, or changed but unflagged.
  - `sha256sum -c` gives 20 FAILED in the A200 packet and 57 in the A202 packet, exactly the redacted sets. Every manifest line equals its original hash.
- **Page hashes.**
  - All 74 raw-artifact rows (73 distinct hashes) resolve as original hashes. 29 name redacted files: 18 captures, 6 analyses, 3 censuses, 1 entity dump and 1 lock log.
  - The four quoted tool hashes whose files are redacted (`8c9f2885`, `45889a7d`, `c4ef8c9a`, `bdd228a1`) and the three unquoted scripts (`run_a.sh`, `run_b.sh`, `run_c.sh`) are exactly the seven redacted tools.
- **Redaction statement.** `:540` names the capture server's own host name class.
- **Commits.** All three PR commits are one line with no trailers.

## 4. Prior findings at this head

Read after my own pass. Each item is judged against my own receipts.

| Prior item | Severity | Status at b71061d7 | Evidence |
|---|---|---|---|
| R265-4 F1: capture server host name in DHCP option 12 and mDNS of six captures | MINOR | CLOSED, option (a) | DHCP opt 12 masked (59), mDNS owner/PTR masked (24+24); 0 hits pin/history/PR/tip vs 83 raw + 83 DNS-label at the control; `:540` names the class; counts 77/71/29 unchanged (census_*.txt, verify_manifest_pin.txt) |
| R264-4 S1: same host name, "stays" sentence | SUGGESTION | taken via R265-4 F1 (a) | as above |
| R264-3 F1: console adapter USB serial in scripts | MAJOR | still CLOSED | no `by-id`/`usb-` string at the pin; scripts read `P=/dev/<adapter>` |
| R264-3 F2: digest recovers a "withheld" firmware value | MINOR | still CLOSED (decision 5802093720) | `:129` says the digest identifies the value by design; digest recomputed |
| R265-3 F1: B1/B3 switch facts vs captures | MINOR | still CLOSED | ARP probes from 0.0.0.0 and announcement from the link-local address, IGMP from it and a second address, DNS-SD `_oca._tcp` service present (masked) |
| R265-3 F2: holdover at the identity change | MINOR | still CLOSED | `:339`; re-derived 3 to 5 samples, 0.31 to 0.52 s (recheck_prior_items.txt) |
| R264-2 F1 = R265-2 F1: peer identity hex-encoded | MAJOR | still CLOSED | 0 hits for product/vendor/firmware classes in any encoding; masked prefix visible only as `####` |
| R264-2 F2 = R265-2 F2: tool redaction paragraph | MINOR | still CLOSED | `:220-227` matches the seven redacted tools |
| R264-1 F1 = R265-1 F1: bare-metal gate red | BLOCKER | still CLOSED | rc 0 locally; hosted `docs-check` success at this head; probe fires on the page |
| R264-1 F2 = R265-1 F4: follow-up issues | MINOR | still CLOSED | `:53` and `:467` link #529; `:473-487` and `:496` link #530 and #495; `:488-492` give items 8 and 10 reasons |
| R264-1 F3 = R265-1 F2: dark window, loss holdover, read-only commands, envelope records, census, daemon scope | MINOR | still CLOSED | dark window 1.04 to 1.76 s, all DUT-sent; loss holdover 3 to 5 samples, 0.30 to 0.50 s; 38,954 read-only commands; envelope counts; A200 census; `:45`, `:259` name two hosts (daemon process check not re-executable from the archive) |
| R265-1 F3: stale "reaches asCapable" row | MINOR | still CLOSED | `:41` re-derived (section 3) |
| R264-1 F4: box 5 traceability and privacy | MINOR | CLOSED | all table hashes resolve; privacy part closed with R265-4 F1 |
| R265-4 S1 = R264-4 S3: `LINKG_STAT` "2.73 s" as one value (`:340`) | SUGGESTION | not taken; optional | unchanged text; inside the stated 0.1 s resolution |
| R265-4 S2 (= R265-1 S2 in part): clock-fit keep rule (`:177-179`) | SUGGESTION | not taken; optional | my differently-kept fit reproduces every page time within 0.01 s, so no result depends on it |
| R265-4 S3 = R264-4 S2: firmware classification `:540` vs `:129` | SUGGESTION | not taken; optional | `:540` still lists the peer firmware string under bench-identifying strings masked |
| R264-1 F5, F6; R264-2 S1; R265-2 S1, S2 | SUGGESTION | not taken; optional | no effect on coverage |
| R264-2 S2, R264-3 S1/S2, R265-3 S1, R265-1 S1 | SUGGESTION | taken | `:541`, `:129`, `:540`, `:534-537` |

## 5. Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 117 page `:34-64`, `:118-134`, `:232-452`, `:503-529` against raw files at `bb8c690f`; GM_LOSS_RECOVERY.md `:88-118` against decision 5795898094; BUILDING.md 4.1; REQ-VER-05; compliance rows 4.2.6.1.1 and 4.2.6.2.6; external records 5584039577, 5670665596, 5794859125 | R265-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| RTL | CLEAN | diff paths and gitlinks (unchanged from base); REGISTER_MAP.md rows for every decoded CSR; KL_ptp_clock_validity.sv:60-78,117-122,185-211,245-248; milan_datapath.sv:1927-1945 | R265-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Robustness | CLEAN | 237 files of the pin; 231 blobs and 4 commits of `ede8d48e..bb8c690f`; 379 blobs of `bb8c690f..915d2faa`; 6 blobs and 3 commits of the PR range; 22 captures; failure-path statements (attempt 1, envelope exclusion, drop logs, bench-state restore) | R265-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Tests | CLEAN | 13 documentation gate runs at the head; 8 planted probes; 5 independent re-derivation scripts plus the manifest, fragment, census and capture-field scripts; exact-head hosted check runs (executed vs skipped) | R265-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |
| Docs | CLEAN | 117_GPTP_SILICON_EVIDENCE.md (629 lines), GM_LOSS_RECOVERY.md, findings/README.md; 38 fragment links; MANIFEST.json; both MANIFEST.sha256; 82 full and 35 abbreviated page hashes; PR commit messages | R265-5 | b71061d7fbc1119b02eb430f293672ff8b3f85b8 |

Every lens was applied at the merge candidate head itself. No BLOCKER, MAJOR or MINOR is open under any lens. The two new SUGGESTIONs and the carried optional ones do not affect coverage.

## 6. Real limits

- **Physical.** Physical calibration was NOT RUN. I touched no hardware, and field skips are not hardware proof. Every silicon statement rests on the published captures, transcripts and logs.
  - Two further items can't be re-run from the archive: the daemon process check (`:259`) and the controller-side enumeration statistics (`:461`).
- **Census scope.** The census covers the token classes I could derive from public material. Classes masked before the earliest generation I inspected (`32aec661`, the second of five) were covered by field extraction, printable-string, decoded-payload and pattern scans, not by value.
  - A value shorter than 4 octets, or one that is not printable, would evade those scans.
  - I did not fetch the first generation.
- **Not re-derived.** These were checked only for internal consistency:
  - the reference-peer table (`:358-365`);
  - the Step 4 steady-state controller values;
  - the Run B burst timings in observations 1 and 2;
  - observations 4 and 8 to 12.
- **Clock placement.** Tap times use my own fit. In cycle 1 it kept 4 of 28 windows, with a maximum residual of 0.59 ms. It reproduces the page within 0.01 s.
- **Probes.** The em-dash gate cannot be probed without a commit, and no commit was made.
- **Not executed.** The scoped Verilator was not used, because the diff has no RTL or testbench. No full parent, PP, gPTP, Yosys or builder bank was run, and no container, act or host runner.
- **Manager bank.** I could not verify the stated bank pass at this head from public evidence.
  - The brief's evidence link is the superseded archive tree `32aec661`, which holds bench packets only.
  - The last manager head note (5805121280) says "Bank r5 is running".
- **Clone state.** It was restored and verified after the probes:
  - 865 tracked blobs rehashed with 0 mismatches;
  - index equal to the HEAD tree, with no stage, skip-worktree or assume-unchanged flags;
  - exec bits consistent;
  - gitlinks unchanged from the base;
  - `protocol-processor` and `gptp-processor` at their gitlinks and clean.

## 7. Pending manager duties

1. **Final candidate.** Validate the current-dev candidate at the merge turn, on live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a` against source base `ede8d48e`, with the full local bar and post-merge containment. This round validated the source head only.
2. **Bank evidence.** Publish the bank r5 result for `b71061d7`. The brief's link resolves to the superseded archive, not to bank output.
3. **Superseded archives.** GitHub still serves all four superseded generations by SHA prefix (`160debeb`, `32aec661`, `74ac94e8`, `db842315`; see `receipts/superseded_archive_reachability.txt`).
   - `32aec661` still carries the classes the later redactions removed: the capture server host name, the switch's DNS-SD firmware, unit and remote identifiers, and the peer's vendor, product and firmware bytes (`receipts/census_superseded_control.txt`, class labels only).
   - Complete the purge requested under 5800264651.
   - Stop naming superseded SHAs in new public text, including review briefs; this round's brief linked `32aec661` as the evidence tree.
4. **Hosted and act acceptance** at the exact head. Executed and successful: `docs-check`, `docs-check-no-git`, `elaborate`, `rtl-fast`, `wire-accountability`, `full-ci-gate`, `changes` and `bdd-conformance`. Skipped through the docs-only path: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the shard matrices and physical gPTP (`receipts/hosted_checks_b71061d7.txt`).
5. **Issue #117 stays open.** The PR body says "Relates to #117". Box 4 carries a FAIL and NOT RUN rows, box 2's peer-side recovery is NOT RUN, and audio is deferred to 2026-12-31.
6. **R265-5-S1.** Consider taking it before the merge fixes `bb8c690f` into dev's history.

## 8. Receipts and scripts

Every published file is listed in `MANIFEST.sha256`. The scripts use only the standard library, and none of them embeds an identity token.

- **Scripts** (`scripts/`):
  - `verify_manifest.py`, `identity_census.py`, `pcap_identity_fields.py`, `printable_strings_census.py`;
  - `recompute_step3.py`, `recheck_stream.py`, `recheck_counts.py`, `recheck_prior_items.py`, `recheck_census.py`;
  - `check_fragments.py`.
- **Receipts** (`receipts/`): gate runs, probes, census results, re-derivations, external-hash checks, hosted checks, archive reachability, branch protection and clone integrity.
- **Not published.** The private token list and all extracted trees stay in `scratch/`.

R265-5 FINISHED
