# Fresh validation receipts

These receipts describe head `bc89c6c1c6289cb286a39406413ebc1c742d7745`.
All runs were started after the host crash. Earlier root-level M4 receipts
and the old root-level scratch index are historical and do not clear a gate.
The packet manifest proves file integrity, not acceptance or review approval.

`PROVENANCE.json` records raw source sizes and SHA-256 values alongside the
sizes and SHA-256 values of the published, redacted bytes. Paths and host
identifiers are replaced only in the published copies. Hashes in the packet
manifest refer to those published copies. `SCRATCH-ARTIFACTS.json` records
large or raw artifacts retained outside the packet.

`maap-default.log` includes the unit run and the complete mutation campaign.
Every planted defect must build, exit 1 and fail its named check. Abnormal
termination does not satisfy that criterion. Forty-one defects and two clean
controls are graded. Coverage uses the matching pinned 5.050 coverage reader.
The current coverage receipt is `gate-coverage-final.log`.

`static-results.json` gives the fifteen commands and statuses.
The documentation commands use an installed documentation environment;
`python3` in the portable command list denotes that interpreter.
`source-integrity.json` binds tracked bytes and required submodules to commits.
`commits.json` lists the five local commits and their changed paths.

`area/measurement.json` identifies the recipe, device, geometry and threading.
The attribution scope is the `g_maap.maap_engine` hierarchy row in the
whole-datapath 1x1 OOC result. Both that row and the whole-datapath row are
preserved. Cumulative input hashes and patches bind each item to its result.
These are attribution reports, not the shipping resource gate's three endpoints.

The fresh baseline synthesis completed successfully before a report-parser
failure. The parser was corrected and read those same fresh reports; its
zero-second parsing entry is not a synthesis runtime. No pre-crash result
was reused. Every synthesis has a separate `run.rc` receipt.

To reproduce area attribution, supply clean base and lane worktrees, a new
disk-backed work directory, the installed synthesis executable and the shared
synthesis lock to `area/reproduce.py`. Run no other heavy lane work beside it.
The helper uses the unchanged repository recipe and limits synthesis and
general threads to one. It returns 3 if the final MAAP growth exceeds the
assigned +60 LUT or +60 FF ceiling; each successful synthesis itself returns 0.
The final handoff, rather than this receipt index, records the resulting decision.
