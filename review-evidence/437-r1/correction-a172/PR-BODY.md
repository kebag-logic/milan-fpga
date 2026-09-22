[A172] Proposed draft PR body; not applied to GitHub

A tag within a live list paragraph could incorrectly start an HTML block, dropping real headings or swallowing fences/comments/pre blocks and inventing headings. Dedented quotes and footnotes could also retain a stale list context. This change fixes those decisions and adds both navigation and real-Git provenance controls from the public review counterexamples.

At `b5e6c23e1b9802b5cacbc62db212064d7e429862` (tree `2fd42873a06123f87f539c116e4969c87f5e33d8`), TOC selftests pass 909/909 and em-dash selftests pass 254 arms. The tracked corpus and all 707 prior arms remain unchanged; 23 isolated mutants fail named controls in both consumers. No budgets or exemption/provenance policy change. Exact focused validation and receipts are in the correction packet.

Acceptance is incomplete: R237 F2 remains open because the nine determinable historical descriptions do not account for all eleven IDs. Additional unclosed-comment/raw-HTML rendered-output mismatches remain publicly recorded for manager decision. Optional item-HTML termination work remains outside this correction under #495. All five selected heading omissions remain documented. Named corrected findings still require independent re-review; no lens or finding is author-cleared.

Full native, act, hosted, current-candidate, review and merge bars remain manager-owned. This body is a proposed handoff artifact, not a ready/approved status claim.

Closes #437
