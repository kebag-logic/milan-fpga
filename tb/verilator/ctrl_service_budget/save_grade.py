# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""A save's grading (#665): the saves a log shows, read off the store's flash steps; a change's time from its mark to
durable against its stated worst case (save_window.bound_ms), a change while a save is in flight's too; each
channel's longest record while every channel is held at its refill rate; the passes that carry the store's step
(THE STEP); and an aged window's opening age and the aged step among its records. grade.grade calls these for every
group; grade.save_phase reads a save's flash phases off first_save.
"""
from __future__ import annotations

from dataclasses import dataclass

import grade
import save_window
import scenario


@dataclass
class Save:
    """The first save a log shows, read off the store's flash steps (sim_main.cpp's FLASHOP, FLASHRD, FLASHPOLL)."""
    erase: int                              # its erase's cycle
    base: int                               # the slot it writes
    pages: list[tuple[int, int, int]]       # each page program: cycle, address, bytes
    image: int                              # the bytes its pages program, the container's length
    verified: list[tuple[int, int]]         # each read-back of the slot after its last page: its last read, bytes
    durable: int | None                     # the last read of the read-back that completes the verify, or None
    steps: list[int]                        # every flash step's cycle from its erase to durable (or the log's end)


def first_save(log: grade.Log, n: int = 0) -> Save | None:
    """The log's first save (or its n-th after it): its erase, the pages programmed before the next erase, and the
    slot's read-backs after the last page, the verify, which ends when they have read back every programmed byte
    (nvm_store.c, the verify step); None when the log shows no such erase."""
    erases = [(c, a) for c, op, a, _ in log.flash_ops if op == grade.FLASH_ERASE]
    if len(erases) <= n:
        return None
    erase, base = erases[n]
    stop = erases[n + 1][0] if len(erases) > n + 1 else 1 << 62
    pages = [(c, a, n) for c, op, a, n in log.flash_ops if op == grade.FLASH_PROGRAM and erase < c < stop]
    image = sum(n for *_, n in pages)
    last = pages[-1][0] if pages else 1 << 62
    verified, done, durable = [], 0, None
    for first, end, address, n in merged_reads(log):
        if last < first < stop and base <= address < base + image:
            verified.append((end, n))
            done += n
            if durable is None and done >= image:
                durable = end
    until = durable if durable is not None else 1 << 62
    steps = sorted([erase, *(c for c, _, _ in pages), *(c for c in log.polls if erase <= c <= until),
                    *(first for first, _, a, _ in merged_reads(log) if erase < first <= until
                      and base <= a < base + image)])
    return Save(erase, base, pages, image, verified, durable, steps)


def merged_reads(log: grade.Log) -> list[tuple[int, int, int, int]]:
    """The journal's runs of reads (FLASHRD), each later one that starts inside the span a run has read and within a
    millisecond of its last (sim_main.cpp's read_gap) merged into it: one read-back step's span, whatever word
    reads it took."""
    out: list[list[int]] = []
    for first, last, address, n in log.reads:
        if out and out[-1][2] <= address <= out[-1][2] + out[-1][3] and first - out[-1][1] <= log.sys_hz // 1000:
            run = out[-1]
            run[1], run[3] = max(run[1], last), max(run[3], address + n - run[2])
        else:
            out.append([first, last, address, n])
    return [tuple(run) for run in out]


def save_time(log: grade.Log, group: scenario.Group) -> dict | None:
    """A change from its mark, the group's save.change, to durable (first_save), against its stated worst case
    (save_window.bound_ms, from the image the group declares): durable within the bound, or not, or never in the
    run. A group that declares a save in flight (save_window.second) times its save.second instead, to durable in
    the save after the first, against the bound with that save in flight, and is refused unless that change was
    marked past the first's first-dirty window and before the first save's erase. The longest gap between
    consecutive flash steps of the save is reported beside it."""
    if not group.save:
        return None
    marks = {name: cycle for cycle, name in log.marks}
    flight = group.save.get('flight')
    which = 'save.change' if flight is None else 'save.second'
    if which not in marks:
        raise grade.Refusal(f'{group.name}: the save was never marked ({which})')
    change = marks[which]
    save = first_save(log, 0 if flight is None else 1)
    if flight is not None and not in_flight(log, marks, change):
        raise grade.Refusal(f"{group.name}: its second change at {change} was not marked past the first change's "
                            f"first-dirty window and before the save in flight erased its slot")
    image, records = group.save['image'], group.save['records']
    if save is not None and save.pages and save.image != image:
        raise grade.Refusal(f'{group.name}: the save programmed {save.image} bytes, its image is {image}')
    bound = save_window.bound_ms(image, records, flight=flight)
    durable = save.durable if save is not None else None
    ms = round(log.ms_of(durable - change), 3) if durable is not None else None
    end = int(log.summary.get('sys', 0))
    gaps = [b - a for a, b in zip(save.steps, save.steps[1:])] if save is not None else []
    return dict(change_sys=change, durable_sys=durable, ms=ms, bound_ms=bound, within=ms is not None and ms <= bound,
                waited_ms=round(log.ms_of(end - change), 3), image=image, records=records, flight=flight,
                steps=save_window.steps(image, records), flash_steps=len(save.steps) if save else 0,
                longest_gap_ms=round(log.ms_of(max(gaps)), 3) if gaps else None, flooded=bool(log.floods))


def in_flight(log: grade.Log, marks: dict[str, int], change: int) -> bool:
    """A second change at change was marked while the first change's save was in flight: past the first's
    first-dirty window, so its capture may have started, and before that save erased its slot."""
    first = first_save(log)
    return ('save.change' in marks and first is not None
            and marks['save.change'] + save_window.DIRTY_MS * log.sys_hz // 1000 < change < first.erase)


def held_load(log: grade.Log, group: scenario.Group) -> None:
    """A held group's receive channels must commit every record its load offered from its change on
    (save_window.loaded), so a burst the filter or a bucket refused is not a load the group held."""
    change = next(cycle for cycle, name in log.marks if name == 'save.change')
    got = {name: sum(1 for c, ch, *_ in log.rxc if ch == n and c >= change) for n, name in grade.CHANNEL.items()}
    if got != group.save['offered']:
        raise grade.Refusal(f"{group.name}: its receive channels committed {got} from its change, the held load "
                            f"offered {group.save['offered']}; refused frames {log.refused[:4]}")


def held(grader: grade.Grader, group: scenario.Group) -> list[dict]:
    """Under every channel at its refill rate (save_window.loaded), each channel's longest record: every record
    from its receive commit to the end of the pass that released it, as the composed rows end (service)."""
    if not group.save or not group.save.get('loaded'):
        return []
    held_load(grader.log, group)
    finish = int(grader.log.summary.get('sys', 0))
    rows = []
    for ch, name in grade.CHANNEL.items():
        records = grade.releases(grader.log, ch)
        if not records:
            continue
        timed = [(r if r is not None else finish) - c for c, _, r in records]
        n = max(range(len(records)), key=lambda k: (records[k][2] is None, timed[k]))
        commit, interface, released = records[n]
        probe = scenario.Probe(f'{group.name}.held.{name}.if{interface}',
                               f'{name.upper()} record, every channel at its refill rate, the longest',
                               grade.SERVICE_FAMILY[name], f'rxc:{ch}', [], path=f'held.{name}')
        row = dict(probe=probe.name, row=probe.row, family=probe.family, interface=interface,
                   path=list(probe.path_key()), start_sys=commit, wait_ms=0.0, ring=name, records=len(records),
                   ahead=sum(1 for _, _, r in records[:n] if r is None or r > commit), starved=released is None)
        stop = finish
        if released is not None:
            taking = grader.taking_pass(released)
            if taking is None:
                raise grade.Refusal(f'{probe.name}: the release at {released} belongs to no work pass')
            stop = grade.served(grader, taking, released)
            row.update(grade.pass_figures(taking))
        row.update(end_sys=stop, sys_cycles=stop - commit, cpu_cycles=grader.cpu_cycles(stop - commit),
                   ms=round(grader.ms(stop - commit), 5), passes=len(grader.window_passes(commit, stop)),
                   **grade.verdicts(grader.ms(stop - commit), probe))
        if released is None:
            row.update(within_budget=False, within_ceiling=False)
        rows.append(dict(row, status='measured'))
    return rows


def step_figures(grader: grade.Grader) -> dict:
    """The passes that carry the store's step (THE STEP, ctrl_loop.h), those that write nothing to the mailbox and
    the work passes: how many, the longest and the longest step, the store's and its flash port's own CPU cycles
    in its pass (build.STORE_MODULES)."""
    passes = list(grader.log.step_passes) + [(p.start_sys, p.cycles, p.count('store')) for p in grader.log.passes
                                             if p.fields.get('step')]
    if not passes:
        return dict(passes=0)
    longest, store = max(passes, key=lambda r: r[1]), max(passes, key=lambda r: r[2])
    return dict(passes=len(passes), cycles=longest[1], ms=round(grader.cpu_ms(longest[1]), 5), start_sys=longest[0],
                store_cycles=store[2], store_ms=round(grader.cpu_ms(store[2]), 5), store_start_sys=store[0])


#: The event type of a TICK record (the contract's), whose word 1 carries its centiseconds.
EV_TICK = next(e.value for e in scenario.CONTRACT.event_types if e.name == 'TICK')


def step_kind(log: grade.Log, start: int, cycles: int) -> str:
    """What the store's step did in the pass [start, start + cycles] (the CPU runs on the bus clock): a page's
    issue, a read-back, a busy poll, an erase, or a step that touched no flash (the capture, the seal, an idle
    store's)."""
    end = start + cycles * log.sys_hz // log.cpu_hz
    if any(start <= c <= end for c, op, _, _ in log.flash_ops if op == grade.FLASH_PROGRAM):
        return 'issue'
    if any(start <= c <= end for c, op, _, _ in log.flash_ops if op == grade.FLASH_ERASE):
        return 'erase'
    if any(start <= first <= end for first, *_ in log.reads):
        return 'read-back'
    return 'poll' if any(start <= c <= end for c in log.polls) else 'none'


#: The step an aged window's phase must take as its aged step (save_window.AGED_LEAD).
AGED_KIND = {'blank': 'read-back', 'program': 'issue', 'verify': 'read-back'}


def opening_age(log: grade.Log, last: int, start: int) -> int:
    """The step's age as a window opens at start: the centiseconds the TICK records posted after the last pass that
    carried the step started at last (ctrl_loop.c counts centiseconds, a TICK record carries one or more)."""
    return sum(w[1] & 0xFFFF for c, w in log.records if last < c <= start and w[0] & 0xFF == EV_TICK)


def empty_passes(log: grade.Log, index: int, start: int) -> list[int]:
    """The passes after pass index, up to the one running at start, that took nothing: no work pass by that index
    (sim_main.cpp prints a pass that writes nothing to the mailbox only in its run's IDLE line)."""
    work = {p.index for p in log.passes}
    running = max((p.index for p in log.passes if p.start_sys <= start), default=index)
    return [i for i in range(index + 1, running + 1) if i not in work]


def aged_steps(grader: grade.Grader, start: int, until: int, last_release: int) -> list[dict]:
    """The aged steps' passes (STEPPASS aged=1) that start in [start, until): each one's start after start, CPU time,
    the store's own, its step (step_kind), and whether it came among the records, before the last release."""
    log = grader.log
    return [dict(start_ms=round(log.ms_of(s - start), 3), cycles=c, ms=round(grader.cpu_ms(c), 5), store=st,
                 kind=step_kind(log, s, c), among=s < last_release)
            for _, s, c, st, aged in log.stepped if aged and start <= s < until]


def aged_refusal(name: str, age: int, got: int, empty: list[int], inside: list[dict]) -> str | None:
    """Why an aged window is refused, or None: it opened at another age than its name declares, a pass took nothing
    between its last step and its opening, or, at the age limit, no aged step taking its phase's heavy step ran in it
    (AGED_KIND), which its next centisecond brings whether or not its records are all released by then."""
    phase = name.partition('@')[2].partition('-')[0]
    if empty:
        return (f"{len(empty)} pass(es) took nothing between its last step and its window, so the step's age "
                "started again")
    if got != age:
        return f"the window opened with the step's age at {got} centiseconds, not {age}"
    if age == save_window.step_age() and not any(a['kind'] == AGED_KIND[phase] for a in inside):
        return f"opened at the age limit, but no aged {AGED_KIND[phase]} ran in it ({inside})"
    return None


def aged_window(grader: grade.Grader, group: scenario.Group, start: int, end: int) -> dict | None:
    """An aged window's (save_window.aged_window) opening age and the aged steps among its records.

    The age is opening_age from the last pass that carried the store's step before the window, through passes that
    each took input (empty_passes: a pass that takes nothing ends the age, ctrl_loop.c). The aged steps among its
    records start after it opened and before the last of its records is released, those after it inside the window
    until its end (aged_steps): a window that drains before its next centisecond takes its aged step after its
    records. Refused for aged_refusal's reasons; otherwise the age, the aged steps among its records and after them,
    and the last release, after the window opened."""
    age = save_window.aged_age(group.name)
    if age is None:
        return None
    log = grader.log
    before = [s for s in log.stepped if s[1] < start]
    if not before:
        raise grade.Refusal(f"{group.name}: no pass carried the store's step before its window, so it has no age")
    index, last = before[-1][:2]
    released = [r for ch in grade.CHANNEL for c, _, r in grade.releases(log, ch) if start <= c <= end and r]
    last_release = max(released, default=end)
    inside = aged_steps(grader, start, end + 1, last_release)
    refusal = aged_refusal(group.name, age, opening_age(log, last, start), empty_passes(log, index, start), inside)
    if refusal:
        raise grade.Refusal(f'{group.name}: {refusal}')
    return dict(age=age, last_step_sys=last, among=[a for a in inside if a['among']],
                after=[a for a in inside if not a['among']], last_release_ms=round(log.ms_of(last_release - start), 3))
