# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Config loading + validation.
#!
#! `tomllib` is standard library from Python 3.11, so the harness starts on a
#! bare jump host with no pip install. A placeholder left in the file is a
#! start-up REFUSAL, never a guess: the whole point of the config file is that
#! the scripts carry no bench identity of their own, and a silently-defaulted
#! host would put one back.

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

#: Values that mean "you did not fill this in". Reaching the bench with one of
#: these still in place is a configuration error, not a run.
PLACEHOLDERS = {
    "JUMP_HOST_ALIAS", "CONTROLLER_HOST_ALIAS", "IFACE_NAME",
    "BOARD_A_SSH_ALIAS", "BOARD_B_SSH_ALIAS",
}

DEFAULT_CONFIG_ENV = "MILAN_HARNESS_CONFIG"


class ConfigError(Exception):
    """Raised for anything that would make the run meaningless if guessed."""


@dataclass(frozen=True)
class Board:
    name: str
    ssh: str
    via_jump: bool
    role: str
    csr_base: int
    datapath_clk_hz: int
    version_expect: int
    n_listeners: int
    n_talkers: int
    pcm_ring_csr: int
    mac_loopback_csr: int
    dma_ts_offset_csr: int
    alsa_capture_device: str
    alsa_capture_channels: int
    user_mtd_mount: str
    power_outlet: int
    netif: str

    def cycles_to_us(self, cycles: float) -> float:
        """Latency taps count axis_clk cycles; this is the only conversion."""
        return cycles * 1e6 / self.datapath_clk_hz


@dataclass(frozen=True)
class Config:
    path: Path
    raw: dict
    boards: tuple[Board, ...]

    # --- convenience accessors (all raise ConfigError on a missing section) --
    def section(self, name: str) -> dict:
        try:
            return self.raw[name]
        except KeyError as exc:
            raise ConfigError(f"{self.path}: missing [{name}] section") from exc

    def get(self, section: str, key: str, default=None):
        return self.section(section).get(key, default)

    def board(self, name: str) -> Board:
        for b in self.boards:
            if b.name == name:
                return b
        raise ConfigError(f"no [[board]] named {name!r} in {self.path}")

    @property
    def run_root(self) -> Path:
        return Path(os.path.expanduser(self.get("run", "root", "./harness-runs")))

    @property
    def phase_timeouts(self) -> dict:
        return self.section("phase_timeout_s")

    @property
    def items_path(self) -> str:
        """Where the item registry lives - private repo, config, or env.

        Empty means "not configured", which the runner turns into BLOCKED for
        every item-driven phase. It never crashes and never invents a path.
        """
        return (os.environ.get("MILAN_HARNESS_ITEMS")
                or self.get("items", "path", "") or "")

    @property
    def items_overlay(self) -> str:
        return (os.environ.get("MILAN_HARNESS_ITEMS_OVERLAY")
                or self.get("items", "overlay", "") or "")


def _need(d: dict, key: str, where: str):
    if key not in d:
        raise ConfigError(f"{where}: missing key {key!r}")
    v = d[key]
    if isinstance(v, str) and v in PLACEHOLDERS:
        raise ConfigError(
            f"{where}: {key} is still the template placeholder {v!r} - fill in "
            f"the config file (the scripts deliberately hold no bench identity)"
        )
    return v


def _board(d: dict, idx: int) -> Board:
    where = f"[[board]] #{idx}"
    return Board(
        name=_need(d, "name", where),
        ssh=_need(d, "ssh", where),
        via_jump=bool(d.get("via_jump", True)),
        role=d.get("role", ""),
        csr_base=int(_need(d, "csr_base", where)),
        datapath_clk_hz=int(_need(d, "datapath_clk_hz", where)),
        version_expect=int(_need(d, "version_expect", where)),
        n_listeners=int(d.get("n_listeners", 1)),
        n_talkers=int(d.get("n_talkers", 1)),
        pcm_ring_csr=int(d.get("pcm_ring_csr", 0)),
        mac_loopback_csr=int(d.get("mac_loopback_csr", 0)),
        dma_ts_offset_csr=int(d.get("dma_ts_offset_csr", 0)),
        alsa_capture_device=d.get("alsa_capture_device", "hw:0,0"),
        alsa_capture_channels=int(d.get("alsa_capture_channels", 2)),
        user_mtd_mount=d.get("user_mtd_mount", ""),
        power_outlet=int(d.get("power_outlet", -1)),
        netif=d.get("netif", "eth0"),
    )


def find_config(explicit: str | None = None) -> Path:
    """Locate the config: --config, then $MILAN_HARNESS_CONFIG, then the template.

    The template resolves last and *only* so that ``--dry-run`` works out of the
    box; its placeholders make any real bench call fail loudly.
    """
    for cand in (explicit, os.environ.get(DEFAULT_CONFIG_ENV)):
        if cand:
            p = Path(os.path.expanduser(cand))
            if not p.is_file():
                raise ConfigError(f"config file not found: {p}")
            return p
    return Path(__file__).resolve().parent.parent / "config" / "bench.example.toml"


def load(explicit: str | None = None, *, allow_placeholders: bool = False) -> Config:
    path = find_config(explicit)
    with path.open("rb") as fh:
        raw = tomllib.load(fh)

    if raw.get("schema") != "kebag-logic/milan-harness-config":
        raise ConfigError(f"{path}: not a milan-harness config (wrong `schema`)")

    boards_raw = raw.get("board") or []
    if not boards_raw:
        raise ConfigError(f"{path}: at least one [[board]] table is required")

    if allow_placeholders:
        # --dry-run runs against the mock, so the template is a legitimate input.
        # Substitute a marker so the *shape* is still exercised end to end.
        raw = _substitute_placeholders(raw)
        boards_raw = raw["board"]

    boards = tuple(_board(b, i) for i, b in enumerate(boards_raw))
    names = [b.name for b in boards]
    if len(set(names)) != len(names):
        raise ConfigError(f"{path}: duplicate [[board]] name in {names}")

    for req in ("run", "exec", "retry", "notify", "jump", "controller", "items",
                "audio", "latency", "matrix", "soak", "phase_timeout_s"):
        if req not in raw:
            raise ConfigError(f"{path}: missing [{req}] section")

    _validate_ranges(path, raw)
    return Config(path=path, raw=raw, boards=boards)


def _substitute_placeholders(raw: dict) -> dict:
    def walk(o):
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v) for v in o]
        if isinstance(o, str) and o in PLACEHOLDERS:
            return "mock-" + o.lower().replace("_", "-")
        return o
    return walk(raw)


def _validate_ranges(path: Path, raw: dict) -> None:
    audio = raw["audio"]
    rate = int(audio.get("rate_hz", 0))
    tone = int(audio.get("tone_hz", 0))
    if rate <= 0 or tone <= 0:
        raise ConfigError(f"{path}: [audio] rate_hz and tone_hz must be positive")
    if rate % tone:
        raise ConfigError(
            f"{path}: [audio] {rate} Hz / {tone} Hz is not an integer number of "
            f"samples per period - the coherent (un-windowed) FFT the THD+N "
            f"method depends on requires an exact-period tone"
        )
    lat = raw["latency"]
    if float(lat.get("in_system_budget_us", 0)) <= 0:
        raise ConfigError(f"{path}: [latency] in_system_budget_us must be positive")
    if not lat.get("pto_sweep_us"):
        raise ConfigError(f"{path}: [latency] pto_sweep_us must list at least one pto")
    r = raw["retry"]
    if int(r.get("attempts", 0)) < 1:
        raise ConfigError(f"{path}: [retry] attempts must be >= 1")
