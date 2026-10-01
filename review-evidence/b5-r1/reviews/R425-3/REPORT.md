[R425] NEGATIVE - exact head cf38633ad9a5bdb05517bedba73ce50965af967b

Round R425-3, external independent review of PR #628 (issue #117, bench lane B5, audio continuity row of acceptance box 4). Tree `150f848bdb9c85bf6bd0b005bce4579724ed6aa8`, source base `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`, round-3 commit `cf38633a` on the round-2 head `e29d12b1`. Evidence read: `b5-review-evidence` at `227a6541159dddb237c1d3cec7dc71fbf4063f31` (it contains `ef3a7091`, `2a40015e` and `2345dba7`), author packets `author/`, `author-r2/` and `author-r3/` only.

The page itself holds up at this head. Every round-3 claim I checked reproduces from the public archive, the tables are unchanged where the assignment requires them to be, and the docs gates pass. The verdict is NEGATIVE because of one MINOR finding: the public round-1 evidence packet still exposes a capture channel map, the link type, an interface name and a product family. That breaks the public-text rule the lane is held to. The fix belongs to the manager's archive; nothing in the PR's tree needs to change.

## Findings

### R425-3 F1: MINOR (Conformance, Docs). The public evidence packet exposes a capture channel map, a link type, an interface name and a product family

- **Where.** All in `review-evidence/b5-r1/author/` on `b5-review-evidence`. These files have been unchanged since `ef3a7091` and are still present at the tip `227a6541`.
  - `restore/host-start.txt:13` and `restore/host-end.txt:11`: one network interface name is left in clear. The other interfaces in the same listing are masked as `<host-iface>`.
  - `restore/host-start.txt:1-6` and `restore/host-end.txt:1-6`:
    - the bench host's audio-device list, with the bus positions of the external capture and the SoC board;
    - the SoC board's USB function product string, which names the SoC product family.
  - `HANDOFF.md:24`, `:40`, `:46-47`, `:94` and `:99`, `tools/run_a.py:17` and `:61`, `tools/grade_a.py:65`, and `summary/a-long/summary.json:75` and `:84` (`channel_identification`):
    - the external capture's channel count;
    - which capture channels carry the reference peer's output;
    - the physical digital link type of that connection.
  - `HANDOFF.md:24` also states the peer's dynamic channel map.
  - `redaction.json` records that the capture's identity was deliberately masked in these same files. The channel and link facts next to it were not.
