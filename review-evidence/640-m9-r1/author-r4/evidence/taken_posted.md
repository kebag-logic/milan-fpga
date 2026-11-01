[A720d] TAKEN
Branch: 640-mark2-charter (round 4 on PR #828, from head 69fd18f1; local, not pushed by this lane)
Authoritative references: R757-3 and R758-3 on PR #828; this issue's 2026-10-31 body and comments; #665 and #823 bodies and 2026-10-31 comments; NFR-REL-03 and NFR-LAT-03; the cited IEEE 802.1AS-2020, IEEE 1722-2016 and Milan v1.2 clauses
Interpreted scope: docs only. Close every round-3 finding and residue. A header that fails its read-back is invalidated before any save appends to the old slot, with the power-cut table, NFR-REL-03 and the host flash model extended to that case. The conversion-error bound counts the PHC offset drift from stamping to arrival. The merge placement rule keeps every copy, clean or tu, inside the render buffer and counts it once, and tu on both networks is stated against Milan v1.2 4.4.2.3. Apply the residue fixes. Merge live dev before the gates.
Validation plan: every step of the docs workflow on the committed head, each rc recorded; git diff --check against the merge base; the merge and host flash models rerun with the new cases and mutants.
Blockers: none
