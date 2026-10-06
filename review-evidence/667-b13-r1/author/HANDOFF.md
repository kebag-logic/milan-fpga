# [A549] B13 handoff

Refs #667. Status: REVIEW READY posted; measurements, restoration, findings and gates complete.
Branch: `667-b13-bench`.
Base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Assigned image: dev `28f9666f`, seed `asl`.
Reviewers: [R510] internal and [R511] external.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6009837251

## Progress

| Item | State | Evidence |
|---|---|---|
| Identity gate | PASS | `identity.json`; VERSION and AEM CRC match |
| As-found state | SAVED | `restore-start.jsonl`: 44 rows; 18 bindings zero |
| Two-hour soak | PASS | 7203.971 s; 145 clean checkpoints |
| 100 talker starts | COMPLETE | 14 EARLY-positive binds; LATE zero |
| Restore readback | PASS final | All 44 rows match; servo and audio readback match |
| Documentation gates | PASS | All seven required gates returned zero |
| Local commit | COMMITTED | `afa4e687234b80e9474aa6dd0dc756de16a241bd`; worktree clean |
| Bench lock | RELEASED | Both sessions exited; lock probe returned zero |

## Cycle ledger

| Cycle | UTC | Elapsed soak / cycle action | Counter result | Capture evidence | Status |
|---|---|---|---|---|---|

| soak-000 | 2026-10-06T05:27:01.179292+00:00 | 0.397 s | CLEAN | soak-000 captures | CLEAN |

| soak-001 | 2026-10-06T05:27:54.349502+00:00 | 53.567 s | CLEAN | soak-001 captures | CLEAN |

| soak-002 | 2026-10-06T05:28:44.229802+00:00 | 103.448 s | CLEAN | soak-002 captures | CLEAN |

| soak-003 | 2026-10-06T05:29:34.306281+00:00 | 153.524 s | CLEAN | soak-003 captures | CLEAN |

| soak-004 | 2026-10-06T05:30:24.247967+00:00 | 203.466 s | CLEAN | soak-004 captures | CLEAN |

| soak-005 | 2026-10-06T05:31:14.101259+00:00 | 253.319 s | CLEAN | soak-005 captures | CLEAN |

| soak-006 | 2026-10-06T05:32:04.225667+00:00 | 303.444 s | CLEAN | soak-006 captures | CLEAN |

| soak-007 | 2026-10-06T05:32:54.142720+00:00 | 353.361 s | CLEAN | soak-007 captures | CLEAN |

| soak-008 | 2026-10-06T05:33:44.216482+00:00 | 403.434 s | CLEAN | soak-008 captures | CLEAN |

| soak-009 | 2026-10-06T05:34:34.258599+00:00 | 453.477 s | CLEAN | soak-009 captures | CLEAN |

| soak-010 | 2026-10-06T05:35:24.309334+00:00 | 503.527 s | CLEAN | soak-010 captures | CLEAN |

| soak-011 | 2026-10-06T05:36:13.941672+00:00 | 553.160 s | CLEAN | soak-011 captures | CLEAN |

| soak-012 | 2026-10-06T05:37:04.161872+00:00 | 603.380 s | CLEAN | soak-012 captures | CLEAN |

| soak-013 | 2026-10-06T05:37:54.108915+00:00 | 653.327 s | CLEAN | soak-013 captures | CLEAN |

| soak-014 | 2026-10-06T05:38:44.129289+00:00 | 703.347 s | CLEAN | soak-014 captures | CLEAN |

| soak-015 | 2026-10-06T05:39:34.166521+00:00 | 753.385 s | CLEAN | soak-015 captures | CLEAN |

| soak-016 | 2026-10-06T05:40:24.159915+00:00 | 803.378 s | CLEAN | soak-016 captures | CLEAN |

| soak-017 | 2026-10-06T05:41:14.269389+00:00 | 853.487 s | CLEAN | soak-017 captures | CLEAN |

| soak-018 | 2026-10-06T05:42:04.175626+00:00 | 903.394 s | CLEAN | soak-018 captures | CLEAN |

| soak-019 | 2026-10-06T05:42:54.083795+00:00 | 953.302 s | CLEAN | soak-019 captures | CLEAN |

| soak-020 | 2026-10-06T05:43:44.163492+00:00 | 1003.381 s | CLEAN | soak-020 captures | CLEAN |

| soak-021 | 2026-10-06T05:44:34.238555+00:00 | 1053.457 s | CLEAN | soak-021 captures | CLEAN |

| soak-022 | 2026-10-06T05:45:24.131163+00:00 | 1103.349 s | CLEAN | soak-022 captures | CLEAN |

| soak-023 | 2026-10-06T05:46:14.201415+00:00 | 1153.419 s | CLEAN | soak-023 captures | CLEAN |

| soak-024 | 2026-10-06T05:47:04.234966+00:00 | 1203.453 s | CLEAN | soak-024 captures | CLEAN |

| soak-025 | 2026-10-06T05:47:54.012745+00:00 | 1253.231 s | CLEAN | soak-025 captures | CLEAN |

| soak-026 | 2026-10-06T05:48:44.076801+00:00 | 1303.295 s | CLEAN | soak-026 captures | CLEAN |

| soak-027 | 2026-10-06T05:49:34.206772+00:00 | 1353.425 s | CLEAN | soak-027 captures | CLEAN |

