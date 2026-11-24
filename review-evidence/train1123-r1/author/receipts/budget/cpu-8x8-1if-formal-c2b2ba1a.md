# The formal CPU budget measurement at 8x8-1if on the composed head c2b2ba1a (clean clone): every arm and every group.

## Legs: arm, part, groups, rc, image (ctrl_app.elf sha256, 16 hex), head
- answering-every-port part0: 16 groups; rc 0; image a531bed5eee3db34; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- answering-later part0: 8 groups; rc 0; image 2c61cd273cb7b752; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- answering-ports part0: 50 groups; rc 1; image 6fc878502d988b52; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- answering-ports part1: 52 groups; rc 1; image 6fc878502d988b52; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- declaring-outputs part0: 5 groups; rc 0; image 2b93f111b0a6d311; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- none part0: 33 groups; rc 0; image 0e263f659cc9a42e; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- none part1: 34 groups; rc 1; image 0e263f659cc9a42e; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- none part2: 34 groups; rc 0; image 0e263f659cc9a42e; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- shutdown-entry part0: 2 groups; rc 0; image 553fa36f5ec2db74; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- talker-notices part0: 8 groups; rc 0; image 3cec7c1dc37b07fa; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- valid-destinations part0: 1 groups; rc 0; image 39f27ea39d7dbd20; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da
- valid-destinations part1: 2 groups; rc 0; image 39f27ea39d7dbd20; HEAD c2b2ba1a4742335e0678ec1f00f9033d1913b1da

## Each leg's run summary
- answering-every-port.part0: 16 groups graded, 0 refusals, 0 budget misses (0 of 728 probe instances, 0 of 7 paths), 0 of 19516 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- answering-later.part0: 8 groups graded, 0 refusals, 0 budget misses (0 of 56 probe instances, 0 of 7 paths), 0 of 13770 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- answering-ports.part0: 50 groups graded, 0 refusals, 7 budget misses (7 of 483 probe instances, 4 of 49 paths), 1 of 196051 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- answering-ports.part1: 52 groups graded, 0 refusals, 0 budget misses (0 of 501 probe instances, 0 of 81 paths), 0 of 105242 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- declaring-outputs.part0: 5 groups graded, 0 refusals, 0 budget misses (0 of 64 probe instances, 0 of 54 paths), 0 of 847 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- none.part0: 33 groups graded, 0 refusals, 0 budget misses (0 of 320 probe instances, 0 of 43 paths), 0 of 189005 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- none.part1: 34 groups graded, 0 refusals, 0 budget misses (0 of 323 probe instances, 0 of 55 paths), 1 of 104942 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- none.part2: 34 groups graded, 0 refusals, 7 budget misses (7 of 331 probe instances, 4 of 43 paths), 0 of 29366 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- shutdown-entry.part0: 2 groups graded, 0 refusals, 0 budget misses (0 of 2 probe instances, 0 of 1 paths), 0 of 524 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- talker-notices.part0: 8 groups graded, 0 refusals, 0 budget misses (0 of 16 probe instances, 0 of 2 paths), 0 of 12741 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- valid-destinations.part0: 1 groups graded, 0 refusals, 0 budget misses (0 of 9 probe instances, 0 of 9 paths), 0 of 33117 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)
- valid-destinations.part1: 2 groups graded, 0 refusals, 0 budget misses (0 of 36 probe instances, 0 of 25 paths), 0 of 32561 work passes over the per-pass share 2.000 ms (200,000 CPU cycles)

