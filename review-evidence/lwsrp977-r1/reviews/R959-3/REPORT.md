[R959] POSITIVE - exact head 16b6c950ca320d29876d84c33460c2652650f16d

# R959-3: narrow re-review of kebag-logic/lwSRP PR #22 (for kebag-logic/milan-fpga#977)

- **Head:** `16b6c950ca320d29876d84c33460c2652650f16d`, tree `622309fdba8e09fdb334cf37f0e381e3a898b1bf` (branch `opt-exec-3`). GitHub reports the same PR head.
- **Base:** `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b` (`main`).
- **Delta judged:** `50a2106..16b6c95`. This is one commit, `16b6c95` ("Clarify option work and callback buffer length contracts"). It changes 4 files, with 9 lines added and 9 removed.
- **Scope:** my round-2 report, comment 7211848144. That covers finding R959-2-F1 and residues R959-2-R1 and R959-2-R2. I also check that the delta changes no behaviour.
- **Unchanged verdicts:** code the delta does not touch keeps its R959-2 lens verdict. Only comments and one guide changed, so nothing that verdict relied on has moved.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open at this head.

- **R959-2-F1 is closed.** The manager corrected `author-r2/receipts/INDEX.md` (milan-fpga `9d940063`). My round-2 verifier, unchanged, now reports "matching neither 0" and exits 0.
- **R959-2-R1 is closed.** `src/core/mrp_mad.c:1225` now carries the exact wording I asked for, including the issue ID.
- **R959-2-R2 is closed** for the four places it named: `mrp.h:202-203`, `mrp.h:213`, `integrator.md:121` and `integrator.md:125` now admit the buffer length. Two more copies of the narrow wording, which I missed in round 2, remain. They are recorded below as RESIDUE R959-3-R1.
- **No behaviour change:**
  - The three changed source files are byte-identical to `50a2106` once comments are stripped, and their line counts are unchanged.
  - With every option off, all 260 of 260 default objects are byte-identical to `main`'s.
  - With options on, all 160 of 160 objects are byte-identical to `50a2106`'s.
  - The author's options-off differential digests at this head equal their round-2 digests at `50a2106`.
- **Two RESIDUE items** (R959-3-R1, R959-3-R2) and some suggestions remain. None of them makes the verdict negative.

## Reconstruction and authorities

- **Rules:** `CONTRIBUTING.md` (this repository has no `AGENTS.md`). It sets the 25-word sentence limit, linked references, no generated assets, no private infrastructure, and one-line commit subjects without bodies or trailers.
- **Issue #977 scope:** I used the frozen acceptance and the manager's rulings as I reconstructed them in R959-2. Every option must leave transmitted behaviour unchanged, except for the one documented one-port difference. With options off, the build must be `main`'s.
- **Interface authority:** the `mrp_app_ops` contracts in `src/include/shish_lan/mrp.h`, the integrator guide's "Application callback contract", and the option comments.
- **Evidence:**
  - milan-fpga `98e1c6bdf778a6e26785f1cf8da592f0ffec6c1d`, `review-evidence/lwsrp977-r1/`: `author-r3/`, the corrected `author-r2/receipts/INDEX.md` and `MANIFEST.json`;
  - my own R959-2 scripts from that tree.
- **Reading order:**
  - I ran my own pass over the delta first.
  - Then I read my round-2 report, and after that the finding headers of the external review at `50a2106` (comment 7211628029, POSITIVE).
  - I did not open `author-r3/inputs/`, which holds fetched review texts, or any other reviewer's report directory.

## What I ran (receipts listed in MANIFEST.sha256)