| soak-028 | 2026-10-06T05:50:24.231167+00:00 | 1403.449 s | CLEAN | soak-028 captures | CLEAN |

| soak-029 | 2026-10-06T05:51:14.364156+00:00 | 1453.582 s | CLEAN | soak-029 captures | CLEAN |

| soak-030 | 2026-10-06T05:52:04.698440+00:00 | 1503.916 s | CLEAN | soak-030 captures | CLEAN |

| soak-031 | 2026-10-06T05:53:00.424880+00:00 | 1559.643 s | CLEAN | soak-031 captures | CLEAN |

| soak-032 | 2026-10-06T05:53:45.267274+00:00 | 1604.485 s | CLEAN | soak-032 captures | CLEAN |

| soak-033 | 2026-10-06T05:54:34.796921+00:00 | 1654.015 s | CLEAN | soak-033 captures | CLEAN |

| soak-034 | 2026-10-06T05:55:24.686701+00:00 | 1703.905 s | CLEAN | soak-034 captures | CLEAN |

| soak-035 | 2026-10-06T05:56:14.637474+00:00 | 1753.855 s | CLEAN | soak-035 captures | CLEAN |

| soak-036 | 2026-10-06T05:57:04.405494+00:00 | 1803.623 s | CLEAN | soak-036 captures | CLEAN |

| soak-037 | 2026-10-06T05:57:54.416842+00:00 | 1853.635 s | CLEAN | soak-037 captures | CLEAN |

| soak-038 | 2026-10-06T05:58:44.493596+00:00 | 1903.712 s | CLEAN | soak-038 captures | CLEAN |

| soak-039 | 2026-10-06T05:59:34.520659+00:00 | 1953.738 s | CLEAN | soak-039 captures | CLEAN |

| soak-040 | 2026-10-06T06:00:24.339676+00:00 | 2003.558 s | CLEAN | soak-040 captures | CLEAN |

| soak-041 | 2026-10-06T06:01:14.310380+00:00 | 2053.528 s | CLEAN | soak-041 captures | CLEAN |

| soak-042 | 2026-10-06T06:02:04.406634+00:00 | 2103.625 s | CLEAN | soak-042 captures | CLEAN |

| soak-043 | 2026-10-06T06:02:54.086824+00:00 | 2153.305 s | CLEAN | soak-043 captures | CLEAN |

| soak-044 | 2026-10-06T06:03:44.066352+00:00 | 2203.284 s | CLEAN | soak-044 captures | CLEAN |

| soak-045 | 2026-10-06T06:04:34.035399+00:00 | 2253.253 s | CLEAN | soak-045 captures | CLEAN |

| soak-046 | 2026-10-06T06:05:24.153502+00:00 | 2303.371 s | CLEAN | soak-046 captures | CLEAN |

| soak-047 | 2026-10-06T06:06:14.101821+00:00 | 2353.320 s | CLEAN | soak-047 captures | CLEAN |

| soak-048 | 2026-10-06T06:07:04.074124+00:00 | 2403.292 s | CLEAN | soak-048 captures | CLEAN |

| soak-049 | 2026-10-06T06:07:54.051643+00:00 | 2453.270 s | CLEAN | soak-049 captures | CLEAN |

| soak-050 | 2026-10-06T06:08:43.985506+00:00 | 2503.203 s | CLEAN | soak-050 captures | CLEAN |

| soak-051 | 2026-10-06T06:09:34.022458+00:00 | 2553.240 s | CLEAN | soak-051 captures | CLEAN |

| soak-052 | 2026-10-06T06:10:24.028190+00:00 | 2603.246 s | CLEAN | soak-052 captures | CLEAN |

| soak-053 | 2026-10-06T06:11:14.055604+00:00 | 2653.274 s | CLEAN | soak-053 captures | CLEAN |

| soak-054 | 2026-10-06T06:12:04.126769+00:00 | 2703.345 s | CLEAN | soak-054 captures | CLEAN |

| soak-055 | 2026-10-06T06:12:54.084967+00:00 | 2753.303 s | CLEAN | soak-055 captures | CLEAN |

| soak-056 | 2026-10-06T06:13:43.970435+00:00 | 2803.188 s | CLEAN | soak-056 captures | CLEAN |

| soak-057 | 2026-10-06T06:14:34.196235+00:00 | 2853.414 s | CLEAN | soak-057 captures | CLEAN |

| soak-058 | 2026-10-06T06:15:24.041045+00:00 | 2903.259 s | CLEAN | soak-058 captures | CLEAN |

| soak-059 | 2026-10-06T06:16:14.062542+00:00 | 2953.281 s | CLEAN | soak-059 captures | CLEAN |

| soak-060 | 2026-10-06T06:17:04.010298+00:00 | 3003.228 s | CLEAN | soak-060 captures | CLEAN |

| soak-061 | 2026-10-06T06:17:53.923519+00:00 | 3053.141 s | CLEAN | soak-061 captures | CLEAN |

| soak-062 | 2026-10-06T06:18:44.062313+00:00 | 3103.280 s | CLEAN | soak-062 captures | CLEAN |

| soak-063 | 2026-10-06T06:19:33.979025+00:00 | 3153.197 s | CLEAN | soak-063 captures | CLEAN |

