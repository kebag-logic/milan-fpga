<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# release_merge - KL_pp_release_merge suite

Proves that the two release sources feeding the TX slot pool cannot lose a
slot handle when they pulse together. `make` builds and runs the shipping
five-slot shape. Exit 0 means PASS.

The directed checks cover idle and reset behavior, one release from either
source, simultaneous distinct releases, simultaneous duplicate releases,
pending releases combined with fresh lower-priority handles, invalid handles,
and reset while a release remains pending. Every accepted distinct handle is
observed once and the output returns to idle after the pending set drains.
