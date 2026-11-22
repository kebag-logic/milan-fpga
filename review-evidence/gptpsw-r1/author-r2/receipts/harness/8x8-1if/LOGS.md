# The 8x8-1if gPTP legs' raw logs (not copied: over 200 KB each)

| Log | Bytes | sha256 |
|---|---:|---|
| backlog-adp.log | 14353193 | b0510725cfd715b328d81004ee7db0baddea78d9d79532f8ad0a8e193ef8836c |
| backlog-adp-refill.log | 14501782 | 410f7860918ab111acb1af3e2732a7b1ce73268cdab3b710aee931fd63d35070 |
| backlog.log | 14043465 | c1be7eb0a365c3adba39ccda017c2997617df66a96d3e9988a1fa43d93b3f4b5 |
| backlog-owed.log | 14624183 | 9c9354f10217e26c298a0f322587802ea4287a2cd01436e5b9816c3f982df768 |
| fixture.log | 2777591 | f2dbf15238dc31ac3bf2462bf83750106785a9470d6cc4288c657c9afda6d4db |
| gptp-master.log | 8658234 | 40852b3dfbb74122e6a8394743dbb28383947e5e25398f21e67ffda15e414349 |
| gptp-slave.log | 8654172 | 696d4d01001156ccaeaadf3986bfd1822938a06e07cdfd8f9699fdacf49a06f3 |

Built and run at `0e476c94` from a clean clone: `leg.sh <clone> <build> 8x8-1if <groups> --with-gptp` (bin/leg.sh), MAKEFLAGS -j8 on 8 booked CPUs.
