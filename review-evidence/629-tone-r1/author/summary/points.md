## pts1

captures: tap 15:27:28.7 for 24.484 s; external 15:27:30.7 for 16.056 s; McASP0 15:27:32.7 for 10.284 s

| Point | Frames | Channel | Level, dBFS RMS | Range, LSB | 997 Hz | 9,973 Hz | SHA-256 |
|---|---|---|---|---|---|---|---|
| (a) the peer's link tap, the peer's talker | 1,151,058 | 0 | -141.09 | -2 to 1 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `6abff90594872f7c...` |
| (a) the peer's link tap, the peer's talker | 1,151,058 | 1 | -141.1 | -2 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `6abff90594872f7c...` |
| (a) the peer's link tap, the peer's talker | 1,151,058 | 2 | -141.48 | -1 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `6abff90594872f7c...` |
| (a) the peer's link tap, the peer's talker | 1,151,058 | 3 | -141.49 | -1 to 0 | absent (0.040 % of the power within 5 Hz) | absent (0.044 % of the power within 5 Hz) | `6abff90594872f7c...` |
| (b) the DUT's link tap, the peer's talker | 1,151,052 | 0 | -141.09 | -2 to 1 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `3e1d81ba2e507e0f...` |
| (b) the DUT's link tap, the peer's talker | 1,151,052 | 1 | -141.1 | -2 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.041 % of the power within 5 Hz) | `3e1d81ba2e507e0f...` |
| (b) the DUT's link tap, the peer's talker | 1,151,052 | 2 | -141.48 | -1 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `3e1d81ba2e507e0f...` |
| (b) the DUT's link tap, the peer's talker | 1,151,052 | 3 | -141.49 | -1 to 0 | absent (0.040 % of the power within 5 Hz) | absent (0.044 % of the power within 5 Hz) | `3e1d81ba2e507e0f...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 0 | -141.09 | -2 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.042 % of the power within 5 Hz) | `7e059d75bf3c1d03...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 1 | -141.1 | -2 to 0 | absent (0.038 % of the power within 5 Hz) | absent (0.039 % of the power within 5 Hz) | `7e059d75bf3c1d03...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 2 | -141.48 | -1 to 0 | absent (0.043 % of the power within 5 Hz) | absent (0.041 % of the power within 5 Hz) | `7e059d75bf3c1d03...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 3 | -141.49 | -1 to 0 | absent (0.034 % of the power within 5 Hz) | absent (0.041 % of the power within 5 Hz) | `7e059d75bf3c1d03...` |
| (d) the external capture, the peer's digital output | 768,000 | 0 | None | 0 to 0 | absent (0.000 % of the power within 5 Hz) | absent (0.000 % of the power within 5 Hz) | `7040fae17dc84aae...` |
| (d) the external capture, the peer's digital output | 768,000 | 1 | None | 0 to 0 | absent (0.000 % of the power within 5 Hz) | absent (0.000 % of the power within 5 Hz) | `7040fae17dc84aae...` |

align (b) vs (c): SAMPLE-EXACT, 480,000 of 480,000 frames equal, first window matched 1 offset(s), slips [], differing 0

counters before dut STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 23629, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 22063
counters before peer STREAM_INPUT 0: MEDIA_LOCKED 0, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 0, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 0
counters after dut STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 219522, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 214061
counters after peer STREAM_INPUT 0: MEDIA_LOCKED 0, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 0, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 0

