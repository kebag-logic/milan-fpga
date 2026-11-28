[A825] REVIEW READY: round 13 of #977, milan-fpga `pf-977-1` at `4461d77ca34ec1203321821a3313071ff1923984`. tsn-c-stack is at `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` and lwSRP at `main` `e27b34c9231abaa862bdb73f807238b330aa4c51`, both unchanged. Nothing is pushed or posted.

This round answers the re-reviews of round 12: PR #993 comments 7230545660 (internal R957-4, POSITIVE) and 7230559804 (external R958-4, NEGATIVE). The 8x8/1if load ceiling of 0.79 waits on the owner's answer (R958-4-F1). It is one droppable commit, `4461d77c`, the last on the branch, so `git revert 4461d77c` alone drops it.

**1. What changed** (3 commits past `3256d1d2`)

| Finding | Commit or file | Fix |
|---|---|---|
| R958-4-F2 MINOR | `receipts/deliv13.py.txt`, `receipts/meas/deliv13-*`; `48c7481a` | **The extractor.** Each registering record is associated with its own tagged receive commit: the RXC on SRP's channel whose frame the harness tagged with the record's name. That commit must equal the group JSON's `start_sys` for the record. The transmit-only probes after a burst triple, whose start is the triple's last record's commit and which tag no frame, are excluded and counted. A record with no tagged commit (and no such alias start), with more than one, with one on another channel, or with one the harness puts elsewhere is refused, and the run exits 1. **The fixture.** `--selftest` holds the queued triple at 10000, 20000 and 30000: three distinct commits; the excess placed only in the last record's five-pass window is observed (shares 0, 500 and 1,250 a sink); the transmit alias is excluded; the four refusals hold; and the earlier rule takes 10000 three times (8 of 8). **The re-extraction.** From the existing r10d logs at both shapes and both arms, every `srp-register` group (20 logs a point): 44 records a point at 44 distinct commits, 6 aliases excluded, none refused. The maximum against the accepted after-window baseline is unchanged, as are both comparison medians, so `DELIVERY_US`, its floor and `DELIVERY_BESIDE` stand. `load_grade.py`'s comment and the design document's section 13 state the association. |
| R958-4-R1 | `48c7481a`, `4461d77c` | `load_grade.py:13,374`, `load_deliveries.py:3` and `flip_grade.py:66` cite "#977, the manager's decision of 2026-11-27 on deferred deliveries". No source comment names the comment ID. FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY keep the link. |
| R958-4-F1 MAJOR (owner) | `831ffe10`, `4461d77c` | R1 rewords a line that `3256d1d2` added, so `831ffe10` reverts it and `4461d77c` restates the 0.79 raise last. Its content is `3256d1d2`'s apart from that citation, and it still cites "owner decision pending". The manager amends the citation when the owner answers; the PR must not merge with "pending". |
| R958-4-R2 | `receipts/supersession-author-r10-index.md`, `receipts/supersession-author-r11-index.md`; `PR-BODY.md` | Two new dated files, for publication beside the old indexes, whose bytes stay as they are. The round-10 note records that round 11's packet and the current PR supersede four pieces of its wording: the pending-80-ms wording, the reviewer placeholders, the all-zero run counts and the default-option explanation. Both notes map each `.txt.gz` row to its published `.txt` path, with `MANIFEST.json` as hash authority. The PR summary now reads "Code corrections are applied; the historical index notes remain to be published." |

**2. Results**

| Item | Result |
|---|---|
| Every product ELF against `25ff0632`'s | **80 of 80 byte-identical** at `4461d77c` (plat_ledger's platform images and the harness's 72; `receipts/elf-identity-4461d77c.txt`). Round 10d's measurement and both routes stand. No arm was re-run. |
| The extractor's self-test | 8 of 8 controls hold (`receipts/meas/deliv13-selftest.txt`). The queued triple yields commits 10000, 20000 and 30000. The excess placed in the last record's window alone gives shares 0, 500 and 1,250 a sink, so the later window is observed. The alias is excluded. A missing, doubled, wrong-channel and misplaced commit is each refused. The earlier rule takes 10000 three times. |
| The re-extraction, both arms, every `srp-register` group (20 logs a point) | 8x8/1if: 44 records at 44 distinct commits, 6 aliases excluded, none refused, rc 0. 1x1/1if: the same. Round 12 located 22 distinct records a point. The other 22 are the twelve later burst records, the eight setup advertise records it skipped by name, and the plain group's two. |
| DELIVERY_US, against the after-window baseline | 8x8/1if 15,104 cycles a sink, **160 us** (answering-ports swap); 1x1/1if 18,778, **200 us** (answering-ports JoinIn of both kinds with a change owed). Unchanged. |
| Beside it: the 50 ms and 500 ms pre-record medians | 8x8/1if 11,573 and 13,642 cycles, 125 and 145 us; 1x1/1if 18,076 and 18,765, 190 and 200 us. Unchanged. |
| 8x8/1if load at the pin | **0.78214** (0.76614 without the term), within 0.79 and over 0.77. At `48c7481a` (the ceiling reverted) `flip_grade --check --point 8x8/1if` fails at 0.782, rc 1. |
| 1x1/1if load at the pin | 0.53254, against 0.70 |
| The floors | `DELIVERY_US` at 155 us (8x8/1if) and at 195 us (1x1/1if) are each refused "under its measurement's ... by the rule" (`receipts/meas/load-flip-4461d77c.txt`) |
| The ceiling's edge and revert | 0.790 passes and 0.791 fails. With FLIP at 0.77 both ceiling controls escape. `git apply -R --check` of `4461d77c`'s patch is clean. |
| `load_grade --check` / `--selftest` / `load_deliveries.py` | PASS / 32 of 32 / every control refused |
| `flip_grade --check` at 1x1/1if and 8x8/1if / `--selftest` | PASS, PASS / 628 of 628 |
| Harness self-tests (clean clone at `4461d77c`) | `run.py --self-test` 0 failures, `kept_grade` 33, `shape_costs` 25 of 25 and `--check` PASS |
| Python and C++ idiom gates | PASS |
| Docs workflow | 100 of 100 steps (em-dash base dev-soft-core `0b594023`), no tracked file changed |
| `git diff --check` over the PR delta | no hit, against `71bad8c0` and against `0b594023` |
| Source comments | `git grep 7229657853` over the Python sources: no hit. The FR_NFR and SPLIT_CONTROL_MEMORY links are kept. |
| Firmware gate | not re-run: no firmware-tree file changed this round |

**3. Open for the owner and the reviewers**

- **The 8x8/1if load ceiling, 0.77 to 0.79** (R958-4-F1). If it is refused, revert `4461d77c`; the 8x8/1if flip check then fails at 0.782 (`receipts/meas/flip-without-ceiling-48c7481a.txt`), and 8x8/1if waits for #1025's margin recovery.
- **Publication.** The two supersession files, and this packet.

The receipts are under `receipts/`, indexed in `receipts/INDEX.md`.
