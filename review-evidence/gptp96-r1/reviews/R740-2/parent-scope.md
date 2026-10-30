[A10] **The sweep starts now, at the owner's request of 2026-10-30.** Every lane runs at lane-queue priority 2, below release (0) and Mark II (1), so it never takes CPU from the #76 work.

**Order:**
1. **Now, D0 (milan-fpga, executor [A706]): the inventory and verification audit.** Branch `797-d0-audit` from dev.
   - Write a generator, `scripts/docs_inventory.py`, that lists every Markdown file and README with: its area; its line count; its declared audience and purpose (from the page's own first lines, or a mapping table the script owns); what code or spec it describes; and its status (current, stale, superseded, obsolete), each status with its evidence.
   - Regenerate `docs/DOCUMENTATION_AUDIT.md` from that generator. The page is generated, never hand-edited, and a freshness gate checks it.
   - Verify every normative or numeric statement on the release-facing pages against the source at the head and against the clauses. Write each contradiction as a finding with file:line, the source line or clause, and the correction, grouped by area for the area lanes. The release-facing pages are the README, `docs/README.md`, guides, integration, reference, `REQUIREMENTS.md` and `FR_NFR.md`.
   - Do not rewrite pages in D0. Fix only a one-line factual error on a page no running lane touches.
2. **Now, G (FPGA-gPTP): the same pass on that repository's docs,** by PR there. Executor [A707].
3. **After processor #203 merges, P (protocol-processor),** by PR there.
4. **After D0 lands, the area lanes,** fed by D0's findings: overview and guides (the start-here path and `docs/GLOSSARY.md`); design; reference (with the ETH_GUARD and link-control addition above); testing and CI; findings; module READMEs.
   - Pages the release lanes are editing wait until those lanes merge. Today these are `CHANGELOG.md`, `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md`, `docs/testing/TESTING.md`, `docs/integration/BUILDING.md` and `BAREMETAL_FIRMWARE.md`, `docs/design/REBOOT_RESET.md` and the diagrams.

The rules are the issue's. `dev-soft-core` takes the merged result through its next dev sync.

