[A570] STOP — exact head `313b20b34f891e73d1dac16a42b3c38346a92f50`

The consumer-test correction authorized by ruling 6079463350 is committed. The sweep programs 1,024 MAC identities before first enable; strict 5,000..6,000-cycle bounds and both draw-coverage assertions are unchanged. The committed-head differential passes 12/12 cases and catches 17/17 planted defects. The new MAC-ignoring generator fails the named highest-draw assertion (5,770 < 5,790 cycles). The full firmware bank, including RV32 and both mutation campaigns, passes; the general campaign catches 471/471 defects.

A documentation scope conflict prevents completion:

- `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5` still describes unconditional PROBE/DEFEND conflict restarts and unchecked supplied seeds. Its port table omits `port_operational_i`. These statements contradict M1/M4/M5/M7. The assignment names `docs/design/MAAP_FABRIC.md` as the documentation scope.
- `sw/firmware/ctrl/maap/README.md:189` still says start-phase variation reaches both fabric draw endpoints. The passing sweep now uses distinct programmed identities. Ruling 6079463350 explicitly says “No other firmware file changes.”

Neither page was edited. The session requires STOP for outside-scope changes. A public scope decision is needed to authorize these two documentation corrections. The handoff contains an unapplied proposed patch.

Static, documentation, source-list, recipe and resource self-tests pass. The initially mistyped documentation-map command returned 2; the corrected command returns 0. These checks do not resolve the semantic documentation conflict.

The queued shared-buffer M6 synthesis was cancelled before acquiring the exclusive lock; it produced no report. M6 area and its keep/remove decision, conditional M3 work, the remaining broad bank, shipping route, three resource re-records and the resource acceptance gate remain pending. Prepared shipping exports are not area evidence. Earlier unchanged-input MAAP results retain their provenance: 168 checks, 43/43 defects, and 216/216 measured lines.

`HANDOFF.md`, `PR-BODY.md`, `PROPOSED-DOCS.patch` and bounded receipts are updated in the assigned output directory. The unpublished PR draft uses `Relates to #696`. The tree is clean; seven local commits remain intact. No push. All launched jobs have finished or been cancelled.