## Findings the legs recorded (BUDGET, STATED, REFUSED, NOTICE, SAVE, AGED, OWED, DECLARING)
NOTICE notice-every-0: committed 7.517 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 7.692 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 1.460 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 1.637 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 3.553 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 3.730 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 5.449 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 5.624 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 1.797 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 1.970 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 3.889 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 4.065 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 5.781 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 5.951 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 7.844 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 8.010 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 9.554 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 9.728 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 9.873 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 10.041 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 11.550 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 11.724 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 11.869 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 12.035 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 13.527 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 13.701 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 13.846 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 14.013 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 15.544 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 15.717 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 15.862 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 16.028 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 17.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 17.676 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 17.820 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 17.988 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 23.037 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 23.161 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 23.331 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-0: committed 23.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 7.520 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 7.694 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 1.460 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 1.638 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 5.451 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 5.627 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 3.558 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 3.737 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 1.797 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 1.971 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 3.896 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 4.071 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 5.783 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 5.953 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 7.847 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 8.013 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 9.557 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 9.731 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 9.876 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 10.044 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 11.552 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 11.727 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 11.872 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 12.038 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 13.530 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 13.704 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 13.849 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 14.016 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 15.546 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 15.719 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 15.864 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 16.030 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 17.505 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 17.679 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 17.823 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 17.990 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 23.040 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 23.165 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 23.334 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-1: committed 23.506 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 7.517 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 7.691 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 1.460 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 1.637 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 3.554 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 3.730 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 5.446 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 5.622 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 1.797 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 1.970 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 3.890 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 4.065 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 5.778 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 5.948 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 7.844 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 8.010 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 9.553 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 9.727 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 9.872 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 10.040 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 11.549 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 11.723 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 11.868 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 12.034 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 13.526 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 13.700 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 13.845 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 14.012 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 15.542 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 15.716 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 15.860 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 16.027 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 17.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 17.676 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 17.820 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 17.987 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 23.037 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 23.162 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 23.331 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-2: committed 23.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 7.518 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 7.692 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 1.460 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 1.637 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 3.554 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 3.731 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 5.447 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 5.622 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 1.797 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 1.970 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 3.890 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 4.065 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 5.779 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 5.948 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 7.844 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 8.011 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 9.553 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 9.728 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 9.873 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 10.040 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 11.549 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 11.724 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 11.868 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 12.035 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 13.527 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 13.701 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 13.846 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 14.012 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 15.543 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 15.716 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 15.861 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 16.028 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 17.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 17.676 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 17.821 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 17.988 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 23.037 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 23.162 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 23.331 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-3: committed 23.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 7.560 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 7.735 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 1.462 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 1.640 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 3.347 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 3.524 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 5.465 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 5.642 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 1.799 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 1.973 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 3.684 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 3.859 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 5.798 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 5.968 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 7.887 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 8.054 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 9.386 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 9.561 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 9.707 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 9.874 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 11.383 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 11.558 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 11.703 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 11.869 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 13.361 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 13.536 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 13.681 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 13.848 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 15.378 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 15.552 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 15.697 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 15.864 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 17.339 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 17.513 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 17.658 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 17.825 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 22.875 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 23.000 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 23.169 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-4: committed 23.341 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 7.314 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 7.490 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 1.463 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 1.640 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 3.347 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 3.524 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 5.464 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 5.642 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 1.799 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 1.973 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 3.684 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 3.859 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 5.798 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 5.967 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 7.642 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 7.809 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 9.354 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 9.529 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 9.674 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 9.841 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 11.350 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 11.525 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 11.670 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 11.836 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 13.328 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 13.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 13.648 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 13.815 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 15.346 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 15.519 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 15.664 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 15.831 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 17.306 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 17.480 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 17.625 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 17.792 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 22.841 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 22.966 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 23.135 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-5: committed 23.307 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 5.405 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 5.579 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 3.516 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 3.693 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 7.473 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 7.647 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 1.422 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 1.604 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 1.763 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 1.936 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 3.852 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 4.027 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 5.734 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 5.904 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 7.799 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 7.966 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 9.508 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 9.682 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 9.827 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 9.995 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 11.504 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 11.678 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 11.823 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 11.989 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 13.481 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 13.655 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 13.800 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 13.967 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 15.497 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 15.671 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 15.815 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 15.982 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 17.457 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 17.631 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 17.775 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 17.942 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 22.992 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 23.116 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 23.285 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-6: committed 23.457 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 5.428 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 5.604 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 7.273 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 7.448 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 1.423 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 1.602 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 3.314 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 3.493 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 1.761 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 1.935 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 3.652 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 3.827 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 5.760 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 5.929 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 7.600 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 7.767 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 9.309 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 9.484 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 9.630 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 9.797 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 11.306 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 11.482 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 11.626 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 11.793 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 13.285 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 13.459 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 13.605 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 13.771 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 15.302 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 15.476 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 15.621 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 15.787 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 17.263 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 17.437 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 17.581 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 17.749 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 22.801 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 22.925 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 23.095 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-every-7: committed 23.266 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 4.838 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 5.008 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 16.999 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 17.176 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 2.784 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 2.963 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 17.329 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 17.497 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 5.165 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 5.337 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 18.239 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 18.416 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 18.568 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 18.736 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 20.252 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 20.426 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 3.139 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 3.326 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 20.572 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 20.742 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 4.063 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 4.253 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 4.415 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 4.601 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 22.239 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 22.413 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 22.558 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 22.726 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 24.212 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 24.385 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 24.531 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 24.698 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 26.235 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 26.409 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 26.555 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 26.723 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 28.167 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 28.292 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 28.462 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-0: committed 28.633 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 4.482 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 4.654 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 2.997 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 3.171 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 7.320 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 7.491 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 3.328 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 3.500 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 19.357 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 19.533 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 4.812 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 4.989 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 5.822 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 5.999 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 7.645 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 7.815 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 19.691 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 19.858 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 20.988 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 21.164 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 6.157 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 6.336 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 21.310 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 21.477 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 23.166 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 23.340 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 23.485 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 23.652 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 25.139 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 25.312 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 25.458 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 25.625 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 27.144 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 27.318 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 27.462 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 27.630 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 29.074 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 29.198 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 29.369 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-1: committed 29.540 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 17.531 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 17.708 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 3.882 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 4.057 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 4.212 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 4.381 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 17.862 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 18.029 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 5.371 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 5.547 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 2.582 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 2.770 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 19.172 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 19.347 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 19.499 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 19.666 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 21.190 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 21.365 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 2.934 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 3.120 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 5.705 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 5.885 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 21.510 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 21.677 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 23.173 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 23.347 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 23.492 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 23.659 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 25.190 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 25.361 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 25.508 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 25.675 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 27.161 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 27.333 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 27.478 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 27.646 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 29.088 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 29.212 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 29.383 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-2: committed 29.554 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 5.644 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 5.816 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 4.303 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 4.476 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 19.180 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 19.356 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 2.785 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 2.963 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 19.509 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 19.676 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 3.127 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 3.307 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 5.972 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 6.145 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 7.128 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 7.303 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 7.464 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 7.637 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 20.605 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 20.781 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 4.639 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 4.824 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 20.927 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 21.094 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 22.783 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 22.957 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 23.102 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 23.269 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 24.755 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 24.928 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 25.074 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 25.241 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 26.761 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 26.934 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 27.079 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 27.247 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 28.691 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 28.815 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 28.986 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-3: committed 29.157 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 17.903 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 18.081 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 4.295 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 4.469 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 5.808 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 5.982 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 6.137 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 6.307 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 18.233 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 18.400 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 19.747 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 19.924 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 2.827 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 3.015 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 3.182 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 3.363 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 20.081 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 20.249 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 21.757 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 21.932 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 4.633 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 4.817 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 22.078 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 22.245 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 23.736 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 23.910 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 24.055 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 24.223 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 25.754 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 25.925 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 26.072 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 26.239 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 27.724 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 27.897 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 28.041 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 28.209 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 29.844 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 29.969 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 30.139 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-4: committed 30.310 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 18.743 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 18.920 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 6.666 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 6.839 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 5.168 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 5.344 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 6.994 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 7.164 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 19.072 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 19.240 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 20.181 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 20.359 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 3.068 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 3.256 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 3.422 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 3.603 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 3.860 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 4.045 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 4.203 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 4.385 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 5.503 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 5.682 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 20.504 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 20.671 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 22.165 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 22.339 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 22.484 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 22.651 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 24.138 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 24.311 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 24.457 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 24.624 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 26.147 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 26.319 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 26.465 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 26.633 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 28.087 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 28.212 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 28.382 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-5: committed 28.553 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 16.801 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 16.977 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 4.591 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 4.764 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 17.130 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 17.297 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 18.249 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 18.423 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 3.073 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 3.254 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 3.418 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 3.597 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 18.575 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 18.743 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 20.266 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 20.440 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 20.598 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 20.765 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 4.922 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 5.104 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 22.079 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 22.254 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 22.398 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 22.566 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 25.059 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 25.231 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 25.378 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 26.089 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 26.249 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 26.417 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 26.562 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 28.246 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 28.402 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 28.569 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 28.713 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 30.189 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 30.324 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 30.446 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 30.612 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-6: committed 32.254 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 5.650 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 5.822 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 7.146 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 7.317 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 2.780 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 2.957 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 19.177 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 19.353 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 4.302 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 4.480 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 3.121 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 3.300 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 7.471 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 7.642 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 19.506 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 19.673 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 5.988 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 6.165 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 20.606 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 20.781 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 4.643 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 4.827 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 20.927 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 21.095 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 22.586 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 22.760 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 22.905 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 23.073 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 24.755 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 24.928 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 25.074 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 25.241 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 26.761 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 26.935 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 27.079 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 27.247 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 28.690 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 28.814 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 28.985 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-burst-7: committed 29.156 ms after its port's answer to the last of 16 recipients (bound 130 ms) within
NOTICE notice-retried-0: committed 8.275 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-1: committed 8.100 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-2: committed 8.190 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-3: committed 8.191 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-4: committed 8.189 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-5: committed 8.191 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-6: committed 8.101 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
NOTICE notice-retried-7: committed 8.191 ms after its port's answer to the last of 16 recipients (bound 20 ms) within
BUDGET backlog.owed.if0: 64.036 ms over its budget 20 ms
BUDGET backlog.owed_behind0.if0: 64.231 ms over its budget 20 ms
BUDGET backlog.owed_behind1.if0: 64.424 ms over its budget 20 ms
BUDGET backlog.owed_behind2.if0: 64.616 ms over its budget 20 ms
BUDGET backlog.owed_behind3.if0: 64.809 ms over its budget 20 ms
BUDGET backlog-owed.service.acmp.last.if0: 63.048 ms over its budget 20 ms
BUDGET backlog-owed.service.aecp.last.if0: 63.083 ms over its budget 20 ms
AGED 24 windows opened with the step's age at its limit or one short of it, 9 aged steps among their records; the least margin 8.039 ms, backlog-adp@program-aged2-7.service.srp.last.if0 at 11.961 ms
SAVE save-second: durable 23789.630 ms after its change (stated worst case 23,830 ms, 398 steps, longest gap between flash steps 30.875 ms) within
SAVE save-held: durable 1353.448 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 32.748 ms) within
STATED srp-bound: a build-one pass of 171,645 CPU cycles, over its stated 147,500
STATED srp-bound: a pass's polls base of 58,780 CPU cycles, over its stated 30,000
STATED srp-bound: an SRP record's apply of 137,607 CPU cycles, over its stated 37,500
STATED srp-bound: a tier-2 slice of THE TRANSMIT's build of 171,645 CPU cycles, over the stated slice 147,500
STATED #977 (https://github.com/kebag-logic/milan-fpga/issues/977): srp-kept and srp-bound are graded together on one image, this run graded srp-bound alone
AGED 24 windows opened with the step's age at its limit or one short of it, 9 aged steps among their records; the least margin 8.062 ms, backlog-adp@program-aged2-2.service.srp.last.if0 at 11.938 ms
SAVE save-starved: durable 12926.984 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 31.988 ms) within
SAVE save: durable 1299.649 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 102.332 ms) within
STATED srp-kept: an SRP record's apply of 130,428 CPU cycles, over its stated 37,500
STATED srp-kept: an SRP record's apply of 69,970 CPU cycles, over its stated 37,500
STATED srp-kept: an SRP record's apply of 133,402 CPU cycles, over its stated 37,500
STATED #977 (https://github.com/kebag-logic/milan-fpga/issues/977): srp-kept and srp-bound are graded together on one image, this run graded srp-kept alone
DECLARING aecp-outputs: 13 completion(s) in 13 record(s), 2 in rounds of THE RETRY, 42 GET_STREAM_INFO(s) of a STREAM_OUTPUT left
AGED 15 windows opened with the step's age at its limit or one short of it, 6 aged steps among their records; the least margin 8.444 ms, backlog-adp@blank-aged2-5.service.srp.last.if0 at 11.556 ms
SAVE save-second: durable 23789.706 ms after its change (stated worst case 23,830 ms, 398 steps, longest gap between flash steps 30.867 ms) within
AGED 18 windows opened with the step's age at its limit or one short of it, 9 aged steps among their records; the least margin 8.497 ms, backlog-adp@verify-aged2-7.service.srp.last.if0 at 11.503 ms
SAVE save-starved: durable 12926.878 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 32.079 ms) within
SAVE save: durable 1297.919 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 102.104 ms) within
OWED srp.kept_advertise.if0: a record of 138,467 CPU cycles, 1455 us by the rule, over CTRL_LOOP_SRP_UNIT_US 375 us, owed to #977 (https://github.com/kebag-logic/milan-fpga/issues/977)
OWED srp.kept_recount.if0: a record of 71,791 CPU cycles, 755 us by the rule, over CTRL_LOOP_SRP_UNIT_US 375 us, owed to #977 (https://github.com/kebag-logic/milan-fpga/issues/977)
OWED srp.kept_failed.if0: a record of 142,582 CPU cycles, 1500 us by the rule, over CTRL_LOOP_SRP_UNIT_US 375 us, owed to #977 (https://github.com/kebag-logic/milan-fpga/issues/977)
OWED srp.bound_advertise.if0: a record of 142,137 CPU cycles, 1495 us by the rule, over CTRL_LOOP_SRP_UNIT_US 375 us, owed to #977 (https://github.com/kebag-logic/milan-fpga/issues/977)
OWED srp-bound: a work pass of 216,785 CPU cycles at bus cycle 617570490 over THE SHARE, the bound path's registrations, owed to #977 (https://github.com/kebag-logic/milan-fpga/issues/977)
STATED srp-kept: an SRP record's apply of 138,121 CPU cycles, over its stated 37,500
STATED srp-kept: an SRP record's apply of 71,445 CPU cycles, over its stated 37,500
STATED srp-kept: an SRP record's apply of 141,898 CPU cycles, over its stated 37,500
STATED srp-bound: a pass's polls base of 60,490 CPU cycles, over its stated 30,000
STATED srp-bound: a walk item of 13,656 CPU cycles, over its stated 12,000
STATED srp-bound: an SRP record's apply of 141,791 CPU cycles, over its stated 37,500
STATED srp-bound: a tier-2 slice of SRP's records of 154,605 CPU cycles, over the stated slice 147,500
STATED #977 (https://github.com/kebag-logic/milan-fpga/issues/977): srp.kept_failed.if0: kept <= bound broken, 142,582 CPU cycles against the bound record's 142,137
BUDGET backlog.owed.if0: 64.014 ms over its budget 20 ms
BUDGET backlog.owed_behind0.if0: 64.207 ms over its budget 20 ms
BUDGET backlog.owed_behind1.if0: 64.397 ms over its budget 20 ms
BUDGET backlog.owed_behind2.if0: 64.587 ms over its budget 20 ms
BUDGET backlog.owed_behind3.if0: 64.778 ms over its budget 20 ms
BUDGET backlog-owed.service.acmp.last.if0: 63.036 ms over its budget 20 ms
BUDGET backlog-owed.service.aecp.last.if0: 63.071 ms over its budget 20 ms
AGED 15 windows opened with the step's age at its limit or one short of it, 6 aged steps among their records; the least margin 8.352 ms, backlog-adp@program-aged2-6.service.srp.last.if0 at 11.648 ms
SAVE save-held: durable 1344.602 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 33.156 ms) within
NOTICE talker-notice-0.declared.if0: committed 11.662 ms after its event's commit at sys 300000965, the last of 16 recipients at sys 301167195 (bound 20 ms) within
NOTICE talker-notice-0.withdrawn.if0: committed 10.267 ms after its event's commit at sys 360000955, the last of 16 recipients at sys 361027640 (bound 20 ms) within
NOTICE talker-notice-1.declared.if0: committed 10.245 ms after its event's commit at sys 300100141, the last of 16 recipients at sys 301124658 (bound 20 ms) within
NOTICE talker-notice-1.withdrawn.if0: committed 9.256 ms after its event's commit at sys 360100131, the last of 16 recipients at sys 361025744 (bound 20 ms) within
NOTICE talker-notice-2.declared.if0: committed 9.256 ms after its event's commit at sys 300200141, the last of 16 recipients at sys 301125753 (bound 20 ms) within
NOTICE talker-notice-2.withdrawn.if0: committed 8.217 ms after its event's commit at sys 360200131, the last of 16 recipients at sys 361021853 (bound 20 ms) within
NOTICE talker-notice-3.declared.if0: committed 8.256 ms after its event's commit at sys 300300141, the last of 16 recipients at sys 301125753 (bound 20 ms) within
NOTICE talker-notice-3.withdrawn.if0: committed 7.199 ms after its event's commit at sys 360300131, the last of 16 recipients at sys 361019996 (bound 20 ms) within
NOTICE talker-notice-4.declared.if0: committed 7.248 ms after its event's commit at sys 300400141, the last of 16 recipients at sys 301124893 (bound 20 ms) within
NOTICE talker-notice-4.withdrawn.if0: committed 6.207 ms after its event's commit at sys 360400131, the last of 16 recipients at sys 361020869 (bound 20 ms) within
NOTICE talker-notice-5.declared.if0: committed 5.449 ms after its event's commit at sys 300500141, the last of 16 recipients at sys 301045045 (bound 20 ms) within
NOTICE talker-notice-5.withdrawn.if0: committed 5.250 ms after its event's commit at sys 360500131, the last of 16 recipients at sys 361025165 (bound 20 ms) within
NOTICE talker-notice-6.declared.if0: committed 4.661 ms after its event's commit at sys 300600141, the last of 16 recipients at sys 301066287 (bound 20 ms) within
NOTICE talker-notice-6.withdrawn.if0: committed 4.492 ms after its event's commit at sys 360600131, the last of 16 recipients at sys 361049325 (bound 20 ms) within
NOTICE talker-notice-7.declared.if0: committed 3.857 ms after its event's commit at sys 300700141, the last of 16 recipients at sys 301085816 (bound 20 ms) within
NOTICE talker-notice-7.withdrawn.if0: committed 3.677 ms after its event's commit at sys 360700131, the last of 16 recipients at sys 361067809 (bound 20 ms) within
SAVE srp-talker-held: durable 1535.388 ms after its change (stated worst case 12,950 ms, 398 steps, longest gap between flash steps 40.985 ms) within

