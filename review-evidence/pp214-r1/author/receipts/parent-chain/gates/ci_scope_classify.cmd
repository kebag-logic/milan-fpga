bash -c git diff --no-renames --name-only 604899c08ff1cd1830e1dd08b733109ef852400c HEAD | tee /dev/stderr | python3 scripts/ci_scope.py
