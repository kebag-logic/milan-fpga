bash -c $'for c in 84f6d6a 03862f75c89e5c1d84baa4735eff1c1c6f796e25; do git ls-tree -r $c | grep -v "\tdocs/" | sha256sum; done' (cwd scratch/clones/gates)