## The statement survey (survey 8x8-1if rc=1)
{"ordinary costs": 0, "long costs": 0, "datapath": 0, "compare ordinary": 1} | long: item.aecp_long (the polls): 30,948 CPU cycles, 325 us by the rule, against aecp_long 320 us at 8x8/1if: OVER; declaring-outputs-part0/aecp-largest-notice; the notice kind (aecp_kinds.py): 30,948 CPU cycles, 325 us by the rule, against aecp_long 320 us at 8x8/1if: OVER; declaring-outputs-part0/aecp-largest-notice (15 frame(s))
# 8x8/1if at shape (1, 9, 9); its records and events NEAREST 8x8/2if's; record.aecp by class in record_classes.py (long 1720, paced 685, other 265 us)
cost                                     most cycles       us  rule stated verdict  statement; where
base                                          25,489   254.89   270    300 within   load_grade.stated(8x8/1if) GRADED base; valid-destinations-part1/srp-talker-held
base                                          25,489   254.89   270    300 within   load_grade.stated(8x8/1if) STATED_US base; valid-destinations-part1/srp-talker-held
base                                          25,489   254.89   270    300 within   poll_grade.STATED_US[(1, 9, 9)] base; valid-destinations-part1/srp-talker-held
build                                              0     0.00     0   1795 within   load_grade.stated(8x8/1if) GRADED build; answering-every-port-part0/notice-every-0
build                                              0     0.00     0   1795 within   load_grade.stated(8x8/1if) STATED_US build; answering-every-port-part0/notice-every-0
build                                              0     0.00     0   1795 within   whole_grade.stated_us((1, 9, 9)) build (ctrl_loop.h); answering-every-port-part0/notice-every-0
build_one                                    119,755  1197.55  1260   1475 within   load_grade.stated(8x8/1if) GRADED build_one; valid-destinations-part1/srp-talker-held
build_one                                    119,755  1197.55  1260   1475 within   load_grade.stated(8x8/1if) STATED_US build_one; valid-destinations-part1/srp-talker-held
build_one                                    119,755  1197.55  1260   1475 within   whole_grade.stated_us((1, 9, 9)) build-one (ctrl_loop.h); valid-destinations-part1/srp-talker-held
centisecond                                   23,251   232.51   245    510 within   load_grade.stated(8x8/1if) GRADED centisecond; valid-destinations-part1/srp-talker-held.log
centisecond                                   23,251   232.51   245    510 within   load_grade.stated(8x8/1if) STATED_US centisecond; valid-destinations-part1/srp-talker-held.log
event.ACMP                                    15,761   157.61   170    210 within   load_grade.stated(8x8/1if) GRADED event.ACMP; TIMER#1, 46 taken
event.ACMP                                    15,761   157.61   170    350 within   load_grade.stated(8x8/1if) STATED_US event.ACMP; TIMER#1, 46 taken
event.ADP                                      7,620    76.20    85    120 within   load_grade.stated(8x8/1if) GRADED event.ADP; TIMER#0, 301 taken
event.ADP                                      7,620    76.20    85    120 within   load_grade.stated(8x8/1if) STATED_US event.ADP; TIMER#0, 301 taken
event.AECP                                     7,285    72.85    80    120 within   load_grade.stated(8x8/1if) GRADED event.AECP; TIMER#3, 36540 taken
event.AECP                                     7,285    72.85    80    120 within   load_grade.stated(8x8/1if) STATED_US event.AECP; TIMER#3, 36540 taken
event.GM                                       3,228    32.28    35    320 within   load_grade.stated(8x8/1if) GRADED event.GM; GM, 555409 taken
event.GM                                       3,228    32.28    35    320 within   load_grade.stated(8x8/1if) STATED_US event.GM; GM, 555409 taken
event.LINK                                    23,054   230.54   245    300 within   rows_grade.ROW_COSTS[8x8/2if] event.LINK; LINK, 248 taken
event.MAAP                                    18,298   182.98   195    225 within   load_grade.stated(8x8/1if) GRADED event.MAAP; TIMER#2, 674 taken
event.MAAP                                    18,298   182.98   195    225 within   load_grade.stated(8x8/1if) STATED_US event.MAAP; TIMER#2, 674 taken
event.TICK                                     3,731    37.31    40     85 within   load_grade.stated(8x8/1if) GRADED event.TICK; TICK, 95576 taken
event.TICK                                     3,731    37.31    40     55 within   load_grade.stated(8x8/1if) STATED_US event.TICK; TICK, 95576 taken
events_none                                    3,957    39.57    45     45 within   load_grade.stated(8x8/1if) GRADED events_none; valid-destinations-part1/srp-talker-held.log
events_none                                    3,957    39.57    45     45 within   load_grade.stated(8x8/1if) STATED_US events_none; valid-destinations-part1/srp-talker-held.log
item.acmp                                      6,008    60.08    65     80 within   load_grade.stated(8x8/1if) GRADED item.acmp; answering-ports-part0/backlog-owed
item.acmp                                      6,008    60.08    65     80 within   load_grade.stated(8x8/1if) STATED_US item.acmp; answering-ports-part0/backlog-owed
item.acmp                                      6,008    60.08    65     80 within   poll_grade.STATED_US[(1, 9, 9)] acmp; answering-ports-part0/backlog-owed
item.acmp_declined                             1,594    15.94    20     30 within   load_grade.stated(8x8/1if) GRADED item.acmp_declined; answering-ports-part0/backlog-owed
item.acmp_declined                             1,594    15.94    20     30 within   load_grade.stated(8x8/1if) STATED_US item.acmp_declined; answering-ports-part0/backlog-owed
item.acmp_declined                             1,594    15.94    20     30 within   poll_grade.STATED_US[(1, 9, 9)] acmp_declined; answering-ports-part0/backlog-owed
item.acmp_kept                                 7,714    77.14    85    440 within   load_grade.stated(8x8/1if) STATED_US record.acmp; answering-ports-part0/backlog-owed
item.aecp                                     13,466   134.66   145    145 within   poll_grade.STATED_US[(1, 9, 9)] aecp; talker-notices-part0/talker-notice-0
item.aecp_long                                     0     0.00     0    320 within   poll_grade.STATED_US[(1, 9, 9)] aecp_long; answering-every-port-part0/notice-every-0
item.aecp_long                                     0     0.00     0    320 within   poll_grade.STATED_US[(1, 9, 9)] aecp_long; answering-every-port-part0/notice-every-0
item.mrpdu                                         0     0.00     0   1475 within   load_grade.stated(8x8/1if) GRADED item.mrpdu; answering-every-port-part0/notice-every-0
item.mrpdu                                         0     0.00     0   1475 within   load_grade.stated(8x8/1if) STATED_US item.mrpdu; answering-every-port-part0/notice-every-0
item.mrpdu                                         0     0.00     0   1475 within   poll_grade.STATED_US[(1, 9, 9)] mrpdu; answering-every-port-part0/notice-every-0
item.rebuild                                  20,752   207.52   220    590 within   poll_grade.STATED_US[(1, 9, 9)] rebuild; answering-ports-part1/adp-link
item.reclaim                                   1,575    15.75    20     40 within   load_grade.stated(8x8/1if) GRADED item.reclaim; none-part0/srp
item.reclaim                                   1,575    15.75    20     40 within   load_grade.stated(8x8/1if) STATED_US item.reclaim; none-part0/srp
item.reclaim                                   1,575    15.75    20     40 within   poll_grade.STATED_US[(1, 9, 9)] reclaim; none-part0/srp
item.record                                   34,487   344.87   365    375 within   poll_grade.STATED_US[(1, 9, 9)] retained; valid-destinations-part1/srp-talker-held
item.retained                                      0     0.00     0    375 within   load_grade.stated(8x8/1if) GRADED item.retained; answering-every-port-part0/notice-every-0
item.retained                                      0     0.00     0    375 within   load_grade.stated(8x8/1if) STATED_US item.retained; answering-every-port-part0/notice-every-0
item.retained                                      0     0.00     0    375 within   poll_grade.STATED_US[(1, 9, 9)] retained; answering-every-port-part0/notice-every-0
item.walk                                      2,773    27.73    30    120 within   load_grade.stated(8x8/1if) GRADED item.walk; valid-destinations-part0/srp-talker
item.walk                                      2,773    27.73    30    120 within   load_grade.stated(8x8/1if) STATED_US item.walk; valid-destinations-part0/srp-talker
item.walk                                      2,773    27.73    30    120 within   poll_grade.STATED_US[(1, 9, 9)] walk; valid-destinations-part0/srp-talker
item.withdraw                                  6,912    69.12    75    110 within   poll_grade.STATED_US[(1, 9, 9)] withdraw; answering-ports-part1/backlog
record.acmp                                   21,143   211.43   225    305 within   load_grade.stated(8x8/1if) GRADED record.acmp; declaring-outputs-part0/aecp-fanout.log
record.acmp                                   21,143   211.43   225    440 within   load_grade.stated(8x8/1if) STATED_US record.acmp; declaring-outputs-part0/aecp-fanout.log
record.adp                                    11,522   115.22   125    135 within   load_grade.stated(8x8/1if) GRADED record.adp; none-part0/backlog-adp-refill.log
record.adp                                    11,522   115.22   125    240 within   load_grade.stated(8x8/1if) STATED_US record.adp; none-part0/backlog-adp-refill.log
record.maap                                   14,273   142.73   150    185 within   load_grade.stated(8x8/1if) GRADED record.maap; valid-destinations-part1/srp-talker-loss.log
record.maap                                   14,273   142.73   150    185 within   load_grade.stated(8x8/1if) STATED_US record.maap; valid-destinations-part1/srp-talker-loss.log
record.srp                                   142,582  1425.82  1500    375 OVER-raw load_grade.stated(8x8/1if) GRADED record.srp; none-part1/srp-kept.log
record.srp                                   142,582  1425.82  1500    375 OVER-raw load_grade.stated(8x8/1if) STATED_US record.srp; none-part1/srp-kept.log
step                                          81,751   817.51   860   1030 within   load_grade.stated(8x8/1if) GRADED step; answering-ports-part1/save-starved
step                                          81,751   817.51   860   1030 within   load_grade.stated(8x8/1if) STATED_US step; answering-ports-part1/save-starved
step                                          81,751   817.51   860    975 within   whole_grade.stated_us((1, 9, 9)) step (ctrl_loop.h); answering-ports-part1/save-starved
item.aecp.notice                              13,466   134.66   145    275 within   load_grade.stated(8x8/1if) GRADED item.aecp.notice; talker-notices-part0/talker-notice-0 (16 frame(s))
item.aecp.notice                              13,466   134.66   145    275 within   load_grade.stated(8x8/1if) STATED_US item.aecp.notice; talker-notices-part0/talker-notice-0 (16 frame(s))
item.aecp.response                             2,491    24.91    30     65 within   load_grade.stated(8x8/1if) GRADED item.aecp.response; answering-ports-part0/backlog-owed (1 frame(s))
item.aecp.response                             2,491    24.91    30     65 within   load_grade.stated(8x8/1if) STATED_US item.aecp.response; answering-ports-part0/backlog-owed (1 frame(s))
event.AMAP_LIVE_WRITE                          1,651    16.51    20     30 within   rows_tiers.DATAPATH_US[8x8/2if] AMAP_LIVE_WRITE; datapath-events.log@76419717
event.AS_PATH_CHANGED                          2,812    28.12    30     40 within   rows_tiers.DATAPATH_US[8x8/2if] AS_PATH_CHANGED; datapath-events.log@72016645
event.AVB_INFO_CHANGED                         2,553    25.53    30     40 within   rows_tiers.DATAPATH_US[8x8/2if] AVB_INFO_CHANGED; datapath-events.log@71816365

