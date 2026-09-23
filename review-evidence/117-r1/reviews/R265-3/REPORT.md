[R265] NEGATIVE - exact head 8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1

Round R265-3, external independent review of issue #117 / PR #531, cleared context.

- Head `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1`, tree `fe7079365e3d61364b7d6602a6e3abab20c1d222`.
- Source base `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The PR has three commits, `c3eb95fa`, `0abf147f` and `8016f7ac`, each a one-line message with no trailers.
- Diff: `docs/findings/117_GPTP_SILICON_EVIDENCE.md` (A), `docs/design/GM_LOSS_RECOVERY.md` (M), `docs/findings/README.md` (M). Nothing else changes: no HDL, firmware, config or gitlink.
- Evidence pin `74ac94e8eb331202f39d66cc006bc2640481e6da`; evidence branch tip `4165beb89afe217931bc52a8aaf800303e7bee1b`.
- All five lenses applied: Conformance, RTL, Robustness, Tests, Docs.

Reconstruction order, all from public state:

1. AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6, and the deny-list in `scripts/docs_check.py`), then `docs/README.md`.
2. Issue #117 body and frozen acceptance, with the decisions in comments 5561827955, 5565246390, 5789767491, 5794146393, 5794354283, 5794950660 and 5795898094, and the build, flash and bench records in 5794274143, 5794859125, 5795658105 and 5796668867.
3. `REGISTER_MAP.md`, `MILAN_COMPLIANCE_MATRIX.md`, `GM_LOSS_RECOVERY.md` and the RTL `KL_ptp_clock_validity.sv`.
4. The diff, blame and history; the pinned archive, the branch history and the superseded public archive objects.
5. The manager's PR comments 5800264651 and 5801414288.

The prior findings (PR comments 5800196179 and 5800161462) were read only after the verdict and ledger below had been drafted.

## Verdict

**NEGATIVE.** Two MINOR findings leave `Docs` unclean, and the other four lenses are clean at this head. Both findings are statements on the evidence page that its own pinned raw artifacts contradict:

- **F1:** the switch facts behind owner blockers B1 and B3;
- **F2:** "holdover clear" while the grandmaster is absent.

Neither was introduced by the round-3 correction: blame puts them at `c3eb95fa` and `0abf147f`. No prior round raised them, and no acceptance verdict on the page depends on either.

Everything the round was asked to verify is closed, with no new defect in the corrected passages:

- **R264-2 F1/F2/S2 and R265-2 F1/F2 are closed.** See the table below.
- **Identity.** The pin, the whole evidence-branch history and the PR carry none of the deny-listed peer or switch names, and none of the reference peer's four original ENTITY identity-field values. That holds in raw, UTF-16LE/BE, hex (eight separator forms), base64 and base64url, capture bytes included.
- **Page hashes.** Every page hash resolves through `MANIFEST.json` or is declared, correctly, as outside the archive.
- **Archive statements.** The counts, the redaction statement, line 129 and the Tool revisions paragraph all match the archive.
- **Superseded links.** No commit in the PR links a superseded archive object.

## Findings

### R265-3-F1 - MINOR - Docs - owner-blocker facts about the bench switch contradict the published captures

- **Where:**
  - `docs/findings/117_GPTP_SILICON_EVIDENCE.md:526`, B1: "The switch has no AVDECC entity and no address on the AVB segment, and no management path or credentials are provisioned on any bench host";
  - `:528`, B3: "The switch's firmware identity is not readable. It has no AVDECC entity and no management path. Its Announce fields above are its only recorded identity."
  - The page presents B1's facts as ones that "still hold" (`:523`).
- **Authority:** issue #117 box 5 requires topology, capture points and raw artifacts. The head commit's own subject is "correct the ... page against the raw packets". An evidence page must not state as fact what its published captures contradict.
- **Evidence:** `receipts/switch_addressing.txt`, from `scripts/switch_addressing.py`, covers every frame sourced by the switch MAC in the 22 pinned captures:
  - **A200 steady state:** the Run A and Run B tap captures carry 3 IGMP reports with a non-link-local IPv4 source address.
  - **Every A202 cycle** (tap capture and controller-host capture alike): ARP probes, then ARP announcements claiming an IPv4 link-local address, then IGMP from that address and from the non-link-local one.
  - **One mDNS response per cycle**, from the link-local address, with 3 PTR, 1 SRV, 1 TXT, 1 A and 1 NSEC records. The SRV record advertises a TCP control service with a port.
  - **The TXT record** has 8 strings, 6 of them keys with a namespace prefix. They include a firmware-version key whose value is published unmasked in all 12 captures, and a serial-number key whose value is masked. No value is reproduced in this packet.
- **Impact:**
  - The durable record says the switch has no address on the AVB segment, no management path, and no identity readable beyond its Announce fields. It keeps B3 open as an owner blocker on that premise, yet its own published captures show all three statements to be untrue. The switch even advertises a firmware version.
  - A reader deciding further bench work is misled, for example on reading the switch's firmware identity or on moving the grandmaster without a power cycle.
  - No box verdict depends on it.
- **Required outcome:** B1 and B3 state only what the captures and the checks support. For example:
  - after power-on the switch self-assigns an IPv4 link-local address, and it also sources IGMP from a second IPv4 address;
  - it advertises a TCP control service by DNS-SD, and its TXT record carries a firmware version;
  - no management credentials or path are provisioned on any bench host, and the control service was not used.

  B3's status follows from that. Alternatively, drop the contradicted clauses. If the firmware value is to stay unpublished, S1 applies.
- **Verification:** re-read B1 and B3 at the corrected head against `receipts/switch_addressing.txt`, and rerun `scripts/switch_addressing.py` on the pin.

### R265-3-F2 - MINOR - Docs - "holdover clear" while the grandmaster is absent contradicts the transcripts

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:335-338`: "In all six cycles, from the identity change until the switch returned: ... `TU=1`, holdover clear". The loss-declaration bullet at `:326` and the Step 4 "Grandmaster loss" row at `:439` do not record the bit either.
- **Authority:**
  - the pinned console transcripts;
  - `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:186-199`, which arms the 0.25 to 0.5 s discontinuity holdover on any change of the published grandmaster identity;
  - `docs/design/GM_LOSS_RECOVERY.md:48-64`.
