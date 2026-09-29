# [A441] Round 2 handoff: PR #620, bench lane B1

Refs #599 (acceptance 4), #394 (acceptance 2, e1 only), #387 (acceptance 4).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885377252
- Round-1 reviews answered: [R402-1](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5885301111) and [R403-1](https://github.com/kebag-logic/milan-fpga/pull/620#issuecomment-5885368914), both NEGATIVE at `f9eab5bf`.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885391766
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/599#issuecomment-5885742531 (`REVIEW-READY.md` is the posted text; the API readback equals it apart from a trailing newline).

## State

REVIEW READY at head **`931c3edfced972e01356cd989b5092a1672de5a3`**, one commit on `f9eab5bf55ca4471e6e48ae3d38018d7e804505b` (branch `b1-bench-0929`, local only, not pushed). The commit subject is one line with no body and no trailers. The worktree is clean.

- Docs and packet only. No bench access: no console, JTAG, power strip, tap, controller host or DUT action, and the bench lock was not taken.
- Changed files: `docs/findings/387_SOFTWARE_GM_STEP.md` (+71/-11) and `docs/findings/599_394_E1_LINK_CYCLES.md` (+72/-11). Nothing else.
- This directory is the redacted round-2 packet, meant for `review-evidence/b1-r1/author-r2/` on `b1-review-evidence`. The manager pins that commit in the PR body at archive time.

## Ruling 1: #387 acceptance 4 is PARTLY MET

Changes at `931c3edf`, `docs/findings/387_SOFTWARE_GM_STEP.md`:

| Line | Change |
|---|---|
| 12 | Verdict cell: `PARTLY MET`. It lists what is met (ten PHC steps of +9.99/-10.00 ms on a locked CRF stream, no `mr` change, MEDIA_RESET flat, neither listener unlocked, `A_MCSRV_STAT` LOCKED). It then names each gap of the one-counted-event contract: `tu` signalled 2-3 times per step instead of once; asCapable lost for 2.0 s after every step (#621); DUT GPTP_GM_CHANGED +3 at nine of ten edges against one grandmaster change; the counted render re-base not observable (no AAF stream, no register). The bound sentence now reads "Item 2 sets no time bound; the DUT was steady again 3.00-4.53 s after each step", consistent with the contract check's last row. "inside the 5 s bound" is gone. |
| 24 | Contents entry for the renamed section. |
| 110-115 | What would make the re-base observable: an AAF stream bound into the DUT's render stage across each step, and the stage's recentre count published on a register or console command. Today it is a verification tap (`REGISTER_MAP.md`, render setpoint state, "recentre counters remain separate verification taps"). |
| 186-194 | After the contract check: item 2 decides one counted `tu` event per step (the #602 ruling removes only `mr` and MEDIA_RESET); two or three episodes per step, and the re-base not observable, make acceptance 4 PARTLY MET. "Media" in the last row is reconciled with the DUT's CLOCK_DOMAIN UNLOCKED counts (R403-1 F1). |
| 196-234 | Section renamed "Deviation from the one-counted-event contract" and described as a departure from it: every one of ten steps departed; two or three `tu` episodes instead of one counted event; GPTP_GM_CHANGED +3 at nine edges, +1 at the tenth. "Item 2 does not grade it" is removed (it does). The proposed follow-up is now #621, recorded and not fixed here. |

The measurement tables are byte-identical: `tables/table_identity.py` and its output `tables/table_identity.txt` compare every table of both pages at `f9eab5bf` and `931c3edf` with `git show`.

- `599_394_E1_LINK_CYCLES.md`: 8 of 8 base tables byte-identical, including its verdict table. One new table: the saved-state table.
- `387_SOFTWARE_GM_STEP.md`: 5 of 5 non-verdict tables byte-identical: per-step, per-run, contract check, tool hashes and raw artifacts. The verdict table changed in its #387 row only. One new table: the saved-state table.
- The table-line diff shows exactly one removed and one added verdict row, plus the two added saved-state tables. `RESULT measurement/contract/hash tables changed: 0`, rc 0.

The PR body (`PR-BODY.md`) and REVIEW READY carry PARTLY MET and the same four gaps.

## Ruling 2: raw retention and unarchived claims

### Durable copy and MANIFEST

- Source: the lane's temporary raw directory `/tmp/b1-a438/raw` (213 files, 176,644,961 bytes), **copied, not moved**. The source is untouched: 213 files still present, every hash equal to the index.
- Destination (private cold storage, NFS hard mount): **`/srv/fast-nas/milan-archive/bench/b1-0929/raw/`**, copied with `rsync -a --checksum`, rc 0.
- MANIFEST on the NAS: `/srv/fast-nas/milan-archive/bench/b1-0929/MANIFEST.tsv` (path, bytes, SHA-256, matching page row) and `MANIFEST.sha256` (`sha256sum` format). The copies in this packet are `retention/MANIFEST.tsv` (SHA-256 `35a3e8e91d00e26aed026fb0731f5db21ef9589b2b2e5166893d496502a50910`) and `retention/MANIFEST.sha256` (`d21d7337872a45b4c3cd3c5b1747ef95ca3acb00e8af63bd0085bf7e1b6f28ca`). They are byte-identical to the NAS copies. `sha256sum -c MANIFEST.sha256` on the NAS: rc 0.
- Verification: `retention/verify_archive.py` produced `retention/verify_archive.txt`, TOTAL pass=495 fail=0, rc 0. It hashed every archived copy.
  1. 213/213 index entries (`r1/RAW-ARTIFACTS.json`) have an identical archived copy, and no archived file is unlisted.
  2. **100/100 raw-artifact rows of the two pages** (65 on the #599 page, 35 on the #387 page, 18 actions) equal their archived copy in bytes and SHA-256. No archived console, controller transcript, tap capture, controller-port capture, event record or port log of those actions lacks a row.
  3. 181/181 per-action index entries (`r1/bench/<action>/raw-artifacts.json`) agree with the archive.
- Command: `python3 -B retention/verify_archive.py /srv/fast-nas/milan-archive/bench/b1-0929/raw <repo at 931c3edf> retention/MANIFEST.tsv`.

Per action (every file's SHA-256 is in the appendix and in `retention/MANIFEST.tsv`):

| Action | Files | Bytes | Page rows matched |
|---|---:|---:|---:|
| top-level files (action stdout, census, setup, restore, snapshots, preflight) | 32 | 177,431 | 0 |
| dryrun | 9 | 456,534 | 0 (no page rows; its console and controller transcript are also in `r1/`) |
| bmsr-proof | 9 | 2,040,893 | 5 |
| baseline-bound | 9 | 3,932,124 | 5 |
| cycle01-cycle10 | 90 | 90,272,241 | 50 |
| gm01-gm05 | 55 | 79,304,305 | 35 |
| final | 9 | 461,433 | 5 |
| **Total** | **213** | **176,644,961** | **100** |

### Page statements

- `599_394_E1_LINK_CYCLES.md:335-349`: the public packet is on branch `b1-review-evidence` under `review-evidence/b1-r1/author-r2/`, and PR #620 records its pinned commit. The packet is redacted. The per-action indexes' temporary paths are historical names, as on the #600 page. Raw captures are in private cold storage, keyed by the SHA-256 values in the page's table. The retention manifest matches every copy. The extraction scripts reproduce the four claims.
- `387_SOFTWARE_GM_STEP.md:303-307`: the same packet location and cold-storage statement, keyed by its own table.

### Each claim of R402-1 F2 and R403-1 F2

Every script hash-checks each raw input before it reads it: against the page's raw-artifact row where one exists, and against `r1/RAW-ARTIFACTS.json` always. It stops with rc 2 on any mismatch. Each output file starts with its `INPUT` lines. All were run against the NAS copy at head `931c3edf`, rc 0.

| Claim (page:line at `931c3edf`) | Script | Output | Result |
|---|---|---|---|
| Peer delay 0 ns at five takeovers, 4,039-4,701 ns at five releases, 373-389 ns elsewhere (`387:212-220`) | `extract/extract_pdelay.py` | `extract/extract_pdelay.txt` | REPRODUCED. Takeover clears: 0, 0, 0, 0, 0 ns. Release clears: 4,393, 4,039, 4,701, 4,378, 4,231 ns. The other 2,359 samples of the five runs: 373-389 ns. The page now says "in every other sample of the five runs", and that each odd reading held four or five samples, about 1 s. Inputs: `gm0[1-5]/console.jsonl`, `gm0[1-5]/events.jsonl`, all with page rows. |
| 7,520 console rounds, MAC_STATUS and `link_status` agree in all (`599:94-96`) | `extract/extract_console_rounds.py` | `extract/extract_console_rounds.txt` | REPRODUCED. 19 action consoles, 7,520 rounds, each with exactly one read of each word, equal in 7,520. The page now says "of the session's nineteen actions". The dryrun console has no page row; it is index-checked and also in `r1/bench/dryrun/`. |
| Alignment test: role changed no grandmaster; DUT and peer GPTP_GM_CHANGED stayed 22 and 60 (`387:60-68`) | `extract/extract_alignment_counters.py` | `extract/extract_alignment_counters.txt` | REPRODUCED. Test window 06:03:37.2Z-06:04:17.6Z (`r1/gm/slave-test.log`). DUT/peer 22/60 with the switch as grandmaster at the last cycle-10 poll (06:01:54.6Z), at the post-test snapshot (06:04:37.95Z) and at run 1's first poll (06:05:46.9Z, after its own alignment phase). Inputs: `cycle10/controller.jsonl`, `gm01/controller.jsonl` (page rows), `post-slave-test-snapshot.jsonl` (index only). |
| `asl` seed reads `809fcffa` (`599:39`) | `extract/extract_seed_crc.py` | `extract/extract_seed_crc.txt` | REPRODUCED. The unchanged round-1 tool `r1/tools/expected_crc.py` (SHA-256 `04d128bb...19d7`, equal to the round-1 manifest) ran over the builder's `build_ax7101_{eto,eppo,asl}_tdm8dev13eda870` directories. It gives payload CRC32 `d84bce7b`, `bf44ccc9` and `809fcffa`, each over 3,825,788 bytes. The `asl` payload SHA-256 is `392fe782...4e4a` and the bit file `d84d0a9e...8d91`. The directories are tied to dev `13eda870` by their names; they were not rebuilt. Command: `python3 -B extract/extract_seed_crc.py <builder-work>/build_ax7101_eto_tdm8dev13eda870 <...>_eppo_<...> <...>_asl_<...>`. |

Shared helper: `extract/b1r2_common.py`. No claim was qualified or removed; all four are now archived with a script and its output.

## Ruling 3: redacted packet

- `r1/` is the round-1 author packet, redacted by `scrub/redact_r1.py`. The private token list stays outside the packet. `r1/REDACTION.json` records every file's original and published SHA-256 and its replacements per placeholder.
  - 245 round-1 files: 235 copied, 30 of them redacted, 10 excluded. The exclusions are 5 packet captures, which carry host MACs in every frame, and 5 bytecode files. Round-1 publication excluded both kinds too.
  - Placeholders: `<controller-host-eui64>`, `<controller-host-if>`, `<capture-host-if>`, `<capture-host-mac>`, `<tap-driver>` and `<account>`.
  - Tool hashes quoted on the pages refer to the originals. Two tools changed by redaction, `r1/tools/b1_analyze.py` and `r1/tools/phc_restore.py`. `REDACTION.json` maps them to their original hashes, which equal the pages' rows.
- Private-token scan: `scrub/scan_private.py` over this whole directory, with the private list outside it. Output: `scrub/scan_private.txt`, **0 hits** in every kind. The kinds are host names, console port, interface names, account name, capture-host NIC MACs, controller-host NIC MAC and MAC-derived EUI-64, and the tap driver name.
- R403-1's `scripts/scrub_packet.py` over this whole directory and both pages at `931c3edf`: `scrub/scrub_packet.txt`, rc 0.
  - "scrub pages: 2 scanned, 0 findings".
  - "scrub packet: 0 findings".
  - Extra shapes, reported and not graded:
    - MACs `00:00:00:00:00:00` (loopback), `02:00:00:00:00:01` (DUT) and `3c:c0:c6:01:02:03` (the tree-published peer), all on its public list.
    - `11.4.4.3`, an IEEE 802.1AS clause number in a comment of `r1/tools/wire_summary.py`, not an address.
    - One file-listing line in `r1/capture/capture-prerequisite-raw.txt` whose owner and group now read `<account>`.
    - Temporary-directory paths: index paths and tool paths.
  - No interface name, no account name, no host MAC and no home path.
- The masked reviewer-script outputs in `reviewer-scripts/` passed the same scan.

## Ruling 4: saved-state layer

Both restore sections carry the table:

- `599_394_E1_LINK_CYCLES.md:287-331`, the full derivation.
- `387_SOFTWARE_GM_STEP.md:266-291`, the table, the short cause and a link to the derivation.
- `599:125-127` now says the bench never rebooted, flashed or power-cycled the DUT, and that its own saved-state writer committed twice.
- `599:267` says everything was restored as found except this layer.

| Saved-state field | Identity gate, 05:31:24Z | Final restore, 06:22:44Z |
|---|---|---|
| NVM slots A / B, image sequence | 227 / 228, image 228 | 229 / 230, image 230 |
| Commits ok / failed | 0 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000444`, 0 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc30000e4`, pend 0 (backed 1, dirty 0, valid 1, unres 0, load accepted 1) | `0xc34000e4`, pend 1 (bit 22), otherwise identical |

**Cause, from the captures** (`extract/extract_saved_state.py`, output `extract/extract_saved_state.txt`, rc 0). The script reads the two readbacks (matched to the round-1 manifest), every PP_STAT sample of the 19 hash-checked consoles, and every hash-checked controller transcript, in time order.

- `nvm_pend` read 0 in every sample up to 05:38:28.99Z, the end of the link-drop proof. It read 1 in every sample from 05:41:15.67Z, the bound baseline, and never 0 again.
- Between those samples the setup (`setup-raw.jsonl`, 05:41:01.64Z) issued the session's first three state-changing commands: the peer listener's CONNECT_RX (to DUT talker uid 1), the DUT listener's CONNECT_RX (uid 1 from peer talker uid 2), and the DUT's SET_CLOCK_SOURCE to source 1 (`0024000000010000`).
- The restore (`restore-raw.jsonl`, 06:22:05.01Z) issued the other three: SET_CLOCK_SOURCE to source 0 and both DISCONNECT_RX.
- Every other controller command in all 19 action transcripts and the census, snapshot and descriptor transcripts is a read: GET_AVB_INFO, GET_COUNTERS, GET_RX_STATE and READ_DESCRIPTOR.
- The DUT listener kept talker `3cc0c60102030000` uid 2, count 1 and flags `0x0002` in every poll from the bound baseline to run 5. Stream ID, destination and VLAN read zero while the talker's stream was absent in each cycle. No commit came of it: the total is two.
- PP_STAT `nvm_dirty` read 0, `nvm_alarm` 0 and the verdict nibble 0 in all 7,520 samples. So neither commit fell inside a sampled action; the commit instants were not sampled.
- Which action committed which record: only the binding records, ids `0x20`-`0x2F`, have a writer (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 11), and a commit follows only a completed record write.
  - The **setup's bind of DUT stream input 1 committed image 229 (slot A)**.
  - The **restore's unbind committed image 230 (slot B)**.
  - The alternating slots and the count of two fix the order.
- The two SET_CLOCK_SOURCE writes committed nothing. The clock-source records `0x0A`-`0x11` have no writer. Each write set the dynamic-state store's sticky level, one of `nvm_pend`'s four sources.
- At the end, dirty, open-record and alarm read 0 and both commits succeeded. The binding source was therefore clear. No SET_NAME or map write was issued. The one live source is the dynamic-state level.

Stated plainly on both pages:

- The persisted records were not read back or compared with the found state.
- The pending flag cannot be cleared without a DUT reset, which this lane may not perform.

### Separate report: does a sticky `nvm_pend` after two successful commits match the contract?

**Yes. It matches the contract as written at `13eda870`, for this cause.** It is the documented behaviour of a persisted field that has no record writer, not a commit or acknowledgement defect.

1. **The source is sticky by design.**
   - `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:292` sets `dirty_o` on any persisted-field write except IDENTIFY, and `:266` clears it only in reset. SET_CLOCK_SOURCE is such a write.
   - `hdl/milan/KL_pp_shadow.sv:958-959` ORs that level into `nvm_pend_w`, which the backend publishes at `PP_NVM_STAT[22]` and `PP_STAT[11]`.
2. **The contract says the bit stays set until reset for this group.**
   - `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1283` (section 11, clock source `0x0A` to `0x11`): record writer NONE, "nvm_pend 1 until reset".
   - `:992-993`: "Names, maps and dynamic fields still lack record writers. Their sticky sources therefore clear only at reset."
   - `:999`: "NOTHING ELSE affects it: no ACK, RELEASE, commit, deadline or heartbeat."
   - `:277`: "No acknowledgement touches it."
   - `CHANGELOG.md:275-300` (release `0x0002_0060`) widened the bit. It states that the dynamic-state level already publishes class 1, and that for the groups without a record writer "Only reset clears that source".
3. **Commits cannot clear it.**
   - `:1000`: the writer "commits on nvm_dirty only". The two commits came from the binding records, the only record writer, and retired only their own dirty work.
   - The binding source (`nvm_unflushed_o`) did clear: final dirty 0, unres 0, no alarm, failed 0.
4. **Restoring the found value does not clear it either.** The level is set by any write, not by a difference from the saved value. So SET_CLOCK_SOURCE back to source 0 left it set. This is also what the contract says.
5. **What the bit is honest about.** The clock-source selection is not persisted at all. `SAVED_STATE_MATERIALIZATION.md:6` reads "ACCEPTED contract; materializer not implemented" (scope D3, UNRESOLVED 1, under #70). So the durable reading (backed 1, dirty 0, stale 0, pend 0) is withheld until reset, as the contract intends.
6. **What would not match the contract**, none of which was observed:
   - the bit cleared by a commit or an acknowledgement;
   - the bit set with no persisted-field write since reset (here it rose exactly in the setup window);
   - the bit still set after a reset with no new write. That last case is not testable without a reset.

For the manager's decision: this is no contract defect. The product gap behind it is the unimplemented materializer, already owned by #70 (D3). A useful operational note either way: the lane now on the bench inherits `PP_STAT 0x5b000c44` (pend 1) and images 229/230 until a reset. A lane allowed to reset could confirm three things with one `milan_nvm` readback: pend clears, the restored DUT listener reads unbound, and the clock source boots at its image default.

## Ruling 5: publication-bound wording (R402-1 S1)

- `599_394_E1_LINK_CYCLES.md:100-102`: "A published link edge therefore lies inside a 0.25 s console bracket. The physical edge may precede that bracket by up to the 250 ms publication bound." This replaces "The poll adds up to one further period".
- `599:219-221`: the per-cycle bullets now say the published PHY link state fell or rose in brackets, and that each physical edge may precede its bracket by up to the 250 ms publication bound.

## Reviewer scripts re-run at the new head

Run against the unredacted round-1 operator packet (not published). Outputs are masked by the private list and stored in `reviewer-scripts/`.

- R402-1 `scripts/rederive.py <root with author/ = round-1 packet> <repo at 931c3edf>`: **TOTAL pass=483 fail=0**, rc 0 (`reviewer-scripts/r402-rederive-at-931c3edf.txt`).
- R403-1 `scripts/rederive.py <repo at 931c3edf> <round-1 packet>`: **DIFFS: none**, rc 0 (`reviewer-scripts/r403-rederive-at-931c3edf.txt`).
- Not re-run:
  - R402-1 `verify_hashes.py` and R403-1 `check_page_hashes.py` both need the publication `MANIFEST.json` of the withdrawn archive, which this lane does not hold.
  - `retention/verify_archive.py` covers the same page-row check against the archived bytes themselves.

## Gates at `931c3edf` (foreground, not piped, physical `/data` path; `gates/`)

All rc 0 (`gates/gates.txt`, one output file per gate):

| # | Command | Result |
|---|---|---|
| 1 | pinned md env `scripts/docs_check.py` | 0 findings, 176 md + 938 scrubbed files, self-test 23/23, arms 4/4 |
| 2 | pinned md env `scripts/check_doc_style.py` | OK, 22 current documents |
| 3 | pinned md env `scripts/gen_toc.py --check` | OK, 118 pages |
| 4 | pinned md env `scripts/check_em_dash.py --base 13eda870` | 0 findings over 792 added lines in 2 pages, arms 339/339 |
| 5 | pinned md env `scripts/check_doc_paths.py` | OK, 854 cited paths |
| 6 | `python3 scripts/ci_scope.py --selftest` | PASS |
| 7 | `python3 scripts/check_baremetal_only.py --check` | OK, 0 findings over 936 files |
| 8 | `python3 scripts/check_feature_status.py --self-test` | 46/46, 0 findings |
| 9-11 | `git diff --check`; `git diff --check 13eda870..HEAD`; `git diff --check f9eab5bf..HEAD` | clean |

The pinned Markdown environment is `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python` (CPython 3.14.7). `check_baremetal_only` needs PyYAML, which the pinned lock does not carry, so gates 6-8 use the system `python3`, as in round 1.

## Open items and limits

- The pinned commit of the public packet is for the manager to fill in at archive time. The pages name the branch and path only.
- Not taken, because they are outside the rulings: R403-1 S1 (per-action check scripts do not assert the predicates), S3 (0.22-0.97 s measured from the bracket end), S4 (findings index), and R402-1 S2 (a generator for `summary/page-*.md`).
- The render re-base leg of #387 acceptance 4 stays owed. It needs an AAF stream and a published recentre count.
- #621 stays open; the asCapable loss is in the tree.
- The `asl` build directory is tied to `13eda870` by its name only; ROM and QSPI were not rebuilt.

## Packet layout (this directory)

| Path | What |
|---|---|
| `HANDOFF.md` | this file |
| `PR-BODY.md` | proposed PR body with the Round 2 section |
| `REVIEW-READY.md` | the posted REVIEW READY text |
| `MANIFEST.sha256` | SHA-256 of every packet file except itself |
| `retention/` | `verify_archive.py`, its output, and the retention `MANIFEST.tsv` / `MANIFEST.sha256` (copies of the NAS files) |
| `extract/` | the four claim extractions, the saved-state derivation, the shared helper, and each output |
| `tables/` | `table_identity.py` and its output (byte-identity of the measurement tables) |
| `scrub/` | `redact_r1.py`, `scan_private.py`, and the two scrub results |
| `reviewer-scripts/` | masked outputs of the reviewers' re-derivations at `931c3edf` |
| `gates/` | gate outputs and `gates.txt` |
| `r1/` | the round-1 author packet, redacted, with `REDACTION.json` |

## Appendix: retention MANIFEST (NAS `/srv/fast-nas/milan-archive/bench/b1-0929/raw/`)

Generated from `retention/MANIFEST.tsv`; page rows are `page:line` at `931c3edf`.

| Path | Bytes | SHA-256 | Page row |
|---|---:|---|---|
| `baseline-bound.out` | 3716 | `3720aec750eacddd9db4ccd09d25675eeb8b6360f8e92e9ced35936558cdcbaa` | - |
| `baseline-bound/console.jsonl` | 281035 | `1a18cf76b5dd2cc6c7a29daf6ce0976e9ba3ef152ae77cb904b828394cc72829` | 599_394_E1_LINK_CYCLES.md:369 |
| `baseline-bound/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `baseline-bound/controller-wire-capture.txt` | 181 | `8ac705277e27273f42b63c29f49f70d1f41fc55ef2919a9adfcdd9c7d92b7d45` | - |
| `baseline-bound/controller-wire.pcap` | 83285 | `e1759b461f8fc1bb12423200998c552074277e8be9befa5b515a3a77b1bbebf8` | 599_394_E1_LINK_CYCLES.md:371 |
| `baseline-bound/controller.jsonl` | 158776 | `5f349b929152cc145ae47f2d9993f132c76a5e832b0f863bd6132f5fe4ce12b3` | 599_394_E1_LINK_CYCLES.md:370 |
| `baseline-bound/events.jsonl` | 3523 | `19b117327439c17e549ea2d6ffce513d1d5c32df8287891e72914c91a1180a22` | 599_394_E1_LINK_CYCLES.md:373 |
| `baseline-bound/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `baseline-bound/tap-capture.txt` | 185 | `91aa0d274cf2da33f4f7063d4e24f8ab5cf2e9885a77b98aad655a7bc2b83674` | - |
| `baseline-bound/tap.pcap` | 3405061 | `8dbb5991e4005f2f19401270e3b756d866c773e2804b9c1254b8fb5f0d56a3af` | 599_394_E1_LINK_CYCLES.md:372 |
| `bmsr-proof.analysis.out` | 7971 | `cea5899759b73b29a83f7b3b696b048eb26e83ade63222e9153b69fa381a6b2e` | - |
| `bmsr-proof.out` | 4617 | `199eb34d5318b66a61ecadf1917910b6bdf973ee6f97085622a96c1213093588` | - |
| `bmsr-proof/console.jsonl` | 1030629 | `4764df46a24c298998419f68415bbf17d2ed4b3cee77a771e341aa117ca01686` | 599_394_E1_LINK_CYCLES.md:374 |
| `bmsr-proof/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `bmsr-proof/controller-wire-capture.txt` | 183 | `64019e509c97bf0930a24252345d36dfbdfdae22c025beed092a1f9877bd5a13` | - |
| `bmsr-proof/controller-wire.pcap` | 221631 | `1047525ce7111d045cd4a0418268b4685f89eafdf12ebc00b2e30d84bc2597f7` | 599_394_E1_LINK_CYCLES.md:376 |
| `bmsr-proof/controller.jsonl` | 391063 | `16d12ad49a454ee78317ec9e7a06bd721d289753eb8b0337e2925f2209aff7ee` | 599_394_E1_LINK_CYCLES.md:375 |
| `bmsr-proof/events.jsonl` | 4432 | `1a64223ddc6fcd7fffdab74c920544f20ba1c18983158d29ee0fe54ff05737c4` | 599_394_E1_LINK_CYCLES.md:378 |
| `bmsr-proof/results.json` | 78 | `5dac67330990e703cf25df9fc08adf367f31a4a43ae32d5a390dc2e5e302dd4f` | - |
| `bmsr-proof/tap-capture.txt` | 183 | `37cf2174d47174bb1151093ae17a4ba645840e5142afc5221a592f06ce4e3f2c` | - |
| `bmsr-proof/tap.pcap` | 392694 | `8626e39d5be93c84cef647a6eeb858a09b7c590d2fa4017a04281a41fff3dd4d` | 599_394_E1_LINK_CYCLES.md:377 |
| `census-end-raw.jsonl` | 29785 | `c29bcd82902947e0146b3c25e0625df04f3d331e49edb8245380495a094a4351` | - |
| `census-end.err` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `census-start-raw.jsonl` | 29738 | `0ad29ceccf8f8f2a0ffdf12fb0f1a2b6f990ad7236fded3005caec7576be5fc3` | - |
| `census-start.err` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle01.out` | 4606 | `3e285549e47c2d131f8cb58e754bb71042dd1ab81dac3b5b5a7a681a9914dae5` | - |
| `cycle01/console.jsonl` | 1030610 | `4a9064e38aa89e07d055ad06c11be6321693ae8cf6dc25e6a559c6d4381607c4` | 599_394_E1_LINK_CYCLES.md:379 |
| `cycle01/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle01/controller-wire-capture.txt` | 183 | `a4a8fb12d114474abf13a23c8780e78f86707b4549c3f88e0a5794535b9b3f9c` | - |
| `cycle01/controller-wire.pcap` | 221088 | `d47c3064750add2ad9121fbe582f3ea734305b364e39f1a66a409916f2ba5636` | 599_394_E1_LINK_CYCLES.md:381 |
| `cycle01/controller.jsonl` | 387042 | `b920fef033174caed079734b8cab04477f0c5aa9cb0cd2415d494dd8dcdd215e` | 599_394_E1_LINK_CYCLES.md:380 |
| `cycle01/events.jsonl` | 4427 | `9fa46da855f28c3f6d2b0d9b143b1aed9fdf833c6235a993c177abbc491453d7` | 599_394_E1_LINK_CYCLES.md:383 |
| `cycle01/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle01/tap-capture.txt` | 185 | `69d243a7068241519dc04aba1ed167e219a3343616bcf53cc349005b45c25595` | - |
| `cycle01/tap.pcap` | 7389317 | `1d4590facaf2dd1067b2d238e60121f6e164b1bf0f98fe8d86c4122388c77c29` | 599_394_E1_LINK_CYCLES.md:382 |
| `cycle02.out` | 4605 | `0ce85e23bea79ded4e897b4276e71f83412877e107f140376522f6c873bfea32` | - |
| `cycle02/console.jsonl` | 1030651 | `c54a59cfb1b48c35a134d50a81995a83b9af841a3485bcf96c90f227399d0461` | 599_394_E1_LINK_CYCLES.md:384 |
| `cycle02/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle02/controller-wire-capture.txt` | 183 | `a1f854f1704650c2659fc8db4e856ac872c24e921a28722744acdd9ea5a0f143` | - |
| `cycle02/controller-wire.pcap` | 223641 | `e062b34a22bd919ef1b62787f2ad220d9742f14742ea832cf33415e8094d465d` | 599_394_E1_LINK_CYCLES.md:386 |
| `cycle02/controller.jsonl` | 393492 | `82e82dfa50a5b6a0cd297d5de307be73477b4aa2007ab6f425256f14ea33dbab` | 599_394_E1_LINK_CYCLES.md:385 |
| `cycle02/events.jsonl` | 4426 | `37120ebbcc5ba17b068a7b5ab07c80007678989465ab0e0075f2b2f4854cb4cf` | 599_394_E1_LINK_CYCLES.md:388 |
| `cycle02/results.json` | 78 | `5dac67330990e703cf25df9fc08adf367f31a4a43ae32d5a390dc2e5e302dd4f` | - |
| `cycle02/tap-capture.txt` | 185 | `53f0efc181d412f27812023eefc619f5271773574d143450aa441f82aae7fb8d` | - |
| `cycle02/tap.pcap` | 7308248 | `f321bec940aba6c1ab0d1bb37b9ea401ed61c20ab2b23915ecb1d0d6418b45ba` | 599_394_E1_LINK_CYCLES.md:387 |
| `cycle03.out` | 4602 | `544fdafea75820880c15a164230491e32e58f832eefa2d936deebe717b059fa1` | - |
| `cycle03/console.jsonl` | 1030581 | `8e395b8e1b7401f60194e7318a30a5c0f101015dbcb4de0e8d0f26d9a8a3a712` | 599_394_E1_LINK_CYCLES.md:389 |
| `cycle03/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle03/controller-wire-capture.txt` | 183 | `1351f9a503f33cb163431adfc9a42599979f818e2d8808b78ce546d13773af89` | - |
| `cycle03/controller-wire.pcap` | 218508 | `028bce855ebb0f5ca525d648d581dcd2c44299fbea57b80a6b60af9cd4ce07ca` | 599_394_E1_LINK_CYCLES.md:391 |
| `cycle03/controller.jsonl` | 386971 | `ff4296d591d8c887c5ff581ddd03aa4e33efc84b6a76cee76a73941123779357` | 599_394_E1_LINK_CYCLES.md:390 |
| `cycle03/events.jsonl` | 4423 | `ad25b1385eb6124597406e4637060e5cab087ff4f8d93a9fc01f02ac0faa0553` | 599_394_E1_LINK_CYCLES.md:393 |
| `cycle03/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle03/tap-capture.txt` | 185 | `83f99b4f78b441bb59017f282e8d06e1306e0a3e5fb501c535e9c1cd08af1a50` | - |
| `cycle03/tap.pcap` | 6990195 | `1064e8021bedd01eb31d29e32d311f6c2870d725c97ccbb7cc6f6244f4d244be` | 599_394_E1_LINK_CYCLES.md:392 |
| `cycle04.out` | 4595 | `cc54f2fc88270fa49e3b931e0265cef5e0f90b32884787bdd76b39a675311fc9` | - |
| `cycle04/console.jsonl` | 1030948 | `d8b2168bf3757aa561554f71200a237cdd58f950f91b206b493741b45c4fbfcf` | 599_394_E1_LINK_CYCLES.md:394 |
| `cycle04/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle04/controller-wire-capture.txt` | 183 | `562941ccfac18a32eb19359ff07aa9aa608c89e1d0a1d3db14f35e19b7803908` | - |
| `cycle04/controller-wire.pcap` | 225327 | `6d94816f6795e1b6fcde6a85878b509b71cc07fc59ee9a8dd1fea1eba765bed8` | 599_394_E1_LINK_CYCLES.md:396 |
| `cycle04/controller.jsonl` | 392490 | `b75848b86669821d816f224528403212ce6e551ee08cf70f4a8e3f0603ac4e6a` | 599_394_E1_LINK_CYCLES.md:395 |
| `cycle04/events.jsonl` | 4416 | `4ee4418dcda6f632c3f2d0be8f05eb90ab7592f6bb1ac343c80e1348db12bd89` | 599_394_E1_LINK_CYCLES.md:398 |
| `cycle04/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle04/tap-capture.txt` | 185 | `a71690db0ca9e101f75d109d480e84218b4e64bae77dd56e6a2f2dfe58832e39` | - |
| `cycle04/tap.pcap` | 7653986 | `50766adf9764cb6b918bd43f101a970fd84dcc27063b40e8bda1374526b8ed4a` | 599_394_E1_LINK_CYCLES.md:397 |
| `cycle05.out` | 4603 | `aa9b11cac9d782ce7c245260f1b942216dbbd0e1f20ffd5e614b857f21cc894a` | - |
| `cycle05/console.jsonl` | 1031063 | `13e290bdc7be01d09e4f81268e87b802f858e1c642784cdff2507167a0d41c61` | 599_394_E1_LINK_CYCLES.md:399 |
| `cycle05/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle05/controller-wire-capture.txt` | 183 | `544e49200ff5f1c531410c60644ac724fa6e1dfdefb503f853d8d9ff775b4554` | - |
| `cycle05/controller-wire.pcap` | 223217 | `679072d7a99a0a90ea51c1630fd773a1a562ae4a8adfe0d7c1f1cc756ee1f2f8` | 599_394_E1_LINK_CYCLES.md:401 |
| `cycle05/controller.jsonl` | 392836 | `3fc16cd6946b59fc08e75f99dd28b33dedb856b0020c48ca51b319df0caad077` | 599_394_E1_LINK_CYCLES.md:400 |
| `cycle05/events.jsonl` | 4424 | `db41a82c607677eb7d8dfb344b706506968c711f4effa1b0ad2de949100baa1d` | 599_394_E1_LINK_CYCLES.md:403 |
| `cycle05/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle05/tap-capture.txt` | 185 | `f46a5a15f0046286b491c5e8512f2a87acbbfc21ade810562db061c3c7684d3c` | - |
| `cycle05/tap.pcap` | 7471838 | `1c650feec66029c52844f385087ac44f99488cc170aeba24f244cbcb95cc20bb` | 599_394_E1_LINK_CYCLES.md:402 |
| `cycle06.out` | 4602 | `f5bdd2843578f31d116a1eb3e32171182f253c7c91ae1630e86bd4a937a067e1` | - |
| `cycle06/console.jsonl` | 1030958 | `db21fc3b4633fac8ae9f96a91e401ddce2d36e6a540242eb8a25f61317410117` | 599_394_E1_LINK_CYCLES.md:404 |
| `cycle06/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle06/controller-wire-capture.txt` | 183 | `c3e27f8164cfb4c72b420b07ce9b61b34f577eb501cd8c6fdd411537241fda21` | - |
| `cycle06/controller-wire.pcap` | 216528 | `ea1366598313b314fba8e294ab8d9aa122f6c5db379466fa703218eed28ce140` | 599_394_E1_LINK_CYCLES.md:406 |
| `cycle06/controller.jsonl` | 376378 | `2331685243cad23f55a533dcf582546358fb3e9e5600448050e7bd8c15f9c22e` | 599_394_E1_LINK_CYCLES.md:405 |
| `cycle06/events.jsonl` | 4423 | `f2fdc17ddd29104c89e4a5c528a72fcd703ecee1cbcd2969ba3a76dbff5a5e73` | 599_394_E1_LINK_CYCLES.md:408 |
| `cycle06/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle06/tap-capture.txt` | 185 | `8136627882149e191af1b337108c567d404542fb5e8ecc473d94c3f7c7437512` | - |
| `cycle06/tap.pcap` | 7419798 | `1bd3902547dfbe627d598c5c7444e0aacf4dba23ba157b3a0ca0093b7cad4aae` | 599_394_E1_LINK_CYCLES.md:407 |
| `cycle07.out` | 4609 | `75c490b210fbdc27e263cd0f26dcd5ec67892955b818e1df28c426130a86a3be` | - |
| `cycle07/console.jsonl` | 1030626 | `ee0ef7e43a5b782fa36b43b86fa77297bb0c19e681312fdc8fec4a3a18817656` | 599_394_E1_LINK_CYCLES.md:409 |
| `cycle07/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle07/controller-wire-capture.txt` | 183 | `d43b673851ce160aaa9e963e37ae76555f392dc6603b4191cb2ac514988be316` | - |
| `cycle07/controller-wire.pcap` | 223209 | `75b9db5c039952e1ebfb27eb044558ad15ee7c1acfb9910a27f764c529ae9c48` | 599_394_E1_LINK_CYCLES.md:411 |
| `cycle07/controller.jsonl` | 392833 | `b0735c1dd0bcc4708689f86767c5f8ccbf2899bad59cfcb883c14dba92c2dd70` | 599_394_E1_LINK_CYCLES.md:410 |
| `cycle07/events.jsonl` | 4430 | `ac2f72ca6ea59cd87e25c74f3408d54122f974cf9f2d49fe6d56390e838db0c4` | 599_394_E1_LINK_CYCLES.md:413 |
| `cycle07/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle07/tap-capture.txt` | 185 | `4ea3c5e525db1dbd9d080de3a03ba760114b7452f3bda9ba676485d4c9de88cc` | - |
| `cycle07/tap.pcap` | 7517794 | `7e1970fd874ddc66af58dece8d06bd6d18c570d0b2bf3ccc39b6f9781fbd6677` | 599_394_E1_LINK_CYCLES.md:412 |
| `cycle08.out` | 4608 | `0d77bc3dab76fe1b9e401b13d4f9c11c1a1ee64d4dfe4fc63cd1ab4cc4d691c4` | - |
| `cycle08/console.jsonl` | 1030503 | `e08f65975c6683a36fe775f7057e6e2ad23409daae9e48e46892d260e79f5e8b` | 599_394_E1_LINK_CYCLES.md:414 |
| `cycle08/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle08/controller-wire-capture.txt` | 183 | `3e50b80d7d1e95329a18aeeaeebd5a4b85e473218d30d04a07098eac32f7ba53` | - |
| `cycle08/controller-wire.pcap` | 223027 | `9472394b0c949a7bfccf27fce7dcf7e8e5e576e3b011491ab12da09f93036ab8` | 599_394_E1_LINK_CYCLES.md:416 |
| `cycle08/controller.jsonl` | 392607 | `6e26bcf5d77ebe3754e19f38c3948737ec957776bd2b11f691072805069bd1a1` | 599_394_E1_LINK_CYCLES.md:415 |
| `cycle08/events.jsonl` | 4429 | `e05c8054b43f53d89fd46dd7e983f3f1a234c0e7e470a3bcba5830902b0d2451` | 599_394_E1_LINK_CYCLES.md:418 |
| `cycle08/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle08/tap-capture.txt` | 185 | `4bfe748dd858a3a31f2eee97750b7ebb9de2a01960f848ec231baffefa7c0f79` | - |
| `cycle08/tap.pcap` | 7499543 | `4e51f77ff27b158c1baa32fad0aa666ae6f30900e2b98ccbd30fa70d4883d709` | 599_394_E1_LINK_CYCLES.md:417 |
| `cycle09.out` | 4606 | `7e47afc9c6061110649519d347ef29e92000b72ccd284b91a9f62ff025c894cf` | - |
| `cycle09/console.jsonl` | 1030587 | `c4966de2234ed48bff7b39d4aa14d2fd5587c38a84c7f304c514bc8d52c64199` | 599_394_E1_LINK_CYCLES.md:419 |
| `cycle09/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle09/controller-wire-capture.txt` | 183 | `7cc20089360ba56cabeb54794669977bbe41ceee059acf27fef48aa4161a4e00` | - |
| `cycle09/controller-wire.pcap` | 222394 | `e7f43fc866cc6926177c6285752126a991a75a6b051a2258dade061bb158a08a` | 599_394_E1_LINK_CYCLES.md:421 |
| `cycle09/controller.jsonl` | 387426 | `13518a9b122d9684cb467fe386d99cf930299141eb7b625016954a4c5f0a33dc` | 599_394_E1_LINK_CYCLES.md:420 |
| `cycle09/events.jsonl` | 4427 | `49e70cddae0f081dd04b9fe2424d3bb7cb178d60c366747e88aa2075d9b79649` | 599_394_E1_LINK_CYCLES.md:423 |
| `cycle09/results.json` | 78 | `5dac67330990e703cf25df9fc08adf367f31a4a43ae32d5a390dc2e5e302dd4f` | - |
| `cycle09/tap-capture.txt` | 185 | `0ff663b69966a4033720ce67d0703856af3e0c93fdc1383d57cf9bcb7cb7ccf5` | - |
| `cycle09/tap.pcap` | 7026007 | `cfe8b42e0be6917aa09b25859788e989f082e075b482b28cae95ab9276e59e4a` | 599_394_E1_LINK_CYCLES.md:422 |
| `cycle10.out` | 4602 | `25d70d242bd65f8893fad326257e049722d9fb0a991274946d53bcddc9cb4f50` | - |
| `cycle10/console.jsonl` | 1030456 | `855eaa4aaa2091c8f176e683237cde2986de1c1da99954eb6b0dfba25dbf1b66` | 599_394_E1_LINK_CYCLES.md:424 |
| `cycle10/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `cycle10/controller-wire-capture.txt` | 183 | `92348c7bb418504a9b35763c813501cdb7b26b342b9c5b6a57dc32099064afdc` | - |
| `cycle10/controller-wire.pcap` | 217955 | `09723298565221fa07bf305a8a442a45469e62fa5d6131fdda0057e6b8e8a965` | 599_394_E1_LINK_CYCLES.md:426 |
| `cycle10/controller.jsonl` | 387630 | `268c21ddd42314c14c48407554caab9f734afa97367a06a0b8fc679108f04c38` | 599_394_E1_LINK_CYCLES.md:425 |
| `cycle10/events.jsonl` | 4423 | `cefe475b77241b654714a49bd8f9d42d22f91f8732838e479cd1ad6f2780e875` | 599_394_E1_LINK_CYCLES.md:428 |
| `cycle10/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `cycle10/tap-capture.txt` | 185 | `ef97bc3638bc884d1907ed57d735a0f6e638e53777946678da02d77a486f226a` | - |
| `cycle10/tap.pcap` | 7535225 | `959b33d3e92e700d54ba77ebfa9d095a2f1d64c34974bae4b0dbb34ce9a76518` | 599_394_E1_LINK_CYCLES.md:427 |
| `dryrun.out` | 3699 | `d94dd4d2cf99e4df7f04ff62ed14aef3efb2b87304cb59ce69d347aa49675f10` | - |
| `dryrun/console.jsonl` | 187346 | `d0a032aff9ceee502d80dfab55319f7d0ece0d9ec9e0e20ca20069c05afcff4e` | - |
| `dryrun/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `dryrun/controller-wire-capture.txt` | 181 | `a2a4c0ed158856ac2d2af21c4c6746e64644c4c1169efd99328a6f90070b1e65` | - |
| `dryrun/controller-wire.pcap` | 56760 | `df05ed4d47362d2aec2f825b85d175874b72ee26b3cedb74c57ad43860baffdf` | - |
| `dryrun/controller.jsonl` | 105802 | `5b17a3804d30aac8e896052ae20eeb7b80ad97da5761aa2031c6f1607d3468a8` | - |
| `dryrun/events.jsonl` | 3522 | `1af879b692d2a8f48f434f5b0f4afc8512ceacb69b50c434c158a4edacc68607` | - |
| `dryrun/results.json` | 78 | `5dac67330990e703cf25df9fc08adf367f31a4a43ae32d5a390dc2e5e302dd4f` | - |
| `dryrun/tap-capture.txt` | 181 | `f4e9cfe7021dcf6d328500d94075fdcc9d2fc331fcba623500c65be3ed233dd1` | - |
| `dryrun/tap.pcap` | 102664 | `e8bb7c7014fa9581794ff53ee86b3d1aab5ef9f21c4ee082138a5b88c517ca52` | - |
| `final.out` | 3699 | `9899ba46f9352856a12300dcd13d2db799cfebbd644ee0ef539fb24f5d0dcedb` | - |
| `final/console.jsonl` | 187365 | `a31acfa62ec6dafb4cc435d4bc2d659cce5ad57e4aa4884e3701810163f83abc` | 599_394_E1_LINK_CYCLES.md:429 |
| `final/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `final/controller-wire-capture.txt` | 181 | `d2fa709f88773e777c91e0946fb1c46cfce9a3ab65f66a8a4a4e0334f9b9c94c` | - |
| `final/controller-wire.pcap` | 55794 | `d7f133423855bdf01caf76f0bc83d8fa951489144295184fbd4ee64b26571ed9` | 599_394_E1_LINK_CYCLES.md:431 |
| `final/controller.jsonl` | 106986 | `c3d713b1e6a7b3e1c19a91dde235257bf24f4d7a92f4a3a53b8365b470d0f8f0` | 599_394_E1_LINK_CYCLES.md:430 |
| `final/events.jsonl` | 3524 | `7273adbd2c3885e6a610f43a786f3969a79b94f434636133031df18917244f5c` | 599_394_E1_LINK_CYCLES.md:433 |
| `final/results.json` | 78 | `ce072d8b1542034b26424f9aaa58540be1e6806242539bb1d7032bc5a1513d47` | - |
| `final/tap-capture.txt` | 181 | `831da20ec27698c9858117ba45bd30c028381ef9d5fed34c96b59787f8df7fbb` | - |
| `final/tap.pcap` | 107324 | `d4a257684d4a5d3cf007b45d0801e51b9a89b94bc6bb8e527bd6355f1d99b591` | 599_394_E1_LINK_CYCLES.md:432 |
| `gm01.out` | 4295 | `264a3f29fac40e0a8113190a4a6f4cc81f76deb1042d5ed2ac6130e7ff619fe6` | - |
| `gm01/console.jsonl` | 1124688 | `f72e7065b6f5a363d2a20d6258679463341ebd7343b6d9177c3188f9d6551ed2` | 387_SOFTWARE_GM_STEP.md:325 |
| `gm01/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `gm01/controller-wire-capture.txt` | 183 | `27a9a4ccc3f61c065f176f868f800065b9df2842cfec3662ec0847e1619ff5c6` | - |
| `gm01/controller-wire.pcap` | 459526 | `77de6b4ed15dcb48be985dea76476c8c6696ddb8dd215b3e81b6e3912d17c1ca` | 387_SOFTWARE_GM_STEP.md:327 |
| `gm01/controller.jsonl` | 639590 | `f252de61752452c992829302d352cc8592d6650545113b9a5fc2e41740e69f9f` | 387_SOFTWARE_GM_STEP.md:326 |
| `gm01/events.jsonl` | 4122 | `537d187739b2fce75f7478c6194fb37be79ee548abdae4e18a203ae1f8f87bb9` | 387_SOFTWARE_GM_STEP.md:329 |
| `gm01/ptp4l-gm.log` | 479 | `1aef82ba0ca494f70c96a6710271f21ad2967a47362fa2409915ce9fa96d837e` | 387_SOFTWARE_GM_STEP.md:331 |
| `gm01/ptp4l-slave.log` | 3448 | `880fdb8d204b61b899294363b8cc6e09379c9bd5d62a4bb8e3bfcd90a1eb456e` | 387_SOFTWARE_GM_STEP.md:330 |
| `gm01/results.json` | 91 | `38815a5da7afee5374a5d9148516dfd8c419f347c2b85eebf7b8fff6f112ec2c` | - |
| `gm01/tap-capture.txt` | 187 | `44cc9cbe723239d4a8bf60adb564ca9d6e31cfa5cde9d00c0d2698c6b71e8f77` | - |
| `gm01/tap.pcap` | 13625805 | `9a85c4b61f6a21f8f7239f4960088e3273d70f3a1ff08f47d8ef24c286218a64` | 387_SOFTWARE_GM_STEP.md:328 |
| `gm02.out` | 4293 | `5d770c304d926855d4803f8d9be71948d98cd29e3e18a94e0011c6e2bc5545eb` | - |
| `gm02/console.jsonl` | 1124293 | `9ee376fafce7b093324dfe3d1632d4c9fd62291410940028947785692b019065` | 387_SOFTWARE_GM_STEP.md:332 |
| `gm02/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `gm02/controller-wire-capture.txt` | 183 | `3d51551ebbb2b5b536f85465600541786f51573a1f8c157040096773b0301675` | - |
| `gm02/controller-wire.pcap` | 461331 | `9abe94d91ad0113807da88849a990fc3298807a627cf3cc0ae556aa8c8970cfe` | 387_SOFTWARE_GM_STEP.md:334 |
| `gm02/controller.jsonl` | 639591 | `b7134efdda62576ba5294ccb291bd01b1246166bd0a3326fc89630dc2db6b7ec` | 387_SOFTWARE_GM_STEP.md:333 |
| `gm02/events.jsonl` | 4120 | `e8ebad60b8eb0c86c14c6c4938e5a9ad00fc9a23a26942cc9e03e2ac59909126` | 387_SOFTWARE_GM_STEP.md:336 |
| `gm02/ptp4l-gm.log` | 479 | `db7adce82609d24de2612c11f79168bf683d42c6af8a77d4eb350f115af3c61c` | 387_SOFTWARE_GM_STEP.md:338 |
| `gm02/ptp4l-slave.log` | 3456 | `a4872aa922897a7113bad409757257de0db0ef3abf6243ea46b1be104333c873` | 387_SOFTWARE_GM_STEP.md:337 |
| `gm02/results.json` | 91 | `38815a5da7afee5374a5d9148516dfd8c419f347c2b85eebf7b8fff6f112ec2c` | - |
| `gm02/tap-capture.txt` | 187 | `8953a337ad22a28747f71f8acb8bd02d732117c5174c17f8cb5b0fffdcf78ef7` | - |
| `gm02/tap.pcap` | 13619719 | `fbb55efea84122a31325698595045b58cf2309d1b8b2c49661e1ced3a3210642` | 387_SOFTWARE_GM_STEP.md:335 |
| `gm03.out` | 4290 | `b6866d2bcc44b9b48d75bd7897993099adfacf33e39726e319997c1ccce5d2d2` | - |
| `gm03/console.jsonl` | 1124314 | `bbcc51d0f77f4a79946c858ffe1c64c05b6e470da42336bcff9ea7334edd093f` | 387_SOFTWARE_GM_STEP.md:339 |
| `gm03/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `gm03/controller-wire-capture.txt` | 183 | `d4b3e1782a273ef3da0e890917078e7785fc0d6267f42718376ee512acfb6866` | - |
| `gm03/controller-wire.pcap` | 461864 | `5e1d6020f10f05450a1672a008213322b88fa40f1abf1fbc61b780af6f96fcf2` | 387_SOFTWARE_GM_STEP.md:341 |
| `gm03/controller.jsonl` | 639595 | `8a602368bc8d5fe367d365c066b76bfe7647f1ff36a8a469af64045b24fad416` | 387_SOFTWARE_GM_STEP.md:340 |
| `gm03/events.jsonl` | 4117 | `9c05be2ba65a213c8dae22c2ae4e40a1a6db9528f987242d877fb2be4689b6e5` | 387_SOFTWARE_GM_STEP.md:343 |
| `gm03/ptp4l-gm.log` | 479 | `be71fc54bafcd6acc2f172c2ba799d348e93920e427845639eadbc101c4fc32f` | 387_SOFTWARE_GM_STEP.md:345 |
| `gm03/ptp4l-slave.log` | 3455 | `8771d269dbaf77d532007c9fb8ca23d5debdb1a0a3d9cc21fec5b19075f1120e` | 387_SOFTWARE_GM_STEP.md:344 |
| `gm03/results.json` | 91 | `38815a5da7afee5374a5d9148516dfd8c419f347c2b85eebf7b8fff6f112ec2c` | - |
| `gm03/tap-capture.txt` | 187 | `a81b15291ee32f5269a402f0e74771b7d14cf946b260c84047c11c3a7303134b` | - |
| `gm03/tap.pcap` | 13625642 | `c27b4e7eb119e3bc1eedc17d5c7708b986db9778b01fa0ded209089e01882c59` | 387_SOFTWARE_GM_STEP.md:342 |
| `gm04.out` | 4288 | `d39611f6e995a1afca469db8a52140a0551b2023a950ed1917424104de3cb54e` | - |
| `gm04/console.jsonl` | 1124629 | `e2e1914554e0dbd8bb9dac97d3257709ea62d5d546870ba53de315bea8d803a6` | 387_SOFTWARE_GM_STEP.md:346 |
| `gm04/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `gm04/controller-wire-capture.txt` | 183 | `ec90abfbc4b0a1007ae54cc935d9ad1eab59adff290bb82556da8ab9a6c64088` | - |
| `gm04/controller-wire.pcap` | 469859 | `33751c9cdc0c6161dafa7d1a060fc81a108659dfaa2f5d0dd939ee2453a637d5` | 387_SOFTWARE_GM_STEP.md:348 |
| `gm04/controller.jsonl` | 640655 | `281e445fbdee2f89bd3924c3947d3ab1712179704f2786c5a12b69413cac097d` | 387_SOFTWARE_GM_STEP.md:347 |
| `gm04/events.jsonl` | 4115 | `7bff01660d336620fc162bcf02f2cd98cf18eac94e9fd2909efb55b71ae44ec5` | 387_SOFTWARE_GM_STEP.md:350 |
| `gm04/ptp4l-gm.log` | 479 | `69cf477bca78bf606adf5a4239658fabce48e6266a6ed3c22c1d68a9db102970` | 387_SOFTWARE_GM_STEP.md:352 |
| `gm04/ptp4l-slave.log` | 3455 | `23ff472a8a031be3484731b848d6dfeab6239c444e39ba8109f490eac7cc7873` | 387_SOFTWARE_GM_STEP.md:351 |
| `gm04/results.json` | 91 | `38815a5da7afee5374a5d9148516dfd8c419f347c2b85eebf7b8fff6f112ec2c` | - |
| `gm04/tap-capture.txt` | 187 | `2a78696175a609ee1d99c7f1dcee4a1556062b7b20b39a9c929dfb192703f1c6` | - |
| `gm04/tap.pcap` | 13630825 | `747248b7c98ec0ea49b0e408ceb37bb4d10c6ce8c28e0e31d61b31c7b88d9a22` | 387_SOFTWARE_GM_STEP.md:349 |
| `gm05.out` | 4294 | `d998f394587485596fdc2a06078ede486f005ad7c5221261ad02c4504c5b695a` | - |
| `gm05/console.jsonl` | 1124327 | `04efafe2c570666386ecfe2f8afd34e4c855dd0e00c62878d6b231651b15bf7b` | 387_SOFTWARE_GM_STEP.md:353 |
| `gm05/controller-errors.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `gm05/controller-wire-capture.txt` | 183 | `5aefff9426a746cc5a727e73d1506c0b2070b446928613b2f37ddc4cd73b6aa5` | - |
| `gm05/controller-wire.pcap` | 463422 | `f7bc4660584866629e59987febf6606129b8b520e0ecbb5a06c7f952cc3f1bf0` | 387_SOFTWARE_GM_STEP.md:355 |
| `gm05/controller.jsonl` | 641526 | `988fb3a7a589f0153c857e8958febb2e5125b53f3b029c35b4d0b0d10c571670` | 387_SOFTWARE_GM_STEP.md:354 |
| `gm05/events.jsonl` | 4121 | `bdfbfbfef6b47670c31e6102efbf78b944dc23c30f150357ead05c2cfcc03a60` | 387_SOFTWARE_GM_STEP.md:357 |
| `gm05/ptp4l-gm.log` | 553 | `2de4be8f78691f3727c1ee89ac37979a338e03f713d575ae910e1c7e0fd4a870` | 387_SOFTWARE_GM_STEP.md:359 |
| `gm05/ptp4l-slave.log` | 3455 | `e8eddea557e3fb3572922a324286ca17db160b146f074a414e4e2341e1e4bd46` | 387_SOFTWARE_GM_STEP.md:358 |
| `gm05/results.json` | 91 | `38815a5da7afee5374a5d9148516dfd8c419f347c2b85eebf7b8fff6f112ec2c` | - |
| `gm05/tap-capture.txt` | 187 | `f976932974419fb534f2b82b1f2a5f798c5aa19243713b899e0ce98b86fecdea` | - |
| `gm05/tap.pcap` | 13620466 | `444488b1b1f0b9293bbd544860cc66feef0d5e53172b1b861428d7f48f99c060` | 387_SOFTWARE_GM_STEP.md:356 |
| `identity-aecp-raw.jsonl` | 1424 | `6543037f79868386065fde5f8c0d2f573831cc7f86891dba1d93e2b2c4b5edc3` | - |
| `peer-config1-desc-raw.jsonl` | 10201 | `92a60fe90d1ba597ed2a6a213c4e4ce954b3fc4c38eba8a8ef0bca5dedcf1068` | - |
| `post-slave-test-snapshot.jsonl` | 5222 | `158bb09b10da511a85dfda63615dcaa5498f84aa2c89ac2408a128152e80a792` | - |
| `preflight-hosts.txt` | 420 | `7d03f4a897994cae66f532f49269b50d69b6f06f06defb4ac94bf5890343720b` | - |
| `restore-raw.jsonl` | 2716 | `9a2a09694a4ddcc67a466376633d580fa58cc935d6a6ed8f8a92771817e9572c` | - |
| `restore.err` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
| `setup-raw.jsonl` | 6725 | `b2876767d5ffeeaeeaf57efa1fc5f9c80c84c6c126eae6a1b3a3a305600f9f22` | - |
| `setup.err` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | - |
