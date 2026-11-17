The split boot simulation, the platform ledger and the memory test at 1a1e6665, on a clean clone.

- `boot-1x1-1a1e6665.log`, `boot-8x8-1a1e6665.log`: rc 0, PASS. 59 frames, 10 publications, the longest frame
  14,537 and 14,545 CPU cycles (145.37 and 145.45 us) against the stated 155 us; seven advertisement writes (the
  boot's 9 0x0200, 4 0x0001, 0 0x1200, then 9 and 4 after each of two losses); `[0, 13]`, `[0, 0]`, `[13]`. Every
  figure equals the measured head 8beada76's (`../measure/`): the images are byte-identical.
- `boot-self-test-1a1e6665.log`: rc 0; 6 of 6 native controls, 6 of 6 plants caught (phy-unadvertised, its anchor
  renamed this round, among them), 8 of 8 placement controls.
- `plat-ledger-self-test-1a1e6665.log`: rc 0, four points PASS (rom 119,500 / 121,084 / 132,204 / 133,772 B; 43.5 /
  44.5 / 56.5 / 61.0 RAMB36; ctrl_plat unchanged), 8 of 8 controls.
- `test-ctrl-memory-1a1e6665.log`: rc 0, `test_ctrl_memory: 0 failure(s)`.