- **Authority.**
  - The round 2 assignment (#117 comment 5926598386): "Public text names no host, peer, switch or instrument, and states no wiring, channel map or clock topology". The round 3 assignment (#117 comment 5927406852) keeps the same constraints.
  - The B5 assignment (#117 comment 5925737609): "states no wiring or clock topology: at most 'the reference peer' and 'an external audio capture'".
  - CONTRIBUTING.md section 6: equipment is named by role, never by vendor or product, and no interface names.
  - The lane's own round-2 and round-3 scans treat channel numbers as private. They cover only the round-2 and round-3 packets, not this round-1 packet.
- **How found.** A label-only scan over the PR body, the commit messages, the added lines, the lane comments and all three author packets: `receipts/public_scan.txt`, using `scripts/public_scan.py` with a token list kept outside the packet. Every hit was then read by hand.
  - The page, the index row, the PR body and the commit messages carry none of these classes.
  - The page's own terms (the SoC board, its McASP0, the USB capture path) are already established in `docs/findings/451_TDM8_FIRST_LIGHT.md` and `docs/findings/451_USB_AUDIO_CAPTURE.md`. The same holds for the DUT board name in the console identity, and for generic OS audio utilities in the SoC logs. I accepted all of these.
- **Impact.** The capture's channel layout, the link type and the bus positions identify the bench equipment and its wiring. The lane's redaction was written to hide exactly this. A reader of the public archive can recover what the page was written to withhold.
- **Required outcome.** Either:
  - the public evidence no longer states these items. They are masked by label, the same way the capture identity already is, and the archive manifest is updated. Whether to rewrite the evidence branch history is the manager's decision; or
  - a recorded owner or manager decision states that capture channel indices, the link type, bus positions, the SoC product family and that interface name are allowed in public evidence.

  The page needs no change.
- **Verification.** Rerun `scripts/public_scan.py` over the republished archive tip and check that the `capture-channel-index`, `capture-channel-count`, `link-type-a`, `interface-name` and `soc-product` classes show 0 hits. Also check that `summary.json`'s per-channel identification is masked. Or cite the decision.

### R425-3 S1: SUGGESTION (Conformance, Docs). What an AUDIO_CLUSTER read would show

- **Where.** `docs/findings/117_AUDIO_CONTINUITY.md:374-378`.
- **What is wrong.** The page says "Each AUDIO_CLUSTER descriptor names its cluster's signal source". The repository's own encoding of IEEE 1722.1 7.2.16 does not always name a physical source:
  - it writes `signal_type` INVALID for an input-port cluster;
  - it writes AUDIO_UNIT for an output-port cluster (`avdecc/aem_descriptors.py:590`).
- **Effect.** A peer that follows the same convention would answer the proposed read with the audio unit itself. That read would not settle the Direction B question either.
- **Why not higher.** The page's conclusion ("open", NOT RUN) is correct as written, and the PR body's open item only says the read "would show the source each cluster names". So this is optional.
- **Suggested change.** Qualify that sentence, or the open item, when it is next touched.

### R425-3 S2: SUGGESTION (Docs). How the p95 is computed

- **Where.** `docs/findings/117_AUDIO_CONTINUITY.md:312`.
- **What is unstated.** The restart p95 of 0.0389 s is the nearest-rank 95th percentile of the 30 cycles. Linear interpolation over the same 30 rows gives 0.0344 s (`receipts/table_check.txt`). The table does not say which rule it uses.
- **Why only a suggestion.** The table is byte-identical to round 1, so this is optional. Naming the rule would make the figure reproducible from the page alone.

## Round-3 items, judged at this head

- **R425-2 F1 (the read record) is resolved.** It was tested from the public archive alone, with `scripts/f1_repro.sh` (receipt: `receipts/f1_repro.txt`).
  - The published `.gz` is `6e0028a6...`. The page's `gunzip -kf` (`:206`, `:449`) restores `a-long-reads.u16` at 131,540 bytes, sha256 `2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`.
  - Plain `gunzip -k` refuses with rc 2 and leaves the masked copy (`8897abce...`) in place, which is why the page and the corrected NOTE say `-kf`.
  - The NOTE now reads `gunzip -kf` (`2345dba7`).
  - `b5_attrib.py figures author receipts` reproduces `author-r2/receipts/attribution.txt` byte for byte (`18ebbfc1...`). `b5_round3.py figures` reproduces `author-r3/receipts/round3_figures.txt` byte for byte (`9fa0f027...`). Steps 1-3 at `:446-456` work as written.
  - Negative control: running `b5_attrib.py` over the masked record is refused (rc 1).
- **R425-2 F2 (the Direction B reason) is resolved.** At `:27` and `:369-379` the page now says that the descriptors naming each cluster's source were not read, because the walk is defective, so the question is open. NOT RUN is kept. I checked the facts it rests on myself, with `scripts/audio_unit_check.py` over `author/restore/peer-descs-2.jsonl` (receipt: `receipts/audio_unit_check.txt`):
  - AUDIO_UNIT 0 declares 0 external ports, 0 internal ports, 0 controls, 0 selectors, 0 mixers, 0 matrices, 0 splitters, 0 combiners, 0 demultiplexers, 0 multiplexers, 0 transcoders and 0 control blocks.
  - STREAM_PORT_INPUT 0 has 16 clusters at 0. STREAM_PORT_OUTPUT 0 has 4 clusters at 16. Both have 0 static maps.
- **The walk text (`:381-391`) is correct.**
  - `author/tools/b5_ctl.py:153`, `:160` and `:162` read clusters as 0x0010, maps as 0x0014 and external ports as 0x0011/0x0012. Against `avdecc/aem_descriptors.py:99-103` (AUDIO_CLUSTER 0x0014, AUDIO_MAP 0x0017), the external-port codes are each one too high.
  - The record shows 57 exchanges: 20 READ_DESCRIPTOR of type 0x0010 at indices 0 to 19, every one NO_SUCH_DESCRIPTOR; no read of 0x0011, 0x0012, 0x0014 or 0x0017; and two GET_AUDIO_MAP.
- **"236 of 239" is stated everywhere it applies:** `:25`, `:238-250`, `:415-416` and the index row.
  - The three other skips are 72 frames at 34.0 s, and 78 and 108 frames on consecutive reads at 634.0 s, 258 frames in all. Their nearest stalls are 125, 127 and 128 reads away.
  - The 236 hold 109,670 frames, against a stall excess of 109,069.3. All 239 hold 109,928 = 106,754 (220 skips of 240 frames or more) + 2,916 (16 aligned skips of 60 to 239) + 258.
  - All of this matches `round3_figures.txt` A and `attribution.txt`.
- **The 1 ms concentration (`:268-272`, `:428-431`) is stated as an observation only.** 22 of the 121 off-stall clusters, against 7 / (51,828 / 16) x 121 = 0.26 by chance.
- **The planted control is now described as "linear by construction" (`:230-233`).** `round3_figures.txt` C shows a largest difference of 0.00 frames.
- **The R424-2 S4 items are taken.**
  - The free-run rule is cited (`:36-39`). The anchor exists at `docs/reference/REGISTER_MAP.md:203`, and `:132` carries the rule's text.
  - "In order" is defined as 0 backward steps (`:126-128`, `:181`).
  - The zero-frame ordinals (`:283-287`) match `author-r3/receipts/zero_frame_ordinals.txt`: 6 events, each with one-frame skips at offsets -6 and +6 and consecutive ordinals across the zero frame.
- **Tables are as required** (`scripts/table_check.py`, receipt: `receipts/table_check.txt`).
  - There are 15 tables and 119 table lines at `bf9e5d82`, `e29d12b1` and `cf38633a`.
  - Tables 1-14 are byte-identical to round 2 and to round 1.
  - Table 0 (the summary verdict table) changes only cell 2 (Evidence) of the continuity row and of the Direction B row. The Item and Verdict cells are unchanged.
- **The PR is scoped correctly.** The body says `Refs #117`, and the body and the three commit messages carry no closing keyword. The PR changes exactly two files, `docs/findings/117_AUDIO_CONTINUITY.md` and `docs/findings/README.md`. The commits are one line each with no trailers.
- **The docs gates pass at the exact head:** rc 0 for each of the following (`scripts/run_gates.sh`, receipts: `receipts/gates/`). The pinned Markdown lock (cmarkgfm 2025.10.22, html5lib 1.1) was installed with hashes in a disposable environment. The working tree was clean afterwards.
  - `docs_check.py`: 0 findings over 182 pages.
  - `check_doc_style.py`.
  - `gen_toc.py --check` and `--verify-anchors`: 283 links.
  - `check_em_dash.py --base e4b771f9`: 0 findings over 505 added lines; `--selftest` also passes.
  - `check_doc_paths.py`: 861 paths.
  - `ci_scope.py --selftest`.
  - `check_baremetal_only.py --check`.
  - `check_feature_status.py --self-test`: 46/46 and 0 findings.
  - `git diff --check` against the base and against `e29d12b1`.

## Lens results

```text
[R425] PASS RTL - git diff --stat e4b771f9..cf38633a (docs/findings/117_AUDIO_CONTINUITY.md, docs/findings/README.md only); page :56-69 identity table - no HDL, firmware, build or configuration artifact in scope; image identity values unchanged from rounds 1-2 (table 1 byte-identical), so no RTL contract, CDC, width or FSM claim is made or altered
[R425] PASS Robustness - page :199-300, :321-331, :413-436 against author-r2/receipts/attribution.txt, author-r3/receipts/round3_figures.txt, zero_frame_ordinals.txt, summary.json - edge handling checked: zero frames between consecutive ordinals, losses hidden inside lost stretches (4 beats, 1 slip), the cycle-20 stall bound, the non-aligned skips excluded from the stall attribution, the hash-pinned and assert-guarded tools refusing a masked or inconsistent record (receipts/f1_repro.txt, receipts/mutation_probes.txt)
[R425] PASS Tests - author-r2/tools/b5_attrib.py, author-r3/tools/b5_round3.py at the archive tip - both reproduce their receipts byte for byte; the masked record is refused; mutation probes move the figures the page relies on: one stall flattened gives stalls 220->219 and aligned 236->235 / unaligned 3->4; a planted 1 ms read delay moves the off-stall 1 ms count 22->21 (receipts/mutation_probes.txt); restart, skip-size and per-second figures recomputed from the page table and summary.json (receipts/table_check.txt)
```

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #117 body and the B5 round 1-3 assignments; the page `:15-39`, `:367-391` against `avdecc/aem_descriptors.py:99-103`, `:579-591`, `b5_ctl.py:130-162`, `peer-descs-2.jsonl`; the public-text rule against the archive | R425-3 | cf38633ad9a5bdb05517bedba73ce50965af967b |
| RTL | CLEAN | the diff's file set (two Markdown files); identity table byte-identical | R425-3 | cf38633ad9a5bdb05517bedba73ce50965af967b |
| Robustness | CLEAN | the page `:199-300`, `:321-331`, `:413-436`; round 2-3 receipts; hash pins and asserts in both tools | R425-3 | cf38633ad9a5bdb05517bedba73ce50965af967b |
| Tests | CLEAN | `b5_attrib.py`, `b5_round3.py` reproduction, negative control and three mutation probes; recomputed tables | R425-3 | cf38633ad9a5bdb05517bedba73ce50965af967b |
| Docs | UNCLEAN (F1) | the page, the index row, the PR body, the commit messages, author packets 1-3, the docs gates | R425-3 | cf38633ad9a5bdb05517bedba73ce50965af967b |

## Limits

- I did not read the IEEE 1722.1 text itself. Its clause and table numbers were checked against the repository's own encoding (`avdecc/aem_descriptors.py`), which is what the page cites.
- The raw captures (the graded pair, the read times) are not public. Their hashes and every figure derived from them rest on the published derived record and receipts. The ordinals around the zero frames were read by the author from the local graded pair and are not reproducible from public data.
- Physical calibration was NOT RUN. The bench host's clock is uncalibrated, and field skips are not hardware proof. I made no bench access.
- My public-text scan uses a finite token list. A clean result covers those classes only.
- Hosted checks at the exact head, read once, as information only:
  - executed and successful: `changes`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `full-ci-gate`, `rtl-fast`, `wire-accountability`;
  - skipped contexts: `verilator-suites`, `yosys-portability`, `verilator-lint`, `yosys-elaboration`, the shards and the physical gPTP job;
  - `docs-check` was still in progress when read (`receipts/hosted_checks.tsv`).

## Prior public findings

I read these only after the verdict and ledger above were written. Each is judged again at `cf38633a`.

| Finding | Status at cf38633a | Evidence at this head |
|---|---|---|
| R425-1 F1, R424-1 F1 (MINOR): attributions stated beyond the evidence | Resolved | `:25`, `:28`, `:238-298`, `:419-427` and the index row state each cause only as strongly as the receipts carry it: stall-aligned (236 of 239), not separated, by inference |
| R425-1 F2 (MINOR): figures not reproducible | Resolved | `receipts/f1_repro.txt`: both tools reproduce their published receipts from the public archive alone |
| R425-1 F3 (MINOR): Direction B reason beyond the evidence | Resolved | Superseded by R425-2 F2, resolved below |
| R424-1 F2 (MINOR): controller tool revision | Resolved | `:483-490` says the revision cannot be established and rests the binding record on the logged exchanges |
| R425-2 F1, R424-2 F1 (MINOR): published read record not the hashed one | Resolved | `.gz` restores `2183d57f...`; NOTE corrected to `-kf` (`2345dba7`); page steps `:446-456` reproduce |
| R425-2 F2 (MINOR): Direction B reason asserts an AEM fact not read | Resolved | `:27`, `:369-379`; the facts re-derived in `receipts/audio_unit_check.txt` |
| R425-2 S1, R424-2 S1: where the 1 ms steps fall | Taken | `:268-272`, `:428-431` |
| R425-2 S2, R424-2 S3: what "stall-aligned" covers | Taken | `:25`, `:238-250`, `:415-416`, index row |
| R425-2 S3: planted control is linear | Taken | `:230-233` |
| R424-2 S2: what the walk sent | Taken | `:381-391` |
| R424-2 S4 (R424-1 S2, S3): free-run rule, order criterion, zero-frame ordinals | Taken | `:36-39`, `:126-128`, `:181`, `:283-287` |
| R424-2 S4 (R424-1 S1): forward pointers from the #117 ledger and the #75 index row | Retained by the author as the manager's call | A SUGGESTION. It affects no lens. |

None of the prior rounds raised R425-3 F1. R424-1 recorded the capture channel identity as redacted in the packet. In `redaction.json` the capture's name is redacted, but its channel indices are not (F1 above).

## Pending manager duties

- R425-3 F1: redact and republish the round-1 packet's channel, link, bus, interface and product items, or record the decision that allows them.
- Hosted acceptance at the exact head. `docs-check` was still in progress at my last read.
- The candidate merge result against live `dev` (`ea3fb38877842f223afea97e3bd72a10500455c9`), built at the merge turn. This round validated the source head only.
- The second independent review, and a merge only with explicit maintainer authorization.

R425-3 FINISHED