- format-check: {"ok": true, "talker": "peer-out-0", "listener": "dut-in-0", "talker_fmt": "0205022001006000", "listener_fmt": "0205022001006000", "set": null, "listener_after": "0205022001006000"}
- bind: {"talker": "peer-out-0", "listener": "dut-in-0", "status": 0, "conn_count": 1, "stream_id": "0000000000000000"}
- unbind: {"tag": "control-unbind-as-found", "talker": "020000fffe000001", "tu": 0, "listener": "peer-in-0", "status": 0, "conn_count": 0}
- format-check: {"ok": true, "talker": "peer-out-0", "listener": "peer-in-0", "talker_fmt": "0205022001006000", "listener_fmt": "0205022002006000", "set": {"fmt": "0205022001006000", "status": ["SUCCESS"], "echoed": "0205022001006000"}, "listener_after": "0205022001006000"}
- bind: {"talker": "peer-out-0", "listener": "peer-in-0", "status": 0, "conn_count": 1, "stream_id": "0000000000000000"}
- unbind: {"tag": "teardown", "talker": "<peer-eid>", "tu": 0, "listener": "peer-in-0", "status": 0, "conn_count": 0}
- unbind: {"tag": "teardown", "talker": "<peer-eid>", "tu": 0, "listener": "dut-in-0", "status": 0, "conn_count": 0}
- format-restore: {"listener": "peer-in-0", "fmt": "0205022002006000", "status": ["SUCCESS"]}
- format-check: {"ok": true, "talker": "020000fffe000001-out-0", "listener": "peer-in-0", "talker_fmt": "0205022002006000", "listener_fmt": "0205022002006000", "set": null, "note": "the as-found bind, restored"}
- rebind-as-found: {"status": 0, "conn_count": 1, "stream_id": "0200000000010000"}
- final: equal_to_found=False differ=['rx-peer-0']

## pts2

captures: tap 15:31:13.1 for 24.528 s; external 15:31:15.1 for 18.205 s; McASP0 15:31:17.1 for 16.204 s

