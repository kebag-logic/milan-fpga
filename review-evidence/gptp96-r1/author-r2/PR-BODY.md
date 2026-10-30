[A707b]

Documentation sweep for this repository, part of the parent documentation sweep (parent #797). This revision answers both round 1 reviews; all their findings are fixed.

Closes #96

## What changes

- **Start-here path.** `README.md` gains scope, the 802.1AS-2011 + Cor1/Cor2 + Milan v1.2 edition statement, a reading order and a repository layout. `docs/README.md` routes new readers there.
- **Defined terms.** New `docs/GLOSSARY.md` has protocol terms with their 802.1AS-2011 and Milan clause numbers, and engine terms linked to the guide sections that define them.
- **Summaries.** A short summary now opens each long page (integration, HDL, test, manager).
- **Document status.** `docs/README.md` has a status table listing every maintained Markdown page (audience, what it describes, status). The 18 archive pages keep their own Historical banners.
- **One table for values.**
  - `docs/INTEGRATION.md#protocol-constants` names each generator constant with its value and clause.
  - Every other page names the constant and links its row instead of restating the number.
  - The manager guide's ROM budget is a table.
  - The duplicated out-of-context resource table now lives only in the HDL guide.
  - Older measurement deltas, which also carried a workflow label, moved to a new archive page.
- **Missing suites.** The test guide now lists the gasket and independent-decode suites that `make tb` runs. Both suite directories gain a README.

## Corrections (the doc was wrong; the code was right)

1. The peer-delay clause table cited the 2020 edition. It now cites 802.1AS-2011 11.2.2, 11.2.15.2.3, 11.2.15.2.4 and 11.2.16.
2. The self-publication and gmPresent rules cited 2020 10.3.13.2.4. They now cite 2011 10.3.12.1.4 i) and g).
3. "Annex B.1.1 holdover" named no document. It is Milan v1.2 Annex B.1.1; 802.1AS-2011 B.1.1 is frequency accuracy.
4. The usable Sync pair rule now cites Figure 11-6 (11.2.13), not 10.3.11, which owns only the ageing.
5. The documented generator command used `--mac 02:a1:b2:c3:d4:e5`, which the generator refuses (exit 2). It now uses `0x02A1B2C3D4E5`.
6. ROM budget: shipping uses 1,022 of 1,024 words, two free, not 1,021 and three. Seeded images use 1,023.
7. The slew-active consumer connection is no longer owed. Parent #545 is closed and parent `dev` carries the level; the guide now says so, with pinned links.
8. **Follow_Up clause.** The glossary cited 11.4.3, which is the Sync message. It now cites 11.4.4 (Follow_Up) and 11.4.7 (Pdelay_Resp_Follow_Up), the two companions the guide means.
9. **Publication timing.** The new summaries said the publication outputs change together on `pub_commit_o`. They do not: each `pub_*_o` output is wired straight to its staging register (`KL_gptp_engine.sv:1134-1146`), and microcode writes the fields over several instructions before `COMMIT`.
   - The summaries, the Publication section, the HDL invariant, the README, the manager status table and the glossary now say: sample on `pub_commit_o`; between pulses the outputs can show a partial tuple.
   - The PHC and port-enable summary lines are also made exact.
10. **Archive pointer.** The PR #76 resource-delta page now links the measurement reports themselves at parent `4999d8d6`, not that commit's change set.

## Freshness checks (`scripts/check_docs.py`, part of `make docs`)

- Every maintained Markdown page must have exactly one Current row in the status table, and every row must name an existing page.
- **Constants rows.**
  - Each row is found by its constant name, whatever the value cell holds.
  - The value must be a plain decimal equal to the generator constant.
  - A bold, negative or unit-bearing cell is a named finding, not a silent skip.
  - All 17 expected constants must have a row, so a deleted row fails.
- **ROM budget.**
  - The table must equal the generator's own word count, for the shipping image and for a seeded image.
  - Rows are parsed strictly, and a duplicate row fails.
- **No copies.**
  - A current page outside the constants table may not restate a timed or rate constant with its unit.
  - Unit-converted and spelled forms count, for example "375 ms", "20 us", "300 s", "five-minute" and "200 ppm".
  - Fenced commands are exempt.
- The docs gate no longer writes a bytecode cache into `hdl/`.
- The self-test grows from 10 arms to 41. Every rule has a true control that passes and planted defects that fail it.
- **Planted defects in a copy of the real tree** each fail, while the unmutated copy passes: 15 defects in all.
  - Stale constants: plain, bold, negative, with a unit, deleted, unnamed.
  - A changed generator constant with the docs untouched.
  - A formatted or duplicate ROM row.
  - Five re-added value copies.
  - A status row for a missing page.

  The previous checker let 10 of them through.
- **Checker mutants.** Each of seven deliberate weakenings of the checker makes the self-test fail.

## Findings for a code change (not fixed here: no RTL or generator edits in this PR)

- `hdl/top/KL_gptp_engine.sv:43-45`. The header says the publish bank is "latched by OP_COMMIT". No such latch exists: the outputs are continuous assigns of the staging registers. The phrase "becomes ... becomes wires" is also repeated. The comment is wrong; the RTL and these docs agree.
- `hdl/ucode/gen_gptp_ucode.py:2499`. The `--p1` default is a literal `248`, a second home beside `P1_C`. It should read `default=P1_C`.
- `hdl/ucode/gen_gptp_ucode.py:284`, `:292-296`, `:315-317`. Version-history notes in the module docstring read as current:
  - asCapable cleared "at the fourth" lost response. The microcode and the docs clear at `LOST_CLEARS_AT_C`, per 802.1AS-2011 Figure 11-8 as Cor1 changes it.
  - Sync receipt timeout "clears sync-ok". It ages the grandmaster when gmPresent (10.3.11, Figure 10-13).
  - The Milan 4.2.6.2.5 cease "still deliberately out". It is implemented.
- The HDL guide's synthesis figures are dated (main `5dce647a`, 2026-10-11), and later RTL has landed since. They need a re-measurement.

## Gates

All at the previous head `86073476` and at this head, rc 0:
- `make docs`, `make diagrams-check`, `make contract`, `make lint`, `git diff --check`;
- the microCPU, parser (with mutants), engine run, gasket (with mutants), independent-decode (with mutants) and bench-tag suites. Check tallies are identical at both.

Not run:
- The engine mutation arm. Its inputs are unchanged by this PR, and it runs far longer than one session allows.
- `make ooc`, which needs synthesis.

Parent consumer gates, because docs-gate scripts changed. A parent checkout at PR #805's head had its gitlink set to the previous head and to this head:
- `make -C gptp-processor docs` and the parent code-quality ratchets (naming, fail-fast, test evidence, hygiene) pass at both.
- The parent's gPTP-docs and submodule-docs gates fail identically at both. The parent pages pin the earlier gitlink, so any bump needs those pins updated.
- With the parent pins rewritten to the new gitlink, the parent gPTP-docs gate passes at both.

Two reviews required.
