[R639] NEGATIVE - exact head 4391f353690972f4844cb641b1e77fa94f38cdf4

Independent pass recorded before reading prior public findings. This records the reviewer-owned initial verdict, not completion of reconciliation or gate execution.

F1 MAJOR, Conformance/Robustness/Tests/Docs: target-specific Make variables incorrectly override command-line variables at scripts/ci_make_walk.py:374. A pristine-census fixture accepts both --write and --check while real Make selects the hidden script. Guide claims real override precedence.

F2 MAJOR, Conformance/Robustness/Tests/Docs: traversal memoization omits incoming environment at scripts/ci_make_walk.py:403 and scripts/ci_command_table.py:146. Two literal invocations with distinct exported values are accepted, although the second reaches an unclassified command. Neither the committed census nor the command table was modified. This is a resolved literal input, not unknown runtime assembly.

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | issue 737 image assignment and round-five ruling; inventory and both walkers; independent-probes.json | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| RTL | CLEAN | full diff contains no RTL/workflow/gitlink changes; Entity shape 228 checks; pp_srcs check and self-test; Dockerfile/compiler pins and source declarations | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Robustness | UNCLEAN | unknown-node controls, drift controls, image archive/privacy/lock controls, independent literal scope probes | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Tests | UNCLEAN | all three inventory suites pass, independently planted accepted escapes; image smoke source and public receipts; grouped builder union verified | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |
| Docs | UNCLEAN | CI_IMAGE.md census promises override and scope semantics that the probes disprove; rebuild, source closure, environment and privacy sections read | R639-5 | 4391f353690972f4844cb641b1e77fa94f38cdf4 |

Image exports independently hashed equal; full archive scan authenticates manifest, configuration, all fourteen compressed/uncompressed layer identities and pinned upstream privacy provenance. Shipped controls pass under extracted CPython 3.12.3. Full permitted workflow-step campaign remains in flight. Prohibited banks and orchestration, image runtime, hosted acceptance and merge-candidate work remain explicit limits.