| soak-064 | 2026-10-06T06:20:24.128937+00:00 | 3203.347 s | CLEAN | soak-064 captures | CLEAN |

| soak-065 | 2026-10-06T06:21:14.139202+00:00 | 3253.357 s | CLEAN | soak-065 captures | CLEAN |

| soak-066 | 2026-10-06T06:22:05.074847+00:00 | 3304.292 s | CLEAN | soak-066 captures | CLEAN |

| soak-067 | 2026-10-06T06:22:54.934395+00:00 | 3354.152 s | CLEAN | soak-067 captures | CLEAN |

| soak-068 | 2026-10-06T06:23:44.955131+00:00 | 3404.173 s | CLEAN | soak-068 captures | CLEAN |

| soak-069 | 2026-10-06T06:24:35.157229+00:00 | 3454.375 s | CLEAN | soak-069 captures | CLEAN |

| soak-070 | 2026-10-06T06:25:25.333730+00:00 | 3504.552 s | CLEAN | soak-070 captures | CLEAN |

| soak-071 | 2026-10-06T06:26:15.418665+00:00 | 3554.637 s | CLEAN | soak-071 captures | CLEAN |

| soak-072 | 2026-10-06T06:27:05.630790+00:00 | 3604.849 s | CLEAN | soak-072 captures | CLEAN |

| soak-073 | 2026-10-06T06:27:55.026515+00:00 | 3654.244 s | CLEAN | soak-073 captures | CLEAN |

| soak-074 | 2026-10-06T06:28:45.012158+00:00 | 3704.230 s | CLEAN | soak-074 captures | CLEAN |

| soak-075 | 2026-10-06T06:29:34.862474+00:00 | 3754.080 s | CLEAN | soak-075 captures | CLEAN |

| soak-076 | 2026-10-06T06:30:24.905751+00:00 | 3804.124 s | CLEAN | soak-076 captures | CLEAN |

| soak-077 | 2026-10-06T06:31:15.094023+00:00 | 3854.312 s | CLEAN | soak-077 captures | CLEAN |

| soak-078 | 2026-10-06T06:32:04.771954+00:00 | 3903.990 s | CLEAN | soak-078 captures | CLEAN |

| soak-079 | 2026-10-06T06:32:55.224510+00:00 | 3954.442 s | CLEAN | soak-079 captures | CLEAN |

| soak-080 | 2026-10-06T06:33:45.427554+00:00 | 4004.646 s | CLEAN | soak-080 captures | CLEAN |

| soak-081 | 2026-10-06T06:34:35.493703+00:00 | 4054.712 s | CLEAN | soak-081 captures | CLEAN |

| soak-082 | 2026-10-06T06:35:26.007538+00:00 | 4105.225 s | CLEAN | soak-082 captures | CLEAN |

| soak-083 | 2026-10-06T06:36:15.956060+00:00 | 4155.174 s | CLEAN | soak-083 captures | CLEAN |

| soak-084 | 2026-10-06T06:37:06.002214+00:00 | 4205.220 s | CLEAN | soak-084 captures | CLEAN |

| soak-085 | 2026-10-06T06:37:55.731336+00:00 | 4254.949 s | CLEAN | soak-085 captures | CLEAN |

| soak-086 | 2026-10-06T06:38:45.292783+00:00 | 4304.511 s | CLEAN | soak-086 captures | CLEAN |

| soak-087 | 2026-10-06T06:39:35.943890+00:00 | 4355.162 s | CLEAN | soak-087 captures | CLEAN |

| soak-088 | 2026-10-06T06:40:25.484139+00:00 | 4404.665 s | CLEAN | soak-088 captures | CLEAN |

| soak-089 | 2026-10-06T06:41:15.867448+00:00 | 4455.085 s | CLEAN | soak-089 captures | CLEAN |

| soak-090 | 2026-10-06T06:42:05.697096+00:00 | 4504.915 s | CLEAN | soak-090 captures | CLEAN |

| soak-091 | 2026-10-06T06:42:56.268054+00:00 | 4555.486 s | CLEAN | soak-091 captures | CLEAN |

| soak-092 | 2026-10-06T06:43:45.821155+00:00 | 4605.039 s | CLEAN | soak-092 captures | CLEAN |

| soak-093 | 2026-10-06T06:44:35.468825+00:00 | 4654.687 s | CLEAN | soak-093 captures | CLEAN |

| soak-094 | 2026-10-06T06:45:25.230354+00:00 | 4704.448 s | CLEAN | soak-094 captures | CLEAN |

| soak-095 | 2026-10-06T06:46:15.447995+00:00 | 4754.666 s | CLEAN | soak-095 captures | CLEAN |

| soak-096 | 2026-10-06T06:47:07.081398+00:00 | 4806.299 s | CLEAN | soak-096 captures | CLEAN |

| soak-097 | 2026-10-06T06:47:55.882327+00:00 | 4855.100 s | CLEAN | soak-097 captures | CLEAN |

| soak-098 | 2026-10-06T06:48:44.223417+00:00 | 4903.441 s | CLEAN | soak-098 captures | CLEAN |

| soak-099 | 2026-10-06T06:49:34.117711+00:00 | 4953.336 s | CLEAN | soak-099 captures | CLEAN |

| soak-100 | 2026-10-06T06:50:24.276267+00:00 | 5003.494 s | CLEAN | soak-100 captures | CLEAN |

