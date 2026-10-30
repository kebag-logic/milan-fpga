diff --git a/tb/nvm_port/README.md b/tb/nvm_port/README.md
index 2caa9da..2ae4b5e 100644
--- a/tb/nvm_port/README.md
+++ b/tb/nvm_port/README.md
@@ -1,6 +1,11 @@
 <!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
 # nvm_port — KL_pp_nvm_port class-F suite
 
+**In short.** The class F NVM port on its own, against independent device models: its
+handshakes, its device-face deadline, its behaviour across resets, and the coverage of every
+device-error arm. `make` runs three builds; `make figures` re-measures every figure this
+page quotes and fails if the page has drifted, and CI runs it.
+
 Proves the class-F NVM port (`hdl/packet_engine/KL_pp_nvm_port.sv`,
 [02 §8](../../docs/architecture/02_interfaces.md) F02.8 +
 [07 §5](../../docs/architecture/07_memory_maps.md) F07.8): `make` = build + run,
