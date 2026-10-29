# New #94 checks and the planted controls that fail them

| New check | Controls whose run prints it as FAIL |
|---|---|
| #94 toggle: three multi-answered requests cease | the cease entry keeps asCapable |
| #94 toggle: the cease sends no request | the cease entry ends the cease at once; the cease entry keeps asCapable |
| #94 toggle: the first request comes within one interval of the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg |
| #94 toggle: the first request goes out at once after the rise | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a rise sends no request at once; a disabled port keeps its credit and its SEND |
| #94 toggle: nothing is transmitted while the port is disabled | a disabled port keeps its credit and its SEND |
| #94 toggle: then one request every interval | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and its SEND |
| #94 toggle: lostResponses starts at zero: four losses commit nothing | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge leaves the interval unanswered; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and its SEND |
| #94 toggle: the fifth loss after the rise commits asCapable FALSE | lost responses clear asCapable at the sixth; a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the cease entry ends the cease at once; the cease entry keeps asCapable; a disabled port keeps its credit and its SEND |
| #94 link loss: a capable master before the loss | a portEnabled edge keeps the cease |
| #94 link loss: asCapable falls at the falling edge | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event |
| #94 link loss: the publication holds while the port is disabled | slot 6 runs no NOT_ENABLED leg; the falling edge raises no event; a disabled port keeps its transmit credit; a disabled port keeps its credit and its SEND |
| #94 link loss: the first request goes out at once after the rise | a portEnabled edge keeps the cease; a rise sends no request at once; a disabled port keeps its credit and its SEND |
| #94 link loss: nothing is transmitted while the port is disabled | a frame built across the fall is sent; a disabled port keeps its credit and its SEND |
| #94 built across the fall: a capable master first | a portEnabled edge keeps the cease |
| #94 built across the fall: the request before it is answered | egress claims survive the fall |
| #94 built across the fall: the response is not sent | a frame built across the fall is sent; a disabled port keeps its credit and its SEND; egress claims survive the fall |
| #94 built across the fall: a request after the rise is answered at once | egress claims survive the fall |
| #94 countdown: capable before the storm | a portEnabled edge keeps the cease |
| #94 countdown: three multi-answered requests cease | the cease entry keeps asCapable; egress claims survive the fall |
| #94 countdown: the first request after the cease follows the last by the countdown and two beats | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; the countdown loads one beat less; the cease entry ends the cease at once; the cease entry keeps asCapable; egress claims survive the fall |
| #94 countdown: the ladder re-earns after the cease | a portEnabled edge keeps the cease |
| #94 toggle: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; the ladder raises asCapable at the first exchange |
| #94 toggle: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease |
| #94 link loss: one exchange after the rise leaves asCapable clear | a portEnabled edge keeps the cease; slot 6 runs no NOT_ENABLED leg; a portEnabled edge keeps the ladder; the ladder raises asCapable at the first exchange |
| #94 link loss: the second exchange after the rise raises asCapable | a portEnabled edge keeps the cease |
