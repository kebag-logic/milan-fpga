Each shipping shape's marker latency, evaluated from hdl/ieee1722/crf/KL_media_if_latency_pkg.sv at the lane head.
verilator --binary -Wno-fatal -Wno-lint hdl/ieee1722/crf/KL_media_if_latency_pkg.sv lat_tb.sv --top-module lat_tb -o Vlat
