[A615] STOP - PR #738, round 2
Head: da5594321c7a3558ac8ad1ef5e147a77ac15356f (local; not pushed).

The round 2 requirement to preserve the workflow's complete recursive CPU tree conflicts with the requirement that every layer contain no host paths or account names. Verified pinned upstream members already contain absolute user paths:
- VexiiRiscv 235753e24f2d960e49a0852205bae1400bf22c19, src/main/scala/vexiiriscv/soc/litex/Soc.scala:825-827; member SHA-256 f38fcdcdbbb732bfef644442a3e9284bd13ccc8f429c4f91e2920d6b7528790f.
- SpinalHDL 1097c1df52f6b4ac532e42ff35a9c610f8e9a07c, lib/src/main/scala/spinal/lib/eda/altera/QuartusFlow.scala:112; member SHA-256 230d9c2cee5e7ba79999ca4ea534852218f7d6ddb174178581707d3a29d98913.
- Recursive NaxSoftware ae0c08016d0581b9ac79a4feb166e7a532369bd4, riscv-arch-test/rv32i_m/B/andn-01.elf, offsets 39311 and 39551; member SHA-256 ec508e18c368406af065aa1ddc2cbbefadc964481a83bd033df62fccc2fde4b9.

Each source archive matched its size and SHA-256. Identifying values are redacted. Removing or rewriting those members breaks exact-tree equality; changing the ELF also crosses the stated linked-image boundary. A public decision is needed to authorize exact filtering/redaction or a specific allowance for immutable upstream artifacts. No exception or linked-image change was made.

Committed checkpoint: inventory refusal controls for reported indirect installer forms, unsupported setup actions and Makefile recipes; isolated concurrent downloads. Inventory comparison/selftest, builder selftest, Python idiom and whitespace gates returned 0 before commit. The independent download-race probe passed 10/10 trials.

Later image/lock/privacy/package-resolution changes remain uncommitted drafts with known failed checks. One exploratory cold build finished in 434.050 s (3,972,321,413 bytes) and was refused by the privacy scan. No reproducibility pair, final image lock, round 2 smoke acceptance or review-ready verdict is claimed. HANDOFF.md and PR-BODY.md are updated. Nothing was pushed; no PR was edited.
