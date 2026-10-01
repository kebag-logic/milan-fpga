[A474] REVIEW READY

Round 3 for PR #628 (bench lane B5, #117 acceptance box 4, the audio continuity row), under the [A10] round 3 assignment (https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852). It answers R424-2 and R425-2. Docs only, with no bench access. Refs #117.

Commit: `cf38633ad9a5bdb05517bedba73ce50965af967b`
Branch: `b5-bench-1001`, parent `e29d12b1d5ee858eaf4684aaa8dc6647f6309857`, base dev `e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`. One new commit, local only: not pushed, and the PR is not edited.
Changed: `docs/findings/117_AUDIO_CONTINUITY.md` (+93 -35) and its row in `docs/findings/README.md`. No other file.

**F1, the published read record.** The page gives the reproduction steps at `:203-207` and `:446-456`: `gunzip -kf a-long-reads.u16.gz`, check the SHA-256, then run `b5_attrib.py figures`.
- From the public archive alone (`b5-review-evidence@2a40015e`), `gunzip -kf` restores SHA-256 `2183d57f…`, and the published `b5_attrib.py` reproduces the published `attribution.txt` byte for byte.
- The `-f` is needed. The masked `a-long-reads.u16` still sits beside the `.gz`, and the archive note's `gunzip -k` refuses to overwrite it (rc 2, the masked copy kept). The note or the masked copy is the manager's to change.

**1. Direction B reason (R425-2 F2)** at `:27` and `:369-379`.
- "Not visible over AEM" and "would therefore need an instrument or wiring change" are gone.
- The page states the lane rule and what was observed. It adds that each AUDIO_CLUSTER descriptor names its cluster's signal source (`signal_type`, `signal_index`, `signal_output`, IEEE 1722.1 7.2.16), and that those descriptors were not read because the survey walk is defective.
- So whether a known signal can reach the peer's talker channels without a wiring change was not established. NOT RUN stays.

**2. What the walk sent (R424-2 S2)** at `:381-391`. It sent 20 reads of type 0x0010 at indices 0 to 19, each NO_SUCH_DESCRIPTOR. It sent no map read, because both stream ports declare 0 static maps, and no external port read. The dynamic maps came from GET_AUDIO_MAP. The tally of all 57 exchanges is in the round 3 receipt.

**3. Which skips "stall-aligned" covers (R424-2 S3, R425-2 S2)** at `:25`, `:238-250`, `:415-416` and the index row.
- 236 of the 239 skips of 60 frames or more are stall-aligned, 109,670 frames. The stall excess, 109,069 frames, is compared with those, and all 239 hold 109,928.
- The other three are named: 72 frames at 34.0 s into the window, and 78 and 108 frames on consecutive reads at 634.0 s. They are not stall-aligned, and the stall attribution does not cover them.

**4. The 1 ms steps (R424-2 S1, R425-2 S1)** at `:268-272` and `:430-431`, as an observation without attribution. 22 of the 121 off-stall clusters step by 1 ms, against about 0.26 by chance: 7 such steps over 51,828 clear positions, about 3,240 windows of the floor test's 16 reads.

**5. Suggestions.**
- R425-2 S3, taken (`:231-233`): the planted control is linear by construction. A plant reads back as the floor's own step plus the plant, with a largest difference of 0.00 frames, so the control checks where the floor windows sit, not power.
- R424-2 S4, taken where cheap:
  - the free-run acceptance rule, citing the register map's slip counters (`:36-39`);
  - "in order" as 0 backward steps (`:126-128`, `:181`);
  - the ordinals around the six skip, zero, skip events (`:283-287`). They are read from the local graded pair: each zero frame sits between consecutive ordinals, so each event is one frame fewer.
- Retained: the forward pointers from the #117 ledger and the #75 index row. Those are other pages' rows, outside the output the B5 assignment fixed, so they stay the manager's call.

**Tables.** 14 of the page's 15 tables are byte-identical to `e29d12b1`, with 119 table lines at both heads. Every table after the summary verdict table is also byte-identical to round 1's `bf9e5d82`. The summary verdict table changes only the Evidence cells of the continuity row (item 3) and the Direction B row (item 1). Their Item and Verdict cells are unchanged, and no old figure is dropped. The proof gives SHA-256 per table and literal `diff`s.

**Public text.** A label-only scan covered the packet, the added lines and commit messages of `e29d12b1..cf38633a` and of `e4b771f9..cf38633a`. It used the private redaction map, MAC and home-directory patterns, and a private list of channel numbers, clock-topology words, tool names and account and host names. It found 0 hits.

Validation, all rc 0 at `cf38633a` from the physical lane path, none piped:
- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base e4b771f9` (0 findings over 505 added lines) and `check_doc_paths.py`, in the pinned Markdown environment;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `scripts/check_feature_status.py --self-test`;
- `git diff --check`, `git diff --check e4b771f9 HEAD` and `git diff --check e29d12b1 HEAD`;
- `gen_toc.py --verify-anchors`.

Acceptance criteria (the assignment's F1 step and items 1 to 5): met, with the evidence above. Round 3 packet `b5-a474` holds:
- `b5_round3.py` (`415ef1b0…`);
- the round 3 figures, zero-frame ordinals and F1 reproduction receipts;
- the table proof, the scan and the gate outputs;
- `HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256`.

The raw files stay local.

Open risks/questions:
- Direction B is open. A read-only AUDIO_CLUSTER read with type 0x0014 would show each cluster's named source. That needs a decision.
- The three unaligned skips and the 1 ms steps' concentration are stated, not attributed.
- The archive note's `gunzip -k` fails while the masked copy is present (manager).
