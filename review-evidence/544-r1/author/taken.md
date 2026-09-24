[A286] TAKEN
Branch: `544-macro-sample`, base `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
Authoritative references: #544 decision (comment 5822485498), gate 1b and its cost table, PR #535 reviews R272-1 and R273-1.
Interpreted scope: protect the identity sample between its read and mismatch guard, preserving existing verdicts and reporting R273-S3 without fixing it. Reviewers: internal [R316], external [R317].
Validation plan: full builder with the pinned compiler and with cross compilers absent; documentation gates in both inventory modes; bare-metal, style, path, idiom and diff gates; reason-pinned mutations and disconnected-check controls.
Decision clarification pending: both published hostile macros use a parameter `x` in the replacement list, then pass `id` at the call. A literal-only replacement-list check cannot refuse them without a compiler. The author has requested clarification on also refusing the sample passed to a used macro parameter. Baseline probes accept both hostile cases and R273-S3 in both modes. Compiler-side implementation can proceed independently.
