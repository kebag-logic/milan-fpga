# Image identity operands: the #665 flip, rounds 2 and 3 (R880-1-F2, R880-1-F3, R880-2-F1, R879-2-F1)

This directory holds the compared operands behind the flip's image-identity carry, hash-bound, and one driver that
re-derives every claim from them. Nothing here is fetched or built by the driver.

## Replay

```sh
cd identity            # this directory
python3 -I tools/replay.py .
```

Python 3.9 or later, standard library only. The last line must read `== RESULT: ALL CLAIMS HOLD`; the run recorded
here is `replay-output.txt`. An operand the manifests name but the directory lacks is refused by name, and the run
still reaches its RESULT line.

`python3 -I tools/rmutants.py . <work-dir>` first replays an unmodified copy of this directory and grades nothing
unless that holds. It then plants thirteen defects in copies of the operands: round 2's eleven, and the two the
round-2 reviews asked for (a `2` -> `3` digit outside the firmware_version string; an operand removed). A plant
counts as caught only when the replay exits non-zero, reaches its RESULT line, and fails on the plant's own named
check. The run over this directory as published is beside it, in `../identity-checks/`.

Round 3 (the archive's privacy scrub refused five compressed operands whose bytes matched a scrub pattern by
chance): those five are re-encoded, the same compressor at another level, so the scrub leaves their bytes unchanged.
Their decompressed content is the round-2 files' content. `binding.json` `reencoded` lists, for each, the round-2
file hash, the new file hash and the content hash. `MANIFEST.content.sha256` holds the content hash of every
compressed operand, and the replay checks it. `tools/publish_check.py` copies this directory under the archive's
rule (a binary the scrub would alter is refused, a text file is scrubbed). It found nothing refused or altered,
then ran the replay and the plants over that copy (`../identity-checks/publish-check.txt`).

## What is here

| Path | Operands |
|---|---|
| `shipping/<1x1,8x8>/bench/` | the bench re-check's images (built at `8c5e2b4f`, `--eth-port e2`): `alinx_ax7101.bit`, the platform image `ctrl_app.elf`, the export's `aem_desc.bin`/`.json`/`.map`, `csr.csv`/`.json`, `flashboot_layout.json`, `image_manifest.json`, every ROM bank init and `mem.init` |
| `shipping/<1x1,8x8>/flip/` | the same files of round 1's flip images (the gating recipe at `822e3af0`, ExtraPostPlacementOpt) |
| `shipping/<shape>/dump/` | the two routed checkpoints dumped by `tools/dump.tcl` (`.cells`: every primitive cell's name, REF_NAME, LOC, BEL and INIT properties; `.nets`: every net's ROUTE; sorted; xz) and, at 8x8, `tools/bramdump.tcl`'s block RAM dump. The checkpoints themselves are not here (75-93 MB each); their sha256 are in `binding.json` |
| `harness/<point>/<arm>/` | the 16 CPU-budget arm images: `measured.elf` (the formal measurement's, 1x1/1if at `8c5e2b4f`, 8x8/1if at `92de01f7`) and `head.elf` (round 1's re-measure, `f7139ce1`), each arm's `parts.json` |
| `groups/<point>/<arm>/<group>.*` | the 13 re-measured groups: the measured run's result JSON and raw simulation log, and this lane's re-measure's |
| `binding.json` | each operand's published identity and where it was published, the checkpoints' hashes, the rebuilds that tie the harness images to their source heads, and the re-encoded operands (`reencoded`) |
| `MANIFEST.sha256`, `MANIFEST.content.sha256` | every file's sha256 (`sha256sum -c MANIFEST.sha256`), and every compressed operand's content sha256 |
| `receipts/` | the input carry of the flip images to this round's head, and the harness rebuild hash lists |
| `tools/` | the driver, the round 1 and round 2 comparison and dump tools, sanitised of host paths |

## Binding to the published identities and to source

- Bench images: the bench re-check (#665 issuecomment-7063917242) publishes bitstream `c7189218`, firmware
  `c873a0aa` (1x1/1if) and `7d903412`, `d67fd049` (8x8/1if); the operands hash to them.
- Flip images: round 1's REVIEW READY (#665 issuecomment-7070924358) and its receipts publish `68e5308b` and
  `6a1ff1ef` and the platform images' hashes; the operands hash to them. `receipts/inputs-carry-*` hold every input
  of both builds equal at this round's head (19 and 16 files; the gating recipe's `milan_soc.py` without `--build`).
- Harness images: every `measured.elf` is byte for byte the image the harness build (`legs.py build`) makes at the
  bench head `8c5e2b4f`, at both points (the 8x8/1if measurement ran at `92de01f7`). Every `head.elf` is byte for
  byte the image it makes at the PR's head `dd163e41` (and made at `2f985971`, `a9da4c48` and `873a5dc2`).
  `binding.json` lists both rebuilds. The flip images' inputs are equal at `dd163e41` too
  (`receipts/inputs-carry-*-dd163e4143.txt`).

## Rules: what is compared, and what is not

Nothing is excluded unless named here.

- **`.bit`**: the header is parsed field by field (`a` design name, `b` part, `c` date, `d` time, `e` payload length);
  the payload is parsed as the 7-series packet stream. Every differing byte is named. The device loads the payload
  only. The design name carries `SW_CRC` and `SW_HDR_SHA256`, two digests Vivado writes as text (they are not the
  CRC-32 or SHA-256 of the payload or of the whole file; tested); the date and time are the build's.
- **ELF**: the loaded sections byte by byte, then the whole files; each pair differs in six bytes, all loaded.
- **ROM**: the bank init files concatenated against the ELF's load segments, at each segment's load address.
- **Export files**: every differing line is printed.
- **Dumps**: compared as written (sorted text); the cell lines with their INIT properties bit by bit.
- **Groups**: every JSON leaf, none excluded. Round 1's driver (`tools/hcompare.py`, `hcompare2.py`) skipped
  string leaves holding a `/` as paths; at these groups those were the 21 `summary` access tuples per group (such as
  `5181/431867/80/209`), not paths. They are equal; this replay compares them. The raw logs are compared line by line.
  A differing line may differ only inside the ENTITY's firmware_version string. That string is derived from the
  arm's two images, not written into the tool. On a WIRE line, the payload bytes may differ only within an
  occurrence of the measured string that reads as the head's string at the same offset. On a PASS line, the same
  holds for the mailbox words (`W`), laid out as little-endian bytes in their order. Every other line must be equal.

## Result, in figures

| | 1x1/1if | 8x8/1if |
|---|---|---|
| `.bit` bytes differing | 103 | 93 |
| header: design name (`SW_CRC` 8 + `SW_HDR_SHA256`) | 71 (8 + 63) | 69 (8 + 61) |
| header: date + time | 1 + 5 | 1 + 4 |
| payload: the CRC register write | 4 | 4 |
| payload: frame data | 22 bytes, 22 bits, 7 of 9,464 frames | 15 bytes, 15 bits, 7 frames |
| routed cells / nets | all equal but 8 cells' INIT, 22 bits | all equal but 14 block RAMs' INIT, 15 bits |
| platform image | 6 bytes: `lui`/`addi` = crc32 of `aecp_entity_image`, its byte 0x184 `2` -> `3` | the same |
| ROM bank init | the ELF's load segments exactly | the same |
