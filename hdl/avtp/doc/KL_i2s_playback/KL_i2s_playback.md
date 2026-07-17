# Entity: KL_i2s_playback
- **File:** `hdl/avtp/KL_i2s_playback.sv`
- **Spec:** Philips I2S (64 fs, 1-bit delay, MSB first); Pmod I2S2 DAC = CS4344

Zero-CPU audible listener: taps the AAF depacketizer's PCM transfers (never backpressures), takes channels 0..1 of each interleaved S32BE sample frame (top 24 bits), buffers stereo pairs in a FIFO and serializes on the same free-running divider scheme the AAF talker uses as I2S clock master. MVP clocking free-runs vs the talker's media clock: underrun plays silence, overrun drops a pair, both counted in CSR `I2SPB_STAT` (0x6D8) so silicon measures the ppm drift; CRF media-clock discipline (task #20) retires the rails.

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` / `rst_n` | in | `wire` | Clock (I2S master domain) / reset |
| `pcm_t*_i` | in | | Depacketizer PCM tap (observed transfers) |
| `chans_i` | in | `wire [9:0]` | Channels/frame (live format fmt[31:22]) |
| `i2s_mclk_o` / `i2s_sclk_o` / `i2s_lrck_o` / `i2s_sdin_o` | out | | DAC jack (Pmod I2S2 line-out, own pin set) |
| `underruns_o` / `overruns_o` | out | `logic [15:0]` | Drift rails (CSR 0x6D8) |