- **Evidence** (`receipts/step3_holdover_episodes.txt`): in every cycle, `CLKV_STAT[3]` is set in 3 to 5 consecutive 0.1 s samples, 0.31 to 0.52 s from first set to first clear. The episode begins at the very sample where GM first reads `020000fffe000001`. It is a second episode. The first, at sync loss, is the one the page describes at `:325`, and it reproduces exactly (3 to 5 samples, 0.30 to 0.50 s).
- **Impact:**
  - The page states a publication-bit value that the transcripts contradict for the first 0.3 to 0.5 s of the interval it covers.
  - It implies that self-election skips the holdover the RTL arms on every identity change.
  - The Step 4 transition evidence for box 3 omits one publication-word edge, although the box 3 PASS is unaffected.
- **Required outcome:** the "while absent" bullet, and the loss-side row it summarizes, record the holdover episode at the identity change, or restrict "holdover clear" to the time after it.
- **Verification:** compare the corrected text with `receipts/step3_holdover_episodes.txt` (`scripts/step3_holdover_episodes.py`).

### R265-3-S1 - SUGGESTION - Docs - the switch's self-advertisement left in 12 captures is not named by the redaction statement

- **Where:** `docs/findings/117_GPTP_SILICON_EVIDENCE.md:539`, the redaction statement, against the pinned A202 captures `bench-a202/bench/cycle*/tap-c*.pcap` and `bench-a202/bench/cycle*/pw1-c*.pcap`.
- **Evidence:**
  - Masked length-preserving, consistent with the statement: the vendor and product words in the DNS-SD instance name, the host name (SRV target and A record), and the TXT serial-number value.
  - Not masked:
    - the TXT keys, which carry a vendor namespace prefix;
    - a unit identifier, a remote identifier and the firmware-version value.
  - Source: `receipts/switch_addressing.txt`; values are deliberately not reproduced.
