# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! The item registry loader - `es-N.M` rows.
#!
#! **The registry FILE is not in this repository.** Item procedures, expected
#! values and pass criteria are derived from material that stays private; this
#! module is the generic machinery that loads such a file, checks it is sound,
#! and makes an unimplemented item VISIBLE. Only item IDs appear in this repo,
#! which is what `docs/SPEC_TRACEABILITY.md` already does.
#!
#! The registry's whole job is that a run report listing 22 passes cannot stay
#! silent about the rest: every id has a row, a stub row says `not-implemented`
#! out loud, and the file's OWN declared shape (`expect_total`, `[expect]`
#! group counts) is asserted, so a copy-paste that loses a row cannot pass
#! unnoticed. The shape is declared by the file rather than hardcoded here
#! precisely because the shape is part of the private plan.

from __future__ import annotations

import os
import re
import tomllib
from dataclasses import dataclass, replace
from pathlib import Path

ID_RE = re.compile(r"^es-(\d+)\.(\d+)$")
SCHEMA = "kebag-logic/milan-harness-items"
STATUSES = ("implemented", "stub", "manual-only", "blocked")


class RegistryError(Exception):
    """Registry unusable. Callers turn this into BLOCKED, never FAILED."""


class RegistryMissing(RegistryError):
    """No registry configured / the configured path does not exist."""


@dataclass(frozen=True)
class Item:
    id: str
    group: str
    area: str
    mapping: str
    runner: str
    status: str
    note: str

    @property
    def implemented(self) -> bool:
        return self.status == "implemented" and bool(self.runner)

    def sort_key(self) -> tuple[int, int]:
        m = ID_RE.match(self.id)
        return (int(m.group(1)), int(m.group(2))) if m else (999, 999)


class Registry:
    def __init__(self, items: list[Item], source: Path, shape: dict,
                 overlay: Path | None = None):
        self.items = sorted(items, key=lambda i: i.sort_key())
        self.source = source
        self.shape = shape           # the file's own declared shape
        self.overlay = overlay
        self._by_id = {i.id: i for i in self.items}

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, iid: str) -> Item:
        try:
            return self._by_id[iid]
        except KeyError:
            raise RegistryError(f"no such item {iid!r} in {self.source}") from None

    def get(self, iid: str) -> Item | None:
        return self._by_id.get(iid)

    def groups(self) -> dict[str, list[Item]]:
        out: dict[str, list[Item]] = {}
        for i in self.items:
            out.setdefault(i.group, []).append(i)
        return out

    def implemented(self) -> list[Item]:
        return [i for i in self.items if i.implemented]

    def stubs(self) -> list[Item]:
        return [i for i in self.items if not i.implemented]

    def tally(self) -> dict:
        by_status: dict[str, int] = {}
        for i in self.items:
            by_status[i.status] = by_status.get(i.status, 0) + 1
        return {
            "total": len(self.items),
            "implemented": len(self.implemented()),
            "not_implemented": len(self.stubs()),
            "by_status": by_status,
            "by_group": {g: len(v) for g, v in self.groups().items()},
            "source": str(self.source),
        }

    # -------------------------------------------------------------- checking
    def validate(self) -> list[str]:
        """Return findings; an empty list means the registry is sound."""
        findings: list[str] = []
        seen: set[str] = set()
        for i in self.items:
            if not ID_RE.match(i.id):
                findings.append(f"{i.id}: malformed item id")
                continue
            if i.id in seen:
                findings.append(f"{i.id}: duplicate row")
            seen.add(i.id)
            want_group = "es-" + i.id.split("-", 1)[1].split(".", 1)[0]
            if i.group != want_group:
                findings.append(f"{i.id}: group {i.group!r} does not match the id")
            if i.status not in STATUSES:
                findings.append(f"{i.id}: unknown status {i.status!r}")
            if i.status == "implemented" and not i.runner:
                findings.append(f"{i.id}: status implemented but no runner")
            if i.runner and i.status == "stub":
                findings.append(f"{i.id}: has runner {i.runner!r} but status stub")
            if i.status in ("manual-only", "blocked") and not i.note:
                findings.append(f"{i.id}: {i.status} with no note saying why")

        counts = {g: len(v) for g, v in self.groups().items()}
        want_groups = self.shape.get("groups") or {}
        for g, want in want_groups.items():
            got = counts.get(g, 0)
            if got != int(want):
                findings.append(f"{g}: {got} rows, the registry declares {want}")
        for g in counts:
            if want_groups and g not in want_groups:
                findings.append(f"{g}: group not declared in the registry's [expect]")
        want_total = self.shape.get("total")
        if want_total is not None and len(self.items) != int(want_total):
            findings.append(
                f"registry holds {len(self.items)} rows, declares {want_total}")
        if want_total is None and not want_groups:
            findings.append(
                "registry declares no shape (`expect_total` / [expect].groups) - "
                "without it a lost row is invisible, which is the one thing this "
                "file exists to prevent")
        return findings


