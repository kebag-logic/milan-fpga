#!/usr/bin/env python3
"""Recompute save_window.bound_ms's steps and bound from the containers (nvm_stage less its 8-byte look-ahead), and
the change-to-durable worst case when the change arrives just after a save in flight has captured (review R711-4)."""
import math
PAGE, READ, TRAILER, DIRTY, TICK, SLACK, AGE, RECORDS = 256, 128, 4, 1000, 10, 10, 2, 2
for point, stage in (('1x1', 3344), ('8x8/2if', 13264)):
    image = stage - 8
    pages, reads, seal = math.ceil(image / PAGE), math.ceil(image / READ), math.ceil((image - TRAILER) / PAGE)
    s = 1 + RECORDS + 1 + seal + 2 + reads + 2 * pages + reads
    per = (AGE + 1) * TICK
    bound = DIRTY + s * per + SLACK
    capture = 1 + RECORDS + 1
    # a change marked just after the capture of a save in flight: it waits for that save's remaining steps, then
    # its own S steps (its first-dirty window has expired by then)
    change = (s - capture) * per + s * per + SLACK
    print(f'{point}: container {image} B, S = 1 + {RECORDS + 1} + {seal} + 2 + {reads} + {2 * pages} + {reads} = {s}; '
          f'stated bound {bound} ms; a change just after an in-flight capture: about {change} ms')
