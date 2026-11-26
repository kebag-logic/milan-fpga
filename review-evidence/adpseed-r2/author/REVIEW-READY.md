# #970 round 4: tsn-c-stack PR #40, R939-1 F1 and F2 — handoff

**Status (11-26): REVIEW READY.**

- **tsn-c-stack:** `adp-draw-seed` at `9590206015ead2cfd2ef955c2f4ef8d8c4e4762c`, one commit on the pushed `5e6ab995`
  pins `95902060` and re-pins to the stack PR's merge commit later.
- Both are committed and neither is pushed. Nothing was posted or flashed, and the bench was not touched.

**ETA:** nothing pending on this side. The manager pushes `adp-draw-seed`. `PR-BODY-stack.md` is updated for #40.

## 1. R939-1 and what answers it

| Item | Answer at `95902060` |
|---|---|
| F1 (option (a), the manager's decision) | `leave_down` seeds with the plain sum `(uint32_t)e->mac + sample`, the least significant 32 bits modulo 2^32; the end-around carry line is gone. A27's sum check now pins the wrap: MAC `0xFFFFFFFF` with sample 5 seeds exactly as MAC 0 with sample 4, "A27 the seed is the sum's least significant 32 bits, modulo 2^32 (6.2.4.2.2)". A22's zero-mixing constant is re-derived, `0xDE81995C` to `0xDE81995D`, the carry's difference: it still mixes to zero, and the test sees the generator start at 1. The plant `adp-seed-carry-dropped` is replaced by `adp-seed-end-around-carry-added`, caught by A27 by that message. |
| F1, stuck at zero | Still impossible, by two means. (1) `leave_down` maps a seed that mixes to 0 onto 1 (`a->rng = x != 0u ? x : 1u`), held by A22 and the plant `seed-left-at-zero`. (2) No draw path runs before the first `leave_down`: `adp_init` leaves the state 0, and every other caller of `enter_delay` requires WAITING, which only a `leave_down` reaches. The 2,000,000-step walk in R939-1 confirms it. The re-entry rig's constant `0xDA0DB1D5` uses MAC 0, where the sum cannot wrap, so it stands. |
| F2 | A32 `ADiscoverDrawTakesNoSample` delivers an ENTITY_DISCOVER in WAITING, with this entity's ID and with 0. It asserts the delay is drawn (DELAY, `draws` + 1) and the seed count is unchanged. The plant `adp-discover-draw-sampled` changes `adp_rx`'s draw to `leave_down` (the reviewer's `probe-discover-draw-sampled`) and is caught by A32's message. |
| S1 | A27 compares interfaces 0, 1, 2 and 255 pairwise. The reviewer's `probe-interface-low-bit-only` is now the plant `adp-seed-interface-low-bit-only`, caught. |
| R2 | `PORTING.md`'s checklist row reads "a local clock sample at each transition out of DOWN"; DEV-04 reads "The integrator supplies a clock sample (ADP) or entropy (ACMP)". PORTING's contract line states the sum modulo 2^32. |
| R1 | The author evidence note sits in milan-fpga's published `review-evidence/adpseed-r1`, which the manager publishes; not changed here. Its exact fix is in R939-1. |

## 2. Stack validation at `95902060`

- `validate.py --jobs 16 --graphs`: rc 0, 28 of 28 steps (`receipts/r4/tsn-c-stack-*`).
- 512 of 512 plants caught, 0 escaped. Against round 3: one plant replaced, two added; 23 new against `main`.
- Coverage: lines and branches 100 % after the existing exclusions (`adp.c` 215/217 lines, 95/102 branches).
- `baremetal.py` rc 0, Debug and Release.
- Merging into `dev-linux` (9e1cd60f) or into `main` gives the head's own tree (`4064709b`). The source validation
  therefore applies unchanged to the `dev-linux` merge.
- Each changed plant was also run on its own: `adp-seed-end-around-carry-added`, `adp-discover-draw-sampled`,
  `adp-seed-without-interface`, `adp-seed-interface-low-bit-only` and `seed-left-at-zero`, all caught.

## 3. milan-fpga at `4f6ee193`

- The commit:
  - the gitlink to `95902060`;
  - H7 restated for the plain sum: MAC `0xFFFFFFFF` with sample 5 against MAC 0 with sample 4, "H7 the seed is the sum
    modulo 2^32";
