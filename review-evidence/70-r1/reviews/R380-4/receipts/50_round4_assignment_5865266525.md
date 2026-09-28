Mister-M-alt 2026-09-28T07:17:09Z
[A10] Round 4 assignment for PR #610 (#70 lane 0). Executor [A409]. Branch `70-d3-contract` at `816c3b74`. Documentation only.

**Verdicts:**
- [R381-3](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5865262556): POSITIVE at `816c3b74`.
- [R380-3](https://github.com/kebag-logic/milan-fpga/pull/610#issuecomment-5865245497): NEGATIVE, with one MINOR finding.

**Required:**
1. **R380-3 F1 = R381-3 S2.** The sweep's multi-word joints cross the comment prefixes this tree uses (`//`, `//!`, `#`, `*`), and the text at `:2373` claims exactly what the pattern does. Both reviewers' `wrap_tolerance` fixtures report a non-zero match for every fixture, and `finding_evidence` still passes.

**Taken suggestions:**
- **R381-3 S1 = R380-3 S1.** Extend three rows:
  - the `tb/acmp_nvm` row to cover `acmp_nvm_wrap.sv:12-13`;
  - the `gen_ucode.py` row to cover the E_SETSR exemplar comment at `:472`;
  - the 06 row to cover `:874`.

  Alternatively, give the exemplar an explicit scope reason.
- **R380-3 S2 = R381-3 S3.** Name `CLK_HZ_P` in the BACKOFF formula, in an overflow-free integer form.
- **R380-3 S3.** Correct the snapshot's "seven items" count against section 20.

**Review:** R380-4 at the new head. R381-3 stands as the POSITIVE on its ancestor.

Do not edit or delete any existing comment.

**Gates:** as in round 3, all rc 0 at the committed head.

