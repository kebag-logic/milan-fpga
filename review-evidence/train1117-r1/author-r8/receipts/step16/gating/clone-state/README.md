# The gating builds' clones: at `8c5e2b4f` and clean (R865-4-F2)

`tools/gating_clone_state.sh 8c5e2b4f0a487690cf0168f08b55e7f7be91a09c` covers each gating chain's clone (`gate15/clones/g1x1`,
`g8x8`). For each it prints:
- **now:** `git rev-parse HEAD` and `git status --porcelain`, untracked files included;
- **then:** the head and porcelain lines the chain wrote into its own log as it ran. These are at the clone
  (`clone.sh`: `porcelain 0`), the boot simulation (`boot.sh`), the prep before and after (`gprep.sh`) and the Vivado
  build (`gbuild.sh`).

Every head named is `8c5e2b4f`, and every porcelain is empty: `gating-clone-state.log`, rc 0.
`gating-clone-state-plant.log` holds two planted controls, both refused:
- a wrong expected head;
- a copy of the 1x1/1if chain log whose prep left an untracked file.

The bitstreams these builds made, and their loaded firmware against the final head's product images, are in
`../loaded-identity/`.
