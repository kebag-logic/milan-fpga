# Receipt conventions

`INDEX.md` is generated from the files present after sanitizing. Its byte counts and hashes describe the published copies.

`budget/raw-manifest.json` describes the original local artifacts: original size and SHA-256, whether copied, and the stored relative name for copies. After sanitizing, copied entries also record the stored copy's size and SHA-256. Large raw traces are omitted; their owner extracts contain only PARTICIPANT bindings, LeaveAll ENTRY records and final verdict lines, plus raw size and SHA-256.

Host directory prefixes and account identifiers are replaced by placeholders. Remaining matches of the repository's documentation privacy rules are redacted. No cycle count, timing value, exit status or verdict is altered. Receipt scripts carrying placeholders require those placeholders to be bound to local directories before reproduction.

The optional save-second process was deliberately cancelled outside this round's required two-group phase regrade. Its cancelled combined attempt is labelled separately and is never counted as a gate pass. The required product-MAC groups have their own regrade log and rc. Known 8x8 STATED cost failures remain rc 1; passing LeaveAll checks do not turn those whole legs into passes.
