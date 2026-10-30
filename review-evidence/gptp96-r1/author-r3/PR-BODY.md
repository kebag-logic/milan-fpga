[A707c]

This is the documentation sweep for this repository, part of the parent documentation sweep (parent #797). This revision answers the round 2 reviews. Their three findings were about claims: two concern what the docs gate is said to check, and one concerns where the history page links. All three are fixed. Every sentence about the gate now states what it checks, and only that.

Closes #96

## What changes

- **Start-here path.** `README.md` gains:
  - a scope statement;
  - the 802.1AS-2011 + Cor1/Cor2 + Milan v1.2 edition statement;
  - a reading order and a repository layout.

  `docs/README.md` routes new readers there.
- **Defined terms.** New `docs/GLOSSARY.md` gives:
  - protocol terms, with their 802.1AS-2011 and Milan clause numbers;
  - engine terms, linked to the guide sections that define them.
- **Summaries.** A short summary now opens each long page: integration, HDL, test and manager.
- **Document status.** `docs/README.md` has a status table with one row per maintained Markdown page, giving its audience, what it describes and its status. The 18 archive pages keep their own Historical banners.
- **One table for values.**
  - `docs/INTEGRATION.md#protocol-constants` names each generator constant with its value and clause.
  - Other pages name the constant and link its row instead of restating the number.
  - The manager guide's ROM budget is a table.
  - The duplicated out-of-context resource table now lives only in the HDL guide.
  - The older measurement deltas moved to a new archive page.
- **Missing suites.** The test guide now lists the gasket and independent-decode suites that `make tb` runs. Both suite directories gain a README.

## Corrections (the doc was wrong; the code was right)

1. **Peer-delay clauses.** The clause table cited the 2020 edition. It now cites 802.1AS-2011 11.2.2, 11.2.15.2.3, 11.2.15.2.4 and 11.2.16.
2. **Self-publication and gmPresent.** These rules cited 2020 10.3.13.2.4. They now cite 2011 10.3.12.1.4 i) and g).
3. **Holdover annex.** "Annex B.1.1 holdover" named no document. It is Milan v1.2 Annex B.1.1; 802.1AS-2011 B.1.1 is frequency accuracy.
4. **Usable Sync pair.** The rule now cites Figure 11-6 (11.2.13), not 10.3.11, which covers only the ageing.
5. **Generator command.** The documented command used `--mac 02:a1:b2:c3:d4:e5`, which the generator refuses (exit 2). It now uses `0x02A1B2C3D4E5`.
6. **ROM budget.** Shipping uses 1,022 of 1,024 words, leaving two free (the page said 1,021 and three). Seeded images use 1,023.
7. **Slew-active connection.** The consumer connection is no longer owed. Parent #545 is closed and parent `dev` carries the level; the guide now says so, with pinned links.
8. **Follow_Up clause.** The glossary cited 11.4.3, which is the Sync message. It now cites 11.4.4 (Follow_Up) and 11.4.7 (Pdelay_Resp_Follow_Up).
9. **Publication timing.** Each `pub_*_o` output is wired straight to its staging register (`KL_gptp_engine.sv:1134-1146`). The pages now say:
   - consumers sample on `pub_commit_o`;
   - staging writes change the outputs first;
   - the commit cycle always presents a complete tuple.
10. **Archive pointer.** The PR #76 resource-delta page now links the four reports its figures come from: baseline and candidate engine utilization and timing, as files at parent `4999d8d6`.

## Freshness checks (`scripts/check_docs.py`, part of `make docs`)

Each statement below is what the checker enforces. `docs/INTEGRATION.md#protocol-constants` states the same rules beside the table.

- **Status table.**
  - Each maintained Markdown page needs exactly one row, and that row must say Current.
  - The archive directory needs a row that says Historical.
  - A row naming a missing page fails.
- **Constants rows.**
  - Each row is found by its backticked constant name.
  - The value must be a plain or comma-grouped decimal equal to the generator constant. Any other cell, such as bold, negative or unit-bearing, is a named finding.
  - All 17 expected names need a row, and a duplicate row fails.
  - The cadence table in the same section is not checked, and the page says so.
- **ROM budget.**
  - The shipping row must equal the generator's word count for the shipping image.
  - The seeded row must equal its count for `--seq-seed 0x200000`. No other seeded image is checked.
  - Rows are parsed strictly, and a missing or duplicate row fails.
