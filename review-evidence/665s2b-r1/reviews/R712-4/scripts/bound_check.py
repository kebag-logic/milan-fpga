#!/usr/bin/env python3
"""Recompute a save's step count S and stated worst case from the store's constants, independently of save_window.py.

The steps follow nvm_store.c's phases at the reviewed head: the idle step that starts the capture (1), one capture
step per changed record plus the one that finds none left (R + 1), the seal's NVM_STEP_BYTES (256) stretches of the
container less its 4-byte trailer, the erase issue and one busy poll (2), the blank check's 128-byte read-backs, each
page's issue and one busy poll (2 a page), and the verify's read-backs. The container is nvm_stage's size less the
8-byte record-header look-ahead (sw/litex/ctrl_memory_ledger.py STAGE_1X1, STAGE_8X8).

usage: python3 -I bound_check.py
"""
import math

STAGE = {'1x1': 3344, '8x8': 13264}
REC_HDR, TRAILER, STEP, READ, PAGE = 8, 4, 256, 128, 256
DEBOUNCE_MS, TICK_MS, AGE, SLACK_MS, RECORDS = 1000, 10, 2, 10, 2
for point, stage in STAGE.items():
    image = stage - REC_HDR
    seal, reads, pages = math.ceil((image - TRAILER) / STEP), math.ceil(image / READ), math.ceil(image / PAGE)
    s = 1 + (RECORDS + 1) + seal + 2 + reads + 2 * pages + reads
    bound = DEBOUNCE_MS + s * (AGE + 1) * TICK_MS + SLACK_MS
    print(f'{point}: container {image} B, seal {seal}, read-backs {reads} x2, pages {pages}, S = {s}, '
          f'bound {bound} ms, without the 10 ms slack {bound - SLACK_MS} ms')
