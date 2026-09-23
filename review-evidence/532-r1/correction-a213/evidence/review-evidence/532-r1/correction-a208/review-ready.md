[A208] REVIEW READY
Commit: `a37af3c6ad54aa16403861c969f68cf2a83679c6` (tree `9c3c735352d6cf986a4dd311538c605ab346c7b9`) on `532-act-parallel-slots`, three commits on top of `fcce541b`. It is local and unpushed: the manager pushes it to PR #533, whose head is still `fcce541b`.

Changed:
- `aad4a256` merges live dev `759da623` with no conflict. `CI_WORKFLOWS.md` auto-merged: #504's text is the RV32 SDK paragraph in the builder section, and the slot section is untouched. `scripts/check_baremetal_only.py` is dev's version as is, because the branch had not edited it. No dev change references the runner.
- The 29 findings at the merge are 27 in `scripts/act_ci.py` and 2 in `docs/testing/CI_WORKFLOWS.md`. One of the 27 is class R `/sys`, from `CGROUP_ROOT = pathlib.Path("/sys/fs/cgroup")`. Dev alone has 0 findings.
- `3874c454` clears 18 of the act_ci.py lines and both doc lines with no mask:
  - Prose (11 comments and docstrings plus 1 check label) and the 2 doc lines are reworded: "systemd" becomes "the service manager", "unit-property" or "unit"; "userspace NAT" becomes "socket-level NAT".
  - `systemd_property` is renamed `unit_property` (the def and 5 calls, a pure rename).
  - The fake host's DropInPaths fixture becomes `/run/drop-ins/50-MemoryMax.conf`. Only whether it is non-empty is read.
- `a37af3c6` masks the other 9 lines, in `scripts/act_ci.py` only:
  - `TERM_MASKS` gains `ACT_SLOT_TERM_MASK`, built from 7 `(before, literal, after)` exact source lines. Each is `re.escape`d and anchored `^...$`, and only the literal is removed, so the rest of the line is still scanned. The literals are the host executable `systemd-run` (tool inventory, 2 x `require_tool`, fake-host classify, 2 pinned golden argvs) and the dockerd value `native.cgroupdriver=systemd` (command and golden argv).
  - `HOST_RUNTIME_MASKS` gains one alternative next to #376's `/proc` entry: `(?<=^CGROUP_ROOT = pathlib\.Path\(")/sys(?=/fs/cgroup"\)$)`.
  - No other file, product document, ratchet, budget or class exemption changes, and the triplet allowlist is unchanged. The reason (#259's host-tooling non-goal, #376) is in the gate's docstring and comments, and in a new CI_WORKFLOWS.md paragraph after the slot resource list.
  - `_arms_act_slot_masks` adds 64 arms, 8 for each masked line: exact context (clean); then wrong context in the runner, glued literal, prefixed line, trailing text, second term on the line, wrong file and product document (all refused).

Validation at `a37af3c6`:
- `python3 scripts/check_baremetal_only.py --check`: OK, 0 findings across 847 files. The merge `aad4a256` before the correction had 29.
- `python3 scripts/check_baremetal_only.py --selftest`: PASS, 441 arms (dev 377).
- 12 mask mutants, all killed by the new arms: T and R removed; T and R context-free; T whole-line; T and R without the start anchor; T and R without the end anchor; T and R applied to every file.
- `python3 scripts/check_py_idiom.py` rc 0; `python3 scripts/check_sh_idiom.py` rc 0; `python3 scripts/docs_check.py` 0 findings; `python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9` 0 findings over 210 added lines; `python3 scripts/gen_toc.py --check` OK; `git diff --check 759da623..HEAD` clean.
- Also run: `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --verify-anchors` and `check_hygiene.py --check`, all rc 0.
- Candidate `act_ci.py --selftest`, under the bootstrap rule: run only inside a disposable, network-less rootless OCI container (only `lo`, no Docker daemon involved), from a staged clone of the exact commit. The image is ubuntu:24.04 plus python3, python3-yaml, git, sudo, procps, docker.io and gh; the self-test resolves the last four on PATH but never runs a daemon.
  - Head `a37af3c6` (act_ci.py sha256 `e1d614342e30162aae19a5ca8df7fe631784b61212e30dfa7f5ec6b034be276c`): PASS, 363 checks, 0 FAIL, as root and as uid 1000.
  - Control `fcce541b` (sha256 `6723826c...`, the previous receipt's digest): PASS, 363, in the same image, as root and as uid 1000.
  - The only check-label difference is the reworded uplink label.
- The previous author's 38 slot mutations each still apply exactly once to the new act_ci.py (checked statically). None touches a changed line.

Acceptance criteria: this correction changes no runner behavior (prose, one rename and one fixture value), so the #532 acceptance status stands as A203's REVIEW READY recorded it. Acceptance 1 (the live two-slot proof) still needs the audited install. The correction's own goal is met: the scope gate is green with literal, file-pinned, exact-line masks, no broad exemption and no ratchet growth.

Open risks/questions:
- The masks are line-exact. Reindenting or reordering any of the 9 runner lines, or adding a trailing comment, fails the scope gate until the context table is updated. That is fail-closed by design; reviewers should accept or reject the coupling.
- Please check the new wording for accuracy: "socket-level NAT" for pasta's translation onto host sockets, "the service manager" for the build host's unit manager, and "the host service manager as its cgroup driver" in CI_WORKFLOWS.md.
- No hosted or act evidence exists at `a37af3c6` until the manager pushes it. After the push, the trusted dev-runner replay's docs job should show 0 gate findings, 441 gate arms and 363 runner checks.
