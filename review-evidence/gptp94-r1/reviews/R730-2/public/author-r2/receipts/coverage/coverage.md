# #94 checks and the planted controls that fail them

| Check | Controls whose run prints it as FAIL |
|---|---|
| #94 toggle: three multi-answered requests cease | the cease entry keeps asCapable |
| #94 toggle: the cease sends no request | the cease entry ends the cease at once; the cease entry keeps asCapable |
| #94 toggle: the first request comes within one interval of the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg |
| #94 toggle: the first request goes out at once after the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a rise sends no request at once; a disabled port keeps its credit and starts its frames |
| #94 toggle: nothing is transmitted while the port is disabled | a disabled port keeps its credit and starts its frames |
| #94 toggle: then one request every interval | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and starts its frames |
| #94 toggle: lostResponses starts at zero: four losses commit nothing | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge leaves the interval unanswered; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and starts its frames |
| #94 toggle: the fifth loss after the rise commits asCapable FALSE | lost responses clear asCapable at the sixth; a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and starts its frames |
| #94 toggle: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; the ladder raises asCapable at the first exchange |
| #94 toggle: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease |
| #94 link loss: a capable master before the loss | a portEnabled edge keeps the cease |
| #94 link loss: asCapable falls at the falling edge | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event |
| #94 link loss: the publication holds while the port is disabled | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; a disabled port keeps its transmit credit; a disabled port keeps its credit and starts its frames |
| #94 link loss: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; a disabled port keeps its credit and starts its frames |
| #94 link loss: nothing is transmitted while the port is disabled | a disabled port starts an unstarted frame; a disabled port keeps its credit and starts its frames; the withdrawn frame stays offered for a cycle; a stalled frame holds NOT_ENABLED back |
| #94 link loss: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange |
| #94 link loss: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease |
| #94 built across the fall: a capable master first | a portEnabled edge keeps the cease |
| #94 built across the fall: the request before it is answered | egress claims survive the fall |
| #94 built across the fall: the response is not sent | a disabled port starts an unstarted frame; a disabled port keeps its credit and starts its frames; egress claims survive the fall; a stalled frame holds NOT_ENABLED back |
| #94 built across the fall: a request after the rise is answered at once | egress claims survive the fall |
| #94 countdown: capable before the storm | a portEnabled edge keeps the cease; egress claims survive the fall |
| #94 countdown: three multi-answered requests cease | the cease entry keeps asCapable |
| #94 countdown: the first request after the cease follows the last by the countdown and two beats | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the countdown loads one beat less; the cease entry ends the cease at once; the cease entry keeps asCapable; egress claims survive the fall |
| #94 countdown: the ladder re-earns after the cease | a portEnabled edge keeps the cease; egress claims survive the fall |
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

| Control | Arm verdict on its named checks |
|---|---|
| lost responses clear asCapable at the sixth | caught |
| a portEnabled edge keeps the cease | caught |
| slot 6 runs no NOT_ENABLED leg | caught |
| a portEnabled edge keeps the ladder | caught |
| a portEnabled edge leaves the interval unanswered | caught |
| the countdown loads one beat less | caught |
| the cease entry ends the cease at once | caught |
| the cease entry keeps asCapable | caught |
| the ladder raises asCapable at the first exchange | caught |
| the falling edge raises no event | caught |
| a rise sends no request at once | caught |
| a disabled port keeps its transmit credit | caught |
| a disabled port starts an unstarted frame | caught |
| a disabled port keeps its credit and starts its frames | caught |
| egress claims survive the fall | caught |
| the request claim survives the fall | caught |
| the first enable since reset raises events | caught |
| the withdrawn frame stays offered for a cycle | caught |
| a disabled port tears a started frame | caught |
| NOT_ENABLED waits for the serializer | caught |
| a stalled frame holds NOT_ENABLED back | caught |
| NOT_ENABLED keeps the armed response | caught |
| NOT_ENABLED queues behind earlier events | caught |
| the first rise after a disabled release raises nothing | caught |
| dispatch ignores a busy serializer | caught |