- **Assessment:** the MAC-derived identifiers, on the page and in the base tree alike, already expose the switch's registry-resolvable vendor prefix, so the marginal exposure is judged low. Even so, the statement's "stays" sentence does not name these fields.
- **Suggested outcome, for the owner to decide:** either mask them length-preserving (new pin, `MANIFEST.json` update, page re-pin), or name them in the "stays" sentence.

## Prior public findings at this head

| Prior finding | Severity | State at `8016f7ac` | Evidence |
|---|---|---|---|
| R264-2 F1 / R265-2 F1: the pinned archive carried the peer's identity fields hex-encoded | MAJOR | CLOSED; one pending duty remains | See the evidence list below the table. |
| R264-2 F2 / R265-2 F2: stale Tool revisions redaction paragraph | MINOR | CLOSED | `:218-230` names exactly the four quoted hashes whose files are redacted: `8c9f2885` (paths), `45889a7d`, `c4ef8c9a` and `bdd228a1` (paths and identity). It also states that the unquoted `run_a/b/c.sh` are redacted the same way. At the pin, 7 tool files are redacted, and their kinds match (`receipts/tool_redaction_flags_pin.txt`, `receipts/archive_manifest_check_pin.txt`). |
| R264-2 S2: state what `sha256sum -c` reports; "most captures" | SUGGESTION | TAKEN | `:540` states the FAILED-by-design behavior with 20 and 57. Running `sha256sum -c` gives exactly 20 FAILED and 61 OK, then 57 FAILED and 96 OK (`receipts/sha256sum_c_pin.txt`). `:541` says "all 18 captures", which is correct. |
| R264-2 S1: PR body template | SUGGESTION | not taken | Optional. |
| R265-2 S1: cite the #530 disposition for FRAMES_TX | SUGGESTION | not taken | Optional. |
| R265-2 S2: label the clock of the Run B millisecond times | SUGGESTION | not taken | Optional. |
| R264-1/R265-1 items that round 2 closed: dark window, loss-edge holdover, console census, envelope-less records, census, daemon scope, reach-asCapable row | MINOR | still CLOSED; re-derived independently at this head | `receipts/step3_rederive.txt`, `step3_holdover_episodes.txt`, `archive_simple_claims.txt`, `census_acmp_diff.txt` |

Evidence for R264-2 F1 / R265-2 F1:

- **Identity sweep: 0 hits** for the four private field values and the deny-listed stems, in every encoding, over:
  - the pin (228 objects);
  - the evidence-branch history `ede8d48e..4165beb8` (425 objects, the 8 commit messages among them);
  - the PR history (`receipts/identity_sweep_*`).
- **Positive controls fire** on both superseded chains (`receipts/identity_sweep_control_*.txt`).
- **Manifest:** `MANIFEST.json` maps all 236 files, and every published hash matches.
- **Page statements:**
  - line 539 now lists what is withheld and what stays;
  - line 129 cites the field hash as recorded and says it cannot be recomputed from published bytes;
  - the counts 77, 6, 71, 20, 57 and 29 all match (`receipts/archive_manifest_check_pin.txt`).
- **History link:** the manager's decision (5800264651) rejects the superseded objects and squashes the correction commits. At this head no PR commit message or blob links a superseded commit or tree on either chain (`receipts/superseded_links.txt`).
- **Pending duty:** both superseded chains are still served by SHA (`receipts/superseded_chain_served.txt`; see Pending manager duties).

## Checks performed (exact head, or the named pin)