| Probe | Receipt / script | Result |
| --- | --- | --- |
| F1 re-check: round-2 verifier on the corrected packet | `receipts/packet-verify-r2.txt`, `scripts/packet_verify.py` (unchanged from R959-2) | 78 of 78 author-r2 files match their published hashes; 34 are path-redacted. INDEX: 74 entries, all 74 equal to the manifest's original hashes, **matching neither 0**, rc 0 |
| Round-3 packet: files against `MANIFEST.json`, the author-r3 INDEX table against the manifest, git blob ids against the commit tree | `receipts/packet-verify-r3.txt`, `scripts/packet_verify_r3.py` | 572 of 572 author-r3 files match their published hashes; 14 are path-redacted. INDEX: 572 entries, 571 equal to the manifest's originals. The one other entry is `scripts/audit.py`, the scanner the manager withheld, as the INDEX note says. Every delivered file is indexed. 651 of 651 blob ids match the tree |
| Do the author's primary receipts bind their raw logs? | `receipts/author-r3-receipt-binding.txt` | Every raw-log hash in `units.json` and `docs.json` resolves to a delivered raw file, either directly or through the manifest's original hash for a path-redacted log. The other hashes are trace digests and object hashes, not files |
| Options-off differential, cross-head | same receipt | At this head, the default-configuration digests (timer and MAD drivers, profiles OFF and ON) are `b5b59e88`, `b5b59e88`, `4356b787` and `ac5935bd`. They equal the author's round-2 gate digests at `50a2106`. That is 800 of 800 identical and 9 of 9 options set to 0 |
| Default objects, `main` against head: all 10 `src/` sources, gcc and clang, 13 flag sets (-O0/-O1/-O2/-O3/-Os, Milan, -fPIC, -g compared after removing debug sections) | `receipts/objects-probe-main.log`, `scripts/objects_probe.sh` | 260 of 260 byte-identical, 0 build failures |
| Options-on objects, `50a2106` against head: scale, end-station, all options at -O0/-O2/-Os Milan, key only, -g with all options; gcc and clang | `receipts/objects-probe-opts-50a2106.log`, `scripts/objects_probe_opts.sh` | 160 of 160 byte-identical, 0 build failures |
| Sensitivity control for the options-on probe: `93d00cb` against head, gcc | `receipts/objects-probe-opts-control-93d00cb.log` | 73 of 80 identical. `mrp_mad.c` differs in all 7 sets the later `mrp_mad.c` changes reach, -g sets included. So the probe sees code changes |
| Comment-only check: the three changed sources at `50a2106` and head, with comments stripped (`gcc -fpreprocessed -dD -E -P`) | `receipts/delta-checks.txt` | Byte-identical for `mrp_mad.c`, `mrp.h` and `timer.h`. Line counts are unchanged (1958, 470, 89; `integrator.md` 457) |
| Commit metadata and added-line scan (my own pattern categories: lane, reviewer and author labels, round labels, IDs of 7 or more digits, host paths, tool and model names; `#L<n>` anchors removed first) | `receipts/delta-commit-and-scan.txt` | One commit, one subject, 0 body lines. 2,940 added lines (`main...head`) and 9 (`50a2106..head`), 0 matches in each. This agrees with the author's counts |
| Guide checks at head | `receipts/docs-checks.txt` | 1,289 sentences or fragments, 0 over the limit. 0 unlinked references. 79 self-test cases, 0 failures. 438 local links, 0 failures. External URLs were not requested |
| PR and hosted state, read only | `receipts/pr-state.txt` | The PR head is the exact head. 0 check runs, 0 statuses, 0 workflows |
| Restore check | `receipts/restore-check.txt` | HEAD and index tree are `622309fd`. 0 status lines, ignored files included. 74 of 74 blobs and modes match. 0 gitlinks, no `.gitmodules` |

My added-line scan uses its own literal pattern list, which names tool tokens. For the same reason the manager gave for the author's scanner, I do not publish that list. The categories are listed above.

## Round-2 findings at this head

| Finding | Status | Evidence |
| --- | --- | --- |
| R959-2-F1 (MINOR, Tests): INDEX hash for `added-lines-scan.txt` | **Closed** | The INDEX line now gives `f3a07ca0…`, the delivered file's hash. The appended manager note says the gate's original was `f152030f…`, and that only line 4 (the literal pattern list) was replaced before publication. The required verification passes: "matching neither 0", rc 0. See S2 for a remaining inconsistency in the manifest record |
| R959-2-R1 (RESIDUE, Docs): restore comment | **Closed** | `src/core/mrp_mad.c:1225` matches the exact fix word for word. The claim it makes, that the restore compiles as before with LWSRP_LEAN_COPY at 0, holds: 260 of 260 default objects equal `main`'s |
| R959-2-R2 (RESIDUE, Docs): callback contracts omit the buffer length | **Closed for the four named places; residue of the same cause carried as R959-3-R1** | `mrp.h:202-203` and `:213`, `integrator.md:121` and `:125` match the exact fixes. The code agrees. Both decode passes use the one call `mrp_pdu.c:218` with the same `alen`. Re-encoding after a move (`mrp_mad.c:1710`) passes the same `len` from `tx_vector_len`. The three codecs read `buf_len` only for length checks: `mvrp.c:48/66`, `mmrp.c:69/86/93`, `msrp.c:278-304/333-362`, where MSRP's decoder also requires an exact length |
| R959-2-S1: PR object claim narrower than the probe | **Closed** | The PR body now cites "All ten source files, two host compilers, thirteen flag sets" |
| R959-2-S2 to S5 | Retained (S3 to S6 below) | Not in the delta |

