## N8: head build bad277745e09, base build 7b1407b3e807, point 8x8
counts head {'paths': 8, 'path_misses': 0, 'instances': 92, 'instance_misses': 0} base {'paths': 8, 'path_misses': 0, 'instances': 92, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| held.acmp | 0 | 684084 | 654017 | 30067 | 6.84084 (None) | None |
| held.adp | 1 | 704352 | 672847 | 31505 | 7.04352 (None) | None |
| held.aecp | 1 | 508549 | 476251 | 32298 | 5.08549 (None) | None |
| held.maap | 0 | 637566 | 614542 | 23024 | 6.37566 (None) | None |
| held.srp | 1 | 1240809 | 1222688 | 18121 | 12.40809 (None) | None |
| mrpdu | 0 | 236598 | 194492 | 42106 | 2.36598 (None) | None |
| mrpdu | 1 | 382284 | 338083 | 44201 | 3.82284 (None) | None |
| notice.queued | 0 | 5217520 | 5071820 | 145700 | 52.1752 (52.54297) | True |
group notice-every-0: worst work pass head 170746 base 169441 cycles; work passes head 1099 base 1092
group notice-burst-0: worst work pass head 169371 base 164291 cycles; work passes head 948 base 955
largest path delta: 145700 cycles at ('notice.queued', 0)
