#!/usr/bin/env python3
"""R638-3 probe: fetch every retained Ubuntu fallback URL and compare size and SHA-256 with the lock.

Usage: python3 -I verify_fallbacks.py <checkout>/ci/image/sources.lock.json [workers] [only-tools-file]
Transient HTTP 5xx/network errors are retried up to five times with backoff.
Writes one JSON line per package to stdout; nothing is stored on disk.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import sys
import time
import urllib.request

pins = json.load(open(sys.argv[1]))
rows = [r for r in pins['packages'] if r.get('fallback_urls')]
workers = int(sys.argv[2]) if len(sys.argv) > 2 else 16
if len(sys.argv) > 3:
    only = set(open(sys.argv[3]).read().split())
    rows = [r for r in rows if r['tool'] in only]


def check(row):
    for attempt in range(5):
        result = fetch(row)
        if result['ok'] or 'HTTP Error 4' in result.get('error', '') or 'error' not in result:
            break
        time.sleep(5 * (attempt + 1))
    result['attempts'] = attempt + 1
    return result


def fetch(row):
    url = row['fallback_urls'][0]
    digest = hashlib.sha256()
    size = 0
    try:
        with urllib.request.urlopen(url, timeout=180) as response:
            while chunk := response.read(1 << 20):
                digest.update(chunk)
                size += len(chunk)
    except Exception as error:  # noqa: BLE001 - record the failure
        return {'tool': row['tool'], 'ok': False, 'error': str(error)}
    return {'tool': row['tool'], 'ok': size == row['size'] and digest.hexdigest() == row['sha256'],
            'size': size, 'sha256': digest.hexdigest()}


results = []
with ThreadPoolExecutor(max_workers=workers) as pool:
    for result in pool.map(check, rows):
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)
print(json.dumps({'checked': len(results), 'matching': sum(r['ok'] for r in results)}))
