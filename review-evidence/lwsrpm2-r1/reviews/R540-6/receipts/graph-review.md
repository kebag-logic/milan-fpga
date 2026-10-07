<!-- SPDX-License-Identifier: Apache-2.0 -->
# Changed graph review

The retry graph in `doc/developer.md` (block at line 306) was rendered to an image in scratch and viewed.
Eight nodes; labels are readable and the layout is clear.
It matches `reg_event`: a failed reservation keeps the snapshot and arms the 1 cs timer; a tick or receive retries; success clears the pending flag, indicates the saved Leave, publishes, and replays.
