[R617] NEGATIVE - exact head 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3

Independent verdict recorded before reading any other reviewer's findings or report.
All five lenses have been applied. Prior-public-finding reconciliation and final packet integrity checks remain pending in this interim report.

R617-F1 — MAJOR — Conformance, RTL, Tests, Docs — OPEN.
Issue #35's frozen acceptance requires no bank write for a refused frame. No maintainer/manager comment retrieved from that issue changes that requirement. The scope comment requires one drop/no event and the subsequent ruling accepts the one-mux hierarchical difference; neither explicitly waives the bank-write requirement.
At hdl/wire/KL_gptp_rx_parser.sv:452 and :645, bank_we_o is qualified by old bad_r and the new latch takes effect after the flagged byte. Earlier and same-byte writes remain. The new header at :60-62 and PR acceptance replace zero writes by zero later writes. The new feeder at tb/verilator/parser/sim_main.cpp:267 snapshots its baseline after the flagged edge, so its :1262 assertion deliberately ignores those writes.
The reviewer-owned bank_contract.cpp measurement at head returns 24 checks: 12 PASS, 12 FAIL against the literal frozen requirement. Clean controls dispatch for all four required types. Sync flagged at byte 29: drops=1, events=0, writes_before=0, writes_on=1, writes_after=0; at byte 40: one prior write; at EOF byte 57: five prior plus one same-byte write. The other three types also violate total-zero writes. Artifact: receipts/bank_contract/result.csv and run.rc (1).
Impact: the repair meets refusal and drop-count behavior, but the published checked acceptance is weaker than the issue's requirement. This is an acceptance/test/contract mismatch, not a demonstrated shipping-path regression: the parent ties the port low and no event exposes a refused frame's bank.
Required outcome: implement and test the frozen bank-write requirement, or obtain an explicit public scope ruling accepting speculative writes before/on the error edge, then align the issue, header, port guide, PR acceptance and regression to that ruling. This is not wording-only residue because it changes the required observable behavior and test oracle.
Verification: directed first/middle/EOF pulses for all four types count all bank writes, distinguish before/on/after the flag, and agree with the approved contract; one drop/no event, recovery controls and named mutation kills remain required.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R617-F1) | issue35.json; issue35_comments.json; frozen scope; parent tie-off; source.diff; bank_contract result | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| RTL | UNCLEAN (R617-F1) | parser latch ordering, EOF decision, valid gating, bank writes, engine banking, tied/free parser equivalence | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Robustness | CLEAN | independent 57-check probe; eight layouts; pulses, held/multiple errors, gaps, zero-gap adjacency, runts, stray bytes, recovery | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Tests | UNCLEAN (R617-F1) | all four donor gates; 298-check parser; seven named mutants; four independent reapplications and additional mutants; feeder oracle | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |
| Docs | UNCLEAN (R617-F1) | README and current role guides; header/port contract; source evidence anchors; parser README; PR body; public author receipts | R617-1 | 5b4ce3974f7627d57b31167bde50cde8f4bdcdf3 |

No other independent finding is established. All required donor gates passed. The parent hierarchical 3567 -> 3568 (+1 mux) is accepted by the public ruling; 2432-cell flattened statistics and ROM digests match. Raw netlist file hashes differ, so those raw hashes are not a byte-identity proof. Independent parser equivalence with rx_err tied low proves all 749 comparison cells; with the port free bad_r remains unproven. This is parser-only proof, not an executed parent bank.

There is no manager source-head bank. Current-dev candidate builder/native banks, hosted acceptance, parent adoption and merge remain manager duties. Exact-head source check/workflow queries returned zero entries. Physical calibration NOT RUN; field skips are not hardware proof. No source fixes, commits, pushes, GitHub writes or parent banks were performed in this resumed pass.
