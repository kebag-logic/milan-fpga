"""Recompute the console UART table's derived figures from 115,200 baud, 10 bits a character."""
import math
t = 10 / 115200 * 1e3            # ms per character
print(f"character time {t*1000:.3f} us")
for gap in (2.0, 10.0, 20.0):
    n = math.ceil(gap / t)        # the page's rule: the first count whose time passes the gap
    buf = 1 << (n - 1).bit_length()
    print(f"gap {gap} ms: {n-1} chars = {(n-1)*t:.3f} ms, {n} = {n*t:.3f} ms -> need {n}, buffer {buf} B holds {buf*t:.3f} ms")
print(f"16 chars {16*t:.3f} ms; 32 chars {32*t:.3f} ms")