# 2 statement(s) exceeded (OVER: by the rule; OVER-raw: cycles / 100 alone exceeds it)
record.srp                                   142,582  1425.82  1500    375 OVER-raw load_grade.stated(8x8/1if) GRADED record.srp; none-part1/srp-kept.log
record.srp                                   142,582  1425.82  1500    375 OVER-raw load_grade.stated(8x8/1if) STATED_US record.srp; none-part1/srp-kept.log
# aecp-largest-notice: its notices against the largest legal notice's statement at 8x8/1if (poll_grade aecp_long)
item.aecp_long (the polls): 30,948 CPU cycles, 325 us by the rule, against aecp_long 320 us at 8x8/1if: OVER; declaring-outputs-part0/aecp-largest-notice
the notice kind (aecp_kinds.py): 30,948 CPU cycles, 325 us by the rule, against aecp_long 320 us at 8x8/1if: OVER; declaring-outputs-part0/aecp-largest-notice (15 frame(s))
# 2 exceeded

## The AECP records by class (record_classes.py over every leg; record_classes 8x8-1if rc=0)
part0: 8x8/1if answering-every-port, 16 groups, 1040 AECP records
part0: 8x8/1if answering-later, 8 groups, 648 AECP records
part0: 8x8/1if answering-ports, 50 groups, 5578 AECP records
part1: 8x8/1if answering-ports, 52 groups, 3679 AECP records
part0: 8x8/1if declaring-outputs, 5 groups, 130 AECP records
part0: 8x8/1if none, 33 groups, 2661 AECP records
part1: 8x8/1if none, 34 groups, 3173 AECP records
part2: 8x8/1if none, 34 groups, 3396 AECP records
part0: 8x8/1if shutdown-entry, 2 groups, 0 AECP records
part0: 8x8/1if talker-notices, 8 groups, 648 AECP records
part0: 8x8/1if valid-destinations, 1 groups, 0 AECP records
part1: 8x8/1if valid-destinations, 2 groups, 2705 AECP records
8x8/1if reported long: the dearest 85,968 CPU cycles, 905 us by the rule, stated 1720 us (declaring-outputs aecp-largest-notice: the largest legal command's)
8x8/1if held long: the dearest 85,310 CPU cycles, 900 us by the rule, stated 1720 us (none aecp-largest-notice: the largest legal command's)
8x8/1if reported other: the dearest 24,470 CPU cycles, 260 us by the rule, stated 265 us (talker-notices talker-notice-0: command 0x0004)
8x8/1if held other: the dearest 24,873 CPU cycles, 265 us by the rule, stated 265 us (answering-every-port notice-every-0: command 0x0004)
8x8/1if reported paced: the dearest 57,500 CPU cycles, 605 us by the rule, stated 685 us (declaring-outputs aecp-fanout: SET_CONFIGURATION, paced)
8x8/1if held paced: the dearest 55,732 CPU cycles, 590 us by the rule, stated 685 us (answering-ports aecp-fanout: SET_CONFIGURATION, paced)
RESULT: PASS
