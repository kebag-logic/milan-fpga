# Round 10 receipt index

Head `640699e6866602b2a5de5d404c43f3bd4df8037c` on branch `arty-int-1127`, eleven commits on round 9's `575118fac`.
The image is round 9's: firmware, gateware and bitstream are unchanged. The census executables are new, built at `7bc47c0ee82878790da1a4c8765ed21b8b006021`; the later commits change graders and documentation only.
Prepared locally; nothing has been posted or pushed.

[MANIFEST.json](MANIFEST.json) lists the 137 receipt files outside `census-extract/` with each file's bytes and SHA256 before and after redaction.
Every file under this directory, the extract included (972 files), passes through the publication scrub unchanged ([extract/r10-extract.log](extract/r10-extract.log) for the extract's 834).

## 1. The Arty's bind-save bounds (`7af5117f1`, `1903077be`)

- `bind_save.FLIGHT_MS['arty-1x1'] = 400`, `BURST_SAVES['arty-1x1'] = 4`, by PR #1004's ruling of 2026-11-27: the save-bind group's 288.8 ms less its 100 ms window, 188.8 ms, twice, 377.6 ms, rounded up to 50 ms. Section 15 states the bench's 245 ms save (490, stated 500) beside it, and that the rule uses the census model.
- [bind/bind-regrade.log](bind/bind-regrade.log): the 12 bind groups regraded against the stated bounds. In flight at most 369.2 ms (`save-bind-in-capture`), the burst 239.6 ms and 4 saves, the idle store 288.8 ms.
- The link-rate census measured them again; all 12 pass ([census/completed.json](census/completed.json)).
- `selftest_bind.py` held the targets to the two earlier points, so the first harness self-test failed on it in every partition ([validation/attempt0-service-selftest-0.log](validation/attempt0-service-selftest-0.log)); `1903077be` holds them to all three.

## 2. The 100 Mb/s egress gate

- [egress/all.json](egress/all.json), [egress/all.log](egress/all.log), from the recipe [egress/proto.py](egress/proto.py): round 9's instant-egress census replayed through the queue. The free-space outcome changes in 11 of 159 cases: six `notice-burst` cases, three `aecp-largest-notice`, `aecp-outputs` and `backlog-owed`. Two of them also move an AECP completion read.
  So by the ruling's item 3 the census runs again, egress drained at link rate (`egress_queue.hpp`).
- TX_TAIL's readers: `mbx_tx_begin`'s free-space test (`sw/firmware/ctrl/mbx/mbx.c`), AECP's completions in its poll (`sw/firmware/ctrl/aecp/aecp_mbx.c`, a counter notice's next time and REBOOT's last cookie), and REBOOT's drain (`sw/firmware/ctrl/plat/ctrl_plat.c`, `drained`). It is not only the free-space test. Drained at link rate, all three read the link-rate tail.
- [census/](census/): the 159-case link-rate census, 3 windows, no finding ([census/completed.json](census/completed.json)). The qualification passes every check, the 100 Mb/s row among them as `egress-100` ([census/qualification.json](census/qualification.json), [egress/egress-100.log](egress/egress-100.log)).
- [derivation/](derivation/): this census merged with round 9's maxima. Every cost and owner row is unchanged and the rule's row is the installed one, a fixed point. `kept_grade` passes with 5 lines owed to #977.
  [control-derivation/](control-derivation/): with every `srp-kept`/`srp-bound` record counted, no qualifying row; the least last queued notice is again 237.0 ms.
- The row: largest wait 426.47 us (`answering-ports/aecp-largest-notice`), plus the 54.88 us gPTP burst, times 1.05, plus the 0.32 us fixed path: 505.74 us of 1000 us. At most 19 records queue at once; 44 held records in two cases stay the held-egress ledger's.
  The replay, anchored to each record's last mailbox byte, reproduces every testbench departure exactly in all 159 cases.
- [egress/egress-fixed.log](egress/egress-fixed.log): the fixed path on the converted MII chain, at most 312.5 ns over 7 lengths and 64 clock phases, stated 320 ns.
- [egress/egress-selftest.log](egress/egress-selftest.log): 8 controls, and 9 planted defects each caught by its own control.
- [egress/egress-structural.log](egress/egress-structural.log): AECP's admission burst, 16 x 1,514 B, 391.51 us per record at most and 2,177.82 us in all. The rings at capacity, 254 least records, 2,646.82 us.
- [egress/extract-egress.log](egress/extract-egress.log): the same row graded from the published extract, 505.738 us.

## 3. Carried findings

- R928-3-F2: `575118fac` reads a part of exactly the stated limit. `census_extract.py --selftest` plants a part of exactly the limit, a first part of exactly the limit before another, and the reader at a limit of its size ([validation/gate-standalone-census_extract.log](validation/gate-standalone-census_extract.log)).
- R928-3-F3: a line longer than a part is refused, alone, after an emitted part and with no newline (`6e49d1fad`, the same log).
- R927-3-F2: [builder/builder-split.log](builder/builder-split.log) and [builder/builder-split.json](builder/builder-split.json). The command, the four heads, every output's SHA256 and the exit status: 22 outputs identical from `4adfa9dc` to `011aaa6f`, and from `aa53840d9` to the head, both placements; the merge changes `gptp_ucode.hex` only.
- R928-3-F1: [extract/r9-extract.json](extract/r9-extract.json), round 9's extract through the publication scrub as patched on 2026-11-27, 0 of 834 files changed. Round 10's, also 0 of 834.

## 4. Census packet and compact extract

- [census-extract/](census-extract/census.json): 159 cases, 834 files, 1,494,848,712 bytes, largest file 13,999,999 bytes. Its observation lines keep `TXREADY`, which the egress grade reads.
- [extract/regrade-full.log](extract/regrade-full.log) and [extract/extract-regrade.log](extract/extract-regrade.log): 159/159 and cross-case PASS on the full packet and on the extract, identical line for line.
- [extract/extract-control.log](extract/extract-control.log): without `srp-bound` the extract is refused, naming its own breach.

## Gates at the head

[validation/gates10.rc](validation/gates10.rc): ten documentation and idiom gates, eight standalone self-tests (`rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade`, `kept_grade`, `census_extract`, `egress_mii`) and `arty_grade.py`, all exit 0.
[validation/service-selftest.log](validation/service-selftest.log): the harness self-test, 8 of 8 partitions at `1903077be`.
`docs/DOCUMENTATION_AUDIT.md` is regenerated by its own gate (`docs_inventory.py --write`).
The firmware, boot and region gates of round 9 stand: no firmware or gateware source changed.
