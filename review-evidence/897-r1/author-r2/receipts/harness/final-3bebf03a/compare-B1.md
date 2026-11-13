## B1 at 3bebf03a against cec88385: head build 5b41e5e03137, base build 1d8230d5681d, point 1x1
counts head {'paths': 25, 'path_misses': 0, 'instances': 25, 'instance_misses': 0} base {'paths': 25, 'path_misses': 0, 'instances': 25, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| aecp.entity_available | 0 | 10121 | 17125 | -7004 | 0.10121 (0.22839) | True |
| aecp.get_avb_info | 0 | 13466 | 20032 | -6566 | 0.13466 (0.26086) | True |
| aecp.get_configuration | 0 | 16721 | 11020 | 5701 | 0.16721 (0.4303) | True |
| aecp.get_counters | 0 | 14196 | 21031 | -6835 | 0.14196 (0.27241) | True |
| aecp.get_name | 0 | 19179 | 12998 | 6181 | 0.19179 (0.45555) | True |
| aecp.lock_entity | 0 | 18840 | 19782 | -942 | 0.1884 (0.30105) | True |
| aecp.mvu_get_milan_info | 0 | 9148 | 16625 | -7477 | 0.09148 (0.2273) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 22712 | 23936 | -1224 | 0.22712 (0.50394) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 12926 | 13275 | -349 | 0.12926 (0.25878) | True |
| aecp.read_descriptor.t10.i2.c0 | 0 | 12381 | 19308 | -6927 | 0.12381 (0.25608) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 18718 | 12998 | 5720 | 0.18718 (0.44937) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 14829 | 20939 | -6110 | 0.14829 (0.27705) | True |
| aecp.read_descriptor.t14.i0.c0 | 0 | 17329 | 12197 | 5132 | 0.17329 (0.44573) | True |
| aecp.read_descriptor.t15.i0.c0 | 0 | 11565 | 18140 | -6575 | 0.11565 (0.24336) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 18422 | 10916 | 7506 | 0.18422 (0.45441) | True |
| aecp.read_descriptor.t20.i24.c0 | 0 | 12858 | 19303 | -6445 | 0.12858 (0.25312) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 19113 | 12326 | 6787 | 0.19113 (0.45835) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 11724 | 18577 | -6853 | 0.11724 (0.25458) | True |
| aecp.read_descriptor.t5.i1.c0 | 0 | 13288 | 13069 | 219 | 0.13288 (0.25874) | True |
| aecp.read_descriptor.t6.i1.c0 | 0 | 12836 | 20663 | -7827 | 0.12836 (0.26596) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 19098 | 12970 | 6128 | 0.19098 (0.45713) | True |
| aecp.register_unsolicited | 0 | 16000 | 21505 | -5505 | 0.16 (0.42784) | True |
| aecp.set_name | 0 | 26398 | 34012 | -7614 | 0.26398 (0.42126) | True |
| aecp.unknown_command | 0 | 17234 | 19447 | -2213 | 0.17234 (0.43654) | True |
| aecp.unlock_entity | 0 | 26615 | 20518 | 6097 | 0.26615 (0.51557) | True |
group aecp: worst work pass head 67077 base 65963 cycles; work passes head 109 base 109
largest path delta: -7827 cycles at ('aecp.read_descriptor.t6.i1.c0', 0)
