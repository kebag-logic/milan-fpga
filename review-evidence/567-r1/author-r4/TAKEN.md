[A335] TAKEN

Branch: `567-pp-pin-0922e434`, starting at `54b4c3bbbc8cdea5ced0be29c9226fdf82233b74`.
Authoritative references: [Round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845507642), [R327-1](https://github.com/kebag-logic/milan-fpga/pull/569#issuecomment-5845505218), CONTRIBUTING.md and REQUIREMENTS.md Section 8.
Interpreted scope: correct F1's restore instruction, clarify S1's exact-pin ledger requirement, and prepare the complete revised PR body locally for S3. R327 owns the delta review; S2 is tracked separately in #571.
Validation plan: old-pin search, documentation checks in both CI modes, em-dash check against `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, prose style, contents, anchors, cited paths and whitespace checks. Every assigned gate must return 0.
Wording adaptation: S1's assigned sentence contains 11 words, exceeding the style gate's maximum of 10. The same exact-pin requirement is expressed as two sentences: "OOC synthesis requires ledger rows for the pin of record. Rows must match that exact pin."
Blockers: none.
