"""Independent GET_COUNTERS payload decoder (descriptor_type, index, counters_valid, 32 x u32)."""
import struct
NAMES = {
    0x0005: ['MEDIA_LOCKED', 'MEDIA_UNLOCKED', 'STREAM_INTERRUPTED', 'SEQ_NUM_MISMATCH', 'MEDIA_RESET',
             'TIMESTAMP_UNCERTAIN', 'TIMESTAMP_VALID', 'TIMESTAMP_NOT_VALID', 'UNSUPPORTED_FORMAT',
             'LATE_TIMESTAMP', 'EARLY_TIMESTAMP', 'FRAMES_RX'],
    0x0006: ['STREAM_START', 'STREAM_STOP', 'MEDIA_RESET', 'TIMESTAMP_UNCERTAIN', 'FRAMES_TX'],
    0x0024: ['LOCKED', 'UNLOCKED'],
    0x0009: ['LINK_UP', 'LINK_DOWN', 'C2', 'C3', 'C4', 'GPTP_GM_CHANGED'],
}
def decode(hexs):
    b = bytes.fromhex(hexs)
    dt, di, valid = struct.unpack('>HHI', b[:8])
    vals = struct.unpack('>32I', b[8:8 + 128])
    names = NAMES.get(dt, [])
    out = {}
    for i in range(32):
        if valid >> i & 1:
            out[names[i] if i < len(names) else 'C%d' % i] = vals[i]
    return dt, di, valid, out
def delta(a, b):
    return {k: b[k] - a.get(k, 0) for k in b if b[k] != a.get(k, 0)}
