# The head's linked images against the legs'

`ctrl_srp_image.py --with-aecp --layout split` (arm A; at 8x8/2if with `--ledgered-point 8x8-two-interfaces`, as the harness's build names it) at `51fa5f18`: without the drafts by `scripts/images.py`, with both drafts staged by `scripts/build_image.sh`. Against the image each leg at `db77201b` linked. Since `db77201b` the image builder's `main` moved its memory-primitive check into a helper (`51fa5f18`).

| Point | Drafts | Head, sha256 | Leg | Leg, sha256 | Same |
|---|---|---|---|---|---|
| 1x1/1if | no | `dc27389d3e8876f3d58b51bd2f097af931ade0e4f84f21dbbac4bd63b8be8b9a` | N10-A1 | `dc27389d3e8876f3d58b51bd2f097af931ade0e4f84f21dbbac4bd63b8be8b9a` | yes |
| 8x8/2if | no | `f80111d8fa4a09dd5fcda5cea8e90de05a7e90def81f48328e4af73eb93e3f7f` | N10-A8 | `f80111d8fa4a09dd5fcda5cea8e90de05a7e90def81f48328e4af73eb93e3f7f` | yes |
| 1x1/1if | both | `9ea95d00b8d2953b9d05b274fc3b168c21b68c8d75e2121379ed764e583a2fe7` | D10-A1 | `9ea95d00b8d2953b9d05b274fc3b168c21b68c8d75e2121379ed764e583a2fe7` | yes |
| 8x8/2if | both | `6095bf88cbdd4eb2433045fa5ec142b6a397e4fcb92d12f02d4c330858ba2c11` | D10-A8 | `6095bf88cbdd4eb2433045fa5ec142b6a397e4fcb92d12f02d4c330858ba2c11` | yes |
