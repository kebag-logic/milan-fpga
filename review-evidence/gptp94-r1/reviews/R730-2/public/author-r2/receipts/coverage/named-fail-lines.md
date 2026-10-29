### a disabled port starts an unstarted frame (`top/KL_gptp_engine.sv`)
- `FAIL #94 built across the fall: the response is not sent got 0000000000000000 exp 0000000000000001`
- `FAIL #94 link loss: nothing is transmitted while the port is disabled got 0000000000000001 exp 0000000000000000`
- `FAIL #94 stalled first byte: the frame is withdrawn got 0000000000000001 exp 0000000000000000`
- `FAIL #94 stalled first byte: no frame starts while the port is disabled got 0000000000000001 exp 0000000000000000`

### a disabled port keeps its credit and starts its frames (`top/KL_gptp_engine.sv`)
- `FAIL #94 toggle: nothing is transmitted while the port is disabled got 0000000000000001 exp 0000000000000000`
- `FAIL #94 link loss: nothing is transmitted while the port is disabled got 0000000000000007 exp 0000000000000000`

### egress claims survive the fall (`top/KL_gptp_engine.sv`)
- `FAIL #94 built across the fall: a request after the rise is answered at once got 0000000000000000 exp 0000000000000001`

### the request claim survives the fall (`top/KL_gptp_engine.sv`)
- `FAIL #94 t1 after the fall: nothing commits after NOT_ENABLED got 0000000000000001 exp 0000000000000000`
- `FAIL #94 t1 after the fall: the delay holds got 00000000000002bd exp 0000000000000259`

### the withdrawn frame stays offered for a cycle (`wire/KL_gptp_tx_slot.sv`)
- `FAIL #94 link loss: nothing is transmitted while the port is disabled got 0000000000000001 exp 0000000000000000`

### a disabled port tears a started frame (`wire/KL_gptp_tx_slot.sv`)
- `FAIL #94 stalled at byte 1: the started frame keeps its place got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 34: the started frame keeps its place got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 67: the started frame keeps its place got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 1: the started frame completes whole got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 34: the started frame completes whole got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 67: the started frame completes whole got 0000000000000000 exp 0000000000000001`

### NOT_ENABLED waits for the serializer (`top/KL_gptp_engine.sv`)
- `FAIL #94 stalled at byte 1: asCapable falls within 2 ms of the fall got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 34: asCapable falls within 2 ms of the fall got 0000000000000000 exp 0000000000000001`
- `FAIL #94 stalled at byte 67: asCapable falls within 2 ms of the fall got 0000000000000000 exp 0000000000000001`

### a stalled frame holds NOT_ENABLED back (`top/KL_gptp_engine.sv`)
- `FAIL #94 stalled first byte: asCapable falls within 2 ms of the fall got 0000000000000000 exp 0000000000000001`

### NOT_ENABLED keeps the armed response (`ucode/gen_gptp_ucode.py`)
- `FAIL #94 Follow_Up after the fall: nothing commits after NOT_ENABLED got 0000000000000001 exp 0000000000000000`
- `FAIL #94 Follow_Up after the fall: the delay holds got 00000000000002bd exp 0000000000000259`
- `FAIL #94 Follow_Up queued before the fall: nothing commits after NOT_ENABLED got 0000000000000001 exp 0000000000000000`
- `FAIL #94 Follow_Up queued before the fall: the delay holds got 00000000000002bd exp 0000000000000259`

### NOT_ENABLED queues behind earlier events (`top/KL_gptp_engine.sv`)
- `FAIL #94 Follow_Up queued before the fall: the delay holds got 00000000000002bd exp 0000000000000259`

### the first rise after a disabled release raises nothing (`top/KL_gptp_engine.sv`)
- `FAIL #94 disabled warm reset: the first request comes within one interval of the rise got 0000000000000000 exp 0000000000000001`
- `FAIL #94 disabled warm reset: the first request goes out at once after the rise got 0000000000000000 exp 0000000000000001`

