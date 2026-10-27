"""Every case of the two in-tree sweeps, graded by one torture_campaign.py: one line per capture with its verdict,
missed arms, reason and the full event list (every channel, every attribution), and a digest of all of them.

The cases are built exactly as test_audio_composition_sweep and test_audio_slip_before_a_constant_mask build them,
including the composition sweep's clean captures and its four stated voids, so two planners' outputs can be compared
line by line: a changed line is a swept case whose grade or listing changed.

usage: python3 -I -B dump_sweeps.py <torture_campaign.py> <jobs> <out.txt>
"""
import hashlib
import json
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "r699-6-packet", "scripts"))
import probe_lib  # noqa: E402

T = None


def init(path):
    global T
    T = probe_lib.case(probe_lib.load(path))


def cases():
    out = []
    for frames in (8192, 16384):
        out.append(("composition clean", frames, 4, []))
        for d in range(-4, 5):
            for mask in T._SWEEP_MASKS:
                for pair in ((0, 1), (2, 3)):
                    extra = [{"kind": "flip", "index": arm[1] + d, "channel": channel, "mask": mask}
                             for arm in T._sweep_arms(frames) for channel in pair]
                    out.append((f"composition frames={frames} d={d} mask={mask:#x} pair={pair}", frames, 4, extra))
    for at, channel, mask in ((299, 0, 0x40000), (500, 2, 0x80000), (700, 1, 0x200), (701, 1, 0x100)):
        out.append((f"composition void at={at}", 8192, 4, [{"kind": "flip", "index": at, "channel": channel,
                                                             "mask": mask}]))
    masks = (0x80000, 0x40000, 0x100, 0x00F00F00, 0x80100)
    out.append(("before clean", 16384, len(masks), []))
    for length in (64, 65, 100, 300, 2049):
        for begin in (3000, 4089, 6143):
            for gap in (1, 2, 17, 63, 64):
                for n in (3, -2):
                    extra = [{"kind": "drop" if n > 0 else "repeat", "index": begin - gap, "n": abs(n)}]
                    extra += [{"kind": "flip", "index": begin + k, "channel": channel, "mask": mask}
                              for channel, mask in enumerate(masks) for k in range(length)]
                    out.append((f"before length={length} begin={begin} gap={gap} n={n}", 16384, len(masks), extra))
    return out


def one(case):
    name, frames, channels, extra = case
    verdict, detail, _ = T._sweep_grade(frames, extra, channels=channels)
    events = sorted((json.dumps(e, sort_keys=True) for e in detail["events"]))
    record = [verdict, sorted(a["index"] for a in detail["planted_missed"]), detail.get("why"), events]
    return name + " | " + json.dumps(record, sort_keys=True)


def main():
    path, jobs, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    init(path)
    todo = cases()
    with multiprocessing.Pool(jobs, initializer=init, initargs=(path,)) as pool:
        lines = pool.map(one, todo, chunksize=4)
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    digest = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    print(json.dumps({"cases": len(lines), "sha256": digest}))


if __name__ == "__main__":
    main()
