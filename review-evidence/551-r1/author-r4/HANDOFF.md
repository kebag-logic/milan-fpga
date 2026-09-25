# [A315] History split handoff

Assignment: https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5832468673

PR: https://github.com/kebag-logic/milan-fpga/pull/553

Branch: `551-licence-real-grant`. Work remains local and unpushed.

## The two commits

1. `8dc98a429bd9918ad643fdb0051c2c9660395722`
   Subject: `Merge dev into 551-licence-real-grant`
   Ordered parents: `babb8925030612e47c687b1fda1a1ce614988721`, `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.
2. `f219a5edaa191b33acc8b77abd22469f8f0db1f9`
   Subject: `Require unwarmed refusal arm with admission controls and documentation`
   Parent: `8dc98a429bd9918ad643fdb0051c2c9660395722`.
   Holds the remaining original round content: mandatory unwarmed refusal, reverse-TSpec admission control, documentation and RTL comment updates. Ten files, 94 insertions and 131 deletions. No new content was introduced.

## Merge scope

The merge preserves the automatic merge and resolves only five marked blocks:

- `docs/reference/REGISTER_MAP.md`: two blocks.
- `hdl/milan/milan_datapath.sv`: two blocks.
- `tb/verilator/milan_dp/README.md`: one block.

Each replacement is an exact contiguous block from `9eee4383`. The resolved blocks preserve the real-grant licence qualification and the incoming processor behavior. The README conflict retains the notification/GSI coverage and licence coverage together.

Beyond the conflict hunks: **none**. No build repair was needed. Other automatically merged changes are inherited from the two parents.

An independent `git merge-tree --write-tree --no-messages` recomputation verified that only the three conflicted files differ from the automatic merge. Replacing exactly its five marked blocks reproduces the new merge's bytes. This used Git objects in the existing repository, without another checkout or a tree export. See `merge-scope-proof.txt`, `conflict-resolutions.json`, and `merge-remerge.diff`.

## Validation

Commands ran in the foreground, with no gate output piped.

On merge `8dc98a429bd9918ad643fdb0051c2c9660395722`:

```sh
rtk proxy timeout 3600s make -C tb/verilator/milan_dp crflic CRFLIC_MDIR=obj_crflic_a315_merge VERILATOR_JOBS=4
```

Exit 0; 253 checks, zero failures; `RESULT: PASS`. The build used Verilator 5.052 and a fresh object directory under the candidate checkout. Evidence: `merge-crflic.log`. The merge retains the original opt-in unwarmed arm; making that arm mandatory belongs to the following commit.

Whitespace gates, all exit 0 with no output:

```sh
git diff --check 8dc98a429bd9918ad643fdb0051c2c9660395722^1 8dc98a429bd9918ad643fdb0051c2c9660395722
git diff --check 8dc98a429bd9918ad643fdb0051c2c9660395722^2 8dc98a429bd9918ad643fdb0051c2c9660395722
git diff --check 8dc98a429bd9918ad643fdb0051c2c9660395722 f219a5edaa191b33acc8b77abd22469f8f0db1f9
```

At final head:

```sh
python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
```

Exit 0: zero findings over 197 added lines in seven Markdown pages; controls 339/339. Evidence: `em-dash.log`. The first attempt exited 2 because the default Python lacked `html5lib`. Installed the repository's exact hash-pinned `tools/markdown/requirements.txt` in `/tmp/milan-551-a315-markdown-rlktl6rp`, then ran the gate with that environment's `bin/python3` and a 600-second timeout. Evidence: `markdown-install.log`, `gates-initial.json`. No dependency or toolchain was placed in this output directory.

## Tree-equality proof

```text
Original commit: 9eee43831d487a52637d34d87a727f6e174e7cab
Original tree:   aca067d42122d785d8319d4d0926484dd9351568
Final commit:    f219a5edaa191b33acc8b77abd22469f8f0db1f9
Final tree:      aca067d42122d785d8319d4d0926484dd9351568
git diff --exit-code 9eee4383 HEAD: empty, exit 0
First-parent commits after babb8925: 2
Tracked worktree/index: clean
Submodule gitlinks: unchanged (mode 160000 and exact object IDs)
Submodule checkouts: unchanged from initial state
Local safety branch: keep-9eee4383 -> 9eee43831d487a52637d34d87a727f6e174e7cab
```

The content restoration used `git -c submodule.recurse=false checkout 9eee4383 -- .`. The staged tree was checked against T before committing; the committed tree was checked again afterward. All four gitlinks and actual submodule checkouts match the original state. See `initial-state.json`, `merge-state.json`, and `tree-equality.txt`.

Only the requested history split and targeted gates were performed. No push, PR edit, merge into dev, sub-agent, other checkout, or hardware operation occurred. No private transcript or other session's management directory was read. Final content is byte-identical to the supplied original head.