| soak-101 | 2026-10-06T06:51:14.163198+00:00 | 5053.381 s | CLEAN | soak-101 captures | CLEAN |

| soak-102 | 2026-10-06T06:52:04.002491+00:00 | 5103.220 s | CLEAN | soak-102 captures | CLEAN |

| soak-103 | 2026-10-06T06:52:54.685647+00:00 | 5153.904 s | CLEAN | soak-103 captures | CLEAN |

| soak-104 | 2026-10-06T06:53:44.618589+00:00 | 5203.837 s | CLEAN | soak-104 captures | CLEAN |

| soak-105 | 2026-10-06T06:54:34.610227+00:00 | 5253.828 s | CLEAN | soak-105 captures | CLEAN |

| soak-106 | 2026-10-06T06:55:24.228608+00:00 | 5303.447 s | CLEAN | soak-106 captures | CLEAN |

| soak-107 | 2026-10-06T06:56:14.332607+00:00 | 5353.551 s | CLEAN | soak-107 captures | CLEAN |

| soak-108 | 2026-10-06T06:57:04.536780+00:00 | 5403.754 s | CLEAN | soak-108 captures | CLEAN |

| soak-109 | 2026-10-06T06:57:54.665183+00:00 | 5453.883 s | CLEAN | soak-109 captures | CLEAN |

| soak-110 | 2026-10-06T06:58:44.434869+00:00 | 5503.653 s | CLEAN | soak-110 captures | CLEAN |

| soak-111 | 2026-10-06T06:59:34.460730+00:00 | 5553.678 s | CLEAN | soak-111 captures | CLEAN |

| soak-112 | 2026-10-06T07:00:24.865957+00:00 | 5604.084 s | CLEAN | soak-112 captures | CLEAN |

| soak-113 | 2026-10-06T07:01:14.497272+00:00 | 5653.711 s | CLEAN | soak-113 captures | CLEAN |

| soak-114 | 2026-10-06T07:02:04.310884+00:00 | 5703.529 s | CLEAN | soak-114 captures | CLEAN |

| soak-115 | 2026-10-06T07:02:54.183232+00:00 | 5753.401 s | CLEAN | soak-115 captures | CLEAN |

| soak-116 | 2026-10-06T07:03:44.271480+00:00 | 5803.489 s | CLEAN | soak-116 captures | CLEAN |

| soak-117 | 2026-10-06T07:04:34.154194+00:00 | 5853.372 s | CLEAN | soak-117 captures | CLEAN |

| soak-118 | 2026-10-06T07:05:24.164892+00:00 | 5903.383 s | CLEAN | soak-118 captures | CLEAN |

| soak-119 | 2026-10-06T07:06:14.221145+00:00 | 5953.439 s | CLEAN | soak-119 captures | CLEAN |

| soak-120 | 2026-10-06T07:07:04.218133+00:00 | 6003.436 s | CLEAN | soak-120 captures | CLEAN |

| soak-121 | 2026-10-06T07:07:54.514802+00:00 | 6053.722 s | CLEAN | soak-121 captures | CLEAN |

| soak-122 | 2026-10-06T07:08:44.013172+00:00 | 6103.231 s | CLEAN | soak-122 captures | CLEAN |

| soak-123 | 2026-10-06T07:09:34.232871+00:00 | 6153.451 s | CLEAN | soak-123 captures | CLEAN |

| soak-124 | 2026-10-06T07:10:24.085807+00:00 | 6203.304 s | CLEAN | soak-124 captures | CLEAN |

| soak-125 | 2026-10-06T07:11:14.137951+00:00 | 6253.356 s | CLEAN | soak-125 captures | CLEAN |

| soak-126 | 2026-10-06T07:12:04.164019+00:00 | 6303.382 s | CLEAN | soak-126 captures | CLEAN |

| soak-127 | 2026-10-06T07:12:54.132217+00:00 | 6353.350 s | CLEAN | soak-127 captures | CLEAN |

| soak-128 | 2026-10-06T07:13:44.209113+00:00 | 6403.427 s | CLEAN | soak-128 captures | CLEAN |

| soak-129 | 2026-10-06T07:14:34.319622+00:00 | 6453.538 s | CLEAN | soak-129 captures | CLEAN |

| soak-130 | 2026-10-06T07:15:24.378426+00:00 | 6503.596 s | CLEAN | soak-130 captures | CLEAN |

| soak-131 | 2026-10-06T07:16:14.243612+00:00 | 6553.462 s | CLEAN | soak-131 captures | CLEAN |

| soak-132 | 2026-10-06T07:17:04.267555+00:00 | 6603.486 s | CLEAN | soak-132 captures | CLEAN |

| soak-133 | 2026-10-06T07:17:54.331806+00:00 | 6653.550 s | CLEAN | soak-133 captures | CLEAN |

| soak-134 | 2026-10-06T07:18:44.379256+00:00 | 6703.597 s | CLEAN | soak-134 captures | CLEAN |

| soak-135 | 2026-10-06T07:19:34.246160+00:00 | 6753.464 s | CLEAN | soak-135 captures | CLEAN |

| soak-136 | 2026-10-06T07:20:24.206157+00:00 | 6803.424 s | CLEAN | soak-136 captures | CLEAN |

