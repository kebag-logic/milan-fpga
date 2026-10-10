#!/usr/bin/env python3
"""Write disposable harness variants of sim_phc_step.cpp for review probes.

Usage: make_harness_probes.py <exact-head sim_phc_step.cpp> <output dir>

answered:  the unanswered-crossing arm answers its crossing request again
           (answer_crossing=true); the named third-request check must fail.
partial:   the crossing request receives Pdelay_Resp but never its
           Pdelay_Resp_Follow_Up; IEEE 802.1AS-2020 11.2.19 counts that
           exchange lost, so the named third-request check must still pass.
"""
import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, name: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{name}: anchor not unique")
    return text.replace(old, new)


def main() -> None:
    src = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    answered = replace_once(src, 'silence_across_step("unanswered crossing", false)',
                            'silence_across_step("unanswered crossing", true)', "answered")
    (out / "answered").mkdir(exist_ok=True)
    (out / "answered" / "sim_phc_step.cpp").write_text(answered)
    partial = replace_once(
        src, "    if (!answer_ || !answer_probe_) return;\n",
        "    if (!answer_) return;\n"
        "    if (!answer_probe_) {\n"
        "      const uint64_t t2p = tx_cycle_ * kTickNs + kPeerEpochNs + link_ns_;\n"
        "      auto rp = header(3, seq, 20, 0x0200);\n"
        "      rp.timestamp(t2p); rp.put(kOurId, 8); rp.put(1, 2);\n"
        "      schedule(std::move(rp), tx_cycle_ + (2 * link_ns_ + kTurnNs) / kTickNs);\n"
        "      return;\n"
        "    }\n", "partial")
    (out / "partial").mkdir(exist_ok=True)
    (out / "partial" / "sim_phc_step.cpp").write_text(partial)


if __name__ == "__main__":
    main()
