[R533] NEGATIVE - exact head 42a0371affceb2a07a734449d706be01fa5abc9a

Independent delta pass completed before reading prior public findings. Final prior-finding disposition and integrity receipts are being assembled.

R533-2-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs
Artifact: sw/firmware/ctrl/srp/srp_mbx.c:306, :315, :510; sw/firmware/ctrl/test/srp_mbx.cpp:568; sw/firmware/ctrl/srp/README.md:47.
A successful replacement of the lowest-index shared binding clears its cached declaration while the shared Applicant retains Ready. When every binding is ineligible, reconciliation compares zero against zero and fails to withdraw the shared declaration. Independent IF=1 and IF=2 probes observe Ready renewals at 1000 ms and 2000 ms, no Lv. IEEE 802.1Q-2018 35.1.2.2 and issue #665 comment 6033558691 require the shared declaration to reflect all accepted bindings. Preserve shared state through replacement and verify actual withdrawal on the wire.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Milan 4.2.7.2.2, IEEE 802.1Q-2018 35.1.2.2; srp_mbx.c; wire probes | R533-2 | 42a0371affceb2a07a734449d706be01fa5abc9a |
| RTL | UNCLEAN | srp_mbx.c shared Applicant ownership; eight merge-conflict resolutions; unchanged F4 RTL | R533-2 | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Robustness | UNCLEAN | link fence/recreate tests; shared-binding replacement probe | R533-2 | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Tests | UNCLEAN | srp_mbx.cpp, srp_walk.cpp, srp_latency.cpp; four killed mutations; missing rebind observable | R533-2 | 42a0371affceb2a07a734449d706be01fa5abc9a |
| Docs | UNCLEAN | SRP README binding contract; size fixture and public ROUND2-SIZE.json | R533-2 | 42a0371affceb2a07a734449d706be01fa5abc9a |

Baseline SRP suites, selected processor wire differentials and desk latency checks pass for IF=1/2. Largest-shape RV32 object checks pass. Four independently planted defects were caught. No source was edited. This is a source review; full banks, hosted acceptance, final candidate and hardware proof remain outside this execution.
