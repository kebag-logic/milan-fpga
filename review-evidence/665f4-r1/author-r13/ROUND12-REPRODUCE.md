[A560]

# Round 12 evidence reproduction

Candidate: `efea74858dffc482820d4f19c26c38796a57ff75`.
The checkout and dependency recipe is in `PR-BODY.md`.
All commands in `ROUND12-GATES.json` are argument arrays with their working
directories. Substitute the path aliases before executing them. The Markdown
command table displays those same arguments; its shell quoting is descriptive.

## Path aliases

| Alias | Meaning |
| --- | --- |
| `$SOURCE` | Candidate checkout, including its recorded active submodules. |
| `$SCRATCH` | Writable disk scratch; copy `round12-helpers/.` here. |
| `$BUILDER_TREE` | Builder audit snapshot at `$SCRATCH/builder-tree`. |
| `$COMPILER_TREE` | Compiler audit snapshot at `$SCRATCH/compiler-tree`. |
| `$ARCHIVE_TREE` | Tracked source archive prepared by `final_docs.py`. |
| `$MAILBOX_TREE` | Tracked mailbox inputs prepared by `mailbox.py`. |
| `$SDK` | SDK installed and verified by `scripts/ci_rv32_sdk.py`. |
| `$DOCS_ENV` | Environment containing repository documentation dependencies. |
| `$RUNTIME` | Verified runtime archives and their fresh provenance file. |
| `$PINNED_HDL` | Executable for pinned release 5.050. |
| `$PINNED_HDL_DIR` | Directory containing that executable. |
| `$PINNED_HDL_LIMITED` | Executable copy of `round12-helpers/verilator-j8`. |
| `$PACKET` | This evidence directory. |

`$BUILDER_SDK`, `$USER_HOME` and `$EARLIER_SCRATCH` in normalized evidence describe
original environment locations; they are not instructions to use those paths.
Builder receipts distinguish the ordinary selector from its pinned-SDK audit.
Runtime archive hashes and build provenance are in `ROUND12-SIZES.json`; use
`ctrl_image_runtime.py` to rebuild the archives when necessary, and regenerate
its provenance with the new artifact paths. No archive or toolchain is bundled.

## Helpers

Copy the small helper files to disk scratch before running them. Set and export
`SOURCE`, `SCRATCH`, `SDK`, `DOCS_ENV`, `RUNTIME`, `PINNED_HDL`,
`PINNED_HDL_DIR`, `PINNED_HDL_LIMITED` and `MILAN_RV32_CC`.
Set `TMPDIR` to that scratch directory. Run helpers from the candidate checkout
unless a receipt names a different working directory.

`run.py` writes a log, rc file and hashed JSON receipt. `launch.py` starts it with
`setsid nohup`; wait for the recorded process using foreground intervals of at
most 45 seconds, and do not finish while a job is running. The limiter reserves
two HDL build slots and rewrites inner `-j` requests to eight. Campaigns use four
workers. Keep service memory below 9 GB and free disk above 30 GB.

The portable helper copies use environment variables for installed dependencies;
`ROUND12-HELPERS.json` hashes those copies. The executed limiter's original hash
is recorded separately. Reviewer input hashes and public source commits are in
`ROUND12-REVIEW-INPUTS.json`.

`compiler_gates.py` serializes its audits with a shared lock and accepts an
existing successful receipt. Start with fresh scratch to rerun them. In this
round both audit worktrees freeze `7b47f333ecde4af16e32ca95730f56c3c454d0eb`.
The later candidate changes only the IF=1 mutation-selection prefix, outside
their inputs. The compiler bank ran concurrently in its own worktree; the
builder group waited for that same bank. The source receipt records this
one-file delta. The full campaign, coverage and final docs checks repeat at
the candidate head.

Every Round 11 gate label maps to its Round 12 counterpart in
`ROUND12-GATE-PARITY.json`. `ROUND12-DEVELOPMENT.json` preserves preliminary and
superseded attempts separately from final receipts. Gate success is test
evidence; independent verdicts and hosted acceptance remain separate duties.
