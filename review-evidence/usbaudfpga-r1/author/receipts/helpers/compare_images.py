"""Compare complete programming data while recording container identity separately."""
from pathlib import Path
import argparse
import hashlib
import json

def programming_data(path):
    data = path.read_bytes()
    offset = 0

    def take(size):
        nonlocal offset
        if size < 0 or offset + size > len(data):
            raise ValueError("truncated image container")
        value = data[offset:offset+size]
        offset += size
        return value

    def length(size):
        return int.from_bytes(take(size), "big")

    if take(length(2)) != bytes.fromhex("0ff00ff00ff00ff000"):
        raise ValueError("unexpected image preamble")
    if length(2) != 1:
        raise ValueError("unexpected first field length")
    for tag in b"abcd":
        if take(1) != bytes([tag]):
            raise ValueError("unexpected metadata field")
        metadata = take(length(2))
        if not metadata.endswith(b"\0"):
            raise ValueError("unterminated metadata field")
    if take(1) != b"e":
        raise ValueError("missing programming-data field")
    payload = take(length(4))
    if not payload or offset != len(data):
        raise ValueError("empty programming data or trailing container bytes")
    return data, payload

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    before, a = programming_data(args.before)
    after, b = programming_data(args.after)
    digest = lambda value: hashlib.sha256(value).hexdigest()
    result = {"container_bytes_identical": before == after,
              "programming_data_identical": a == b,
              "before_container_sha256": digest(before),
              "after_container_sha256": digest(after),
              "before_programming_sha256": digest(a),
              "after_programming_sha256": digest(b),
              "before_programming_bytes": len(a),
              "after_programming_bytes": len(b)}
    (args.out / "before.configuration.bin").write_bytes(a)
    (args.out / "after.configuration.bin").write_bytes(b)
    (args.out / "comparison.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result))
    if a != b:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
