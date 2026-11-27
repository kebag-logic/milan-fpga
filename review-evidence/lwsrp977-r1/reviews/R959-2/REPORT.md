[R959] NEGATIVE - exact head 50a2106483141fcd7d1b20654bcf0803e7c3020a

# R959-2: independent re-review of kebag-logic/lwSRP PR #22 (for kebag-logic/milan-fpga#977)

- **Head:** `50a2106483141fcd7d1b20654bcf0803e7c3020a`, tree `74f0d3e54480d8c841c66d0958a2b3a9fe20d789` (branch `opt-exec-3`).
- **Base:** `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b` (`main`).
- **Delta judged:** `73007b48..50a2106`, ten commits `7b5e821`..`50a2106`. Code the delta does not touch keeps its round-1 lens verdict.
- **Round-1 reports resolved below:** the internal review (comment 7210816023) and the external review (comment 7210817308).

## Verdict

The head is sound.

- Every round-1 finding of both reports is closed at its cause (table below). I verified each closure myself.
- The one source change with every option off is `src/core/mrp_mad.c:1219-1226`. The default arm now copies `sizeof(previous_value)` through `RX_KEPT`, with no local.
- With every option off, the library's objects are byte-identical to `main`'s. That holds for 260 of 260 objects: all 10 sources under `src/`, gcc and clang, 13 flag sets. The flag sets include -O0, -O1, -O3, and -g after stripping debug sections. It also holds for 28 of 28 compile-only RV32I objects.
- A control run of the same probe against `73007b48` finds the four -O0 `mrp_mad.o` differences that round 1 reported. So the probe is sensitive, and the fix closed the gap.
- Options-off behaviour is therefore `main`'s.

**Why the verdict is NEGATIVE:** one MINOR finding is open, R959-2-F1. It is in the author's published evidence packet, not in the lwSRP head. One receipt's hash in `author-r2/receipts/INDEX.md` does not match the published receipt. Closing it needs no source change. There are also two RESIDUE items and some suggestions.

## Reconstruction and authorities

- **Rules:** `CONTRIBUTING.md`, which covers coding rules, the 25-word sentence limit, links, no generated assets, no private infrastructure, and one-line commit subjects. This repository has no `AGENTS.md`.
- **Guides:** `README.md`, `doc/{architecture,developer,integrator,manager,tester}.md`, `doc/tools/README.md`.
- **Issue #977:** I read the body, its acceptance (ruling of 2026-11-22) and the manager's rulings:
  - 2026-11-23: the option-(a) rate, the bound, round 2 and round 3 scope;
  - 2026-11-25: the owner's option (b), ceiling 0.76;
  - 2026-11-26: the round-5 ruling;
  - 2026-11-27: the round-7 decision and the PR #993 population ruling.
- **For this PR, those rulings mean:**
  - lwSRP may carry the buckets, the one-port MAP work and no validation zeroing;
  - the refused-allocation difference must be documented;
  - every option must leave transmitted behaviour unchanged except that one documented difference.
- **Interface authorities:** `src/include/shish_lan/mrp.h` (the `mrp_app_ops` contracts), `src/ports/timer.h`, and the IEEE 802.1Q-2018 and Milan v1.2 clauses that the option comments cite.
- **Evidence:** the published packet `review-evidence/lwsrp977-r1/author-r2` at milan-fpga `16162ec2b6c26d1d2ba3e3f0e2d4568a4d462694`, plus that commit's `MANIFEST.json`.
- **Order of reading:** I did my own pass over the delta first, then read the two round-1 reports. I did not open the packet's `reviews/` directory.

## What I ran (receipts in MANIFEST.sha256; host paths shown as `$PACKET` and `$CLONE`)

