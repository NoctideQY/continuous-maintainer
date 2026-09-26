#!/usr/bin/env python3
"""Determine whether a maintenance project is due from maintenance-state.md."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


KEY_RE = re.compile(r"^([A-Za-z_]+):\s*(.*?)\s*$")
CADENCE_RE = re.compile(r"^(?:every\s+)?(\d+)\s+day[s]?$", re.I)


def parse_state(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = KEY_RE.match(line.strip())
        if match:
            values[match.group(1)] = match.group(2).strip().strip("'\"")
    return values


def cadence_delta(value: str) -> timedelta:
    normalized = value.lower().strip()
    if normalized == "daily":
        return timedelta(days=1)
    if normalized == "weekly":
        return timedelta(days=7)
    if normalized in {"biweekly", "fortnightly"}:
        return timedelta(days=14)
    if normalized == "monthly":
        return timedelta(days=30)
    match = CADENCE_RE.match(normalized)
    if match:
        return timedelta(days=int(match.group(1)))
    raise ValueError(f"Unsupported cadence: {value!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--now", help="Override current time with an ISO-8601 timestamp")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    state_path = root / "maintenance-state.md"
    if not state_path.exists():
        print(json.dumps({"initialized": False, "due": True, "reason": "missing maintenance-state.md"}))
        return 0

    state = parse_state(state_path)
    timezone = ZoneInfo(state.get("timezone", "UTC"))
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone)

    last = state.get("last_maintenance_at")
    if not last:
        print(json.dumps({"initialized": True, "due": True, "reason": "no completed maintenance"}))
        return 0

    last_dt = datetime.fromisoformat(last)
    next_due = last_dt + cadence_delta(state.get("cadence", "weekly"))
    result = {
        "initialized": state.get("initialized", "false").lower() == "true",
        "due": now >= next_due,
        "now": now.isoformat(),
        "last_maintenance_at": last_dt.isoformat(),
        "next_due_at": next_due.isoformat(),
        "cadence": state.get("cadence", "weekly"),
        "timezone": state.get("timezone", "UTC"),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
