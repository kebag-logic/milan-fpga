[A654] TAKEN
Branch: processor `190-per-source-tspec` from main 5addf29759a22372ed6aa3e1d52a3aad29e3ecd7
Authoritative references: ruling 6256563927 (PART 1 only); IEEE 802.1Q-2018 35.2.2.8.4; Milan v1.2 4.3.3.2 Table 4.4
Interpreted scope: replace the scalar `cfg_tspec_max_frame_i[15:0]` with the approved per-source `cfg_tspec_max_frame_i[N_STREAM_OUT_P*16-1:0]`, indexed like `cfg_stream_id_i`, so every engine-driven DECLARE_TALKER captures its own source's MaxFrameSize (`protocol_processor_top.sv:2700`); suite cases for two sources with different values, each with a planted mutant; the docs that record the port. No register-map change and no other port or parameter change.
Validation plan: every processor suite, lint, make check, gen_matrix --check, syn/yosys/run.sh and every campaign that builds the top, at base and head; parent consumer gates on an uncommitted scratch parent that drives every slot with the old scalar (no parent behaviour change).
Blockers: none yet
comment id 6256580298
