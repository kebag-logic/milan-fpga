#!/usr/bin/env python3
"""R381-3 arithmetic probe for D3 section 5.1 RETRY_BACKOFF_CYC_P.

The page gives ceil(processor_clock_hz * 500 / 1000). In SystemVerilog, a
32-bit `int unsigned` parameter times an unsized literal is evaluated at 32
bits (IEEE 1800-2017 11.6.1), so a literal transcription wraps. This models
that evaluation; it is not a simulation of any shipped RTL.
"""
M = 1 << 32
for hz in (50_000_000, 100_000_000, 125_000_000):
    exact = -(-hz * 500 // 1000)
    wrapped = ((hz * 500) % M) // 1000
    safe = (hz + 1) // 2
    print(f"CLK_HZ_P={hz}: page value {exact} cycles ({exact / hz * 1000:.1f} ms); "
          f"32-bit literal transcription {wrapped} cycles ({wrapped / hz * 1000:.1f} ms); "
          f"(CLK_HZ_P+1)/2 = {safe}; bits needed {exact.bit_length()}")
print("page examples: 100 MHz -> 50,000,000 and 50 MHz -> 25,000,000:",
      -(-100_000_000 * 500 // 1000) == 50_000_000 and -(-50_000_000 * 500 // 1000) == 25_000_000)
