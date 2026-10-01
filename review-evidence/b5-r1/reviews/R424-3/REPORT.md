[R424] NEGATIVE - exact head cf38633ad9a5bdb05517bedba73ce50965af967b

Round R424-3, internal independent review of PR #628 (Refs #117, acceptance box 4, the audio continuity row; bench lane B5, evidence only).

- Head `cf38633ad9a5bdb05517bedba73ce50965af967b`, tree `150f848bdb9c85bf6bd0b005bce4579724ed6aa8`; parent (round 2) `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`; round 1 `bf9e5d82a401d167a8ffc786677a19dc7aac0cf2`; base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.
- Round 3 is one commit on `docs/findings/117_AUDIO_CONTINUITY.md` (+93 -35) and its row in `docs/findings/README.md` (1 line). Nothing else changes against the base.
- Assignment: #117 comment 5927406852. Archive note: PR #628 comment 5927406516.
- Evidence read: branch `b5-review-evidence` at `227a6541159dddb237c1d3cec7dc71fbf4063f31`, under `review-evidence/b5-r1/`. That commit contains `ef3a7091` (round 1, `author/`), `1116f856` (round 2, `author-r2/`), `2a40015e` (the `.gz` record), `2345dba7` (the corrected NOTE) and the round 3 packet `author-r3/`.

**Verdict basis.** One MINOR is open, R424-3-F1, a Docs defect in text that round 3 added. It leaves Docs UNCLEAN, so the verdict is NEGATIVE. Conformance, RTL, Robustness and Tests are CLEAN at this head.

Every item the round 3 assignment set is met, and both round 2 findings are resolved:

- **F1, the read record.** It restores from the public archive alone to SHA-256 `2183d57f…`, and the page's steps reproduce `attribution.txt` and `round3_figures.txt` byte for byte.
- **R425-2 F2, the Direction B reason.** Resolved.
- **Tables.** 14 of 15 are byte-identical to round 2, and only the two named Evidence cells change.
- **PR, public text and gates.** The PR says Refs #117 only, the public text is clean, and the docs gates are rc 0.

My own pass over the diff and the figures came before I read any prior review on this PR.

## Findings

**R424-3-F1 - MINOR - Docs - `docs/findings/117_AUDIO_CONTINUITY.md:199-207`, `:440-456` (packet names also at `:185-186`, `:202-204`) - the new reproduction steps do not say where the packets they operate on are published**

- *Authority/evidence.*
  - AGENTS.md section 2: "A future cold reviewer must be able to reconstruct the task from GitHub and the repository alone". The Docs lens adds: "enough evidence for another cold reviewer".
  - Round 3 added a numbered procedure (`:447-456`), which says: "In the round 2 packet's receipts, run `gunzip -kf …`", then "Run `b5_attrib.py figures` with the lane packet and that receipts directory", then run `b5_round3.py` "from the round 3 packet `b5-a474`".
  - The page names the packets only by their lane labels `b5-a472`, `b5-a473` and `b5-a474`. It does not name a branch, a path, a link or a commit. A search of the page for `review-evidence` or a branch name finds nothing.
  - In the public archive the packets sit at `review-evidence/b5-r1/author/`, `author-r2/` and `author-r3/` on branch `b5-review-evidence`. Those directory names do not carry the lane labels.
  - Sibling findings pages that publish packets say where they are:
    - `docs/findings/606_FIRST_BIND_MEASUREMENT.md:257` and `:297` give the branch and path for both rounds;
    - `617_DIN_FRAME_COHERENCE_BENCH.md:276-277` and `451_USB_AUDIO_CAPTURE.md:217-218` give the branch and path;
    - `117_GPTP_SILICON_EVIDENCE.md:652-654` adds a link pinned to a commit.
- *Impact.* From the merged page alone, a reader cannot follow the steps it gives, or find the published analysis behind "each cause below is stated only as strongly as the published analysis carries it". The figures do reproduce (`f1_reproduction.txt`). But only the PR thread and the archive commit messages locate the inputs, and neither is durable repository documentation. If the evidence branch moves, nothing on the page pins what was meant.
- *Not attributed to Conformance or Tests.* The assignment items are met literally: the analysis is published, and the gunzip step is on the page. #117 box 5's "exact hashes, tool revisions" are given by SHA-256 (`:458-504`), and the tools reproduce when they are found. The defect is that the documentation cannot be located.
- *Required outcome.* The page states where each packet is published: branch `b5-review-evidence`, `review-evidence/b5-r1/{author,author-r2,author-r3}/`, at a pinned archive commit that contains all three (for example `227a6541` or a later one). It maps each lane label to its directory, so that steps 1 to 3 at `:449-456` can be followed from the page alone. No figure or table cell changes.
- *Verification.* At the corrected head, run `scripts/f1_repro.sh` against the archive commit that the page names, using only what the page gives. The tables stay byte-identical (`scripts/table_identity.py`), and the docs gates stay rc 0.

