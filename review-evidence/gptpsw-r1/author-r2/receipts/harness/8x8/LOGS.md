# The 8x8 gPTP legs' raw logs (not copied: over 200 KB each)

| Log | Bytes | sha256 |
|---|---:|---|
| backlog-adp.log | 11808521 | 6004251f4b45e89248343b0952b07cd8985342e153a4a15dbf3dea75a68bea0b |
| backlog-adp-refill.log | 11928223 | 2a91a30592f6a4c9563aafd30ca6795744af53f5936de7ce4e993815702b33ad |
| backlog.log | 11547153 | be933841d457960bb810ce869c4e48f1c8d45fdf02fa57bae0b85a1a45b3118f |
| backlog-owed.log | 12022160 | 83cfeef31c436208232204d83c2f7db0559f654969ad95f0e00e18388c90f43d |
| gptp-master.log | 7107663 | 19cf3196d89d77b5bda39f23d7d4dfafb29d6349d273e468e62b932f963211cc |
| gptp-slave.log | 7102668 | 6b456b64dacbeaa448c4ab515d3de5855391ff484a4606304a637a44be7ae407 |

Built and run at `0e476c94` from a clean clone: `leg.sh <clone> <build> 8x8 <groups> --with-gptp` (bin/leg.sh), MAKEFLAGS -j8 on 8 booked CPUs.