| soak-137 | 2026-10-06T07:21:14.218622+00:00 | 6853.437 s | CLEAN | soak-137 captures | CLEAN |

| soak-138 | 2026-10-06T07:22:04.172394+00:00 | 6903.390 s | CLEAN | soak-138 captures | CLEAN |

| soak-139 | 2026-10-06T07:22:54.202182+00:00 | 6953.420 s | CLEAN | soak-139 captures | CLEAN |

| soak-140 | 2026-10-06T07:23:44.179464+00:00 | 7003.397 s | CLEAN | soak-140 captures | CLEAN |

| soak-141 | 2026-10-06T07:24:34.708156+00:00 | 7053.926 s | CLEAN | soak-141 captures | CLEAN |

| soak-142 | 2026-10-06T07:25:24.806424+00:00 | 7104.024 s | CLEAN | soak-142 captures | CLEAN |

| soak-143 | 2026-10-06T07:26:14.704281+00:00 | 7153.922 s | CLEAN | soak-143 captures | CLEAN |

| soak-144 | 2026-10-06T07:27:04.751870+00:00 | 7203.970 s | CLEAN | soak-144 captures | CLEAN |

| start-001 | 2026-10-06T07:28:32.533132+00:00 | 3.236 s | EARLY 0; LATE 0 | start-001 captures | EARLY 0; LATE 0 |

| start-002 | 2026-10-06T07:28:38.299475+00:00 | 3.234 s | EARLY 0; LATE 0 | start-002 captures | EARLY 0; LATE 0 |

| start-003 | 2026-10-06T07:28:44.062981+00:00 | 3.234 s | EARLY 0; LATE 0 | start-003 captures | EARLY 0; LATE 0 |

| start-004 | 2026-10-06T07:28:49.863971+00:00 | 3.236 s | EARLY 0; LATE 0 | start-004 captures | EARLY 0; LATE 0 |

| start-005 | 2026-10-06T07:28:55.748799+00:00 | 3.236 s | EARLY 0; LATE 0 | start-005 captures | EARLY 0; LATE 0 |

| start-006 | 2026-10-06T07:29:01.583476+00:00 | 3.233 s | EARLY 0; LATE 0 | start-006 captures | EARLY 0; LATE 0 |

| start-007 | 2026-10-06T07:29:07.454407+00:00 | 3.234 s | EARLY 1; LATE 0 | start-007 captures | EARLY 1; LATE 0 |

| start-008 | 2026-10-06T07:29:13.255145+00:00 | 3.232 s | EARLY 0; LATE 0 | start-008 captures | EARLY 0; LATE 0 |

| start-009 | 2026-10-06T07:29:18.989296+00:00 | 3.233 s | EARLY 0; LATE 0 | start-009 captures | EARLY 0; LATE 0 |

| start-010 | 2026-10-06T07:29:24.818240+00:00 | 3.236 s | EARLY 0; LATE 0 | start-010 captures | EARLY 0; LATE 0 |

| start-011 | 2026-10-06T07:29:30.685207+00:00 | 3.233 s | EARLY 0; LATE 0 | start-011 captures | EARLY 0; LATE 0 |

| start-012 | 2026-10-06T07:29:36.418617+00:00 | 3.236 s | EARLY 0; LATE 0 | start-012 captures | EARLY 0; LATE 0 |

| start-013 | 2026-10-06T07:29:42.170998+00:00 | 3.235 s | EARLY 0; LATE 0 | start-013 captures | EARLY 0; LATE 0 |

| start-014 | 2026-10-06T07:29:47.971283+00:00 | 3.233 s | EARLY 0; LATE 0 | start-014 captures | EARLY 0; LATE 0 |

| start-015 | 2026-10-06T07:29:53.739873+00:00 | 3.233 s | EARLY 0; LATE 0 | start-015 captures | EARLY 0; LATE 0 |

| start-016 | 2026-10-06T07:29:59.568108+00:00 | 3.236 s | EARLY 0; LATE 0 | start-016 captures | EARLY 0; LATE 0 |

| start-017 | 2026-10-06T07:30:05.395881+00:00 | 3.234 s | EARLY 0; LATE 0 | start-017 captures | EARLY 0; LATE 0 |

| start-018 | 2026-10-06T07:30:11.158186+00:00 | 3.234 s | EARLY 1; LATE 0 | start-018 captures | EARLY 1; LATE 0 |

| start-019 | 2026-10-06T07:30:16.856279+00:00 | 3.231 s | EARLY 0; LATE 0 | start-019 captures | EARLY 0; LATE 0 |

| start-020 | 2026-10-06T07:30:22.594264+00:00 | 3.233 s | EARLY 0; LATE 0 | start-020 captures | EARLY 0; LATE 0 |

| start-021 | 2026-10-06T07:30:28.334603+00:00 | 3.233 s | EARLY 0; LATE 0 | start-021 captures | EARLY 0; LATE 0 |

| start-022 | 2026-10-06T07:30:34.045157+00:00 | 3.234 s | EARLY 0; LATE 0 | start-022 captures | EARLY 0; LATE 0 |

| start-023 | 2026-10-06T07:30:39.795392+00:00 | 3.232 s | EARLY 0; LATE 0 | start-023 captures | EARLY 0; LATE 0 |

| start-024 | 2026-10-06T07:30:45.552807+00:00 | 3.232 s | EARLY 0; LATE 0 | start-024 captures | EARLY 0; LATE 0 |

