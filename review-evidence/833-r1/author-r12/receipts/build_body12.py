import sys, re
src, gate, out = sys.argv[1:4]
t = open(src).read()
def sub(old, new):
    global t
    assert t.count(old) == 1, old
    t = t.replace(old, new)
sub("[A726k]\n", "[A726l]\n")
sub("- **[Definition of Done](#definition-of-done)**",
    "- **[Round 12](#round-12)** — Dev sync only: dev `cc204c6f` merged with no conflict, the documentation inventory regenerated, and the gates.\n- **[Definition of Done](#definition-of-done)**")
sub("head `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea` (round 11). Round 11's gates are in [Round 11](#round-11).",
    "head `3e475161e528baa655a5ba84d6a38d78f8c64f3b` (round 12, dev `cc204c6f` merged). Round 12's gates are in [Round 12](#round-12).")
sub("Rounds 2 to 11 change only files round 1 changed, so the sweep was not rerun.",
    "Rounds 2 to 11 change only files round 1 changed, so the sweep was not rerun. Round 12 merges dev and regenerates the generated inventory page. It did not rerun the sweep.")
sub("`[A726k]` (round 11)", "`[A726k]` (round 11), `[A726l]` (round 12)")
sub("git diff --check origin/dev...HEAD\n```",
    "python3 scripts/docs_inventory.py --check\ngit diff --check origin/dev...HEAD\n```")
sub("`RESULT: PASS`; `git diff --check` silent.",
    "`RESULT: PASS`; `documentation inventory: OK`; `git diff --check` silent.")
sub("Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 11 gates](#round-11-gates); `behave` 2330 steps passed. The full sweep ran in 4 shards, rc 0, at round 1's head.",
    "Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 12 gates](#round-12-gates). At round 11's head, `behave` passed 2330 steps; it was not rerun in round 12. The full sweep ran in 4 shards, rc 0, at round 1's head.")
sub("- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at this head:",
    "- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at round 11's head `5843d1af`, not re-measured on the round 12 merge:")
r12 = open(gate).read()
sub("## Definition of Done", r12 + "\n## Definition of Done")
open(out, "w").write(t)
print(len(t))
