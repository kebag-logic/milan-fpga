[A172] REVIEW READY - bounded correction; acceptance remains open

Commit: `b5e6c23e1b9802b5cacbc62db212064d7e429862`
Tree: `2fd42873a06123f87f539c116e4969c87f5e33d8`
Branch: `437-container-paragraph-scopes`; clean, local only, not pushed.

Corrected the named R237 F1/F3 and R238 F1/F2 counterexamples. Live-item tags retain paragraph context; outside tags retain opening; dedented quotes/footnotes release context. Added observable marker controls and exact public regression inputs. P01/P04 first-paragraph counterparts also agree. These are corrected-but-unreviewed claims, not reviewer-confirmed resolutions. Original severities and all lenses stand.

Validation: TOC 909/909, check 105 pages, anchors 144; em-dash 254 arms and zero findings against dev `52711029f374650dc93830d5ea28e81cb5c8f410`; 197 real-Git/navigation controls; 23 mutants rejected in both consumers at named arms; 25 focused docs/idiom/hygiene/source gates exit 0. Narrow fake-marker mutation fails exactly the three indented-closer controls in both consumers (TOC 1, em-dash 2), not thematic/ordinal arms. All 707 old arms and 428 #507 closer arms preserved. All three 163-page corpus populations classify identically under baseline/starting/corrected walks. No budget or exemption/provenance decision change.

AC1 remains UNPROVEN: R237 F2 historical correspondence is open. Nine descriptions do not establish all eleven original IDs. Additional outside-tag/unclosed-comment mismatches remain open for manager decision ([exact observation](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5778541581)). Optional R238 F3 is not adopted; #495 residues remain explicitly measured and documented.

Reproduce the source checks with `rtk proxy python3 -B scripts/gen_toc.py --selftest`, `--check`, `--verify-anchors`, and `rtk proxy python3 -B scripts/check_em_dash.py --selftest`. The correction packet holds exact synthetic renderer requests/responses, real-Git bytes/diffs, isolated mutation sources/logs, per-finding response, all command exits and full reproduction scripts.

Disjoint integration proof: [comment5778317377](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5778317377); integration commit `3003bee2a33a6ae2f650ec7bd54fb7730d82086f`, tree `8327dfa5387e01988c567b952b3a2f9f123b7a8c`. Complete original issue patch preserved byte-for-byte before correction.

Manager owns full native/act/hosted/current-candidate bars, source publication, independent R237/R238 re-review, remaining acceptance decisions and eventual authorized merge/containment. No source push, PR metadata change or self-approval. Stopping at this head.