- **Copies.**
  - A row has a unit when its Meaning cell ends in ms, ns or ppm.
  - On current pages, outside the Protocol constants section and outside fenced code, the gate rejects that row's value written as:
    - the integer with its unit symbol, optionally hyphenated;
    - a ms value in whole seconds, or a ns value in whole microseconds, by symbol;
    - a ms value as one to ten whole minutes, in digits or as a number word.
  - Decimal forms (for example "0.375 s") and other unit words (for example "375 milliseconds") are not matched.
  - Rows without a unit, such as ordinals and the ROM depth, are not checked for copies.
  - Review keeps those forms out; the reviewed pages hold none.
- The docs gate no longer writes a bytecode cache into `hdl/`.

**Self-test** (`--selftest`, 42 arms, up from 10 at the base):
- It has a true control for the status, constants, copy and ROM rules.
- Planted defects cover:
  - status: an unlisted page, a missing page, a wrong status and a duplicate row;
  - constants: a drifted, unknown, bold, negative or unit-bearing value, an empty table, and a deleted, unnamed or duplicate row;
  - copies: plain, grouped, converted to µs or s, spelled minutes, a rate, and a copy outside the home section, plus passing controls for a link, a fenced command and an unrelated number;
  - ROM: a drifted used or free count, and a missing, formatted or duplicate row.
- Except the five below, silencing any one finding of these four rules makes the self-test fail.
- Five findings have no arm of their own:
  - "no document status rows";
  - the archive row missing from the status table;
  - "is not a generator constant";
  - "no protocol constant rows";
  - non-decimal ROM counts.

  An arm reaches the two constants findings only together with a missing-row finding. The production gate still reports all five.

**Planted defects in copies of the real tree.** Each fails with its named finding, while the unmutated copy passes:
- stale, formatted, deleted and duplicate constants rows;
- a changed generator constant with the docs untouched;
- stale, formatted and duplicate ROM rows;
- every copy form listed above, on several pages.

The stated passes (decimals, unit words, fenced code, the home section, historical pages) pass as stated.

**Checker weakenings.** Removing the duplicate-row check, the required-name set, strict decimals, the µs conversion, the minute words, the home exemption, the ROM duplicate check or the number lookbehind each makes the self-test fail.

## Findings for a code change (not fixed here: no RTL or generator edits in this PR)

- `hdl/top/KL_gptp_engine.sv:43-45`. The header says the publish bank is "latched by OP_COMMIT". No such latch exists: the outputs are continuous assigns of the staging registers. The phrase "becomes ... becomes wires" is also repeated. The comment is wrong; the RTL and these docs agree.
- `hdl/ucode/gen_gptp_ucode.py:2499`. The `--p1` default is a literal `248`, a second home beside `P1_C`. It should read `default=P1_C`.
- `hdl/ucode/gen_gptp_ucode.py:284`, `:292-296` and `:315-317`. These version-history notes in the module docstring read as current:
  - asCapable cleared "at the fourth" lost response. The microcode and the docs clear it at `LOST_CLEARS_AT_C`, per 802.1AS-2011 Figure 11-8 as Cor1 changes it.
  - The Sync receipt timeout "clears sync-ok". It ages the grandmaster when gmPresent (10.3.11, Figure 10-13).
  - The Milan 4.2.6.2.5 cease is "still deliberately out". It is implemented.
- The HDL guide's synthesis figures are dated (main `5dce647a`, 2026-10-11). Later RTL has landed since, so they need a re-measurement.

## Gates

At the previous head `806957b3` and at this head, all rc 0:
- `make docs`;
- `make diagrams-check`;
- `make contract`;
- `make lint`;
- `git diff --check` from the base.

This revision changes no RTL, generator, test or build input, so the suites were not rerun. The previous revision ran them at its base and head with identical tallies: microCPU, parser with mutants, engine run, gasket with mutants, independent decode with mutants, and bench tag.

Not run:
- The engine mutation arm. This PR does not change its inputs, and it runs far longer than one session allows.
- `make ooc`, which needs synthesis.

Parent consumer gates were run because a docs-gate script changed. A parent checkout at PR #805's head had its gitlink set to the previous head and to this head:
- `make -C gptp-processor docs` passes at both, and so do the parent code-quality ratchets (naming, fail-fast, test evidence, hygiene).
- The parent's gPTP-docs and submodule-docs gates fail identically at both. The parent pages pin the earlier gitlink, so any bump needs those pins updated.
- With the parent pins rewritten to the new gitlink, the parent gPTP-docs gate passes at both.

Two reviews required.
