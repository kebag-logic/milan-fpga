[R594] POSITIVE - exact head 1df3ac18a85c59626491ccb6c0955f834cb1d31f

# R594-2: internal independent review of PR #712 (issue #629, bench lane B15), round 2

- Head `1df3ac18a85c59626491ccb6c0955f834cb1d31f`, tree `94830be1d4efecf402b0866e18edfc2fb85e186d`. Two commits on dev `e8454e2751d05b02ee8e5a571857589ab358ab86`: `70cd90a4` (round 1) and `1df3ac18` (round 2, no rebase or amend). The source base equals live dev.
- Diff (`git diff e8454e27..1df3ac18`): `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` (+395/-1: the title's image list, the introduction pointer, the Contents line, and the dated section "Dev 5603c353, 2026-10-10: lane B15" at `:1875-2263`) and its row in `docs/findings/README.md` (1/1). No code, RTL, firmware, test, generator or gitlink change. `scripts/ci_scope.py` classifies the diff as docs-only (`receipts/ci_scope_diff.txt`: `False`).
- Scope comes from the [B15 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6097827871): find where the Direction B tone is lost and repair it only if the DUT loses it. The branch "Tone absent at (a)" means: read the instrument and peer state read-only and STOP with the evidence. Step 4 asks for a dated "lane B15" section with per-point tables, capture hashes and the #629 checklist judged. The [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6098395010) keeps round 2 to documentation, cites packet `06148614`, and allows no republish. #629's frozen body is the parent acceptance: Direction B's bench quality metric is not claimed met, and #629 stays open.
- The evidence judged is the public packet at `629-tone-review-evidence` = `06148614c910d3986991dd130f95d073b4bbe491`, `review-evidence/629-tone-r1/` (182 files, author material only).

## Verdict

POSITIVE. Every lane B15 statement I checked reproduces from the published packet:

- the decoder summaries, counters, census, NVM and `SLIP_LB` dumps, the peer survey and the board log (43 of 43 checks);
- every hash and byte count on the page (9 evidence rows and 11 raw rows), plus the decoder's as-run prefix;
- the three tool-control sets, which re-run byte-equal.

The round-1 MINORs of both reviewers are resolved at this head, and both residue texts are applied. All five lenses are covered clean. One new RESIDUE item (wording only) and two retained SUGGESTIONs are listed below. Neither changes coverage or the verdict.

The lane's conclusion is supported, and the page states it at the right strength: the tone is absent at the peer's own talker, at the DUT's link and at the DUT's TDM output, and the DUT renders what it receives. The tap decode at (a) finds an idle floor with every per-tone share at the flat-floor value, 0.03 to 0.05 %. A tone that survived to the 24-bit stream at about -140 dBFS or louder would raise that share to tens of percent (probe B, below). The absence is therefore not an artefact of the presence rule's -40 dBFS gate. (c) equals (b) in 480,000 of 480,000 frames in both runs, with one first-window match and no slip. The page discloses the limits itself: no tone at (a), so the DUT is not graded rendering a tone it receives.

## Findings

### R594-2-R1 - RESIDUE - Docs - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:2247-2250` (and rows `:2260-2262`) - only the decoder is named as masked in the lane packet, but three other cited rows were masked there too

- Evidence: `author/redaction.json` at `06148614` lists 31 files that the lane packet already held with identifiers masked. Among the rows this page hashes, that includes:
  - `tools/tone_points_b15.py`, as run `3adb505f...` (the page says so);
  - `runs/pts1/events.jsonl`, as run `d80ffde4...`;
  - `runs/pts2/events.jsonl`, as run `5d4acd1c...`;
  - `restore/census-compare.txt`, as run `f3a32e9e...`.
- The page singles out the decoder alone ("The lane packet already held `tone_points_b15.py` masked, and `redaction.json` alone holds its as-run hash"), which implies the other rows are unmasked as-run files. Every cited hash is correct: each equals its file and its `published_sha256` and `original_sha256` (`receipts/doc_hashes.txt`). So this is wording only. It moves no measurement, figure, verdict or claim, and it exposes nothing.
- Exact fix: replace "The lane packet already held `tone_points_b15.py` masked, and `redaction.json` alone holds its as-run hash." with "The lane packet already held `tone_points_b15.py`, both `events.jsonl` files and `census-compare.txt` masked, and `redaction.json` alone holds their as-run hashes."

### R594-2-S1 - SUGGESTION - Tests, Robustness - `author/tools/align_b15.py:33-38, 85-87` (packet) - alignment key and tail accounting (retains R595-1-S3)

- Probe A6 (`receipts/probe_align_sensitivity.json`): a +256 LSB error on channel 0 still reads SAMPLE-EXACT, because `key()` keeps 8 bits per channel.
- Probe A7: a recording that runs 180,000 frames past the stream's end reads SAMPLE-EXACT with 300,000 of 480,000 frames compared.
- Neither touches B15's two verdicts:
  - the key is injective on -128..127 (A8), and every value at (b) is in -2..+1 and at (c) in -2..0 (`receipts/crosscheck_b15.txt`);
  - compared = recorded = 480,000 and covered = [0, 480000] in both runs.
- Before the tool is reused on a tone at (a): widen the key to the full 24 bits, and require compared == recorded for SAMPLE-EXACT.

### R594-2-S2 - SUGGESTION - Tests, Conformance - `author/tools/tone_points_b15.py` `channel_rows` (packet) - the presence gate is a whole-channel RMS level (retains R594-1-S1, R595-1-S4)

- Probe B: on a floor like the captured one, a 997 Hz tone at -140 dBFS gives share 0.68 and at -120 dBFS 0.995. Both read TONE ABSENT under the rule "share > 0.9 and RMS > -40 dBFS". Below about -150 dBFS the tone does not survive 24-bit rounding.
- B15's conclusion does not depend on the gate. The page reports the shares, and they sit at the flat-floor value.
- For the lane that resumes Direction B (the tone leaves the source at -38.5 dBFS): grade presence against the floor, or record the expected arrival level first, and add a control with a quiet tone that is present.

### Prior public findings at this head

Each is checked against the head bytes and the packet.

| Finding | Status at `1df3ac18` | Evidence |
|---|---|---|
| R594-1-F1 (MINOR, Docs): packet location; evidence files and decoders not hashed; private records not stated | RESOLVED | `:2235-2245`: "Where the packet is", in B8's form: branch, pinned `06148614`, label mapped to `review-evidence/629-tone-r1/author/`, the `MANIFEST.json` convention, the three masked publications. `:2252-2262`: 9 evidence rows, each equal to file bytes, `published_sha256` and `original_sha256`; 11 raw rows equal to `RAW-ARTIFACTS.json`; the as-run prefix `3adb505f` is present in `redaction.json` (`receipts/doc_hashes.txt`, 0 BAD). `:2118-2119` says the tone source's state read and meter rows are held privately |
| R594-1-F2 (MINOR, Docs): outage start | RESOLVED | `:2179-2186`: deliberate stop at 15:27:19.7, unintended from the 15:27:55 `LEG_PRESENT_NOT_STARTED`, restart 15:28:23, about 63 s. `soc/pts1-legs.log`: kill to playback trigger is 63.5 s of board uptime (`receipts/crosscheck_b15.txt`) |
| R594-1-R1 (RESIDUE) | APPLIED | `:1946-1949` carries the exact text |
| R595-1-F1 (MINOR, Conformance, Docs): AUDIO_CLUSTER claim contradicting the published survey | RESOLVED | `:2126-2148`. The 20 NO_SUCH_DESCRIPTOR answers each carry type `0x0010` in configuration 1 (`receipts/crosscheck_b15.txt`). IEEE 1722.1 Table 7.1 gives `0x0010` to EXTERNAL_PORT_INPUT, and `avdecc/aem_descriptors.py:103` gives AUDIO_CLUSTER = `0x0014`. The cited PR #628 review records the same wrong code. The second read is stated as private, with its configuration (1) and the reason the reads disagree. The conclusion is stated to rest on public evidence: the tap decode, and the CONFIGURATION counts (no JACK_INPUT, no port types, CONTROL 1) and AUDIO_UNIT 0 port fields (all external and internal counts 0), which I decoded from `restore/peer-descs.jsonl`. IDENTIFY is also visible publicly in that file's CONTROL 0 payload (`90e0f0000000...01`). Every item of round 2's item 3 is met |
| R595-1-F2 (RESIDUE) | APPLIED | `:1900` table cell and the README row read "with THD+N at the loop's 24-bit floor" |
| R595-1-F3 (RESIDUE) | APPLIED | as R594-1-F1, packet location |
| R594-1-S2 / R595-1-S1 (FRAMES_RX) | APPLIED | `:2055-2056`; increments 191,998 and 199,998 reproduce |
| R594-1-S3 (`SLIP_LB` unexplained) | APPLIED | `:2170-2177`; dumps `0x92` to `0x98`, 146 to 152; two dups per slipped frame on the four-channel stream is the page's own convention (`:1424`) |
| R594-1-S1 / R595-1-S4 (presence gate) | RETAINED as R594-2-S2 | optional |
| R595-1-S3 (alignment key and tail) | RETAINED as R594-2-S1 | optional |
| R594-1-S4 / R595-1-O2 (host virtual interfaces), R594-1-S5 (as-run hash of `align_b15.py`), R595-1-S2 (`tail -2`), R595-1-S6 ("sample-exact" inferred from THD+N) | OPEN, optional | SUGGESTION or observation only; none affects coverage |
| R595-1-O1 (grader identity file unmasked) | Carried by the manager to #495 | already public in `docs/findings/117_GPTP_SILICON_EVIDENCE.md`; not a finding against this head |

## Per-lens results (covering round R594-2, head `1df3ac18a85c59626491ccb6c0955f834cb1d31f`)

- **[R594] PASS Conformance** - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1875-2199` checked against the B15 assignment's steps 1-4, the round 2 items 1-5 and #629's proof items:
  - Identity: `author/identity/identity-verdict.txt` and `grader-identity.txt` match the table. The entity facts, VERSION and AEM CRC agree with `docs/findings/653_DISCONNECT_ORDER_BENCH.md:62-64` and `667_TALKER_START_BENCH.md:21`. CLOCK_SOURCE 1 and 2 are located on STREAM_INPUT 1 and 0 (location_type 5), and 3 answers NO_SUCH_DESCRIPTOR.
  - Branch: the "absent at (a)" branch is taken, with read-only state and a STOP. No DUT change.
  - Binding rule: `summary/points.md` shows the listener format adapted (peer STREAM_INPUT 0, set, echoed, restored) and never the talker's.
  - AAF field decode in `tone_points_b15.py` checked against IEEE 1722-2016 clause 7 (subtype, mr and tv bits, format, nsr 5 = 48 kHz, 10-bit channels_per_frame, bit_depth, stream_data_length, payload at 24).
  - The #629 acceptance table does not claim Direction B; #629 stays open.
- **[R594] PASS RTL** - the diff names only two docs files (`git diff --name-only`; `receipts/ci_scope_diff.txt`), and the gitlinks are unchanged (`receipts/restore_check.txt`). The page's claims about the DUT path, checked against the evidence and the register map:
  - "depacketiser, channel map, sample conversion, TDM render lose nothing here": `summary/pts{1,2}/align-b-c.json`; the DUT input map in `restore/census-start.jsonl` (four mappings, stream channel c to cluster offset c); `c-mcasp.json`, where channels 4-7 are all zero and the low byte is 0.
  - Counters: `summary/points.md` (MEDIA_LOCKED 1, no interruption, mismatch, late, early or invalid timestamp).
  - `SLIP_LB` read against `docs/reference/REGISTER_MAP.md:1846-1880`, with its unit (one dup per fed and primed pair per tick); the residual is honestly marked unexplained and linked to #645.
- **[R594] PASS Robustness** - `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:1975-1994, 2085-2089, 2152-2186` against `summary/*`, `restore/*` and `soc/pts1-legs.log`:
  - malformed and gap paths: 0 bad length, 0 gaps, 0 `tv` clear and 0 `mr` toggles on every selected PDU at (a) and (b);
  - the unusable (d) of `pts1` is disclosed (peer counters 0, digital output exact zero);
  - the restore is complete: census 45 of 46, the one difference being the propagation delay `0x17d` to `0x183` (381 to 387 ns); NVM seq 272 to 276 and commits 38 to 42, `pend=0`, `VD_OK`;
  - the rx-flags `0x0002` vs `0x0082` exception matches `runs/pts1/events.jsonl`;
  - the incident timeline reproduces from the board log.
- **[R594] PASS Tests** - `author/tools/tone_points_b15.py`, `align_b15.py`, `b6_thdn.py` and `b9_thdn.py` at `06148614`:
  - The tap-decode controls re-run byte-equal to `controls/b15-tap-controls.json` (`f69bf5cf...`). Only the two masked identifier placeholders were filled for the run, and the stream ID does not appear in the output.
  - `b6_thdn controls` re-runs byte-equal to `7bbefc71...` and `b9_thdn controls` to `728a4f0e...` (`receipts/probe_b{6,9}_controls.*`).
  - Alignment `compare()` probes on a synthetic floor shaped like the capture: exact copy SAMPLE-EXACT with one match; dropped frame +1 slip at the planted frame; repeated frame -1 slip; one changed LSB one differing frame.
  - Each B15 control can fail for its defect.
  - The two tool blind spots (R594-2-S1) and the presence gate (R594-2-S2) are SUGGESTIONs that do not apply to the recorded runs, for the reasons given.
- **[R594] PASS Docs** - the full diff at the head; the pinned Markdown gates rc 0 (`receipts/gates/`); the page cross-checked against the packet (`receipts/crosscheck_b15.txt`, 0 BAD; `receipts/doc_hashes.txt`, 0 BAD); the README row and the introduction checked against the section:
  - `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base e8454e27`, `check_doc_paths.py`;
  - `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check e8454e27 HEAD`.
  - The added lines carry no new host, address, instrument-product or model identifier; private records are named as private.
  - One RESIDUE (R594-2-R1) carries its exact fix.

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | B15 and round 2 assignments; #629 body; page `:1875-2199`; `author/identity/*`, `summary/points.md`, `tools/tone_points_b15.py` (AAF decode vs IEEE 1722-2016 cl. 7); `restore/peer-descs.jsonl` (CONFIGURATION, AUDIO_UNIT, CONTROL, survey types); `avdecc/aem_descriptors.py:103` | R594-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| RTL | CLEAN | diff file list; `receipts/ci_scope_diff.txt`; gitlinks; `summary/pts{1,2}/align-b-c.json`, `c-mcasp.json`; DUT maps in `restore/census-start.jsonl`; `restore/dut-{start,end}.txt` (`0x8D4`); `docs/reference/REGISTER_MAP.md:1846-1880` | R594-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Robustness | CLEAN | page `:1975-1994, 2085-2089, 2152-2186`; `summary/*` gap, length, `tv` and `mr` fields; `restore/census-compare.txt`; NVM lines; `runs/pts1/events.jsonl` flags; `soc/pts1-legs.log` | R594-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Tests | CLEAN | `tools/tone_points_b15.py`, `align_b15.py`, `b6_thdn.py`, `b9_thdn.py`; byte-equal control re-runs; `receipts/probe_align_sensitivity.json` | R594-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |
| Docs | CLEAN (RESIDUE R594-2-R1 carried) | full diff; `receipts/gates/*` (11 gates rc 0); `receipts/doc_hashes.txt`; `receipts/crosscheck_b15.txt`; README row; round-1 findings table above | R594-2 | `1df3ac18a85c59626491ccb6c0955f834cb1d31f` |

## Real limits

- No bench, instrument or DUT access. The raw captures stay on the bench host, as in lanes B6 to B8. So I checked the per-point figures against the published decoder summaries and alignment JSONs and the tools' published code; I did not recompute them from the captures. Example: ch0 reads -2..+1 at (b) and -2..0 at (c), which is consistent with a 10 s subset of the 24 s stream but not recomputed.
- The tone source's state, its meter rows and the 15:35:10 peer cluster read are private. I cannot verify them, and the page states that the conclusion does not rest on them.
- I took the identity facts from the packet and cross-read them against other findings pages, not against a build of dev `5603c353`.
- No manager source bank runs at this head, and I claim none. The source-head execution evidence is the author's published gate receipts plus my own documentation-gate re-run listed above. Physical calibration was NOT RUN, and field skips are not hardware proof.
- Hosted checks at my read: `rtl-fast`, `elaborate`, `changes`, `full-ci-gate`, `wire-accountability`, `bdd-conformance` and `docs-check-no-git` completed SUCCESS. `docs-check` was IN_PROGRESS. The Verilator, Yosys, firmware-unit and physical contexts were SKIPPED, as expected for a docs-only classification. These are observations only; the manager owns hosted and act acceptance.
- After the probes the clone is byte-exact at the head: 1,270 tracked files with blob hashes and modes equal to the index; no change between index and HEAD or between worktree and index; five gitlinks at their recorded commits (`receipts/restore_check.txt`). No probe ran inside the clone.

## Pending manager duties

- Confirm the hosted `docs-check` at the exact head, and own hosted and act acceptance.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts.
- Carry R594-2-R1 to the residue checklist with its exact text. R595-1-O1 is already carried to #495.
- Obtain the external positive review, maintainer merge authorization, post-merge containment, and the issue state: #629 stays open (Refs only), and #645 stays open.

## Receipts (paths relative to this packet)

- `scripts/check_doc_hashes.py` -> `receipts/doc_hashes.txt` (page hash and byte rows vs packet)
- `scripts/crosscheck_b15.py` -> `receipts/crosscheck_b15.txt` (page figures vs packet records)
- `scripts/probe_align_sensitivity.py` -> `receipts/probe_align_sensitivity.{json,stdout,rc}` (alignment probes A1-A8, presence sensitivity B; probe A5 cuts a genuine stretch of the stream, so its SAMPLE-EXACT is the expected answer)
- `receipts/probe_tap_controls.{json,stdout,rc}`, `receipts/probe_b6_controls.{json,stdout,rc}`, `receipts/probe_b9_controls.{json,stdout,rc}` (control re-runs)
- `receipts/gates/*` (documentation and scope gates at the head), `receipts/ci_scope_diff.txt`, `receipts/restore_check.txt`

R594-2 FINISHED
