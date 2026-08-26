# `tb/verilator/hostplane` — silicon-shape datapath integration

This suite elaborates `milan_datapath` in the parameter combinations used by
the supported board configurations. It complements the small `milan_dp` unit
shape by exercising traffic, timestamps, media routing, filters, and observer
logic concurrently.

## Cases

- Bring-up checks ID/version, station identity, PHC state, filter setup, and
  stream binding.
- Frame delivery interleaves management, time-sync, and bound AAF traffic and
  checks each destination byte-for-byte.
- Timestamp production checks one record per event frame and no record for
  general messages.
- Filter checks cover blacklist and whitelist operation in both directions.
- Observer stress holds an output lane back while media continues, then checks
  release ordering and telemetry purity.
- Configuration smoke elaborates the small, 4-stream, TDM8, and TDM32-master
  shapes used by the builder matrix.

The harness uses little-endian byte lanes and a single clock pump shared by
the CSR BFM. Generated protocol-processor images are created by the Makefile
before elaboration.

## Run

```sh
cd tb/verilator/hostplane
make
make build
```

`make` builds and runs every case. `make build` performs the elaboration-only
gate used when runtime execution is handled by a separate suite shard.
