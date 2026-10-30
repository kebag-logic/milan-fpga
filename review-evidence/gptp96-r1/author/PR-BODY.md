[A707]

Documentation sweep for this repository, part of the parent documentation sweep (parent #797).

Closes #96

## What changes

- **Start-here path.** `README.md` gains scope, the 802.1AS-2011 + Cor1/Cor2 + Milan v1.2 edition statement, a reading order and a repository layout. `docs/README.md` routes new readers there.
- **Defined terms.** New `docs/GLOSSARY.md` has protocol terms with their 802.1AS-2011 and Milan clause numbers, and engine terms linked to the guide sections that define them.
- **Summaries.** A short summary now opens each long page (integration, HDL, test, manager).
- **Document status.** `docs/README.md` has a status table listing every maintained Markdown page (audience, what it describes, status). The 18 archive pages keep their own Historical banners.
- **One table for values.**
  - `docs/INTEGRATION.md#protocol-constants` names each generator constant with its value and clause.
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

## New freshness checks (`scripts/check_docs.py`, part of `make docs`)

- Every maintained Markdown page must have exactly one Current row in the status table, and every row must name an existing page.
- Every protocol-constants row must equal the generator constant it names.
- The ROM budget table must equal the generator's own word count, for the shipping image and for a seeded image.
- The self-test grows from 10 to 23 arms. Every new rule has a true control that passes and planted defects that fail it.
- Planted defects in a copy of the real tree each fail the check, while the unmutated copy passes: a stale ROM count, a drifted constant, a deleted status row, and a changed generator constant with the docs untouched.

## Findings for a code change (not fixed here: no RTL or generator edits in this PR)

- `hdl/ucode/gen_gptp_ucode.py:284`, `:292-296`, `:315-317`. Version-history notes in the module docstring read as current:
  - asCapable cleared "at the fourth" lost response. Microcode and docs clear at the fifth, per 802.1AS-2011 Figure 11-8 as Cor1 changes it.
  - Sync receipt timeout "clears sync-ok". It ages the grandmaster when gmPresent (10.3.11, Figure 10-13).
  - The Milan 4.2.6.2.5 cease "still deliberately out". It is implemented.

  The comments are wrong; the code and the docs agree with the clauses.
- `hdl/top/KL_gptp_engine.sv:43-45`. A repeated phrase in the header comment.
- The HDL guide's synthesis figures are dated (main `5dce647a`, 2026-10-11), and later RTL has landed since. They need a re-measurement.

## Gates

All at base `135afd04` and head `86073476`, rc 0:
- `make docs`, `make diagrams-check`, `make contract`, `make lint`;
- the microCPU, parser (with mutants), engine run, gasket (with mutants), independent-decode (with mutants) and bench-tag suites. Check tallies are identical at base and head.

Not run:
- The engine mutation arm. Its inputs are unchanged by this PR, and it runs far longer than the session allows.
- `make ooc`, which needs synthesis.

Parent consumer gates, because a docs-gate script changed. A parent checkout at PR #805's head had its gitlink set to base and to head:
- `make -C gptp-processor docs` and the parent code-quality ratchets (naming, fail-fast, test evidence, hygiene) pass at both.
- The parent's gPTP-docs and submodule-docs gates fail identically at base and head. The parent pages pin the previous gitlink, so any bump needs those pins updated.
- With the parent pins rewritten to the new gitlink, the parent gPTP-docs gate passes at both.

Two reviews required.
