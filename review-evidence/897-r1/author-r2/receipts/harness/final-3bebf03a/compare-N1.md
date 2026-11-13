## N1 at 3bebf03a against cec88385: head build a1fb80a1d31e, base build ece9b0a576e8, point 1x1
counts head {'paths': 6, 'path_misses': 0, 'instances': 17, 'instance_misses': 0} base {'paths': 6, 'path_misses': 0, 'instances': 17, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| held.acmp | 0 | 1093837 | 1096523 | -2686 | 10.93837 (None) | None |
| held.adp | 0 | 1114105 | 964508 | 149597 | 11.14105 (None) | None |
| held.aecp | 0 | 1107353 | 1109263 | -1910 | 11.07353 (None) | None |
| held.maap | 0 | 896207 | 904765 | -8558 | 8.96207 (None) | None |
| held.srp | 0 | 722819 | 687754 | 35065 | 7.22819 (None) | None |
| notice.queued | 0 | 1136004 | 1206389 | -70385 | 11.36004 (11.56161) | True |
group notice-burst-0: worst work pass head 158769 base 153657 cycles; work passes head 835 base 835
largest path delta: 149597 cycles at ('held.adp', 0)
