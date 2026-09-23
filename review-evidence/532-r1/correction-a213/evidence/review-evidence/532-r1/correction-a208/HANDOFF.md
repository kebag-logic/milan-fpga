# [A208] HANDOFF: #532 / PR #533 correction round (scope gate masks)

Lane: `$LANES/532-act-parallel-slots`, branch `532-act-parallel-slots`.
The head is **local and unpushed**. PR #533 still points at `fcce541b`; the manager pushes.
The worktree is clean.

## Commits on top of `fcce541b` (one-line subjects, no trailers)

| SHA | Subject |
|---|---|
| `aad4a2564dbd548686a8e208d5b55f4758bee075` | Merge dev 759da623 into 532-act-parallel-slots (#532) |
| `3874c454d187a12cfa5d4e1c98f71fc039da2b80` | Reword the act runner's slot prose and rename its unit-property query so the retired-stack terms leave everything but pinned literals (#532) |
| `a37af3c6ad54aa16403861c969f68cf2a83679c6` | Mask the act runner's slot unit executable, cgroup-driver value and cgroup root only on their exact source lines, with arms per mask (#532) |

- Head tree: `9c3c735352d6cf986a4dd311538c605ab346c7b9`.
- `scripts/act_ci.py` sha256 `e1d614342e30162aae19a5ca8df7fe631784b61212e30dfa7f5ec6b034be276c`.
- `scripts/check_baremetal_only.py` sha256 `533c1205ccf39d3edd131d20759e4adceb16c5ba723165f8390347cf44405e51`.

## 1. Merge of live dev `759da623`

- It merged without a conflict.
- `docs/testing/CI_WORKFLOWS.md` auto-merged. Dev's #504 text is the RV32 SDK paragraph in the builder section, and the slot section is untouched.
- `scripts/check_baremetal_only.py` was not edited on the branch, so the merge takes dev's version (#504 SDK masks, #523 process masks) as is.
- No dev change references the runner.

## 2. The 29 findings, and what happened to each

The findings were measured at the merge `aad4a256` (`receipts/gate-findings-merge-aad4a256.txt`). Dev alone is clean: 0 findings over 846 files, 377 self-test arms.

The manager's count of 29 is right, but only 27 are in `scripts/act_ci.py`. The other 2 are in `docs/testing/CI_WORKFLOWS.md`. One of the 27 is the class-R `/sys` in `CGROUP_ROOT = pathlib.Path("/sys/fs/cgroup")`, which the manager's summary did not name.

| Disposition | Lines | How |
|---|---|---|
| Reworded prose | act_ci.py 150, 157, 159, 607, 622, 627, 3960, 4082, 4260, 10720, 11234 (check label); CI_WORKFLOWS.md 1741, 1760 | "systemd" became "the service manager", "unit-property" or "unit". "userspace NAT" became "socket-level NAT" (pasta translates the namespace's layer-2 traffic onto host layer-4 sockets). |
| Changed code, no mask | act_ci.py 4081 plus 4113, 4116, 4208, 4249, 4297 | `systemd_property` renamed to `unit_property`, the def and 5 calls, a pure rename. |
| Changed code, no mask | act_ci.py 10798 | The fake host's DropInPaths fixture changed from `/run/systemd/system.control/cap.conf` to `/run/drop-ins/50-MemoryMax.conf`. `release_slot_slice` reads only whether the value is non-empty. |
| Masked, class T | act_ci.py 172, 3966, 4002, 4037, 10730, 11238, 11253, 11270 | These carry the host executable `systemd-run` (tool inventory, 2 x `require_tool`, fake-host classify, 2 pinned golden argvs) and the dockerd value `native.cgroupdriver=systemd` (command and golden argv). |
| Masked, class R | act_ci.py 168 | `CGROUP_ROOT = pathlib.Path("/sys/fs/cgroup")`, the build host's cgroup mount used by the teardown absence proof. |

The mask mechanism:

- `TERM_MASKS["scripts/act_ci.py"] = ACT_SLOT_TERM_MASK`. It is built from `ACT_SLOT_TERM_CONTEXTS`, 7 `(before, literal, after)` triples. Each triple is `re.escape`d and anchored `^...$` as the exact source line. Only the literal token is removed, so the rest of the line is still scanned by every class.
- `HOST_RUNTIME_MASKS["scripts/act_ci.py"]` gains one alternative next to #376's `/proc` entry: `(?<=^CGROUP_ROOT = pathlib\.Path\(")/sys(?=/fs/cgroup"\)$)`.
- Nothing else is masked. No other file or product document, no ratchet or budget, and no class-wide exemption. The TRIPLET allowlist is unchanged.
- The reason is recorded in the gate's docstring and comments (#259's host-tooling non-goal, #376), and in a new CI_WORKFLOWS.md paragraph after the slot resource list.

The self-test arms are `_arms_act_slot_masks`: 8 literal lines, 8 arms each, 64 new arms in all (377 to 441).

| Arm | Expected |
|---|---|
| exact-context | clean |
| wrong-context in the runner | refused |
| glued literal | refused |
| prefixed line | refused |
| trailing text | refused |
| second term on the same line | refused |
| wrong file | refused |
| product document | refused |

All 12 mask mutants were killed (`receipts/gate-mask-mutations-a37af3c6.log`, driver `receipts/gate-mask-mutations.py`):

- T and R removed;
- T and R context-free;
- T whole-line;
- T and R without the start anchor;
- T and R without the end anchor (R twice);
- T and R unpinned (applied to every file).

## 3. Validation at `a37af3c6`

`receipts/local-gates-a37af3c6.log` and `receipts/extra-gates-a37af3c6.log`:

| Command | Result |
|---|---|
| `python3 scripts/check_baremetal_only.py --check` | OK, 0 findings across 847 files |
| `python3 scripts/check_baremetal_only.py --selftest` | PASS, 441 arms |
| `python3 scripts/check_py_idiom.py` | rc 0 |
| `python3 scripts/check_sh_idiom.py` | rc 0 |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9` | 0 findings over 210 added lines |
| `python3 scripts/gen_toc.py --check` | OK |
| `git diff --check 759da623..HEAD` | clean |
| extra: `check_doc_paths.py`, `check_doc_style.py`, `gen_toc.py --verify-anchors`, `check_hygiene.py --check` | all rc 0 |

### Candidate runner self-test (bootstrap rule)

The candidate runner was never run on the host. Its self-test ran only inside disposable, network-less rootless OCI containers (the container saw only `lo`), and no Docker daemon was used. The helper is `run-selftest-podman.sh <rev> <label> [<uid:gid>]`: a staged clone at the exact commit is mounted read-only and copied inside. The image is `image/Containerfile`: ubuntu:24.04 plus python3, python3-yaml, git, sudo, procps, docker.io and gh. The runner's self-test resolves sudo, docker and gh on PATH, which is why they are installed; it does not use a daemon.

| Rev | User | Result | Receipt |
|---|---|---|---|
| `fcce541b` (control; act_ci.py sha256 `6723826c...`, the same digest as the previous author's receipt) | root | PASS, 363 checks | `receipts/selftest-base-fcce541b.log` |
| `fcce541b` | uid 1000 | PASS, 363 | `receipts/selftest-base-fcce541b-uid1000.log` |
| `a37af3c6` | root | PASS, 363, 0 FAIL | `receipts/selftest-head-a37af3c6.log` |
| `a37af3c6` | uid 1000 | PASS, 363, 0 FAIL | `receipts/selftest-head-a37af3c6-uid1000.log` |

The only check-label difference between base and head is the reworded uplink label.

The previous author's 38 slot mutations (`$REVIEWS/532-a203-packet/mutation-run.py`) were checked statically: each substitution still applies exactly once to the new `act_ci.py`. They were not re-executed, because none of them touches a changed line.

## Public trail

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5798070616
- Manager source validation: https://github.com/kebag-logic/milan-fpga/pull/533#issuecomment-5797709398
- [A208] REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/532#issuecomment-5798338195

## What the manager must do

1. Push `532-act-parallel-slots` (head `a37af3c6`) to PR #533.
2. Run the trusted act replay with the dev runner at the new head. Its docs job runs the scope gate and the candidate's `--selftest`: expect 0 findings, 441 gate arms and 363 runner checks.
3. The rest of A203's handoff is unchanged: audited install, then the live two-slot proof for acceptance 1.

## Open risks and questions

- **The masks are line-exact.** Reindenting or reordering any of the 9 runner lines, or adding a trailing comment, fails the scope gate until the context table is updated. That is fail-closed by design, but it is a maintenance coupling that reviewers should accept or reject.
- **The new wording needs checking for accuracy:** "socket-level NAT" for pasta, "the service manager" for the host's unit manager, and "the host service manager as its cgroup driver" in CI_WORKFLOWS.md.
- **Workstation side effect, my error.** The teardown ran `podman image prune -f` on the rootless container store. Besides my two superseded builds, it removed 25 images that were already there: 3 untagged top-level images (`add2d079da02`, `faf1a2a85d00`, `215c2e01d65c`, about 2 weeks old) and their 22 intermediate layers. All were untagged and no container used them. No tagged image (for example `avb-introspection:verify/latest`), container, Docker daemon object, lane or checkout was touched. The removal log is `receipts/prune-removals.txt`. They cannot be restored; if any of them is still needed, it has to be rebuilt.
- The disposable image and the pulled base were removed (`receipts/teardown.txt`), and so were the scratch clones under `/tmp`. To reproduce, rebuild from `image/Containerfile` with `podman build -t localhost/a208-selftest:ubuntu24 image/`.
