# Issue423 readiness evidence

No production implementation or proof adoption. Never merge this archive branch. The current checker at parent dev b17580b91deb11f3441dfc5d7f9fafe539d929b8 is invoked unchanged.

The public motivating merge is a two-parent no-fast-forward merge: first parent is an ancestor of second, and its tree equals second. Both the original issue base and live donor main still report the three original commits stranded. A portable offline fixture reproduces that refusal. It also proves that merely ignoring such a merge and using the existing historical linear-replay helper would accept both a legitimate later extension and a later exact revert. The latter conflicts with proposed issue423 AC3, so this shortcut is not adopted and the task remains Backlog for independent readiness/design review.

Reproduce from any scratch location: python3 probe/probe_ff_merge.py /path/to/clean-parent-checkout/scripts/check_merge_containment.py . The instrument creates only a disposable Git fixture, reads the checker unchanged, and reports current verdicts plus existing helper results. Commit identities vary with execution time; the topology and outcomes are the assertion. MANIFEST.json records original and path-neutralized published hashes. No private reasoning material is included.
