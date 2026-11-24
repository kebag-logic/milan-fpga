# [A839] Proposal: hosted ccache through the CI image, and Actions cache retention

Status: proposal only. Nothing in `ci/image`, no workflow file and no Actions cache was changed or deleted by this
lane. Figures are from round 2 (REPORT §4) and from a read-only listing of the repository's caches taken
2026-11-24 17:10 CET (`gh api repos/kebag-logic/milan-fpga/actions/caches`, receipts/caches/).

## 0. Summary

1. **Free the quota first (section 2).** The repository holds 326 Actions cache entries, 5.68 GB against GitHub's
   10 GB default. 206 entries (3.64 GB) belong to 14 pull requests that have already merged, and 109 entries
   (1.74 GB) to 7 open ones; dev holds 11 entries (0.31 GB). No PR entry has a dev key: every PR saved its own
   copy of the same tools. Delete the merged PRs' entries now (one manager command, 2.1). Then stop the
   duplication: key each tool cache by its own recipe rather than by every workflow file, and save tool caches
   only from dev (2.2).
2. **ccache in the CI image (section 1.1, the #737 recipe lane).** This gives every Verilator build its
   within-job hits at no quota cost: crf_rx's mutants 47 % less CPU on a cold cache, avtp_rxmon 65 % less
   (round 1), and 6-63 % of a hosted shard's compiles answered within the job (round 2). Logs were identical.
3. **Shards in the image (section 1.2, the adoption lane).** `run_all_suites.sh` already turns ccache on when it
   is on PATH (f09c9a0f), so no suite or workflow command changes for it.
4. **Then a restored per-shard ccache (section 1.3).** Keep one generation of at most 19 x 256 MB, save it
   nightly on dev, and prune older entries. Round 3's stable mutant staging (b01326c5) makes a warm cache answer
   mutant model compiles too: none of those hit across runs before.

## 1. Hosted ccache

### 1.1 The recipe lane (#737, docs/testing/CI_IMAGE.md "Inputs", "Rebuild", "Smoke checks")

The image's package set is derived, never hand-edited. `scripts/ci_tool_inventory.py` derives each request from
the workflow step that installs it (`installed_by`). `ci/image/sources.lock.json` pins each `.deb` by URL, size
and SHA-256 from the dated snapshot (20261014T000000Z). No workflow step installs ccache, and owner 11-14 rules
out per-job installs, so the request must come from the consumer:

1. **The request.** `scripts/run_all_suites.sh` probes `command -v ccache` and exports `OBJCACHE=ccache`
   (f09c9a0f). The inventory already follows executed scripts. It should record that probe as an optional-tool
   consumer: a `tools[]` entry `{"tool": "ccache", "kind": "package", "installed_by": [...]}`. Its `installed_by`
   names the steps that run the sweep: rtl.yml `verilator-shards` "Run this exhaustive suite shard",
   `verilator-preflight` "Run the sweep's preflight self-tests once for this head" (it runs no compile, but the
   probe runs), and `physical-gptp` "Run the physical gPTP suite with its own deadline". The command table
   classifies `ccache` invocations: `ccache` is only ever called through verilated.mk's `$(OBJCACHE)`, which
   prefixes the compiler, so the table entry is the compiler pattern under an `OBJCACHE` prefix. If the inventory
   cannot express an optional-tool probe, the recipe lane decides that mechanism. It is the one design choice
   here; everything below follows from it.
2. **The lock.** `ci/image/resolve_packages.py` resolves noble's `ccache` from the same snapshot and records the
   `.deb`s it pulls in (URL, size, SHA-256, the `tool: ccache` tag) in `sources.lock.json`. Expected: ccache
   4.9.1 and libhiredis1.1.0, the rest already in the base. The resolver's answer is authoritative, not this
   expectation.
3. **PATH.** The Dockerfile's PATH must not gain `/usr/lib/ccache`. Debian's package installs `gcc`/`g++`
   masquerade links there. On PATH they would wrap every compile in the image, including the firmware builders'
   compiles that `firmware-boundary` judges (round 1 §2.3: that gate's compiler invocations are what it proves).
   With only `/usr/bin/ccache` present, ccache runs exactly where `$(OBJCACHE)` asks for it: Verilator's model,
   runtime and testbench compiles.
4. **Smoke.** `ci/image/smoke.py` gains a ccache family, run offline in the produced image. `ccache --version`
   must equal the locked version. Then compile one translation unit twice with `CCACHE_DIR` under `/scratch`:
   the first is a `cache_miss`, the second a `direct_cache_hit` (`ccache --print-stats`), and the two objects are
   byte-identical.
5. **Rebuild and publish** are the manager's, by CI_IMAGE.md "Rebuild": two `--no-cache` builds with identical
   digests, `--record-lock`, the smoke run, then publication. The recipe digest changes with the pin, so the
   image tag changes with it.

### 1.2 The adoption lane (CI_IMAGE.md "CI and act adoption")

When the Verilator workers run in the image (`container: <registry>@<digest>`), nothing else needs to change.
The sweep finds ccache on PATH and exports `OBJCACHE=ccache`. ccache's cache is the job's own `$HOME/.cache/ccache`,
empty at job start. This gives the within-job hits:

| shard (hosted min, 300da99b) | hits within one cold job (round 2 §4.2) | where they come from |
|---|---:|---|
| 17 (23.5) | 416 / 662 (63 %) | avtp_rxmon's 8 builds and 5 mutant drivers share runtime and testbench objects |
| 1 (26.4) | 131 / 471 (28 %) | milan_dp__1's six builds share the runtime |
| 4 (24.8) | 11 / 196 (6 %) | one milan_dp piece: little repeats inside one job |

Verdicts: round 1 compared crf_rx's mutants (23/23) and avtp_rxmon's 3201-line log through ccache against no
cache, and both were identical. The aggregate's tally is unchanged by construction: ccache returns the object
the compiler would have written.

### 1.3 Then a restored per-shard cache (after section 2 frees the quota)

In the `verilator-shards` job, edited in `.github/ci-templates/rtl.yml` and generated by
`scripts/ci_gate_workflows.py`, with `scripts/ci_events.py` pinning the steps:

```yaml
env:   # job level
  CCACHE_DIR: ${{ runner.temp }}/ccache
  CCACHE_MAXSIZE: 256M          # measured working set 136-183 MB per shard (round 2 §4.2)
  CCACHE_COMPRESSION: 'true'
  CCACHE_COMPRESSLEVEL: '1'     # level 9 saves 12 % (156 -> 137 MB on shard 4) for more CPU
steps:
  - name: Restore this shard's compiler cache
    uses: actions/cache/restore@v4
    with:
      path: ${{ runner.temp }}/ccache
      key: ccache-${{ env.VERILATOR_VERSION }}-848d926e-<image digest>-shard${{ matrix.shard }}-${{ github.run_id }}
      restore-keys: ccache-${{ env.VERILATOR_VERSION }}-848d926e-<image digest>-shard${{ matrix.shard }}-
  # "Run this exhaustive suite shard" unchanged
  - name: Save this shard's compiler cache (dev schedule only)
    if: ${{ always() && github.event_name == 'schedule' && github.ref == 'refs/heads/dev' }}
    uses: actions/cache/save@v4
    with:
      path: ${{ runner.temp }}/ccache
      key: ccache-${{ env.VERILATOR_VERSION }}-848d926e-<image digest>-shard${{ matrix.shard }}-${{ github.run_id }}
```

- The key binds the toolchain: the Verilator version and commit, and the image digest, which fixes g++ and
  ccache. It also binds the shard, whose models are mostly disjoint from other shards'. It does not bind an input
  digest: ccache keys every object by its own inputs, and an input digest in the Actions key would make every
  RTL-touching PR miss the whole cache rather than only the objects it changed.
- PRs restore dev's newest nightly entry and never save. A PR can read dev's scope; dev cannot read a PR's.
- A `ccache-prune` job runs on the schedule only, `needs: verilator-shards`, with
  `permissions: {contents: read, actions: write}`. It deletes every `ccache-*-shard<N>-*` entry except the newest
  per shard, so one generation (at most 19 x 256 MB = 4.9 GB, measured ~3.4 GB) is resident.
- `CCACHE_BASEDIR` is not needed. Verilator's generated Makefiles compile with relative paths, and the checkout
  path is the same on every hosted run (`<home-path>/work/milan-fpga/milan-fpga`).
- The contract needs `actions/cache/restore@v4` and `actions/cache/save@v4` added to `RECORDED_ACTIONS`, the new
  steps added to `RTL_STEP_LISTS`, and mutation arms for each new step: a save outside the schedule, a PR save,
  a missing restore-keys line, and a key without the image digest.

Estimates, with a warm restore assumed to hit unchanged models, the runtime and the testbenches:

| shard (hosted min) | what hits | estimate |
|---|---|---|
| 17 (23.5) | avtp_rxmon builds and mutants, milan_dp_render__0 builds | ~-5.5 min |
| 1 (26.4) | milan_dp__1's 6 builds, capture_coherence__3's runtime/testbench | ~-3 to -4 min |
| 4 (24.8) | milan_dp__0's 7 builds (C++ is ~85 % of each build's wall) | ~-3 min |
| 11 (~20-22 after #1001) | crf_rx's mutants: with b01326c5's stable staging, the mutant models too | ~-2 to -3 min |
| 0, 5, 7 | 1-3 builds | < 1 min |

## 2. Actions cache retention

### 2.1 Now: delete the merged PRs' entries (manager, one command; this lane deleted nothing)

PR-scoped entries are readable only by their own PR's runs. Once a PR has merged or closed, nothing can read
them, and they wait up to seven days for GitHub's idle eviction while they count against the quota. At the
listing:

| PRs | entries | bytes |
|---|---:|---:|
| merged: 934 945 947 952 953 958 959 960 961 971 974 975 978 988 | 206 | 3.64 GB |
| open: 966 982 984 986 992 995 1001 | 109 | 1.74 GB |
| dev | 11 | 0.31 GB |

By family: elaborate-sbt 2.41 GB (all PR-scoped, no dev entry); Verilator 2.12 GB (0.09 on dev); Yosys 0.43;
tsn-gen 0.32; rv32-sdk 0.15 (dev only); elaborate pip pins 0.14; everything else under 0.06 GB.

```sh
# for each merged or closed PR still holding entries (re-list first: the set moves)
for pr in 934 945 947 952 953 958 959 960 961 971 974 975 978 988; do
  test "$(gh pr view "$pr" -R kebag-logic/milan-fpga --json state --jq .state)" != OPEN || continue
  gh cache list -R kebag-logic/milan-fpga --ref "refs/pull/$pr/merge" --limit 100 --json id --jq '.[].id' |
    xargs -r -n1 gh cache delete -R kebag-logic/milan-fpga
done
```

This deletes caches only and changes no verdict: a later run of a merged PR does not exist. It frees 3.64 GB.

### 2.2 Durable: stop the duplication (the workflow owner's lane; contract changes in scripts/ci_events.py)

1. **Key each tool by its own recipe.** Today's keys end in `hashFiles('.github/workflows/*.yml')`, so any
   workflow edit on dev or in a PR gives a new key. A PR whose merge commit differs from dev's last saving run in
   any workflow line then misses dev's entry, rebuilds and saves its own: that is why no PR entry above has a dev
   key. Replace the term with the digest of the tool's own build step: the version, the commit and the step's
   normalised script. `scripts/ci_gate_workflows.py` already computes this kind of `recipe_digest` for the fast
   tool key. The generator writes it as a literal and the contract pins it, as it pins the Verilator key today.
   A PR that does not change a tool's recipe then restores dev's exact entry and saves nothing (actions/cache
   does not save on an exact hit).
2. **Save tool caches only from dev.** Split each `actions/cache@v4` tool step into `actions/cache/restore@v4`
   (every event) and `actions/cache/save@v4` with
   `if: github.event_name != 'pull_request' && steps.<id>.outputs.cache-hit != 'true'`. A PR that does change a
   recipe builds the tool for itself once per run and stores nothing. A PR that changes the Verilator recipe pays
   ~6-8 min per run; that is the price of leaving PR scopes empty. Leave the Yosys result cache
   (`yosys-results-*`, 0.01 GB) as it is: its PR-scoped save is its design (#350).
3. **Seed dev for every family.** elaborate-sbt has no dev entry at the listing, although elaborate.yml runs on
   `push: [main, dev]`. Its key also hashes every workflow file, so no PR ever reads dev's entry, and GitHub
   evicts it after seven idle days. With item 1's recipe key, each dev push's entry is the one PRs restore,
   which keeps it read and resident.
4. **On PR close, delete that PR's caches.** This needs a small `pull_request: [closed]` job with
   `permissions: actions: write`, guarded to same-repository PRs like `ci-fail-fast`. It is a new workflow
   surface the contract must inventory, so it is optional: 2.1 run weekly by the manager achieves the same.

Expected steady state: dev's one entry per tool family (~0.4 GB), PR scopes near empty, and room for one ccache
generation (≤ 4.9 GB) under the 10 GB default.
