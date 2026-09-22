[A180] Repeat warning flags in the pp_top VID fixture CFLAGS group

## Status

Local unpublished author commit. Manager validation and independent R252/R253
reviews are pending; this draft is not an approval.

## Description

The supplementary VID-fixture CFLAGS group omits the warning flags required
by the parent's per-group checker, although the common CFLAGS already
enable them. Repeat `-Wall -Wextra` in that group so it satisfies the existing
policy. The fixture macro, value and all recipes and scenarios are preserved.

Closes #102.

## How to reproduce

Use the immutable parent `scripts/check_cpp_idiom.py:cflags_missing` at
`483a133ed08867ea0d300d2b4a027b5b48a4282f` on the base pp_top Makefile:
it returns `['-Wall', '-Wextra']`.

## How to validate

Run the same checker on the corrected file, expecting `[]`. In separate
disposable copies remove each newly repeated flag, expecting exactly that
flag. Build and execute the full pp_top default/fixture recipe with verified
Verilator 5.050 and at most eight compile jobs, including fixture guards.
Run donor lint and `make check`; publish author results as an evidence
comment. Complete manager-owned full native/hosted gates, independent
five-lens reviews, current-main candidate validation and containment.

## DoD

- [x] One-line fix; fixture/default/Domain contracts and parent policy preserved.
- [x] Real checker and both single-flag negative controls pass.
- [ ] Manager complete donor native and hosted bar.
- [ ] Independent R252 internal Codex and R253 external Opus positives.
- [ ] Current-main candidate validation and post-merge containment.

No parent pin adoption is authorized by this donor fix.