| Probe | Receipt | Result |
| --- | --- | --- |
| Packet integrity: every blob's git id checked against the commit tree; every file against `MANIFEST.json`; the author's INDEX against the manifest's originals | `receipts/packet-verify.txt`, `scripts/packet_verify.py` | 78 of 78 files match their published hashes; 34 are path-redacted by design. 73 of 74 INDEX entries match the manifest's original hashes. 1 matches neither: R959-2-F1 |
| Default objects, `main` against head, all 10 `src/` sources, gcc and clang; -O0/-O1/-O2/-O3/-Os, `-DLWSRP_MILAN=1`, `-fPIC`; `-g` builds compared after `objcopy --strip-debug` | `receipts/objects-probe.log`, `scripts/objects_probe.sh` | 260 of 260 byte-identical, 0 build failures |
| The same probe, `main` against `73007b48` (control) | `receipts/objects-probe-control-73007b48.log` | 126 of 130: `mrp_mad.c` differs at -O0, -O0 Milan, -O0 -fPIC and -g -O0, as round 1 found |
| RV32I compile only: clang `--target=riscv32-unknown-elf -march=rv32i -mabi=ilp32 -ffreestanding`, a stub `<string.h>`, the 7 freestanding sources, `-Wall -Wextra -Wpedantic -Werror` | `receipts/rv32-probe.log`, `scripts/rv32_probe.sh` | Default objects 28 of 28 identical to `main`'s (-O0/-O2/-Os/-Os Milan). The scale set, the end-station set, both, and both with Milan each compile 7 of 7 |
| Unit builds (my own cgreen 1.6.3 prefix): default OFF and ON; scale + end-station OFF and ON; end-station without scale OFF; `LWSRP_ONE_PORT_MAP` alone OFF; `LWSRP_LEAN_TX` alone ON | `receipts/runs/unit-*.log`, `scripts/spot_runs.sh` | All rc 0. Assertion counts 27,348 / 27,336 (default and each single switch), 27,376 / 27,364 (scale + end-station). These match the README, the tester guide and the PR |
| Reversals, `--scale ON --end-station ON` (OFF profile) and `--end-station ON --milan ON` | `receipts/runs/rev-es-*.log`, `*.summary.json` | 118 listed. 8 selected, run and killed, 110 skipped; and 4 selected, run and killed, 114 skipped. 0 failures. Every unselected case prints a SKIP line |
| Differential, both profiles, default 200 seeds (no MemorySanitizer) | `receipts/runs/diff-OFF.log`, `diff-ON.log` | 2 drivers, 22 builds, 38 of 38 mutants killed, 0 problems. `lean-tx-word-ends-scan` and `-alone` are killed at seed 3. The one-port and end-station rows show 177 of 200 identical and 23 counted, as the guide states. The OFF-profile end-station digest equals the author's receipt |
| Guide anchors: each `#L<n>` link at head against the line the same link named at `73007b48` | `receipts/anchors-probe.log`, `scripts/anchors_probe.py` | 45 anchors, 0 moved |
| Guide checks: `check_sentences.py`, `check_references.py` and `--self-test`, `check_links.py --local-only` | `receipts/docs-checks.log` | 0 over the limit, 0 unlinked, 79 self-test cases, 438 local links with 0 failures. External URLs were not requested |
| Added-line scan | `receipts/added-lines-scan-repro.txt` | 2,940 added lines (`main...HEAD`) and 567 (`73007b48..HEAD`), 0 label or path matches. 0 commit bodies. This reproduces the content of the receipt behind F1 |
| Restore check after all probes | `receipts/restore-check.txt` | Worktree, index and HEAD agree; 74 tracked blobs and modes equal the HEAD tree; 0 gitlinks; no `.gitmodules`; 0 untracked or ignored files |

## Round-1 findings at this head