The delta also applies the external reviewer's wording residue R960-2-R1, the three "Reason:" sentences. That finding belongs to the external review. I judged the new lines only as part of this delta, against the code:
- `mrp_mad.c:27`: a lookup walks `*bucket_of(ps, key)` through `key_next` (`:592-612`).
- `timer.h:35`: a tick walks only `g_slot[g_now % LWSRP_TIMER_SLOTS]` (`timer.c:208-232`).
- `mrp_mad.c:112`: under LWSRP_LEAN_TX, `deliver_event` is skipped when the tx! row neither moves nor sends (`:1916-1922`). The walk over `ps->attrs` remains, which the new sentence no longer denies.

All three are accurate.

## Findings

### R959-3-R1 - RESIDUE - Docs

- **Artifact:**
  - `CHANGELOG.md:35`;
  - `src/core/mrp_pdu.c:23-24`.
- **Evidence:** R959-2-R2 widened the contracts in `mrp.h` and `doc/integrator.md` to admit the buffer length. Two other copies of the old, narrower wording remain. I missed them in round 2:
  - `CHANGELOG.md:35`: "so it must depend on its type and value only."
  - `mrp_pdu.c:23-24` (the LWSRP_LEAN_VALIDATE option comment): "decode_attr's result, the only thing that pass reads, depends on the wire octets alone."
  - The in-tree decoders also depend on `buf_len`; `msrp.c:347` requires `buf_len == len`. So both sentences are narrower than the contract they summarise.
- **Impact:** wording only. It changes no code, object, measurement or verdict. Each pass and each re-encode passes the same length.
- **Exact fix:**
  - `CHANGELOG.md:35`: "Under LWSRP_TX_MERGE, encode_attr may run again for a moved vector, so it must depend on its type, value and buffer length only."
  - `mrp_pdu.c:23-24`: "decode_attr's result, the only thing that pass reads, depends on the wire octets, their length, offset and type alone."
- **Verification:**
  - `grep -n "type and value only\|wire octets alone" CHANGELOG.md src/core/mrp_pdu.c` prints nothing.
  - The comment-stripped `mrp_pdu.c` is unchanged.
  - `check_sentences.py` still reports 0 over the limit.

### R959-3-R2 - RESIDUE - Docs (PR text)

- **Artifact:** the live PR #22 body, lines 67-68.
- **Evidence:**
  - The body says: "The local head is `16b6c95…`." It also says: "This draft has not been posted, and the local commit has not been pushed."
  - The body is now posted, and the commit is the published PR head (`receipts/pr-state.txt`).
- **Impact:** wording only. It is stale wording from the author's draft and changes no evidence claim.
- **Exact fix:**
  - Line 67: "The head is `16b6c950ca320d29876d84c33460c2652650f16d`. These checks ran at that head; every exit code was zero."
  - Line 68: delete it.
- **Verification:** the PR body no longer contains "local commit" or "has not been posted".

### Suggestions (not blocking)

- **S1:** the LWSRP_LEAN_TX reason sentence (`mrp_mad.c:112`) names only one of the option's two savings. The comment above it also describes the assembler skipping a word with no AttributeTypes left (`tx_assemble`, `:1797-1802`). Possible wording: "Reason: a send skips tx! delivery that changes nothing and AttributeType words that hold none."
- **S2 (manager, publication record):** `MANIFEST.json` lists `author-r2/receipts/added-lines-scan.txt` with `original_sha256` equal to `published_sha256` (`f3a07ca0…`) and `path_redacted: false`. The new INDEX note says the original was `f152030f…` and that line 4 was replaced. Recording that content redaction in the manifest would make the two integrity records agree. One way is an original hash of `f152030f…` or a content-redaction flag. Nothing at the head depends on it.
- **S3 (retained from R959-2-S2):** `tests/check_reversals.py:436` always passes `-DCMAKE_C_FLAGS=…`. With `--end-station OFF` that value is empty, so it replaces any `CFLAGS` from the environment. Pass the cache entry only when `--end-station ON`.
- **S4 (retained from R959-2-S3):** state that removing a timer from inside a tick callback is unsupported, or add a test for it.
- **S5 (retained from R959-2-S4):** the `tx_reverse` fallback for vectors longer than its buffer has no test.
- **S6 (retained from R959-2-S5):** next to the reading-decoder plant (`doc/tester.md:192-194`), name a sanitizer plant that removes the delivering pass's zeroing.

## Lens notes

