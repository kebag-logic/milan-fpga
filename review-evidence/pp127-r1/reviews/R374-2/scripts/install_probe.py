"""Insert the reviewer probe group into a copy of tb/srp_top/sim_main.cpp."""
import sys, pathlib
p = pathlib.Path(sys.argv[1]) / "tb/srp_top/sim_main.cpp"
inc = pathlib.Path(__file__).with_name("r374_probe.cpp.inc").read_text()
s = p.read_text()
s = s.replace("  void bring_up_the_port() {", inc + "  void bring_up_the_port() {", 1)
s = s.replace('    if (!*group || !strcmp(group,"congestion")) check_own_leaveall_congestion_and_recovery();',
              '    if (!*group || !strcmp(group,"congestion")) check_own_leaveall_congestion_and_recovery();\n'
              '    if (!strncmp(group,"r374",4)) r374_probe(group);', 1)
s = s.replace('      && strcmp(group,"peer") && strcmp(group,"congestion")) return 2;',
              '      && strcmp(group,"peer") && strcmp(group,"congestion") && strncmp(group,"r374",4)) return 2;', 1)
# round 2: head's group filter also names "guards"
s = s.replace('      && strcmp(group,"guards")) return 2;',
              '      && strcmp(group,"guards") && strncmp(group,"r374",4)) return 2;', 1)
assert s.count("r374_probe(") == 2 and s.count('strncmp(group,"r374",4)) return 2;') == 1
p.write_text(s)
