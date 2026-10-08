[A560]

# Round 11 linked fixtures

Candidate: `803e8c3c9e7506c4f004d562437ae4f374fbad8e`.

| Shape / IF | Text | Read-only | Data | BSS | Reserved stack | RAM span | Delta round 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 / 1 | 45392 | 2878 | 0 | 23440 | 8192 | 79904 | +368 |
| 1x1 TDM8 / 2 | 46676 | 2878 | 0 | 34808 | 8192 | 92576 | +336 |
| 8x8 / 1 | 45444 | 2878 | 0 | 38200 | 8192 | 94736 | +512 |
| 8x8 / 2 | 46820 | 2878 | 0 | 64328 | 8192 | 122240 | +528 |

The runtime archives are the same hash-verified inputs used in round 10.
Static arenas are already part of BSS. Reserved stack is not a measured
call-chain bound. These opt-in fixtures are linked, not booted.
