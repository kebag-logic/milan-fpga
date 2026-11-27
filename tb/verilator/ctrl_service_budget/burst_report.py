# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Saved-state burst outcomes and report tables for issues #665 and #920."""

def burst_misses(results: list[dict]) -> list[str]:
    """Each name of a burst or a change in flight not durable within its target, or missing at the cut, a next save
    that waited past the first idle step (save_burst.misses), and a bind group's (bind_save.late), each by its group."""
    import bind_save
    import save_burst
    return save_burst.late(results) + bind_save.late(results)


def burst_lines(results: list[dict]) -> list[str]:
    """One BURST line for each graded burst or change in flight: its names' worst time to durable, its target."""
    out = []
    for g in results:
        b = g.get('burst')
        if not b:
            continue
        worst = f"{b['worst_ms']:.3f} ms" if b['worst_ms'] is not None else 'never'
        tail = (f", the cut's container sequence {b['cut_seq']}, {len(b['cut_missing'])} name(s) missing" if
                b['kind'] == 'burst' else f", {b['next_steps']['steps']} steps to the next save's erase "
                f"(want {b['next_steps']['want']})")
        verdict = 'OVER' if save_misses_of(b, g['group']) else 'within'
        out.append(f"BURST {g['group']}: {b['names']} name(s), the latest durable {worst} after its response (name "
                   f"{b['worst_ordinal']}; target {b['target_ms']:,} ms), {len(b['saves'])} save(s){tail} {verdict}")
    return out


def print_bursts(results: list[dict]) -> None:
    """Each burst's and change in flight's BURST line (burst_lines) and bind group's BIND line, as the run prints it."""
    import bind_save
    for line in burst_lines(results) + bind_save.lines(results):
        print(line)


def save_misses_of(burst: dict, group: str) -> list[str]:
    """save_burst.misses of one group's burst."""
    import save_burst
    return save_burst.misses(burst, group)


def burst_table(results: list[dict]) -> list[str]:
    """The bursts' and the changes in flight's section of the table (save_burst.py): each name's latest time from its
    response to durable against the target, the saves, and the cut's container or the next save's start."""
    rows = [(g['group'], g['burst']) for g in results if g.get('burst')]
    if not rows:
        return []
    lines = ['', "Names from their response to durable (save_burst.py; #920, #665's ruling of "
             '2026-11-15, item 1):', '',
             '| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, '
             'or the next save | Verdict |', '|---|---:|---:|---:|---:|---|---|---|---|']
    for group, b in rows:
        worst = (f"{b['worst_ms']:.3f} ({b['worst_ordinal']})" if b['worst_ms'] is not None else
                 f"never ({b['worst_ordinal']})")
        end = (f"sequence {b['cut_seq']}, {len(b['cut_missing'])} missing" if b['kind'] == 'burst' else
               f"{b['next_steps']['steps']} steps (want {b['next_steps']['want']}), {b['next_steps']['gap_ms']} ms")
        lines.append(f"| {group} | {b['names']} | {worst} | {b['target_ms']:,} | {len(b['saves'])} | "
                     f"{', '.join(map(str, b['never'])) or '-'} | {', '.join(map(str, b['over'])) or '-'} | {end} | "
                     f"{'OVER' if save_misses_of(b, group) else 'within'} |")
    return lines
