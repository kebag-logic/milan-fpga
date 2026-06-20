// SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// aecp_sim_main.cpp — Verilator C++ top-level stub for AECP DUT simulation.
//
// This file provides the main() entry point for the Verilator-compiled DUT
// binary.  It creates the model, drives the AXI-Stream stimulus received on
// a UNIX domain socket (bound to --socket <path>), and returns responses.
//
// STATUS: STUB — socket transport and AXI-stream bridge not yet implemented.
//         Build will succeed; binary will print an error and exit(1) until
//         the transport layer is wired up.
//
// Usage (from run-dut-sim.sh):
//   V<MODULE> --socket /work/sock/aecp.sock

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

// Forward declarations for Verilator model (resolved at link time)
// #include "VKL_aecp_packet_validator.h"  // uncomment when building specific module

int main(int argc, char **argv) {
    std::string socket_path;

    for (int i = 1; i < argc; i++) {
        if (std::strcmp(argv[i], "--socket") == 0 && i + 1 < argc) {
            socket_path = argv[i + 1];
            i++;
        }
    }

    if (socket_path.empty()) {
        fprintf(stderr, "[aecp_sim_main] ERROR: --socket <path> argument required\n");
        return 1;
    }

    fprintf(stderr, "[aecp_sim_main] TODO: UNIX-socket AXI-Stream bridge not yet implemented.\n");
    fprintf(stderr, "[aecp_sim_main] Socket path would be: %s\n", socket_path.c_str());
    fprintf(stderr, "[aecp_sim_main] Exiting. Implement the bridge to enable T1 BDD tests.\n");
    return 1;
}