def _items_from(raw: dict, where: Path) -> list[Item]:
    out = []
    for n, r in enumerate(raw.get("item") or []):
        try:
            out.append(Item(
                id=r["id"], group=r["group"], area=r.get("area", ""),
                mapping=r.get("mapping", ""), runner=r.get("runner", ""),
                status=r.get("status", "stub"), note=r.get("note", ""),
            ))
        except KeyError as exc:
            raise RegistryError(f"{where}: [[item]] #{n} missing {exc}") from None
    return out


def _shape(raw: dict) -> dict:
    shape: dict = {}
    if "expect_total" in raw:
        shape["total"] = int(raw["expect_total"])
    groups = (raw.get("expect") or {}).get("groups")
    if groups:
        shape["groups"] = {str(k): int(v) for k, v in groups.items()}
    return shape


def resolve_path(configured: str = "") -> Path:
    """Resolve the registry path, or raise RegistryMissing.

    Order: explicit argument, then `$MILAN_HARNESS_ITEMS`. There is deliberately
    no compiled-in fallback location - a guessed path is exactly the kind of
    bench identity this repo keeps out of its scripts.
    """
    cand = configured or os.environ.get("MILAN_HARNESS_ITEMS", "")
    if not cand:
        raise RegistryMissing(
            "no item registry configured: set [items].path in the bench config "
            "(it lives in the private test repository's validation/ directory) "
            "or $MILAN_HARNESS_ITEMS")
    p = Path(os.path.expanduser(cand))
    if not p.is_file():
        raise RegistryMissing(f"item registry not found at {p}")
    return p


def load(path: str | os.PathLike | None = None,
         overlay: str | os.PathLike | None = None) -> Registry:
    """Load a registry file, merge an optional overlay, validate, return it.

    The overlay may only refine rows the registry already has (area / mapping /
    runner / status / note). It cannot introduce an id and cannot remove one, so
    the declared-shape gate holds either way.
    """
    p = resolve_path(str(path) if path else "")
    with p.open("rb") as fh:
        raw = tomllib.load(fh)
    if raw.get("schema") != SCHEMA:
        raise RegistryError(f"{p}: not a milan-harness item registry (`schema`)")
    items = _items_from(raw, p)
    shape = _shape(raw)

    ov_path = None
    if overlay:
        ov_path = Path(os.path.expanduser(str(overlay)))
        if not ov_path.is_file():
            raise RegistryMissing(f"item overlay not found: {ov_path}")
        with ov_path.open("rb") as fh:
            ov_raw = tomllib.load(fh)
        by_id = {i.id: i for i in items}
        for r in (ov_raw.get("item") or []):
            iid = r.get("id")
            if iid not in by_id:
                raise RegistryError(
                    f"{ov_path}: overlay row {iid!r} is not in the registry - an "
                    f"overlay may refine rows, never add them")
            cur = by_id[iid]
            by_id[iid] = replace(
                cur,
                area=r.get("area", cur.area),
                mapping=r.get("mapping", cur.mapping),
                runner=r.get("runner", cur.runner),
                status=r.get("status", cur.status),
                note=r.get("note", cur.note),
            )
        items = list(by_id.values())

    reg = Registry(items, p, shape, ov_path)
    findings = reg.validate()
    if findings:
        raise RegistryError(f"{p}: registry is not sound:\n  " + "\n  ".join(findings))
    return reg
