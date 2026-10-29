| New check | Controls that fail it |
|---|---|
| #94 Follow_Up after the fall: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 Follow_Up after the fall: nothing commits after NOT_ENABLED | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED keeps the armed response |
| #94 Follow_Up after the fall: the delay holds | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED keeps the armed response |
| #94 Follow_Up after the fall: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange; egress claims survive the fall |
| #94 Follow_Up after the fall: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 t1 after the fall: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 t1 after the fall: nothing commits after NOT_ENABLED | the request claim survives the fall |
| #94 t1 after the fall: the delay holds | the request claim survives the fall |
| #94 t1 after the fall: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange; egress claims survive the fall |
| #94 t1 after the fall: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 Follow_Up queued before the fall: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 Follow_Up queued before the fall: nothing commits after NOT_ENABLED | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED waits for the serializer; a stalled frame holds NOT_ENABLED back; NOT_ENABLED keeps the armed response; NOT_ENABLED queues behind earlier events |
| #94 Follow_Up queued before the fall: the delay holds | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED keeps the armed response; NOT_ENABLED queues behind earlier events |
| #94 Follow_Up queued before the fall: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange; egress claims survive the fall |
| #94 Follow_Up queued before the fall: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 stalled first byte: a capable master first | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 stalled first byte: a frame waits at its first byte | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 stalled first byte: asCapable falls within 2 ms of the fall | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; a stalled frame holds NOT_ENABLED back |
| #94 stalled first byte: the frame is withdrawn | a disabled port starts an unstarted frame; a disabled port keeps its credit and starts its frames; a stalled frame holds NOT_ENABLED back |
| #94 stalled first byte: no frame starts while the port is disabled | a disabled port starts an unstarted frame; a disabled port keeps its credit and starts its frames; a stalled frame holds NOT_ENABLED back |
| #94 stalled first byte: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; egress claims survive the fall; the request claim survives the fall |
| #94 stalled first byte: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange; egress claims survive the fall; the request claim survives the fall |
| #94 stalled first byte: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 1: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 1: asCapable falls within 2 ms of the fall | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED waits for the serializer; a stalled frame holds NOT_ENABLED back |
| #94 stalled at byte 1: the started frame keeps its place | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 1: the started frame completes whole | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 1: nothing else starts while the port is disabled | a disabled port keeps its credit and starts its frames |
| #94 stalled at byte 1: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 34: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 34: asCapable falls within 2 ms of the fall | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED waits for the serializer; a stalled frame holds NOT_ENABLED back |
| #94 stalled at byte 34: the started frame keeps its place | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 34: the started frame completes whole | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 34: nothing else starts while the port is disabled | a disabled port keeps its credit and starts its frames |
| #94 stalled at byte 34: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 67: a capable port first | a portEnabled edge keeps the cease; egress claims survive the fall; the request claim survives the fall |
| #94 stalled at byte 67: asCapable falls within 2 ms of the fall | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; NOT_ENABLED waits for the serializer; a stalled frame holds NOT_ENABLED back |
| #94 stalled at byte 67: the started frame keeps its place | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 67: the started frame completes whole | egress claims survive the fall; a disabled port tears a started frame |
| #94 stalled at byte 67: nothing else starts while the port is disabled | a disabled port keeps its credit and starts its frames |
| #94 stalled at byte 67: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; egress claims survive the fall; the request claim survives the fall |
| #94 disabled warm reset: three multi-answered requests cease | a portEnabled edge keeps the cease; the cease entry keeps asCapable; egress claims survive the fall; the request claim survives the fall |
| #94 disabled warm reset: the first request comes within one interval of the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the first rise after a disabled release raises nothing |
| #94 disabled warm reset: the first request goes out at once after the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a rise sends no request at once; the first rise after a disabled release raises nothing |
| #94 disabled warm reset: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange |
| #94 disabled warm reset: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease |
