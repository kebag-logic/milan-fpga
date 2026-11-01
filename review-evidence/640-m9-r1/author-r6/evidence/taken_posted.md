[A720f] TAKEN
Branch: 640-mark2-charter (round 6 on PR #828, from head 270866ec; local, not pushed by this lane)
Authoritative references: R757-5 and R758-5 on PR #828; the manager's round-6 assignment, which takes R758-5-F1's second outcome; Milan v1.2 Annex D.2; IEEE 802.1BA-2011 6.5
Interpreted scope: docs only, one page. Condition "conversion error never shifts a sample" and the Annex D.2 claim on a valid head. State that a margin under 125 us lapses the head every packet, so interleaved copies can land one sample apart. Add that as an open design item for lane 6 with its verification, the reviewer's published probe as its starting case and its size only as that probe's result. Apply residue RR8 and R758-5-R1, RR9 and RR10. The merge rule does not change.
Validation plan: every step of the docs workflow on the committed head, each rc recorded; git diff --check against the merge base.
Blockers: none
