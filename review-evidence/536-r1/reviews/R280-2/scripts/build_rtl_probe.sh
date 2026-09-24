#!/bin/sh
# Build a disposable copy of the pinned protocol-processor tb/pp_top with a
# frame-replay probe inserted where the suite runs its MVU phase (the same
# engine state M1..M9 run in). The probe reads "<id> <hex frame>" lines from
# $R280_PROBE_IN, feeds each frame, waits 200 ms for an AECP answer, prints
# "<id> RSP <hex>" or "<id> NONE", and exits 0.
# Usage: build_rtl_probe.sh <repo-root> <scratch-dir> <verilator>
set -eu
root=$1; out=$2; vl=$3
rm -rf "$out"; mkdir -p "$out"
( cd "$root/protocol-processor" && git archive HEAD hdl tb/pp_top tb/common ) | tar -x -C "$out"
python3 - "$out/tb/pp_top/sim_main.cpp" <<'EOF'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
anchor = "    MilanInfoPhase{h, d, image_entity}.run();\n"
assert s.count(anchor) == 1, "anchor not unique"
probe = r'''    if (const char* pin = std::getenv("R280_PROBE_IN")) {
      FILE* fi = std::fopen(pin, "r");
      if (!fi) { std::printf("R280 probe: cannot open %s\n", pin); std::exit(2); }
      char id[128]; static char hex[8192];
      while (std::fscanf(fi, "%127s %8191s", id, hex) == 2) {
        std::vector<uint8_t> f;
        for (size_t i = 0; hex[i] && hex[i + 1]; i += 2) {
          unsigned v; std::sscanf(hex + i, "%2x", &v); f.push_back((uint8_t)v);
        }
        h.q_aecp.clear();
        h.feed(f);
        auto got = h.wait_any(h.q_aecp, 200);
        if (got.empty()) { std::printf("R280 %s NONE\n", id); }
        else {
          std::printf("R280 %s RSP ", id);
          for (uint8_t b : got) std::printf("%02x", b);
          std::printf("\n");
        }
        std::fflush(stdout);
      }
      std::fclose(fi);
      std::printf("R280 probe done\n"); std::fflush(stdout);
      std::exit(0);
    }
'''
s = s.replace(anchor, probe + anchor)
if "#include <cstdlib>" not in s:
    s = s.replace("#include <cstdint>\n", "#include <cstdint>\n#include <cstdlib>\n", 1)
open(p, "w", encoding="utf-8").write(s)
EOF
sed -i 's/--build -j 0/--build -j 8/' "$out/tb/pp_top/Makefile"
printf '\nprobe_build: ltn_rom.hex ucode.hex\n\t$(VERILATOR) $(VFLAGS) $(SRCS) $(CPP) -o Vpp_top_sim\n' >> "$out/tb/pp_top/Makefile"
cd "$out/tb/pp_top"
make VERILATOR="$vl" probe_build > build.log 2>&1 || { tail -40 build.log; exit 1; }
ls -la obj_dir/Vpp_top_sim
