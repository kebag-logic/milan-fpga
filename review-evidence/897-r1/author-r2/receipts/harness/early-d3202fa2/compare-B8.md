## B8 at d3202fa2 against cec88385: head build 4f7933da95af, base build fe483ca5322e, point 8x8
counts head {'paths': 39, 'path_misses': 0, 'instances': 39, 'instance_misses': 0} base {'paths': 39, 'path_misses': 0, 'instances': 39, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| aecp.entity_available | 0 | 14017 | 29089 | -15072 | 0.14017 (0.59689) | True |
| aecp.entity_available | 1 | 23431 | 14220 | 9211 | 0.23431 (0.69706) | True |
| aecp.get_avb_info | 0 | 28636 | 19098 | 9538 | 0.28636 (0.74279) | True |
| aecp.get_avb_info | 1 | 25672 | 16124 | 9548 | 0.25672 (0.72494) | True |
| aecp.get_configuration | 0 | 20031 | 12493 | 7538 | 0.20031 (0.66027) | True |
| aecp.get_configuration | 1 | 14351 | 29428 | -15077 | 0.14351 (0.59721) | True |
| aecp.get_counters | 0 | 18704 | 33712 | -15008 | 0.18704 (0.65032) | True |
| aecp.get_counters | 1 | 20585 | 35626 | -15041 | 0.20585 (0.67048) | True |
| aecp.get_name | 0 | 22410 | 14562 | 7848 | 0.2241 (0.68882) | True |
| aecp.get_name | 1 | 24228 | 16239 | 7989 | 0.24228 (0.70727) | True |
| aecp.lock_entity | 0 | 36716 | 29726 | 6990 | 0.36716 (0.76314) | True |
| aecp.lock_entity | 1 | 30619 | 23462 | 7157 | 0.30619 (0.73153) | True |
| aecp.mvu_get_milan_info | 0 | 12095 | 28240 | -16145 | 0.12095 (0.56798) | True |
| aecp.mvu_get_milan_info | 1 | 14379 | 30342 | -15963 | 0.14379 (0.59888) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 27586 | 19121 | 8465 | 0.27586 (0.73825) | True |
| aecp.read_descriptor.t0.i0.c0 | 1 | 20340 | 34805 | -14465 | 0.2034 (0.65988) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 22113 | 13039 | 9074 | 0.22113 (0.64411) | True |
| aecp.read_descriptor.t1.i0.c0 | 1 | 17667 | 32622 | -14955 | 0.17667 (0.64435) | True |
| aecp.read_descriptor.t10.i9.c0 | 0 | 22492 | 13400 | 9092 | 0.22492 (0.68243) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 15063 | 29870 | -14807 | 0.15063 (0.60405) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 27102 | 18996 | 8106 | 0.27102 (0.73294) | True |
| aecp.read_descriptor.t14.i7.c0 | 0 | 14984 | 29175 | -14191 | 0.14984 (0.60479) | True |
| aecp.read_descriptor.t15.i7.c0 | 0 | 14411 | 28678 | -14267 | 0.14411 (0.61014) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 15797 | 29887 | -14090 | 0.15797 (0.62342) | True |
| aecp.read_descriptor.t2.i0.c0 | 1 | 24601 | 17031 | 7570 | 0.24601 (0.71205) | True |
| aecp.read_descriptor.t20.i71.c0 | 0 | 22134 | 13545 | 8589 | 0.22134 (0.68539) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 15491 | 30665 | -15174 | 0.15491 (0.61487) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 22917 | 15180 | 7737 | 0.22917 (0.69593) | True |
| aecp.read_descriptor.t5.i8.c0 | 0 | 22945 | 14188 | 8757 | 0.22945 (0.68961) | True |
| aecp.read_descriptor.t6.i8.c0 | 0 | 16253 | 30057 | -13804 | 0.16253 (0.61595) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 22466 | 13359 | 9107 | 0.22466 (0.68245) | True |
| aecp.register_unsolicited | 0 | 27137 | 18959 | 8178 | 0.27137 (0.72207) | True |
| aecp.register_unsolicited | 1 | 21927 | 15790 | 6137 | 0.21927 (0.68163) | True |
| aecp.set_name | 0 | 45350 | 38130 | 7220 | 0.4535 (0.91887) | True |
| aecp.set_name | 1 | 43689 | 36215 | 7474 | 0.43689 (0.86921) | True |
| aecp.unknown_command | 0 | 23017 | 12383 | 10634 | 0.23017 (0.6868) | True |
| aecp.unknown_command | 1 | 15829 | 29051 | -13222 | 0.15829 (0.61341) | True |
| aecp.unlock_entity | 0 | 28978 | 45603 | -16625 | 0.28978 (0.6865) | True |
| aecp.unlock_entity | 1 | 39198 | 32762 | 6436 | 0.39198 (0.79626) | True |
group aecp: worst work pass head 112674 base 112351 cycles; work passes head 137 base 137
largest path delta: -16625 cycles at ('aecp.unlock_entity', 0)
