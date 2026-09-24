#!/usr/bin/env python3
"""Derive current documentation figures from the head's assembled gate image."""
import json
import math
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
evidence = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'scripts'))
from nvm_contract import FIXED, FLASH_PAGE, SPI_HZ, T_PP_MAX_MS, T_SE_MAX_MS
from nvm_shape import commit_worst_ms

head = json.loads((evidence / 'figures_head.json').read_text())
results = {}
for stem in ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8'):
    f = head[stem]
    image = f['image_len']
    area = sum(row[4] for row in f['records'])
    count = f['nrec']
    pages = math.ceil(image / FLASH_PAGE)
    worst = commit_worst_ms(image)
    assert worst == f['commit_worst_ms']
    instructions = 6 * area + 50 * count
    ddr = 2 * area
    cycles = 10 * instructions + 30 * ddr
    copy_ms = cycles * 1000 / 50_000_000
    result = dict(image_bytes=image, raw_area_bytes=area, record_count=count,
        pages=pages, program_ms=pages*T_PP_MAX_MS,
        readback_ms=image*8*1000/SPI_HZ, worst_commit_ms=worst,
        deadline_margin=FIXED.T_NVM_COMMIT_TIMEOUT_MS/worst,
        erase_percent=T_SE_MAX_MS*100/worst,
        slot_percent=image*100/FIXED.ERASE_BLOCK,
        slot_percent_gate=image*100//FIXED.ERASE_BLOCK,
        instructions=instructions, ddr_accesses=ddr, cycles=cycles,
        copy_ms=copy_ms, copy_2x_ms=2*copy_ms,
        hold_margin=50/copy_ms, hold_2x_margin=50/(2*copy_ms),
        durable_ms=500+1000+worst)
    if stem.endswith('8x8'):
        result.update(dram_window_bytes=40_000+4_096+image,
                      alternative_bram36=math.ceil(image/4_096))
    results[stem] = result
    print(stem)
    print(json.dumps(result, indent=2))
print('Sources: figures_head.json from unchanged tree_figures.py;')
print('gate nvm_shape.commit_worst_ms and nvm_contract constants;')
print('FASTCONNECT 8.1 window terms; SNAPSHOT_OWNERSHIP 18 copy model;')
print('MATERIALIZATION 12 debounce terms. No hardware measurement.')
(evidence/'derived-figures.json').write_text(json.dumps(results,indent=2)+'\n')