**S1 - SUGGESTION - Docs - `:28`, `:413-427`.** The body (`:243-248`) and the continuity row (`:25`) now say that the stall attribution does not cover the three skips of 72, 78 and 108 frames (258 frames). The final row's "the smaller skips are not attributed" and the Limits list leave them out: Limits names only the 237 off-stall skips of 2 to 59 frames as unattributed. One clause in each would make the unattributed set complete. Nothing on the page is wrong, so this is optional.

**S2 - SUGGESTION, retained from R424-1 S1 / R424-2 S4 - `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, `docs/findings/README.md` (#75 row).** The forward pointers to this page. They are outside the output the B5 assignment fixed, so adding them stays the manager's call.

## Round 2 findings and suggestions, resolved or retained at this head

| Finding | Status at cf38633a | Evidence |
|---|---|---|
| R424-2 F1 / R425-2 F1, the published read record does not match the cited hash | RESOLVED | `author-r2/receipts/a-long-reads.u16.gz` (blob `774d4f3d`, unchanged from `2a40015e` to `227a6541`) restores with the page's `gunzip -kf` to `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`, 131,540 bytes. The page's steps `:203-207` and `:446-456` then reproduce `attribution.txt` (`18ebbfc1…`) and `round3_figures.txt` (`9fa0f027…`) byte for byte. `gunzip -k` without `-f` fails with rc 2 while the masked copy is present, as the page says. The NOTE now says `-kf` (`2345dba7`). Negative control: the tool's hash pin refuses the masked copy. Receipts: `f1_reproduction.txt`, `archive_history.txt`. |
| R425-2 F2, the Direction B reason | RESOLVED | See the breakdown below. |
| R424-2 S1 / R425-2 S1, where the 1 ms steps fall | TAKEN | `:268-272`, `:429-431` state 22 of 121 against about 0.26 by chance, as an observation without attribution. I recomputed it independently: 22 of 121, 7 one-millisecond groups in 51,828 clear positions, giving 0.26. With each cluster's own test span instead of 16 reads it is 0.27, so "about 0.26" holds (`indep_figures.txt`). |
| R424-2 S2, the map reads | TAKEN | `:385-391`. My independent decode of `restore/peer-descs-2.jsonl` (`peer_walk.txt`) finds 57 exchanges. 20 are READ_DESCRIPTOR of type 0x0010 at indices 0..19, all NO_SUCH_DESCRIPTOR. There is no read of 0x0011, 0x0012, 0x0014 or 0x0017. Both stream ports have 0 static maps (16 clusters from 0, and 4 from 16), and AUDIO_UNIT 0 has 0 external ports, 0 internal ports and 0 routing elements. |
| R424-2 S3 / R425-2 S2, which skips "stall-aligned" covers | TAKEN | `:25`, `:238-250`, `:415-416` and the index row. Recomputed independently: 236 skips, 109,670 frames, with lags {1: 130, 2: 106}. The three not aligned are 72 frames at read 3390 (34.03 s), and 78 and 108 frames at reads 63168 and 63169 (634.03 and 634.04 s). Their longest intervals are 11.76, 12.11 and 12.11 ms, and the nearest stalls are 125, 127 and 128 reads away. The stall excess is 109,069.3 frames, and all 239 skips hold 109,928. |
| R425-2 S3, the planted control is linear | TAKEN | `:229-233`. Independently, recovered minus unplanted minus plant is 0 at 300 positions for each of 3 plants. |
| R424-2 S4: free-run rule, order criterion, zero-frame ordinals | TAKEN | `:36-38` cites `REGISTER_MAP.md` `0x8D4` (`:1849-1850`: "slip one sample every 1.958 s … the standing free-run rule, slips accepted"), and the anchor gate passes. `:126-128` and `:181` match `author/tools/grade_a.py:144-151` (mod 65,536; 32,768 or more is a backward step). `:283-287` match `author-r3/receipts/zero_frame_ordinals.txt`: skips at offsets -6 and +6, with each zero frame between consecutive ordinals. |
| R424-2 S4: forward pointers | RETAINED as S2 | Manager's call. |
| Round 1 findings (R424-1 F1, F2; R425-1 F1, F2, F3) | Still RESOLVED | Round 3 does not strengthen any attribution: the one-frame drops are still "by inference", and the 2 to 59 class is still "not separated". `:483-490` (controller revision) is unchanged. R425-1 F2's condition, re-derivation from published inputs, is now met from the public archive. R425-1 F3 closes with R425-2 F2. |

**R425-2 F2 breakdown.** The summary cell `:27` and the reason `:369-379` no longer say that the source is not visible over AEM, or that a known signal would need an instrument or wiring change. They now state:

- the lane rule;
- the four clusters on STREAM_PORT_OUTPUT 0, and that the dynamic map draws only from them;
- that no external port, internal port or routing element is declared, which matches my decode of AUDIO_UNIT 0;
- that each AUDIO_CLUSTER names its source in `signal_type`, `signal_index` and `signal_output` (IEEE 1722.1 7.2.16, as `avdecc/aem_descriptors.py:579-591` writes it);
- that those descriptors were not read because the walk is defective, so whether a known signal can reach the peer's talker channels without a wiring change is open.

NOT RUN is kept, and the Verdict cell is unchanged. The wording follows assignment item 1. The type codes cited at `:382-386` match `avdecc/aem_descriptors.py:103` (AUDIO_CLUSTER 0x0014, AUDIO_MAP 0x0017) and IEEE 1722.1 Table 7.1 (0x0010 is EXTERNAL_PORT_INPUT). The walk's external port reads as coded, 0x0011 and 0x0012, are each one too high.

## Lens results (each with the artifact examined at this head)

- `[R424] PASS Conformance - docs/findings/117_AUDIO_CONTINUITY.md:21-39, :238-275, :367-395, :413-456` - checked against:
  - #117 body box 4 and box 5, the B5 assignment 5925737609, and round 3 assignment 5927406852 F1 and items 1 to 5;
  - IEEE 1722.1 Table 7.1 and 7.2.16, through `avdecc/aem_descriptors.py:103,579-591`, and `author/restore/peer-descs-2.jsonl` (`peer_walk.txt`);
  - `docs/reference/REGISTER_MAP.md:1837-1850` and `docs/design/TIME_SYNC.md:463-480` for the beat.

  The row verdict is still "FAIL as measured", and no attribution is stated more strongly than before. The PR body says "Refs #117" with no closing keyword (`closingIssuesReferences` is empty).
- `[R424] PASS RTL - no RTL, constraint or firmware file in e4b771f9..cf38633a (git diff --stat)` - The RTL-facing claims hold:
  - The beat of 1.958 s gives 0.5107 per second, against `SLIP_TDM` at 0.511 per second (`:212-214`, `REGISTER_MAP.md:1849`).
  - 8,000 packets per second is 48 kHz over 6 frames (`:92`, `:251`).
  - The grader's step rule at `:125-128` is `grade_a.py:144-151`.
- `[R424] PASS Robustness - author-r2/receipts/a-long-reads.u16(.gz), a-long-reads.NOTE.md, scripts/f1_repro.sh, scripts/indep_figures.py` - checked:
  - The failure path of the restore: `gunzip -k` gives rc 2, and `-kf` gives rc 0.
  - The masked record is refused by the tool's hash pin, rc 1.
  - The alignment of the 236 skips does not depend on the window: the three unaligned skips are 125 or more reads from any stall.
  - Every stall is followed by exactly one skip of 240 frames or more.
  - The six zero-frame events are each a net one-frame loss, not a substitution.
- `[R424] PASS Tests - author-r2/tools/b5_attrib.py (f1d9b2ba…), author-r3/tools/b5_round3.py (415ef1b0…), scripts/indep_figures.py, scripts/table_identity.py` - The author's tools reproduce both published receipts from the public archive. My implementation, written independently in standard-library Python, re-derives every round 3 figure. The planted control is shown to be linear by construction, which is what the page now claims for it, and nothing more.
- Docs: UNCLEAN (R424-3-F1). Examined: the full page (504 lines), the `README.md` index row, the PR body, the three commit messages (one line each, no trailers), and the docs gates (`gates/summary.txt`, 17 commands, all rc 0 in the hash-pinned Markdown environment):
  - `docs_check.py`: 0 findings;
  - `check_em_dash.py --base e4b771f9`: 0 findings over 505 added lines;
  - `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --selftest/--verify-anchors/--check`, `check_feature_status.py` and its self-test, `check_archive.py`, `check_hygiene.py --check`, `ci_scope.py --selftest`;
  - `check_baremetal_only.py --check`: rc 0 on rerun, after the first attempt stopped with rc 2 because the environment lacked pyyaml;
  - `git diff --check` against both the base and the round 2 head.

  Also examined:
  - Table identity (`table_identity.txt`): 15 tables and 119 table lines at all three heads. Tables 2 to 15 are byte-identical to both round 2 and round 1. Table 1 differs from round 2 only in the Evidence cells of the continuity row and the Direction B row.
  - The public-text scan (`public_scan.txt`) of the page, the index row, the commit messages, the PR body, the round 3 issue comments, the `author-r3/` packet and the NOTE. It found no host, peer, switch, instrument or vendor name, no local path, address or interface, and no clock-topology term. All 24 hits are the word "wiring" in "without a wiring change" or "no … wiring … action". No capture channel number and no peer channel map is stated.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `117_AUDIO_CONTINUITY.md:21-39,238-275,367-395,413-456` against #117 box 4 and 5, assignments 5925737609 and 5927406852; `avdecc/aem_descriptors.py:103,579-591`; `author/restore/peer-descs-2.jsonl` (`peer_walk.txt`); `REGISTER_MAP.md:1837-1850`; PR body and closing references | R424-3 | `cf38633ad9a5bdb05517bedba73ce50965af967b` |
| RTL | CLEAN | Diff scope (docs only); beat, packet-rate and step-rule claims against `REGISTER_MAP.md:1849`, `TIME_SYNC.md:463-480`, `author/tools/grade_a.py:144-151` | R424-3 | `cf38633ad9a5bdb05517bedba73ce50965af967b` |
| Robustness | CLEAN | Restore failure and success paths, masked-record refusal, alignment margin, zero-frame events (`f1_reproduction.txt`, `indep_figures.txt`, `author-r3/receipts/zero_frame_ordinals.txt`) | R424-3 | `cf38633ad9a5bdb05517bedba73ce50965af967b` |
| Tests | CLEAN | `b5_attrib.py` and `b5_round3.py` run on the public archive; independent `scripts/indep_figures.py`; `scripts/table_identity.py`; `scripts/peer_walk.py` | R424-3 | `cf38633ad9a5bdb05517bedba73ce50965af967b` |
| Docs | UNCLEAN (R424-3-F1 open) | Full page, index row, PR body, commit messages; docs gates (`gates/`); `table_identity.txt`; `public_scan.txt`; sibling convention at `606_FIRST_BIND_MEASUREMENT.md:257,297`, `617_DIN_FRAME_COHERENCE_BENCH.md:276-277`, `451_USB_AUDIO_CAPTURE.md:217-218`, `117_GPTP_SILICON_EVIDENCE.md:652-654` | R424-3 | `cf38633ad9a5bdb05517bedba73ce50965af967b` |

## Real limits

- There was no bench access. The raw captures (the graded pair, `cap-ts.bin`, the full grades) are local to the lane and identified by hash only. I did not re-derive anything that needs them:
  - the derivation of the read record from `cap-ts.bin`;
  - the whole-run integrity counts;
  - `zero_frame_ordinals.txt`, which I checked only for internal consistency with the page and the event list.
- I decoded the descriptors by reading the IEEE 1722.1 field order (7.2.3, 7.2.13) from the published payloads. The peer's ENTITY descriptor is redacted in the archive and was not needed.
- The public-text scan uses a generic list of vendor, host, tool, clock-topology, wiring and local-information terms. It does not use the private redaction map, which I did not read. The scan script is kept out of the published manifest because its pattern list spells vendor names. Its output is published.
- Physical calibration is NOT RUN. Printed precision is not calibrated accuracy, and the field skips are not hardware proof.
- Hosted contexts at this head, read-only, at the time of this review:
  - `docs-check` was IN_PROGRESS;
  - `docs-check-no-git`, `wire-accountability`, `rtl-fast`, `changes`, `bdd-conformance`, `elaborate` and `full-ci-gate` had SUCCESS;
  - `verilator-suites`, `yosys-portability`, the shards, `verilator-lint`, `yosys-elaboration` and Physical gPTP were SKIPPED, not executed, as a docs-only PR emits them (`hosted_checks.txt`).
- I did not build the source bank or the current-dev candidate.
- Clone integrity after the probes:
  - HEAD and tree are as above, and the worktree and index equal HEAD;
  - `git ls-tree -r HEAD` equals `git ls-files -s` in mode, blob and path;
  - no untracked or ignored file is left, after I removed the `scripts/__pycache__/` that the gate run created;
  - the gitlinks are `external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `b2db3a97` and `third_party/verilog-axis` `48ff7a7e`.

## Pending manager duties

- Route R424-3-F1 to an executor. It is a single paragraph on the page that names the archive branch, the path and a pinned commit for the three packets. A re-check at the corrected head then covers Docs.
- S2 (the forward pointers) and the open decisions the PR lists: the read-only AUDIO_CLUSTER read with type 0x0014 for Direction B, a lossless capture path, and the peer's clock source.
- Hosted acceptance at the exact head, including `docs-check`, which was still in progress here, and the act replica.
- The final candidate merge against live dev `ea3fb38877842f223afea97e3bd72a10500455c9` from source base `e4b771f9`, and post-merge containment.
- The second independent review (R425-3), and maintainer authorization for any merge.

R424-3 FINISHED
