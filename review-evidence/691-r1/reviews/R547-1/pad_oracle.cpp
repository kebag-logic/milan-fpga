#include "Voracle_top.h"
#include <cstdio>
#include <cstdlib>

int main() {
    Voracle_top dut;
    unsigned held_data = 0, held_valid = 0, checks = 0;
    auto observe = [&]() {
        dut.eval();
        const unsigned last = held_valid && !dut.pad_valid;
        if (dut.new_data != held_data || dut.old_data != held_data ||
            dut.new_valid != held_valid || dut.old_valid != held_valid ||
            dut.new_last != last || dut.old_last != last) {
            std::fprintf(stderr, "FAIL check=%u clk=%u reset=%u pads=%02x/%u expected=%02x/%u/%u new=%02x/%u/%u old=%02x/%u/%u\n",
                checks, dut.clk, dut.rst, dut.pad_data, dut.pad_valid,
                held_data, held_valid, last, dut.new_data, dut.new_valid,
                dut.new_last, dut.old_data, dut.old_valid, dut.old_last);
            std::exit(1);
        }
        ++checks;
    };
    dut.clk=0; dut.rst=0; dut.pad_data=0; dut.pad_valid=0;
    observe();
    // Every byte and every ordered previous/current valid/reset combination.
    // Glitch reset and pads on both clock levels, without a sampling edge.
    for (unsigned byte=0; byte<256; ++byte)
      for (unsigned previous=0; previous<4; ++previous)
        for (unsigned current=0; current<4; ++current) {
          for (unsigned phase=0; phase<2; ++phase) {
            const unsigned state = phase ? current : previous;
            dut.clk=0; observe();
            dut.pad_data=phase ? byte : byte^255;
            dut.pad_valid=state & 1; dut.rst=(state>>1)&1; observe();
            dut.rst^=1; observe(); dut.rst^=1; observe();
            dut.clk=1;
            held_data=dut.rst ? 0 : dut.pad_data;
            held_valid=dut.rst ? 0 : dut.pad_valid;
            observe();
            dut.rst^=1; observe();
            dut.pad_valid^=1; dut.pad_data^=255; observe();
            dut.rst^=1; observe();
          }
        }
    std::printf("PASS: %u independent pad-oracle observations; both receiver versions; startup, both clock levels, reset pulses without edges, all byte/valid/reset transitions\n", checks);
    return 0;
}
