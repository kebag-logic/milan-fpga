The split boot simulation, the platform ledger and the memory test at da8a8b84, on a clean clone.

- `boot-1x1-da8a8b84.log`, `boot-8x8-da8a8b84.log`: rc 0, PASS. 59 frames, 10 publications, the longest frame 14,537
  and 14,545 CPU cycles (145.37 and 145.45 us) against the stated 155 us; seven advertisement writes (the boot's
  9 0x0200, 4 0x0001, 0 0x1200, then 9 and 4 after each of two losses); `[0, 13]`, `[0, 0]`, `[13]`; MDC 950 /
  1,120 / 2,260 ns.
- `boot-self-test-da8a8b84.log`: rc 0; 6 of 6 native controls, 6 of 6 plants caught (phy-unpublished,
  phy-loss-not-latched and phy-unadvertised among them), 8 of 8 placement controls.
- `plat-ledger-self-test-da8a8b84.log`: rc 0, four points PASS, 8 of 8 controls.
- `test-ctrl-memory-da8a8b84.log`: rc 0, `test_ctrl_memory: 0 failure(s)`.