- **Conformance:**
  - The delta changes no transmitted octet, state transition or indication. All 260 default objects are identical to `main`'s, and all 160 options-on objects are identical to `50a2106`'s.
  - The option comments' clause citations are unchanged.
  - The widened callback contracts are what the IEEE 802.1Q-2018 10.8.2.7 codecs need: a FirstValue's length is part of its encoding.
- **RTL (here: the C library and its build):**
  - No preprocessor-visible change: the stripped sources are identical and the line counts unchanged, so `__LINE__`-dependent output cannot move.
  - The `RX_KEPT` macro text is unchanged.
- **Robustness:**
  - The contracts now say what the callers rely on. Each validation and delivery pass and each re-encode passes the same length (`mrp_pdu.c:218`, `mrp_mad.c:1605/1627/1710`).
  - No new failure path.
- **Tests:**
  - F1 is closed, and the round-3 packet verifies (572 of 572 files, INDEX consistent apart from the withheld scanner).
  - The author's receipts bind their raw logs.
  - The options-off differential digests carry over unchanged from `50a2106`.
  - No mutation or sanitizer campaign was due for a comment-only delta.
  - Untouched test code keeps its R959-2 verdict, which F1 alone had kept unclean.
- **Docs:**
  - R1 and R2 are applied word for word.
  - The guide checks pass, and all anchors and line counts hold.
  - No added line carries a lane, round, reviewer or comment label.
  - Residue R959-3-R1 and R959-3-R2 are carried.

## Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | delta against the `mrp_app_ops` contracts and 10.8.2.7; 260/260 default objects against `main`; 160/160 options-on objects against `50a2106`; author-r3 differential digests against author-r2's | R959-3 (delta); R959-2 and R959-1 for untouched code | `16b6c950ca320d29876d84c33460c2652650f16d` |
| RTL (C library and build) | CLEAN | comment-stripped `mrp_mad.c`, `mrp.h`, `timer.h` against `50a2106`; line counts; gcc and clang objects in 21 flag/option sets; sensitivity control | R959-3; R959-2 for untouched code | `16b6c950ca320d29876d84c33460c2652650f16d` |
| Robustness | CLEAN | `mrp.h:199-221` contracts against `mrp_pdu.c:218`, `mrp_mad.c:1596-1632/1710`, and the `buf_len` checks in `mvrp.c`, `mmrp.c`, `msrp.c` | R959-3; R959-2 for untouched code | `16b6c950ca320d29876d84c33460c2652650f16d` |
| Tests | CLEAN (R959-2-F1 closed) | corrected author-r2 INDEX and manager note; author-r3 packet, INDEX, manifest and blob ids; `units.json`, `docs.json`, `differential.json`, `objects.json` and their raw logs | R959-3; R959-2 for test code | `16b6c950ca320d29876d84c33460c2652650f16d` |
| Docs | CLEAN (residue R959-3-R1 and R959-3-R2 carried) | `doc/integrator.md:117-127`, `mrp.h` contracts, the four new comment lines, `CHANGELOG.md:33-36`, `mrp_pdu.c:21-31`, live PR body; guide checks; added-line scan | R959-3 | `16b6c950ca320d29876d84c33460c2652650f16d` |

## Limits

- **Execution at this head:** I compiled objects, ran the guide checks, and verified the packet and receipts. I did not rerun the unit builds, reversals, differential, MemorySanitizer, scenarios, equivalence or RV32I checks here. Those rest on:
  - the author-r3 receipts, which verify against the manifest;
  - identical objects and stripped sources across the delta;
  - for campaigns not repeated this round, the author-r2 receipts and my R959-2 reruns at `50a2106`.
- **Scanner:** the author's scanner (`author-r3/scripts/audit.py`) is withheld. Its zero-match result is reproduced only by my own scan with my own pattern list, which I also do not publish.
- **External links:** checked with `--local-only`; external URLs were not requested.
- **Hosted evidence:** lwSRP has no hosted workflow, and GitHub reports 0 check runs and 0 statuses at the head. Every source-head gate is author-run.
- **Manager source bank:** none was run at this head, and I claim none.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base `d1bb4f4e`, live dev `e275d795`) with the builder and native banks, and link the receipts on the PR.
- Merge so that `main`'s history does not carry the bytecode blob added in `cce36b5`, by squash or a rebuilt branch. Then confirm that `git log --format=%H -- tests/__pycache__` on `main` shows no adding commit.
- Hosted and act acceptance.
- Carry R959-3-R1 and R959-3-R2 to the residue checklist. R959-3-R2 is a PR-body edit the manager can make when publishing.
- Consider S2 (record the scan receipt's content redaction in `MANIFEST.json`).

R959-3 FINISHED
