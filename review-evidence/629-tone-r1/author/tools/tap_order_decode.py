import struct, sys
d = open(sys.argv[1], 'rb').read(); off = 24; t0 = None
ACMP = {6:'BIND_RX_CMD',7:'BIND_RX_RESP',8:'UNBIND_RX_CMD',9:'UNBIND_RX_RESP',10:'GET_RX_STATE_CMD',11:'GET_RX_STATE_RESP',0:'CONNECT_TX_CMD',1:'CONNECT_TX_RESP',2:'DISCONNECT_TX_CMD',3:'DISCONNECT_TX_RESP',4:'GET_TX_STATE_CMD',5:'GET_TX_STATE_RESP',12:'GET_TX_CONN_CMD',13:'GET_TX_CONN_RESP'}
CMD = {0x29:'GET_COUNTERS',0x0F:'GET_STREAM_INFO',0x24:'REGISTER_UNSOL',0x25:'DEREGISTER_UNSOL',0x2B:'GET_AUDIO_MAP',0x09:'GET_STREAM_FORMAT',0x08:'SET_STREAM_FORMAT',0x0E:'SET_STREAM_INFO',0x16:'SET_CLOCK_SOURCE',0x17:'GET_CLOCK_SOURCE',0x27:'GET_AVB_INFO',0x2C:'ADD_AUDIO_MAPPINGS',0x2D:'REMOVE_AUDIO_MAPPINGS',0x04:'READ_DESCRIPTOR',0x28:'GET_AS_PATH',0x4B:'GET_MAX_TRANSIT_TIME',0x00:'ACQUIRE',0x01:'LOCK',0x02:'ENTITY_AVAILABLE'}
W=['MLOCK','MUNLOCK','INTR','SEQ','MRST','TU','TSV','TSNV','UF','LATE','EARLY','FRX']
DUT = '020000fffe000001'
while off + 16 <= len(d):
    ts, tu, incl, orig = struct.unpack('<IIII', d[off:off+16]); p = d[off+16:off+16+incl]; off += 16 + incl
    hdr, f = p[:28], p[28:]
    port = struct.unpack('<I', hdr[8:12])[0] if len(hdr) >= 12 else 0
    tns = struct.unpack('<Q', hdr[12:20])[0] if len(hdr) >= 20 else 0
    if len(f) < 18: continue
    et = f[12:14]; b = 14
    if et == b'\x81\x00': et = f[16:18]; b = 18
    if et != b'\x22\xf0': continue
    a = f[b:]; sub = a[0]; mt = a[1] & 0x0f; st = a[2] >> 3
    if t0 is None: t0 = tns
    t = (tns - t0) / 1e6
    d_ = 'DUT->sw' if port == 3 else 'sw->DUT' if port == 2 else f'p{port}'
    if sub == 0xFC:
        tid = a[12:20].hex(); lid = a[20:28].hex(); luid = struct.unpack('>H', a[30:32])[0] if len(a) >= 32 else -1
        cc = struct.unpack('>H', a[44:46])[0] if len(a) >= 46 else -1
        print(f'{t:12.3f} ms {d_:8} ACMP {ACMP.get(mt, mt)} status={st} listener={lid[-4:]} luid={luid} cc={cc}')
    elif sub == 0xFB:
        tgt = a[4:12].hex(); ctl = a[12:20].hex(); seq = struct.unpack('>H', a[20:22])[0]; ct = struct.unpack('>H', a[22:24])[0]; u = ct >> 15; ct &= 0x7fff
        extra = ''
        if ct == 0x29 and mt == 1 and len(a) >= 32 + 48:
            dt, di = struct.unpack('>HH', a[24:28]); v = struct.unpack('>12I', a[32:80])
            extra = f' desc={dt:#x}/{di} ' + ' '.join(f'{W[i]}={v[i]}' for i in range(12) if v[i] and i < 6)
        if ct == 0x0F and mt == 1 and len(a) >= 32:
            dt, di, fl = struct.unpack('>HHI', a[24:32]); extra = f' desc={dt:#x}/{di} flags={fl:#010x}'
        who = 'DUT' if tgt == DUT else tgt[-4:]
        print(f'{t:12.3f} ms {d_:8} AECP {"RSP" if mt == 1 else "CMD"} {"UNSOL " if u else ""}{CMD.get(ct, hex(ct))} tgt={who} ctl={ctl[-4:]} seq={seq} st={st}{extra}')