| Point | Frames | Channel | Level, dBFS RMS | Range, LSB | 997 Hz | 9,973 Hz | SHA-256 |
|---|---|---|---|---|---|---|---|
| (a) the peer's link tap, the peer's talker | 1,149,834 | 0 | -141.09 | -2 to 1 | absent (0.041 % of the power within 5 Hz) | absent (0.041 % of the power within 5 Hz) | `9d408d76279056d9...` |
| (a) the peer's link tap, the peer's talker | 1,149,834 | 1 | -141.1 | -2 to 0 | absent (0.040 % of the power within 5 Hz) | absent (0.043 % of the power within 5 Hz) | `9d408d76279056d9...` |
| (a) the peer's link tap, the peer's talker | 1,149,834 | 2 | -141.48 | -1 to 0 | absent (0.038 % of the power within 5 Hz) | absent (0.038 % of the power within 5 Hz) | `9d408d76279056d9...` |
| (a) the peer's link tap, the peer's talker | 1,149,834 | 3 | -141.48 | -1 to 0 | absent (0.041 % of the power within 5 Hz) | absent (0.044 % of the power within 5 Hz) | `9d408d76279056d9...` |
| (b) the DUT's link tap, the peer's talker | 1,149,822 | 0 | -141.09 | -2 to 1 | absent (0.041 % of the power within 5 Hz) | absent (0.041 % of the power within 5 Hz) | `88c41bc5c8d78151...` |
| (b) the DUT's link tap, the peer's talker | 1,149,822 | 1 | -141.1 | -2 to 0 | absent (0.041 % of the power within 5 Hz) | absent (0.043 % of the power within 5 Hz) | `88c41bc5c8d78151...` |
| (b) the DUT's link tap, the peer's talker | 1,149,822 | 2 | -141.48 | -1 to 0 | absent (0.038 % of the power within 5 Hz) | absent (0.038 % of the power within 5 Hz) | `88c41bc5c8d78151...` |
| (b) the DUT's link tap, the peer's talker | 1,149,822 | 3 | -141.48 | -1 to 0 | absent (0.042 % of the power within 5 Hz) | absent (0.045 % of the power within 5 Hz) | `88c41bc5c8d78151...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 0 | -141.09 | -2 to 0 | absent (0.040 % of the power within 5 Hz) | absent (0.038 % of the power within 5 Hz) | `1a331755a46b8786...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 1 | -141.1 | -2 to 0 | absent (0.038 % of the power within 5 Hz) | absent (0.050 % of the power within 5 Hz) | `1a331755a46b8786...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 2 | -141.48 | -1 to 0 | absent (0.034 % of the power within 5 Hz) | absent (0.036 % of the power within 5 Hz) | `1a331755a46b8786...` |
| (c) the DUT's TDM output, McASP0 | 480,000 | 3 | -141.48 | -1 to 0 | absent (0.039 % of the power within 5 Hz) | absent (0.052 % of the power within 5 Hz) | `1a331755a46b8786...` |
| control: the peer's link tap, the DUT's talker | 1,149,834 | 0 | -5.76 | -7476354 to 7476354 | present: -1.00 dBFS, 997.0000 Hz (-0.000 ppm), SNR 146.07 dB, THD+N -146.06 dB | absent (0.000 % of the power within 5 Hz) | `9d408d76279056d9...` |
| control: the peer's link tap, the DUT's talker | 1,149,834 | 1 | -5.76 | -7476354 to 7476354 | absent (0.000 % of the power within 5 Hz) | present: -1.00 dBFS, 9973.0000 Hz (-0.000 ppm), SNR 145.99 dB, THD+N -145.99 dB | `9d408d76279056d9...` |
| control: the DUT's link tap, the DUT's talker | 1,149,822 | 0 | -5.76 | -7476354 to 7476354 | present: -1.00 dBFS, 997.0000 Hz (+0.000 ppm), SNR 146.07 dB, THD+N -146.06 dB | absent (0.000 % of the power within 5 Hz) | `88c41bc5c8d78151...` |
| control: the DUT's link tap, the DUT's talker | 1,149,822 | 1 | -5.76 | -7476354 to 7476354 | absent (0.000 % of the power within 5 Hz) | present: -1.00 dBFS, 9973.0000 Hz (-0.000 ppm), SNR 145.99 dB, THD+N -145.99 dB | `88c41bc5c8d78151...` |
| (d) the external capture, the peer's digital output | 768,000 | 0 | -4.63 | -7476354 to 7476354 | present: -1.00 dBFS, 997.0000 Hz (+0.000 ppm), SNR 146.07 dB, THD+N -146.06 dB | absent (0.000 % of the power within 5 Hz) | `fa771dccc383b4b4...` |
| (d) the external capture, the peer's digital output | 768,000 | 1 | -4.63 | -7476354 to 7476354 | absent (0.000 % of the power within 5 Hz) | present: -1.00 dBFS, 9973.0000 Hz (+0.000 ppm), SNR 145.99 dB, THD+N -145.99 dB | `fa771dccc383b4b4...` |

align (b) vs (c): SAMPLE-EXACT, 480,000 of 480,000 frames equal, first window matched 1 offset(s), slips [], differing 0

counters before dut STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 22694, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 17584
counters before peer STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 1590660, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 1590660
counters after dut STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 218933, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 217582
counters after peer STREAM_INPUT 0: MEDIA_LOCKED 1, MEDIA_UNLOCKED 0, STREAM_INTERRUPTED 0, SEQ_NUM_MISMATCH 0, MEDIA_RESET 0, TIMESTAMP_UNCERTAIN 0, TIMESTAMP_VALID 1786899, TIMESTAMP_NOT_VALID 0, UNSUPPORTED_FORMAT 0, LATE_TIMESTAMP 0, EARLY_TIMESTAMP 0, FRAMES_RX 1786899

- format-check: {"ok": true, "talker": "peer-out-0", "listener": "dut-in-0", "talker_fmt": "0205022001006000", "listener_fmt": "0205022001006000", "set": null, "listener_after": "0205022001006000"}
- bind: {"talker": "peer-out-0", "listener": "dut-in-0", "status": 0, "conn_count": 1, "stream_id": "0000000000000000"}
- unbind: {"tag": "teardown", "talker": "<peer-eid>", "tu": 0, "listener": "dut-in-0", "status": 0, "conn_count": 0}
- final: equal_to_found=True differ=[]

