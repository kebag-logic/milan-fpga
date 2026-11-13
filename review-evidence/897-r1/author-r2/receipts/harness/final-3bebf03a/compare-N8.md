## N8 at 3bebf03a against cec88385: head build e8660c8f6272, base build cbede60641b8, point 8x8
counts head {'paths': 6, 'path_misses': 0, 'instances': 45, 'instance_misses': 0} base {'paths': 6, 'path_misses': 0, 'instances': 45, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| held.acmp | 0 | 1309478 | 1309825 | -347 | 13.09478 (None) | None |
| held.adp | 1 | 1154618 | 1115858 | 38760 | 11.54618 (None) | None |
| held.aecp | 1 | 1289274 | 1356622 | -67348 | 12.89274 (None) | None |
| held.maap | 0 | 923334 | 1056115 | -132781 | 9.23334 (None) | None |
| held.srp | 1 | 738553 | 872976 | -134423 | 7.38553 (None) | None |
| notice.queued | 0 | 3273373 | 3328774 | -55401 | 32.73373 (33.23976) | True |
group notice-burst-0: worst work pass head 171541 base 174776 cycles; work passes head 780 base 779
largest path delta: -134423 cycles at ('held.srp', 1)