| Check | Result | Receipt |
|---|---|---|
| Pin archive vs `MANIFEST.json`: 236 files, all published hashes match, nothing unlisted | PASS | `archive_manifest_check_pin.txt` |
| Redacted: 77 in total, 20 in A200 and 57 in A202; 6 path-only and 71 identity. 29 table hashes name redacted files: 18 captures, 6 cycle analyses, 3 censuses, the DUT's Run C dump and the attempt 1 lock log | PASS, matches `:539-541` | same |
| Every full page hash resolves through the manifests, except the 8 the page declares outside the archive | PASS | same, and `external_hash_claims.txt` |
| Those 8: the grader hash equals the blob at `ede8d48e`; `.bit`, payload, `aem_desc.bin` and `e84e579c...` are in `expected-crc.txt`, which is identical in both packets; the build-record hashes are on comment 5794859125; the peer hash is covered by the line 129 row | PASS | `external_hash_claims.txt` |
| Truncated hashes: 21 of 26 resolve to archive files. `95d64fd5`, `ad579e18` and `0e9faf30` are in full on comment 5584039577. `8ef4b008` has no public full value, as stated. `e84e579c` is in the CRC table | PASS | `archive_manifest_check_pin.txt`, `external_hash_claims.txt` |
| Line 129: the field holds 7 octets, and the SHA-256 of the 64-octet original field equals the page value. It is masked length-preserving at the pin, and the 2026-09-14 prefix matches | PASS | `line129_check.txt` |
| Identity sweep (5 deny-listed stems and 4 private values, all encodings, decompressing where needed), with positive controls | 0 hits; controls fire | `identity_sweep_*.txt` |
| Full PR tree, base included: only random 3 to 4 byte matches inside base binary images the PR does not touch | not identity | `identity_sweep_pr_tree.txt` |
| All 10 repository scrub rules over the evidence history and the PR history | 0 hits | `scrub_rules_*.txt` |
| Capture DHCP host names: the switch's is masked; two short role names stay, as stated | PASS; mDNS see S1 | `pcap_name_fields_pin.txt` |
| Superseded links in the PR commits and blobs, with both superseded chains included | 0; the only archive link is the pin | `superseded_links.txt` |
| Step 2: 4,556, 565, 564 and 566 intervals; 568/568 and 570/570 exchanges; turnaround 10,984 to 11,009 ns | PASS | `step2_rederive.txt` |
| Step 3 table, independently re-derived from the clock offsets, the tap line and the console: every cell within 0.01 s; loss offsets; on-to-all-good 19.18 to 20.32 s | PASS | `step3_rederive.txt` |
| Reach-asCapable row: the second completed DUT Pdelay falls within one sample; 1.02 to 1.64 s after the first frame; 377 to 389 ns | PASS | same |
| CONNECT_TX: none between loss and all-good; the first after return comes at 41.285, 42.963 and 41.458 s, and the first CRF PDU follows | PASS | `step3_acmp.txt` |
| `CLKV_TUCNT` +40, +39, +41, +40, +40 and +41, and the `tu` spans | PASS | `step3_tucnt.txt` |
| Envelope-less records: 76; then 38, 0, 38, 45, 0 and 37; then 18; none elsewhere. 19 tcpdump logs with 0 dropped. 14 transcripts with 38,954 read-only commands | PASS | `archive_simple_claims.txt` |
| Census: 18 ACMP states unbound before and after in both packets; one A200 field differs, as stated | PASS | `census_acmp_diff.txt` |
| CSR decodes against the register map and the RTL | PASS | `REGISTER_MAP.md:731,770,875,1347,1392`; `KL_ptp_clock_validity.sv:245-248` |
| 15 documentation gates at head, including `docs_check`, `check_em_dash --base ede8d48e` (0 over 669 added lines), `check_baremetal_only --check`, `gen_toc --check` and `--verify-anchors`, and `check_doc_paths` | all exit 0 | `gates/` |
| Intra-page anchors: 27 links, 15 distinct | all resolve | `intra_page_anchors.txt` |
| Clone restored: HEAD, tree and index exact; 865 tracked files byte- and mode-exact; no hidden flags; gitlinks at their pins | PASS | `restore_verify.txt` |
| `scripts/run_all.sh` regenerates every receipt above | identical | this packet |

Hosted contexts at the exact head, as a record only: the manager owns hosted and act acceptance (`receipts/hosted_check_runs_8016f7ac.tsv`).

