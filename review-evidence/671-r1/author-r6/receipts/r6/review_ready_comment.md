[A592] REVIEW READY (round 6)
Commit: c7d0ad63510cf1aaee41ef440675d110ad2730d7 on `671-read-fault`, two new commits on `0c276b62`: `793641131` (host suite) and `c7d0ad635` (docs). No push, rebase or amend.

Answers [the round-6 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6112358549), R602-5-F1 and R603-5-F1.

Changed:
- **Terms listed once.** `read_fault_cases.COMPARISON` lists the comparison's four terms: verdict, byte count, prefix CRC and trailer. Each entry has the firmware's spelling and the fault that changes that term alone. The term classes, the controls, the findings' wording and the comparison check are all generated from it.
- **One class per term.** Two faulty reads that differ from each other in that term alone open the faulted slot's judgement, then a clean read. The faults:
  - trailer: the trailer's last byte XORed differently on each read (`--read-fault SLOT:-1`, an offset counted back from the length word's end);
  - prefix CRC: the last byte before the trailer (`SLOT:-5`);
  - byte count: a new `--read-length`, which grows the length word by four on each read and forges the CRC so the prefix CRC and the trailer stay fixed;
  - verdict: a new `--read-verdict`, which XORs the entity, model and layout words in turn and forges the CRC closed on the slot's own trailer.

  Each class runs at 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF with the other slot blank, and at both both-valid layouts across the wrap. It runs both ways round, on cold boots and writer restarts, through the same exact read-count, hold, changed-record and other-record assertions: 32 cases per term. A probe build that prints each read's four terms shows that all 384 class cases on three shapes hand the judgement two refusals differing in their own term alone, then VD_OK. Each shape runs 3,550 cases (1,839 cold, 1,711 restart).
- **One control per term.** `r_omit_verdict`, `r_omit_byte_count`, `r_omit_prefix_crc` and `r_omit_trailer` each replace one term with `1` in a copy of the firmware. Each is caught by its own words ("which differ only in their trailer", and so on) on arty 4x4, 1x1 and 8x8. In full count, each is named by all 32 cases of its own class on each shape, and by none of the other three classes.
- **A check fails without them.** Run against the shipped firmware, the check fails when `nvm_reads_agree` compares by other terms than the list, when a term lacks its class at any of those places, or when a term lacks its control. Its self-test requires that failure by name in nine arms: four terms without their class, four without their control, and a fifth firmware term.
- **The production comparison is unchanged.** The firmware is byte-identical to `0c276b62` (sha256 `497845e6...`), so no STOP. Capture and size are unchanged.
- **Docs.** The host README (model, check 13, counts and controls), FASTCONNECT section 7 and the firmware page are updated.

Validation (all rc 0 unless stated; receipts in the handoff):
- Writer gate `--self-test --jobs 4` at `c7d0ad635`: 5 shapes at 3,550 cases. 61 firmware plants reddened (18 #671 × 3 shapes) and 9 comparison-check arms failed by name, in 275.27 s.
- **R603-5 `probe_comparison.py`**: its own assertions hold, and the omission plant now gives **78 standing findings on each of the three shapes** (0 before), 32 of them naming the trailer class.
- **R602-5 `probe_r602_5.py --mutants no_tail,digest_short --sets none --standing`**: **78 findings per shape for `no_tail` and for `digest_short`** (both 0 before). The trailer set reproduces R602-5's own figures.
- Harness equivalence: checks 1-14, the disabled-writer and the boot-walk graders on three shapes, on this harness and `0c276b62`'s, gave 10,641 twin runs with 0 differences. The 384 runs using the new faults ran on the new harness only.
- All 18 #671 controls in full count on three shapes, with identical counts per shape.
- All 101 builder functions with every elaboration arm; part 6 holds the writer gate.
- Co-simulation 465/465 checks and 39/39 mutants, and the service budget.
- Firmware-unit 7/7 (Mark II store 435 tests) and lint/BDD 5/5.
- The 78 runnable docs-check positions.
- The capture receipt gate, whose four mutation arms reject with rc 1 as required.
- Idiom, hygiene, em-dash and diff checks.

Acceptance criteria: #671 items 1-3 are met by the unchanged firmware, as both round-5 reviews found. This round's six assignment items are met as above. There is no RTL, register-map, record-format, gitlink, Makefile or workflow change, and no A/B write-path change.

Open risks/questions:
- The verdict and byte-count classes are constructed CRC-32 collisions in the host model. They pin each term; they do not claim such faults are common.
- The hosted writer gate is estimated at 370-450 s against the builder's 1,200 s; the hosted standalone step took 356 s at `0c276b62`.
- R602-4-S1 and S2 remain optional. The Mark II store's collapse awaits its own Issue. Prefill is #717.

HANDOFF.md and PR-BODY.md have Round 6 sections. The working tree is clean. The head is local: exact-head hosted and act evidence, independent re-review and merge-candidate validation remain. No merge is authorized or performed.