| start-025 | 2026-10-06T07:30:51.378169+00:00 | 3.233 s | EARLY 0; LATE 0 | start-025 captures | EARLY 0; LATE 0 |

| start-026 | 2026-10-06T07:30:57.563649+00:00 | 3.234 s | EARLY 0; LATE 0 | start-026 captures | EARLY 0; LATE 0 |

| start-027 | 2026-10-06T07:31:03.376571+00:00 | 3.233 s | EARLY 1; LATE 0 | start-027 captures | EARLY 1; LATE 0 |

| start-028 | 2026-10-06T07:31:09.263405+00:00 | 3.232 s | EARLY 0; LATE 0 | start-028 captures | EARLY 0; LATE 0 |

| start-029 | 2026-10-06T07:31:15.159403+00:00 | 3.233 s | EARLY 0; LATE 0 | start-029 captures | EARLY 0; LATE 0 |

| start-030 | 2026-10-06T07:31:20.939869+00:00 | 3.233 s | EARLY 0; LATE 0 | start-030 captures | EARLY 0; LATE 0 |

| start-031 | 2026-10-06T07:31:26.693000+00:00 | 3.235 s | EARLY 0; LATE 0 | start-031 captures | EARLY 0; LATE 0 |

| start-032 | 2026-10-06T07:31:32.506076+00:00 | 3.233 s | EARLY 1; LATE 0 | start-032 captures | EARLY 1; LATE 0 |

| start-033 | 2026-10-06T07:31:38.265260+00:00 | 3.234 s | EARLY 0; LATE 0 | start-033 captures | EARLY 0; LATE 0 |

| start-034 | 2026-10-06T07:31:44.133102+00:00 | 3.236 s | EARLY 1; LATE 0 | start-034 captures | EARLY 1; LATE 0 |

| start-035 | 2026-10-06T07:31:49.958272+00:00 | 3.236 s | EARLY 0; LATE 0 | start-035 captures | EARLY 0; LATE 0 |

| start-036 | 2026-10-06T07:31:55.810988+00:00 | 3.233 s | EARLY 0; LATE 0 | start-036 captures | EARLY 0; LATE 0 |

| start-037 | 2026-10-06T07:32:01.630805+00:00 | 3.236 s | EARLY 0; LATE 0 | start-037 captures | EARLY 0; LATE 0 |

| start-038 | 2026-10-06T07:32:09.906534+00:00 | 3.232 s | EARLY 0; LATE 0 | start-038 captures | EARLY 0; LATE 0 |

| start-039 | 2026-10-06T07:32:15.786187+00:00 | 3.235 s | EARLY 0; LATE 0 | start-039 captures | EARLY 0; LATE 0 |

| start-040 | 2026-10-06T07:32:21.560984+00:00 | 3.233 s | EARLY 0; LATE 0 | start-040 captures | EARLY 0; LATE 0 |

| start-041 | 2026-10-06T07:32:27.774561+00:00 | 3.234 s | EARLY 0; LATE 0 | start-041 captures | EARLY 0; LATE 0 |

| start-042 | 2026-10-06T07:32:33.704904+00:00 | 3.234 s | EARLY 0; LATE 0 | start-042 captures | EARLY 0; LATE 0 |

| start-043 | 2026-10-06T07:32:40.354565+00:00 | 3.234 s | EARLY 0; LATE 0 | start-043 captures | EARLY 0; LATE 0 |

| start-044 | 2026-10-06T07:32:46.420801+00:00 | 3.237 s | EARLY 0; LATE 0 | start-044 captures | EARLY 0; LATE 0 |

| start-045 | 2026-10-06T07:32:52.370072+00:00 | 3.233 s | EARLY 0; LATE 0 | start-045 captures | EARLY 0; LATE 0 |

| start-046 | 2026-10-06T07:32:58.235518+00:00 | 3.234 s | EARLY 0; LATE 0 | start-046 captures | EARLY 0; LATE 0 |

| start-047 | 2026-10-06T07:33:04.154101+00:00 | 3.232 s | EARLY 0; LATE 0 | start-047 captures | EARLY 0; LATE 0 |

| start-048 | 2026-10-06T07:33:10.135292+00:00 | 3.234 s | EARLY 0; LATE 0 | start-048 captures | EARLY 0; LATE 0 |

| start-049 | 2026-10-06T07:33:16.143815+00:00 | 3.235 s | EARLY 0; LATE 0 | start-049 captures | EARLY 0; LATE 0 |

| start-050 | 2026-10-06T07:33:22.152618+00:00 | 3.235 s | EARLY 0; LATE 0 | start-050 captures | EARLY 0; LATE 0 |

| start-051 | 2026-10-06T07:33:28.150639+00:00 | 3.235 s | EARLY 0; LATE 0 | start-051 captures | EARLY 0; LATE 0 |

| start-052 | 2026-10-06T07:33:34.199068+00:00 | 3.233 s | EARLY 0; LATE 0 | start-052 captures | EARLY 0; LATE 0 |

| start-053 | 2026-10-06T07:33:40.207532+00:00 | 3.235 s | EARLY 0; LATE 0 | start-053 captures | EARLY 0; LATE 0 |

