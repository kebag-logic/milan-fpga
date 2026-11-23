# Documentation evidence reconciliation

Baseline: `8267b8951616cfd570baf690835d4b0d38f14596`.

## Fixture identities

| Point | Executable symbols | RAMB36 |
|---|---|---:|
| 8x8-one-interface-gptp | {'nvm_stage': 13594, 'image_allocation': 8, 'image_gptp': 1104} | 59.0 |
| 8x8-two-interfaces-gptp | {'nvm_stage': 13594, 'image_allocation': 16, 'image_gptp': 2152} | 64.0 |
| platform-8x8-one-interface-gptp | {'nvm_stage': 13594, 'ctrl_plat': 20160} | 62.0 |

`ctrl_memory_ledger.IMG_GPTP_1/2`: 1,104/2,152 B.

## Plain platform images

Original measurements copied byte for byte into `prior-memory/`; no new image build is claimed.

| Point | Before (`a6323318`) | After (`631dc544`) |
|---|---|---|
| 1x1-if1 | rom 126,632 B, sram 56,800 B, 45 RAMB36 (the 56-RAMB36 budget), ctrl_plat 18112 B: PASS | rom 126,640 B, sram 56,800 B, 45 RAMB36 (the 56-RAMB36 budget), ctrl_plat 18112 B: PASS |
| 8x8-if2 | rom 140,952 B, sram 115,568 B, 63 RAMB36 (platform-8x8-two-interfaces), ctrl_plat 21568 B: PASS | rom 140,960 B, sram 115,568 B, 63 RAMB36 (platform-8x8-two-interfaces), ctrl_plat 21568 B: PASS |

The shared linker order changed in `631dc544`; the prose-only delta here changes no executable input.

## Regraded original ELF artifacts

These larger build artifacts remain outside the output packet. Paths are relative to the prior image directory.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| 1x1-if1/ctrl_app.elf | 159484 | 74b4cbf25e4d8ad1699649a91a0c2ea0849d028ed0bf294d64c10195f3ceeded |
| 1x1-if2/ctrl_app.elf | 163440 | 267ace9656188088ddb7aab4d282b7e1eeebe1fde9edbc24e1575fd1a4e6b8b0 |
| 8x8-if1/ctrl_app.elf | 172164 | 9c5aacf0b8d1c1909364c7f31fccd04d0985e0cd2c8ab77ba01b1b4ddc88f4dc |
| 8x8-if1-gptp/ctrl_app.elf | 186912 | 29da91dec3e17dd34c6317b20fae25c955fdb39398e3ddecc630cab962d4bbc6 |
| 8x8-if2/ctrl_app.elf | 176120 | 0fadf4a3355af704e35e622c0cfd9ff6603117db66232cd274d0d83167578ea6 |
