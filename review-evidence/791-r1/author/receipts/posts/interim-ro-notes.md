# A765 pending notes while the root file system is read-only (to merge into HANDOFF.md)

- 08:2x host clock: the root file system (/, holding /home) was remounted read-only by the kernel (`emergency_ro`).
  /data and /data-2 stay writable.
- Blocked by it: writing the output directory (HANDOFF.md, PR-BODY.md, receipts), sbt (needs ~/.sbt/boot/sbt.boot.lock),
  and the CPU generator's netlist cache under the LiteX tree in /home. So every run that needs a CPU netlist not yet
  cached fails: the 8x8 split boot (`boot-8x8/soc.log`: `java.io.FileNotFoundException: <home>/.sbt/boot/sbt.boot.lock (Read-only file system)`)
  and S2's harness at the new region list.
- Done before it, at 03447eaa on a clean clone: region-decode self-test PASS (final/region-self.log);
  split boot 1x1 PASS (final/boot-1x1.log, ready); product decode 1x1/8x8 PASS (receipts/decode at eb26f22).
- All-fabric compare (second run, before the RO event): AX7101 1x1 and 8x8: CPU netlist name, bytes, region rows,
  vexii_args identical; top .v and soc.h differ in comment lines only (timestamps, hierarchy-comment order). Arty
  configs: export refused by LiteX's PLL search at base and head alike after the CPU named its netlist
  (VexiiRiscvLitex_7c73187a... at both sides for arty_current).