| start-054 | 2026-10-06T07:33:46.246640+00:00 | 3.235 s | EARLY 0; LATE 0 | start-054 captures | EARLY 0; LATE 0 |

| start-055 | 2026-10-06T07:33:52.178545+00:00 | 3.231 s | EARLY 1; LATE 0 | start-055 captures | EARLY 1; LATE 0 |

| start-056 | 2026-10-06T07:33:58.136227+00:00 | 3.235 s | EARLY 0; LATE 0 | start-056 captures | EARLY 0; LATE 0 |

| start-057 | 2026-10-06T07:34:04.104988+00:00 | 3.234 s | EARLY 0; LATE 0 | start-057 captures | EARLY 0; LATE 0 |

| start-058 | 2026-10-06T07:34:10.063798+00:00 | 3.236 s | EARLY 0; LATE 0 | start-058 captures | EARLY 0; LATE 0 |

| start-059 | 2026-10-06T07:34:15.980389+00:00 | 3.232 s | EARLY 1; LATE 0 | start-059 captures | EARLY 1; LATE 0 |

| start-060 | 2026-10-06T07:34:21.961907+00:00 | 3.236 s | EARLY 0; LATE 0 | start-060 captures | EARLY 0; LATE 0 |

| start-061 | 2026-10-06T07:34:27.823230+00:00 | 3.234 s | EARLY 0; LATE 0 | start-061 captures | EARLY 0; LATE 0 |

| start-062 | 2026-10-06T07:34:33.808702+00:00 | 3.232 s | EARLY 0; LATE 0 | start-062 captures | EARLY 0; LATE 0 |

| start-063 | 2026-10-06T07:34:39.710979+00:00 | 3.234 s | EARLY 0; LATE 0 | start-063 captures | EARLY 0; LATE 0 |

| start-064 | 2026-10-06T07:34:45.658838+00:00 | 3.236 s | EARLY 0; LATE 0 | start-064 captures | EARLY 0; LATE 0 |

| start-065 | 2026-10-06T07:34:51.536897+00:00 | 3.236 s | EARLY 1; LATE 0 | start-065 captures | EARLY 1; LATE 0 |

| start-066 | 2026-10-06T07:34:57.447863+00:00 | 3.232 s | EARLY 0; LATE 0 | start-066 captures | EARLY 0; LATE 0 |

| start-067 | 2026-10-06T07:35:03.598340+00:00 | 3.232 s | EARLY 0; LATE 0 | start-067 captures | EARLY 0; LATE 0 |

| start-068 | 2026-10-06T07:35:09.354304+00:00 | 3.232 s | EARLY 0; LATE 0 | start-068 captures | EARLY 0; LATE 0 |

| start-069 | 2026-10-06T07:35:15.206661+00:00 | 3.233 s | EARLY 0; LATE 0 | start-069 captures | EARLY 0; LATE 0 |

| start-070 | 2026-10-06T07:35:21.146871+00:00 | 3.233 s | EARLY 0; LATE 0 | start-070 captures | EARLY 0; LATE 0 |

| start-071 | 2026-10-06T07:35:27.057856+00:00 | 3.235 s | EARLY 1; LATE 0 | start-071 captures | EARLY 1; LATE 0 |

| start-072 | 2026-10-06T07:35:32.951206+00:00 | 3.234 s | EARLY 1; LATE 0 | start-072 captures | EARLY 1; LATE 0 |

| start-073 | 2026-10-06T07:35:38.894863+00:00 | 3.235 s | EARLY 1; LATE 0 | start-073 captures | EARLY 1; LATE 0 |

| start-074 | 2026-10-06T07:35:44.830725+00:00 | 3.232 s | EARLY 0; LATE 0 | start-074 captures | EARLY 0; LATE 0 |

| start-075 | 2026-10-06T07:35:50.695855+00:00 | 3.235 s | EARLY 0; LATE 0 | start-075 captures | EARLY 0; LATE 0 |

| start-076 | 2026-10-06T07:35:56.612531+00:00 | 3.235 s | EARLY 0; LATE 0 | start-076 captures | EARLY 0; LATE 0 |

| start-077 | 2026-10-06T07:36:02.616119+00:00 | 3.232 s | EARLY 0; LATE 0 | start-077 captures | EARLY 0; LATE 0 |

| start-078 | 2026-10-06T07:36:08.533190+00:00 | 3.241 s | EARLY 0; LATE 0 | start-078 captures | EARLY 0; LATE 0 |

| start-079 | 2026-10-06T07:36:14.485098+00:00 | 3.236 s | EARLY 0; LATE 0 | start-079 captures | EARLY 0; LATE 0 |

| start-080 | 2026-10-06T07:36:20.551908+00:00 | 3.234 s | EARLY 1; LATE 0 | start-080 captures | EARLY 1; LATE 0 |

| start-081 | 2026-10-06T07:36:26.492144+00:00 | 3.232 s | EARLY 0; LATE 0 | start-081 captures | EARLY 0; LATE 0 |

| start-082 | 2026-10-06T07:36:32.514155+00:00 | 3.236 s | EARLY 0; LATE 0 | start-082 captures | EARLY 0; LATE 0 |

| start-083 | 2026-10-06T07:36:38.508887+00:00 | 3.236 s | EARLY 0; LATE 0 | start-083 captures | EARLY 0; LATE 0 |