| Finding | Status | Evidence at `50a2106` |
| --- | --- | --- |
| Internal F1 (MAJOR) / external F5: tracked bytecode | **Closed** in the tree; history is a manager duty | `7b5e821` deletes the file and adds `.gitignore` (`__pycache__/`, `*.pyc`). `git ls-files '*.pyc'` is empty. The blob is still in branch history (`cce36b5`), so main stays clean only through a squash or rebuilt-branch merge (pending duty) |
| Internal F2: one-port difference untested | **Closed** | `tests/unit/end_station_test.c:99-156` covers three things. A one-port refusal is refused in the default build and applied under the option. No policy is called at one port. Two ports refuse, retry and call the policy in every build. `review_test.c:288-311` now runs at one and two ports with an option-aware count. `one-port-refusal-kept`, `one-port-inert` and `one-port-policy-called` are KILLED in my runs |
| Internal F3 / external F2: reversal counts | **Closed** | `tests/check_reversals.py:376-394` selects cases, prints SKIP lines, and adds a summary with listed/selected/run/killed/survived/skipped counts. An unreported selected case fails the run (`:504-507`). The counts per mode are 110/4/4/8; I confirmed them by importing the selection function and in my runs |
| Internal F4 / external F2: tester-guide count | **Closed** | `doc/tester.md:222-223` now reads 38 = 10 + 5 + 11 + 12, with end-station 12 = 2 + 1 + 4 + 5. Importing `MUTANTS` gives 10 timer, 16 MAD in the scale build, and 12 in the END_STATION/LEAN_TX builds. The sanitizer's plant is counted apart |
| External F1: empty-word shortcut untested | **Closed** | The driver's AttributeTypes are now {1, 2, 31, 32, 129, 255} (`mad_trace.c:184-195, 445, 525`). Two mutants were added (`check_differential.py:200-204`), each killed at seed 3 in both profiles. The unit test `sparse_attribute_types_each_send_one_message_in_type_order` covers 7 types in 5 combinations, and the unit reversal is KILLED |
| Internal F5: callback contracts | **Closed** (wording residue R959-2-R2) | `mrp.h:202-205` (encode) and `:213-217` (decode); `doc/integrator.md:117-127`; the "changes no output" sentence is narrowed (`integrator.md:89-90`). Code agrees: `mrp_pdu.c:208-215` zeroes only in the delivering pass, and `mrp_mad.c:1708-1710` re-encodes moved vectors |
| Internal F6 / external F3: default objects | **Closed** | 260/260 and 28/28 RV32I as above; the control shows the old difference |
| External F4: no changelog | **Closed** | `CHANGELOG.md` names all nine options, their defaults, `LWSRP_SCALE`'s four, the direct end-station definitions, the one-port exception and the callback contract, and links #977, #872 and #665. Each option row matches its guide row and the compile definitions (`CMakeLists.txt:5`) |
| Internal R1 / external F6: option comments without issue IDs | **Closed** | Each of the nine option blocks now gives reason, requirement clauses and milan-fpga issue IDs (`mrp_mad.c:24-116`, `mrp_pdu.c:21-31`, `mrp.h:29-36`, `timer.h:32-39`, `msrp.c:40-47`). No added line carries a lane, round, reviewer or comment label |
| Internal S1 (timer removal inside a tick) | Retained as a suggestion | Not in the delta |
| Internal S2 (`tx_reverse` long-vector fallback untested) | Retained as a suggestion | Not in the delta |
| Internal S3 (name the delivering pass's zeroing guard as a sanitizer plant) | Retained as a suggestion | `doc/tester.md:192-194` still names only the reading-decoder plant |
| Internal S4 (no hosted workflow) | Retained as a limit | No `.github/`; GitHub lists 0 check runs at the head |

## Findings

### R959-2-F1 - MINOR - Tests

- **Artifact:** milan-fpga `16162ec2`, `review-evidence/lwsrp977-r1/author-r2/receipts/INDEX.md:32` (the sha256 line for `./added-lines-scan.txt`).
- **Evidence:**
  - The INDEX gives `f152030f313134a22871be707affa711c79c7221ff50859a2c5020be452c3839`.
  - The published file hashes to `f3a07ca02371cbacd7bd513bd1dfb6fb77caff3347207f193613b109f7ad7897`. `MANIFEST.json` gives that same value as both its original and its published hash, and it is not path-redacted.
  - The other 73 INDEX entries equal the manifest's original hashes (`receipts/packet-verify.txt`). For the 33 redacted files this is expected: their published copies differ by design.
  - So the index attests a version of this receipt that was not delivered.
- **Authority:** the brief's integrity duty: verify the signed packet and the published receipts. The receipt index is the author's integrity record for the round's evidence.
- **Impact:**
  - The receipt's content holds: `receipts/added-lines-scan-repro.txt` reproduces 2,940 and 567 added lines, 0 matches and 0 commit bodies.
  - The defect is in provenance. A reader cannot tell from the index which scan output the gate produced.
  - No measurement of the head depends on it.
- **Required outcome:** publish a corrected `author-r2/receipts/INDEX.md` whose line for `added-lines-scan.txt` gives the delivered file's hash. Otherwise publish the file that hashes to `f152030f...` and state which one the gate wrote. No lwSRP source change is needed.
- **Verification:** `python3 -I scripts/packet_verify.py <packet-root>` reports "matching neither 0" and exits 0.

### R959-2-R1 - RESIDUE - Docs

- **Artifact:** `src/core/mrp_mad.c:1225`.
- **Evidence:** the new comment reads "The whole value, with no local, so the default object is main's at every optimisation level."
  - It names a branch. After the merge, that branch is this code, so the sentence refers to itself.
  - Unlike the option comments, it gives no issue ID.
- **Exact fix:** `/* The whole value, with no local: with LWSRP_LEAN_COPY at 0 the restore compiles as it did before the option (kebag-logic/milan-fpga#977). */`

### R959-2-R2 - RESIDUE - Docs

- **Artifact:** `src/include/shish_lan/mrp.h:202-203` and `:213`; `doc/integrator.md:121` and `:125`.
- **Evidence:**
  - The contracts say the encoder's result "must depend on attr_type and attr_val alone". They say the decoder's result depends on "attr_type, offset and the buf octets alone" (the guide: "the wire octets, offset and type alone").
  - In-tree codecs also depend on the buffer length. For example, `mvrp_encode_attr` refuses `buf_len < MVRP_ATTR_LEN_VID` (`src/modules/mvrp.c:48`).
  - So the literal rule contradicts the guide's "In-tree applications already meet each rule" (`integrator.md:120`).
  - Behaviour is unaffected: each pass and each re-encode passes the same length.
- **Exact fix:**
  - `mrp.h:202`: "must depend on attr_type, attr_val and buf_len alone".
  - `mrp.h:213`: "must depend on attr_type, offset, buf_len and the buf octets alone".
  - `integrator.md:121`: "must depend on the wire octets, their length, offset and type alone".
  - `integrator.md:125`: "Its output must depend on the type, value and buffer length alone."

### Suggestions (not blocking)

- **S1:** the PR's object claim covers 8 sources at 8 flag sets. `sim_adapter.c` and `switch_ctrl.c` are under `src/` too, and `sim_adapter.c` is in the host library. My probe covers all 10 sources with both compilers, and adds -O1, -O3 and stripped -g (260/260). The PR text could cite the wider set, or keep stating its narrower scope as it does now.
- **S2:** `tests/check_reversals.py:436` now always passes `-DCMAKE_C_FLAGS=…`, which is empty with `--end-station OFF`. That replaces any `CFLAGS` from the environment, which the runner honoured before. Pass the cache entry only when `--end-station ON`.
- **S3 (retained from R959-1-S1):** state that removing a timer from inside a tick callback is unsupported, or test it. One example is `mrp_reclaim` called from an indication during a leave-timer expiry.
- **S4 (retained from R959-1-S2):** the `tx_reverse` fallback for vectors longer than its buffer is unreachable for in-tree applications, and no test exercises it.
- **S5 (retained from R959-1-S3):** name a sanitizer plant that removes the delivering pass's zeroing next to the reading-decoder plant (`doc/tester.md:192-194`).

## Lens notes

- **Conformance:**
  - The delta changes no transmitted octet, state transition or indication with options off: the objects are identical.
  - With options on, the only code change in the delta is the `RX_KEPT` spelling, which keeps `kept` under `LWSRP_LEAN_COPY`.
  - The new clause citations match the code they head:
    - 10.7 for the lookup;
    - 10.8.2 for the Message build;
    - 10.3 for MAP;
    - 35.2.6 and Tables 10-3/10-4 plus Milan 4.2.7.2.2 for rapid replacement;
    - 10.7.8 and 35.2.2 for the copies;
    - 10.8.3 for validation;
    - 10.7.4 and 10.7.11 for the wheel.
  - The end-station suite cites 10.3, 10.8.1.2 and Table 10-4 for its expectations.
- **RTL (here: the C library and its build):**
  - `RX_KEPT` is defined and undefined within `rx_on_attr` (`mrp_mad.c:1223/1226/1293`), and all three uses are inside it. Because macros are lexical, the early returns are harmless.
  - `CMakeLists.txt:77` registers the new suite in every build. `tests/unit/main.c:16,34` adds it with no condition, so the eleven suites and the conditional key suite match the guides.
  - The RV32I compile-only probe passes with `-Werror` for every option set.
- **Robustness:**
  - The re-encode after a merge discards its result (`mrp_mad.c:1710`). This is safe only under the stated encode contract, which is now written down.
  - The lean validation pass's unzeroed buffer is safe only under the stated decode contract, which is now written down. The author's MemorySanitizer run covers it (`diff-*-r2.log`, 39 of 39); I did not rerun the sanitizer.
  - The one-port refusal path is pinned in both directions.
- **Tests:**
  - The new unit tests are option-aware and kill the three one-port reversals and the scan-ending reversal.
  - The differential driver now spans four type words, and both added mutants are killed.
  - The reversal runner can no longer report coverage it did not run.
  - Every count I reran matches the packet and guides.
  - Open: F1, a receipt-index integrity defect.
- **Docs:**
  - CHANGELOG, integrator, tester, manager, architecture and README edits are consistent with the code and the counts.
  - All 45 anchors name the same lines as at `73007b48`, and the guide checks pass.
  - Residue: R1 and R2.

## Ledger (reviewer-owned)

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | option comments' clause citations; `mrp_mad.c:1219-1293`; `end_station_test.c` expectations against 10.3, 10.8.1.2 and Table 10-4; object identity (260/260, RV32I 28/28); differential 38/38 in both profiles | R959-2 (delta); R959-1 for untouched code | `50a2106483141fcd7d1b20654bcf0803e7c3020a` |
| RTL (C library and build) | CLEAN | `mrp_mad.c` `RX_KEPT`; `CMakeLists.txt:77`; `tests/unit/main.c`; host builds with gcc and clang; RV32I compile-only with 4 option sets | R959-2; R959-1 for untouched code | `50a2106483141fcd7d1b20654bcf0803e7c3020a` |
| Robustness | CLEAN | `mrp.h:202-217` contracts against `mrp_pdu.c:208-218` and `mrp_mad.c:1596-1712`; one-port refusal tests; `.gitignore` | R959-2; R959-1 for untouched code | `50a2106483141fcd7d1b20654bcf0803e7c3020a` |
| Tests | UNCLEAN (R959-2-F1) | `end_station_test.c`, `review_test.c`, `check_reversals.py`, `check_differential.py`, `mad_trace.c`; my unit, reversal and differential reruns; the author-r2 packet and manifest | R959-2 | `50a2106483141fcd7d1b20654bcf0803e7c3020a` |
| Docs | CLEAN (residue R1 and R2 carried) | `CHANGELOG.md`, `README.md`, `doc/*.md` delta, the 45 anchors, guide checks, the nine option comments, `mrp.h` contracts | R959-2 | `50a2106483141fcd7d1b20654bcf0803e7c3020a` |

## Limits

- **RV32I:** compile-only, with clang's generic riscv32 target and a stub `<string.h>`. This is not the product toolchain. It ran no link, no cycle measurement and no hardware.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **Sanitizer:** I did not rerun the differential with `--sanitize-memory`. The 39th plant and the sanitizer-clean claim rest on the author's receipts, `diff-OFF-r2.log` and `diff-ON-r2.log`. Their manifest hashes verify.
- **Not rerun at this head by me:** scenarios (`behave`), the codec command, equivalence and its controls, `check_embedded.py`, `check_freestanding.py`, and the default and key reversal runs. Those rest on the author's receipts, which verify against the manifest. The delta does not touch the code they depend on, except the restore spelling, which object identity covers.
- **External links:** checked with `--local-only`; external URLs were not requested.
- **Hosted evidence:** lwSRP has no hosted workflow, and GitHub reports 0 check runs at the head. Every source-head gate is author-run.
- **Manager source bank:** none was run at this head, and I claim none.

## Pending manager duties

- Merge so that `main`'s history does not carry the bytecode blob added in `cce36b5`, by squash or a rebuilt branch. Then confirm that `git log --format=%H -- tests/__pycache__` on `main` shows no adding commit.
- Build and validate the current-dev merge candidate at the merge turn (source base `d1bb4f4e`, live dev `e275d795`), with the builder and native banks, and link the receipts.
- Hosted and act acceptance; carry R959-2-R1 and R959-2-R2 to the residue checklist.
- Obtain the corrected INDEX for R959-2-F1 before treating this review's Tests lens as clean.

R959-2 FINISHED