- **Executed and successful:** `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `full-ci-gate`, `changes` and `bdd-conformance`.
- **Completed as skipped, not executed:** `verilator-suites`, `yosys-portability` and their shard jobs, plus `verilator-lint`, `yosys-elaboration` and the physical gPTP job.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The #117 acceptance boxes and the owner decisions (5561827955, 5789767491, 5795898094) vs page `:34-64`; the bound and its derivation, `docs/design/GM_LOSS_RECOVERY.md:88-118` (3 + 0.375 + 1.625 = 5 s, Milan intervals); Milan rows `MILAN_COMPLIANCE_MATRIX.md:78,83`; the step 2, 3 and 4 values, re-derived | R265-3 | `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1` |
| RTL | CLEAN | No RTL in the diff (3 Markdown files; gitlinks equal the base). The page's CSR decodes (`CLKV_STAT` bits 0/1/3/16, `ASP_CMD` 0x11, `GPTP_LAT` 656/219 ns, `CRFT_CTRL` 0x3002E3, `LINKG_STAT` 0x83/0x03) vs `REGISTER_MAP.md` and `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:119-122,186-211,245-248` | R265-3 | `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1` |
| Robustness | CLEAN | Negative, boundary and failure paths recorded honestly: attempt 1, the NOT RUN and FAIL rows, receipt timeouts, bound and unbound cycles, `RST_EPOCH`. Redaction is length-preserving and complete in structure: every capture parses, record counts equal the tcpdump counts, and nothing outside the four ENTITY fields changed | R265-3 | `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1` |
| Tests | CLEAN | Discriminating evidence checks: the CRC table with the alternative seeds and the replaced image, the cycle 1 outlet proof, the gate arms (docs_check scrub self-test 23/23, em-dash 57/57), and reviewer sweeps whose positive controls fire | R265-3 | `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1` |
| Docs | UNCLEAN (F1 MINOR, F2 MINOR) | `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, `docs/design/GM_LOSS_RECOVERY.md` and `docs/findings/README.md`, against the pin `74ac94e8` archive, the RTL and the issue record | R265-3 | `8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1` |

SUGGESTIONs do not affect coverage. Fixing F1 and F2 changes the page only, so Docs must be covered again at the new head. Conformance and Robustness read the same page, so they are un-covered by any change to it and must be re-applied. RTL and Tests stay banked here while nothing in their scope changes.

## Real limits

- **No hardware.** Physical calibration is NOT RUN, and field or hosted skips are not hardware proof. As the page itself states, these are NOT RUN too: the reference peer's own recovery time, the first reach after the flash, Hive, behave, latency and audio.
- **Build artifacts are not public.** Image identity rests on the page's CRC32 readbacks. The `bios.bin` and `csr.csv` hashes are recorded only on the page.
- **Switch host name and serial are checked by structure only.** Their originals are not public: the fields are masked with `#` in DHCP option 12, the SRV and A records and the TXT serial value, but no value-level sweep for them was possible.
- **Private peer values.** The four original peer field values used by the sweep were decoded in a private scratch area from the superseded public archive object. They are never published, and neither is the decode step, while the purge is pending. Without them, `scripts/run_all.sh` sweeps the deny-listed stems only.
- **Tap-to-server clock line.** My line keeps every per-5 s minimum, so its residual reaches 74 ms, against the page's 2.02 ms after its own selection. The page's residual figure is not reproduced, but every table value agrees within 0.01 s.
- **Not run.** The scoped Verilator was not used, because there is no RTL change to simulate. No full parent, PP, gPTP, Yosys or builder bank was run, by instruction.
- **Prior review archives** on the evidence tip were swept mechanically for identity (0 hits). They were not otherwise read. Prior findings were taken from the public PR comments.

## Pending manager duties

1. **Purge of superseded evidence objects** (decision 5800264651). At 19:45 to 19:49 UTC the repository commits API still served:
   - the `32aec661` chain: `32aec661`, `204879ff`, `6b14c6c0` and `55b23383`;
   - the pre-rewrite `160debeb` chain: `160debeb`, `58d5419e` and `e76011d5`.

   The positive-control sweeps confirm those objects carry the withheld peer fields. PR and issue comments still name `32aec661` and `160debeb`. No PR commit does.
2. **Owner decision on S1**, the switch's DNS-SD fields in 12 pinned captures.
3. **Final current-dev candidate validation at the merge turn:** source base `ede8d48e` against live dev `26d855a9`. That is distinct from the source validation reported at this head.
4. **Hosted and act acceptance.** `verilator-suites` and `yosys-portability` completed as skipped contexts at this docs-only head.
5. **Re-review after F1 and F2 are answered.** The Docs, Conformance and Robustness lenses must be re-covered at the new head.

R265-3 FINISHED