| start-084 | 2026-10-06T07:36:44.403419+00:00 | 3.233 s | EARLY 0; LATE 0 | start-084 captures | EARLY 0; LATE 0 |

| start-085 | 2026-10-06T07:36:50.274620+00:00 | 3.235 s | EARLY 0; LATE 0 | start-085 captures | EARLY 0; LATE 0 |

| start-086 | 2026-10-06T07:36:56.245542+00:00 | 3.234 s | EARLY 0; LATE 0 | start-086 captures | EARLY 0; LATE 0 |

| start-087 | 2026-10-06T07:37:02.114723+00:00 | 3.233 s | EARLY 0; LATE 0 | start-087 captures | EARLY 0; LATE 0 |

| start-088 | 2026-10-06T07:37:07.959588+00:00 | 3.232 s | EARLY 0; LATE 0 | start-088 captures | EARLY 0; LATE 0 |

| start-089 | 2026-10-06T07:37:13.863325+00:00 | 3.234 s | EARLY 0; LATE 0 | start-089 captures | EARLY 0; LATE 0 |

| start-090 | 2026-10-06T07:37:19.745427+00:00 | 3.234 s | EARLY 0; LATE 0 | start-090 captures | EARLY 0; LATE 0 |

| start-091 | 2026-10-06T07:37:25.557253+00:00 | 3.233 s | EARLY 0; LATE 0 | start-091 captures | EARLY 0; LATE 0 |

| start-092 | 2026-10-06T07:37:31.428090+00:00 | 3.233 s | EARLY 0; LATE 0 | start-092 captures | EARLY 0; LATE 0 |

| start-093 | 2026-10-06T07:37:37.255810+00:00 | 3.235 s | EARLY 0; LATE 0 | start-093 captures | EARLY 0; LATE 0 |

| start-094 | 2026-10-06T07:37:43.151914+00:00 | 3.234 s | EARLY 0; LATE 0 | start-094 captures | EARLY 0; LATE 0 |

| start-095 | 2026-10-06T07:37:50.168151+00:00 | 4.250 s | EARLY 1; LATE 0 | start-095 captures | EARLY 1; LATE 0 |

| start-096 | 2026-10-06T07:37:56.104841+00:00 | 3.234 s | EARLY 0; LATE 0 | start-096 captures | EARLY 0; LATE 0 |

| start-097 | 2026-10-06T07:38:02.102289+00:00 | 3.233 s | EARLY 0; LATE 0 | start-097 captures | EARLY 0; LATE 0 |

| start-098 | 2026-10-06T07:38:08.044711+00:00 | 3.233 s | EARLY 1; LATE 0 | start-098 captures | EARLY 1; LATE 0 |

| start-099 | 2026-10-06T07:38:13.954057+00:00 | 3.234 s | EARLY 0; LATE 0 | start-099 captures | EARLY 0; LATE 0 |

| start-100 | 2026-10-06T07:38:19.825504+00:00 | 3.235 s | EARLY 0; LATE 0 | start-100 captures | EARLY 0; LATE 0 |

## Restoration

The four soak bindings were released successfully.
The as-found inventory is saved in `restore-start.jsonl`.
The saved source selection was restored through the documented source-release sequence.
All 42 effective-state observations and both inventories match between phases.
Final readback matches the saved effective state.
NVM sequence is 233, with three successful commits and no failures.
Both sessions deregistered successfully. No capture or probe remains active.

## Artifacts

Bounded receipts belong in this packet.
Large captures and build products remain outside it under `/tmp`.
Locations, sizes and SHA-256 values will accompany retained artifacts.

TAKEN: https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6009853122

The earlier controller build was absent. Pinned source is staged under `/tmp/667-b13`.
Host prerequisites and the read-only board shell check passed.

The controller build and probe compile returned zero.
DUT ENTITY counters return NOT_SUPPORTED; the remaining six descriptors return SUCCESS.
Both DUT AAF and CRF streams are exposed in both directions.

## Final result

The soak completed 7203.971 seconds across 145 clean checkpoints.
Fourteen of 100 startup binds recorded EARLY=1; all LATE counts were zero.
Those fourteen starts had backward first timestamp steps.
The signed steps range from -544469385 to -279759747 ns.
All 1000 initial headers have tv=1 and tu=0.
Absolute gPTP correlation is NOT RUN.
Nine segment-local soak gaps are recovered by overlapping captures.
One soak capture receipt lacks its drop statistic.

The final state comparison passed all 44 rows.
The servo and audio readbacks match the saved bytes.
NVM sequence advanced from 230 to 233, with three successful commits.
Dirty, stale and failed-commit values remain zero.
Both sessions deregistered. All capture and probe processes exited.
The bench lock was checked free.

`validation.json` records all seven successful gates at the local head.
`startup-first-ten.csv` retains every requested initial header.
`startup-counter-timing.csv` bounds each flagged observation before unbind.
`capture-artifacts.jsonl` lists 735 retained captures with sizes and hashes.
`retained-artifacts.jsonl` lists the remaining raw receipts and build products.
`build-inputs.json` records the pinned source inputs.
All packet files are below 200000 bytes.

REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6011787816

Soak times are elapsed since all four binds completed.
Startup action times include the post-unbind wait.
Each requested hold was 2000 ms.
Measured bind-response to unbind-command intervals were 2002.714-2004.055 ms.
