Run from the exact reviewed checkout, with the packet in a separate directory.
The host C/C++ compiler, GoogleTest/GoogleMock and gcov must be available.
Initialize the four active submodules at their recorded gitlinks.

For focused.py and replay.py, supply `--repo "$PWD" --packet "$PACKET"`.
Generated trees and objects go under packet scratch.

1. Run `focused.py --interfaces 1 --mode baseline --jobs 3` and its IF=2 variant.
2. Run `focused.py --interfaces 1 --mode mutants --jobs 3` and its IF=2 variant.
3. Run `focused.py --interfaces 1 --mode asan --jobs 3` and its IF=2 variant.
4. Run `replay.py --interfaces 1 --jobs 3` and its IF=2 variant.
5. Run `python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4 --lwsrp third_party/lwSRP --keep "$PACKET/scratch/coverage"`, with TMPDIR under packet scratch.
6. Run `public_audit.py --packet "$PACKET" --jobs 4` for immutable receipt verification.
7. Run `integrity.py --repo "$PWD"` after all checks.

Each check exits zero only for success. Mutation logs intentionally contain
named failures; compilation failure cannot count as a mutation catch.
Independent invocations may run concurrently under a foreground orchestrator
that waits for every child, with total compilation concurrency at most 16.
The review used four three-worker campaigns initially, then two three-worker
sanitizer runs beside a four-worker coverage run. No shell job was detached.

Documentation commands are recorded in docs.json and its corrected/final
companions. Successful idiom commands take no --check option. The em-dash
gate requires tools/markdown/requirements.txt in a scratch-only environment.

Published logs normalize source/packet directory prefixes to $SOURCE/$PACKET.
Raw copies stay under scratch. receipts/publication-normalization.json records
raw and published hashes. No pass/fail diagnostic is changed.
