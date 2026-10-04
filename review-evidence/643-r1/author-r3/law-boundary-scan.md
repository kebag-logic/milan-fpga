# #643 round 2, item 1: the boundary-band scan

Measured with the round-2 harness's `--law-boundary` leg (window 8 cycles), GNU make 4.3 and the pinned Verilator 5.050, before the walk statistic excluded the snap end, whose earlier pops prefill held. The walks below are recomputed from the logged histograms with the snap end's entry removed where it sits a tick away; where it sits inside the cluster it stays in, so these walks can only overstate the final harness's. The instrument (pop take cycles, PDU ends, fills) and the 8-cycle window are the final ones.

| Processor | History | Phases | Not gradable | Graded pass | Graded fail | Max walk | Walk: phases |
|---|---|---:|---|---:|---:|---:|---|
| dev's pin `631eeb34` (the lane) | ascending | 81 | +2017..+2034 (18) | 63 | 0 | 2 | 0: 1, 1: 63, 2: 17 |
| dev's pin `631eeb34` (the lane) | descending | 81 | +2017..+2034 (18) | 63 | 0 | 3 | 0: 2, 1: 60, 2: 17, 3: 2 |
| dev's pin `631eeb34` (the lane) | alone | 81 | +2016..+2036 (21) | 60 | 0 | 3 | 3: 81 |
| processor `c4cb84ff` (scratch parent, both patches) | ascending | 81 | +2017..+2034 (18) | 63 | 0 | 2 | 0: 1, 1: 63, 2: 17 |
| processor `c4cb84ff` (scratch parent, both patches) | descending | 81 | +2017..+2034 (18) | 63 | 0 | 3 | 0: 2, 1: 60, 2: 17, 3: 2 |
| processor `c4cb84ff` (scratch parent, both patches) | alone | 81 | +2016..+2036 (21) | 60 | 0 | 3 | 3: 81 |

## dev's pin `631eeb34` (the lane)

Per history: the steady PDU ends per nearest-pop offset (taken minus the end beat's cycle; `(snap +n)` is the snap end's next pop, a tick away because prefill held the one before), the walk over the steady ends, the least clearance over every end (the snap included), and the outcome against the 8-cycle window (fill read where graded).

| Phase | Ascending (the leg's own scan) | walk | clear | outcome | Descending | walk | clear | outcome | Alone | walk | clear | outcome |
|---:|---|---:|---:|---|---|---:|---:|---|---|---:|---:|---|
| +1986 | +40:55 +41:79 +42:4 | 2 | 39 | pass, fill 14 | +40:102 +41:36 | 1 | 39 | pass, fill 14 | +39:9 +40:75 +41:53 +42:1 | 3 | 38 | pass, fill 14 |
| +1987 | +38:11 +39:88 +40:39 | 2 | 37 | pass, fill 14 | +39:120 +40:18 | 1 | 38 | pass, fill 14 | +38:9 +39:75 +40:53 +41:1 | 3 | 37 | pass, fill 14 |
| +1988 | +38:53 +39:81 +40:4 | 2 | 37 | pass, fill 14 | +38:134 +39:4 | 1 | 37 | pass, fill 14 | +37:9 +38:75 +39:53 +40:1 | 3 | 36 | pass, fill 14 |
| +1989 | +36:17 +37:94 +38:27 | 2 | 35 | pass, fill 14 | +37:138 | 0 | 36 | pass, fill 14 | +36:9 +37:75 +38:53 +39:1 | 3 | 35 | pass, fill 14 |
| +1990 | +35:1 +36:80 +37:57 | 2 | 34 | pass, fill 14 | +35:7 +36:131 | 1 | 34 | pass, fill 14 | +35:9 +36:75 +37:53 +38:1 | 3 | 34 | pass, fill 14 |
| +1991 | +35:51 +36:86 +37:1 | 2 | 34 | pass, fill 14 | +34:11 +35:127 | 1 | 33 | pass, fill 14 | +34:9 +35:75 +36:53 +37:1 | 3 | 33 | pass, fill 14 |
| +1992 | +34:34 +35:99 +36:5 | 2 | 33 | pass, fill 14 | +33:18 +34:120 | 1 | 32 | pass, fill 14 | +33:9 +34:75 +35:53 +36:1 | 3 | 32 | pass, fill 14 |
| +1993 | +32:23 +33:106 +34:9 | 2 | 31 | pass, fill 14 | +32:22 +33:116 | 1 | 31 | pass, fill 14 | +32:9 +33:75 +34:53 +35:1 | 3 | 31 | pass, fill 14 |
| +1994 | +31:21 +32:107 +33:10 | 2 | 30 | pass, fill 14 | +31:27 +32:111 | 1 | 30 | pass, fill 14 | +31:9 +32:75 +33:53 +34:1 | 3 | 30 | pass, fill 14 |
| +1995 | +30:21 +31:110 +32:7 | 2 | 29 | pass, fill 14 | +30:35 +31:103 | 1 | 29 | pass, fill 14 | +30:9 +31:75 +32:53 +33:1 | 3 | 29 | pass, fill 14 |
| +1996 | +29:28 +30:107 +31:3 | 2 | 28 | pass, fill 14 | +29:40 +30:98 | 1 | 28 | pass, fill 14 | +29:9 +30:75 +31:53 +32:1 | 3 | 28 | pass, fill 14 |
| +1997 | +29:43 +30:95 | 1 | 28 | pass, fill 14 | +28:46 +29:92 | 1 | 27 | pass, fill 14 | +28:9 +29:75 +30:53 +31:1 | 3 | 27 | pass, fill 14 |
| +1998 | +28:68 +29:70 | 1 | 27 | pass, fill 14 | +27:56 +28:82 | 1 | 26 | pass, fill 14 | +27:9 +28:75 +29:53 +30:1 | 3 | 26 | pass, fill 14 |
| +1999 | +27:101 +28:37 | 1 | 26 | pass, fill 14 | +26:65 +27:73 | 1 | 25 | pass, fill 14 | +26:9 +27:75 +28:53 +29:1 | 3 | 25 | pass, fill 14 |
| +2000 | +25:10 +26:119 +27:9 | 2 | 24 | pass, fill 14 | +25:75 +26:63 | 1 | 24 | pass, fill 14 | +25:9 +26:75 +27:53 +28:1 | 3 | 24 | pass, fill 14 |
| +2001 | +24:46 +25:92 | 1 | 23 | pass, fill 14 | +25:92 +26:46 | 1 | 24 | pass, fill 14 | +24:9 +25:75 +26:53 +27:1 | 3 | 23 | pass, fill 14 |
| +2002 | +24:96 +25:42 | 1 | 23 | pass, fill 14 | +24:109 +25:29 | 1 | 23 | pass, fill 14 | +23:9 +24:75 +25:53 +26:1 | 3 | 22 | pass, fill 14 |
| +2003 | +22:15 +23:120 +24:3 | 2 | 21 | pass, fill 14 | +23:117 +24:21 | 1 | 22 | pass, fill 14 | +22:9 +23:75 +24:53 +25:1 | 3 | 21 | pass, fill 14 |
| +2004 | +22:70 +23:68 | 1 | 21 | pass, fill 14 | +22:120 +23:18 | 1 | 21 | pass, fill 14 | +21:9 +22:75 +23:53 +24:1 | 3 | 20 | pass, fill 14 |
| +2005 | +20:4 +21:126 +22:8 | 2 | 19 | pass, fill 14 | +21:129 +22:9 | 1 | 20 | pass, fill 14 | +20:9 +21:75 +22:53 +23:1 | 3 | 19 | pass, fill 14 |
| +2006 | +20:66 +21:72 | 1 | 19 | pass, fill 14 | +20:138 | 0 | 19 | pass, fill 14 | +19:9 +20:75 +21:53 +22:1 | 3 | 18 | pass, fill 14 |
| +2007 | +18:5 +19:126 +20:7 | 2 | 17 | pass, fill 14 | +18:9 +19:129 | 1 | 17 | pass, fill 14 | +18:9 +19:75 +20:53 +21:1 | 3 | 17 | pass, fill 14 |
| +2008 | +18:76 +19:62 | 1 | 17 | pass, fill 14 | +17:19 +18:119 | 1 | 16 | pass, fill 14 | +17:9 +18:75 +19:53 +20:1 | 3 | 16 | pass, fill 14 |
| +2009 | +16:16 +17:122 | 1 | 15 | pass, fill 14 | +16:38 +17:100 | 1 | 15 | pass, fill 14 | +16:9 +17:75 +18:53 +19:1 | 3 | 15 | pass, fill 14 |
| +2010 | +16:99 +17:39 | 1 | 15 | pass, fill 14 | +15:52 +16:86 | 1 | 14 | pass, fill 14 | +15:9 +16:75 +17:53 +18:1 | 3 | 14 | pass, fill 14 |
| +2011 | +14:46 +15:92 | 1 | 13 | pass, fill 14 | +14:59 +15:79 | 1 | 13 | pass, fill 14 | +14:9 +15:75 +16:53 +17:1 | 3 | 13 | pass, fill 14 |
| +2012 | +13:2 +14:129 +15:7 | 2 | 12 | pass, fill 14 | +13:75 +14:63 | 1 | 12 | pass, fill 14 | +13:9 +14:75 +15:53 +16:1 | 3 | 12 | pass, fill 14 |
| +2013 | +13:87 +14:51 | 1 | 12 | pass, fill 14 | +13:84 +14:54 | 1 | 12 | pass, fill 14 | +12:9 +13:75 +14:53 +15:1 | 3 | 11 | pass, fill 14 |
| +2014 | +11:41 +12:97 | 1 | 10 | pass, fill 14 | +12:102 +13:36 | 1 | 11 | pass, fill 14 | +11:9 +12:75 +13:53 +14:1 | 3 | 10 | pass, fill 14 |
| +2015 | +10:3 +11:132 +12:3 | 2 | 9 | pass, fill 14 | +11:120 +12:18 | 1 | 10 | pass, fill 14 | +10:9 +11:75 +12:53 +13:1 | 3 | 9 | pass, fill 14 |
| +2016 | +10:100 +11:38 | 1 | 9 | pass, fill 14 | +10:129 +11:9 | 1 | 9 | pass, fill 14 | +9:9 +10:75 +11:53 +12:1 | 3 | 8 | not gradable |
| +2017 | +8:62 +9:76 | 1 | 7 | not gradable | +8:3 +9:135 | 1 | 7 | not gradable | +8:9 +9:75 +10:53 +11:1 | 3 | 7 | not gradable |
| +2018 | +7:25 +8:113 | 1 | 6 | not gradable | +7:24 +8:114 | 1 | 6 | not gradable | +7:9 +8:75 +9:53 +10:1 | 3 | 6 | not gradable |
| +2019 | +7:129 +8:9 | 1 | 6 | not gradable | +6:37 +7:101 | 1 | 5 | not gradable | +6:9 +7:75 +8:53 +9:1 | 3 | 5 | not gradable |
| +2020 | +6:98 +7:40 | 1 | 5 | not gradable | +5:56 +6:82 | 1 | 4 | not gradable | +5:9 +6:75 +7:53 +8:1 | 3 | 4 | not gradable |
| +2021 | +4:69 +5:69 | 1 | 3 | not gradable | +5:80 +6:58 | 1 | 4 | not gradable | +4:9 +5:75 +6:53 +7:1 | 3 | 3 | not gradable |
| +2022 | +3:37 +4:101 | 1 | 2 | not gradable | +4:102 +5:36 | 1 | 3 | not gradable | +3:9 +4:75 +5:53 +6:1 | 3 | 2 | not gradable |
| +2023 | +2:9 +3:129 | 1 | 1 | not gradable | +3:117 +4:21 | 1 | 2 | not gradable | +2:9 +3:75 +4:53 +5:1 | 3 | 1 | not gradable |
| +2024 | +2:121 +3:17 | 1 | 1 | not gradable | +1:3 +2:135 | 1 | 0 | not gradable | +1:9 +2:75 +3:53 +4:1 | 3 | 0 | not gradable |
| +2025 | +1:98 +2:40 | 1 | 0 | not gradable | +0:22 +1:116 | 1 | 0 | not gradable | +0:8 +1:75 +2:53 +3:1 (snap +2084) | 3 | 0 | not gradable |
| +2026 | -1:72 +0:65 (snap +2083) | 1 | 0 | not gradable | -1:49 +0:88 (snap +2083) | 1 | 0 | not gradable | -1:8 +0:75 +1:53 +2:1 (snap +2083) | 3 | 0 | not gradable |
| +2027 | -2:52 -1:85 (snap +2082) | 1 | 1 | not gradable | -2:70 -1:67 (snap +2082) | 1 | 1 | not gradable | -2:8 -1:75 +0:53 +1:1 (snap +2082) | 3 | 0 | not gradable |
| +2028 | -3:27 -2:110 (snap +2081) | 1 | 2 | not gradable | -2:98 -1:39 (snap +2081) | 1 | 1 | not gradable | -3:8 -2:75 -1:53 +0:1 (snap +2081) | 3 | 0 | not gradable |
| +2029 | -4:9 -3:128 (snap +2080) | 1 | 3 | not gradable | -3:124 -2:13 (snap +2080) | 1 | 2 | not gradable | -4:8 -3:75 -2:53 -1:1 (snap +2080) | 3 | 1 | not gradable |
| +2030 | -4:128 -3:9 (snap +2079) | 1 | 3 | not gradable | -5:18 -4:119 (snap +2079) | 1 | 4 | not gradable | -5:8 -4:75 -3:53 -2:1 (snap +2079) | 3 | 2 | not gradable |
| +2031 | -5:105 -4:32 (snap +2078) | 1 | 4 | not gradable | -6:48 -5:89 (snap +2078) | 1 | 5 | not gradable | -6:8 -5:75 -4:53 -3:1 (snap +2078) | 3 | 3 | not gradable |
| +2032 | -6:92 -5:45 (snap +2077) | 1 | 5 | not gradable | -6:80 -5:57 (snap +2077) | 1 | 5 | not gradable | -7:8 -6:75 -5:53 -4:1 (snap +2077) | 3 | 4 | not gradable |
| +2033 | -8:73 -7:64 (snap +2076) | 1 | 7 | not gradable | -7:113 -6:24 (snap +2076) | 1 | 6 | not gradable | -8:8 -7:75 -6:53 -5:1 (snap +2076) | 3 | 5 | not gradable |
| +2034 | -9:55 -8:82 (snap +2075) | 1 | 8 | not gradable | -9:10 -8:127 (snap +2075) | 1 | 8 | not gradable | -9:8 -8:75 -7:53 -6:1 (snap +2075) | 3 | 6 | not gradable |
| +2035 | -10:36 -9:101 (snap +2074) | 1 | 9 | pass, fill 14 | -10:49 -9:88 (snap +2074) | 1 | 9 | pass, fill 14 | -10:8 -9:75 -8:53 -7:1 (snap +2074) | 3 | 7 | not gradable |
| +2036 | -11:27 -10:110 (snap +2073) | 1 | 10 | pass, fill 14 | -10:90 -9:47 (snap +2073) | 1 | 9 | pass, fill 14 | -11:8 -10:75 -9:53 -8:1 (snap +2073) | 3 | 8 | not gradable |
| +2037 | -12:11 -11:126 (snap +2072) | 1 | 11 | pass, fill 14 | -12:1 -11:128 -10:8 (snap +2072) | 2 | 10 | pass, fill 14 | -12:8 -11:75 -10:53 -9:1 (snap +2072) | 3 | 9 | pass, fill 14 |
| +2038 | -12:128 -11:9 (snap +2071) | 1 | 11 | pass, fill 14 | -13:36 -12:101 (snap +2071) | 1 | 12 | pass, fill 14 | -13:8 -12:75 -11:53 -10:1 (snap +2071) | 3 | 10 | pass, fill 14 |
| +2039 | -13:119 -12:18 (snap +2070) | 1 | 12 | pass, fill 14 | -13:84 -12:53 (snap +2070) | 1 | 12 | pass, fill 14 | -14:8 -13:75 -12:53 -11:1 (snap +2070) | 3 | 11 | pass, fill 14 |
| +2040 | -14:110 -13:27 (snap +2069) | 1 | 13 | pass, fill 14 | -15:3 -14:127 -13:7 (snap +2069) | 2 | 13 | pass, fill 14 | -15:8 -14:75 -13:53 -12:1 (snap +2069) | 3 | 12 | pass, fill 14 |
| +2041 | -15:101 -14:36 (snap +2068) | 1 | 14 | pass, fill 14 | -16:48 -15:89 (snap +2068) | 1 | 15 | pass, fill 14 | -16:8 -15:75 -14:53 -13:1 (snap +2068) | 3 | 13 | pass, fill 14 |
| +2042 | -16:88 -15:49 (snap +2067) | 1 | 15 | pass, fill 14 | -16:104 -15:33 (snap +2067) | 1 | 15 | pass, fill 14 | -17:8 -16:75 -15:53 -14:1 (snap +2067) | 3 | 14 | pass, fill 14 |
| +2043 | -18:74 -17:63 (snap +2066) | 1 | 17 | pass, fill 14 | -18:25 -17:112 (snap +2066) | 1 | 17 | pass, fill 14 | -18:8 -17:75 -16:53 -15:1 (snap +2066) | 3 | 15 | pass, fill 14 |
| +2044 | -19:55 -18:82 (snap +2065) | 1 | 18 | pass, fill 14 | -18:87 -17:50 (snap +2065) | 1 | 17 | pass, fill 14 | -19:8 -18:75 -17:53 -16:1 (snap +2065) | 3 | 16 | pass, fill 14 |
| +2045 | -20:45 -19:92 (snap +2064) | 1 | 19 | pass, fill 14 | -20:15 -19:121 -18:1 (snap +2064) | 2 | 18 | pass, fill 14 | -20:8 -19:75 -18:53 -17:1 (snap +2064) | 3 | 17 | pass, fill 14 |
| +2046 | -21:38 -20:99 (snap +2063) | 1 | 20 | pass, fill 14 | -20:86 -19:51 (snap +2063) | 1 | 19 | pass, fill 14 | -21:8 -20:75 -19:53 -18:1 (snap +2063) | 3 | 18 | pass, fill 14 |
| +2047 | -22:34 -21:103 (snap +2062) | 1 | 21 | pass, fill 14 | -22:22 -21:114 -20:1 (snap +2062) | 2 | 20 | pass, fill 14 | -22:8 -21:75 -20:53 -19:1 (snap +2062) | 3 | 19 | pass, fill 14 |
| +2048 | -23:27 -22:110 (snap +2061) | 1 | 22 | pass, fill 14 | -22:101 -21:36 (snap +2061) | 1 | 21 | pass, fill 14 | -23:8 -22:75 -21:53 -20:1 (snap +2061) | 3 | 20 | pass, fill 14 |
| +2049 | -24:18 -23:119 (snap +2060) | 1 | 23 | pass, fill 14 | -24:45 -23:92 (snap +2060) | 1 | 23 | pass, fill 14 | -24:8 -23:75 -22:53 -21:1 (snap +2060) | 3 | 21 | pass, fill 14 |
| +2050 | +2059:1 (snap -24) | 0 | 24 | pass, fill 14 | -25:7 -24:119 -23:11 (snap +2059) | 2 | 23 | pass, fill 14 | -25:8 -24:75 -23:53 -22:1 (snap +2059) | 3 | 22 | pass, fill 14 |
| +2051 | -25:119 -24:18 (snap +2058) | 1 | 24 | pass, fill 14 | -25:90 -24:47 (snap +2058) | 1 | 24 | pass, fill 14 | -26:8 -25:75 -24:53 -23:1 (snap +2058) | 3 | 23 | pass, fill 14 |
| +2052 | -26:110 -25:27 (snap +2057) | 1 | 25 | pass, fill 14 | -26:52 -25:85 (snap +2057) | 1 | 25 | pass, fill 14 | -27:8 -26:75 -25:53 -24:1 (snap +2057) | 3 | 24 | pass, fill 14 |
| +2053 | -27:101 -26:36 (snap +2056) | 1 | 26 | pass, fill 14 | -28:22 -27:112 -26:3 (snap +2056) | 2 | 26 | pass, fill 14 | -28:8 -27:75 -26:53 -25:1 (snap +2056) | 3 | 25 | pass, fill 14 |
| +2054 | -28:96 -27:41 (snap +2055) | 1 | 27 | pass, fill 14 | -29:8 -28:114 -27:15 (snap +2055) | 2 | 27 | pass, fill 14 | -29:8 -28:75 -27:53 -26:1 (snap +2055) | 3 | 26 | pass, fill 14 |
| +2055 | -29:91 -28:46 (snap +2054) | 1 | 28 | pass, fill 14 | -30:3 -29:106 -28:28 (snap +2054) | 2 | 28 | pass, fill 14 | -30:8 -29:75 -28:53 -27:1 (snap +2054) | 3 | 27 | pass, fill 14 |
| +2056 | -31:83 -30:54 (snap +2053) | 1 | 30 | pass, fill 14 | -31:1 -30:98 -29:38 (snap +2053) | 2 | 29 | pass, fill 14 | -31:8 -30:75 -29:53 -28:1 (snap +2053) | 3 | 28 | pass, fill 14 |
| +2057 | -32:77 -31:60 (snap +2052) | 1 | 31 | pass, fill 14 | -32:1 -31:94 -30:42 (snap +2052) | 2 | 30 | pass, fill 14 | -32:8 -31:75 -30:53 -29:1 (snap +2052) | 3 | 29 | pass, fill 14 |
| +2058 | -33:73 -32:64 (snap +2051) | 1 | 32 | pass, fill 14 | -33:3 -32:96 -31:38 (snap +2051) | 2 | 31 | pass, fill 14 | -33:8 -32:75 -31:53 -30:1 (snap +2051) | 3 | 30 | pass, fill 14 |
| +2059 | -34:65 -33:72 (snap +2050) | 1 | 33 | pass, fill 14 | -34:7 -33:100 -32:30 (snap +2050) | 2 | 32 | pass, fill 14 | -34:8 -33:75 -32:53 -31:1 (snap +2050) | 3 | 31 | pass, fill 14 |
| +2060 | -35:61 -34:76 (snap +2049) | 1 | 34 | pass, fill 14 | -35:18 -34:102 -33:17 (snap +2049) | 2 | 33 | pass, fill 14 | -35:8 -34:75 -33:53 -32:1 (snap +2049) | 3 | 32 | pass, fill 14 |
| +2061 | -36:55 -35:82 (snap +2048) | 1 | 35 | pass, fill 14 | -35:39 -34:93 -33:5 (snap +2048) | 2 | 33 | pass, fill 14 | -36:8 -35:75 -34:53 -33:1 (snap +2048) | 3 | 33 | pass, fill 14 |
| +2062 | -37:49 -36:88 (snap +2047) | 1 | 36 | pass, fill 14 | -37:1 -36:73 -35:63 (snap +2047) | 2 | 35 | pass, fill 14 | -37:8 -36:75 -35:53 -34:1 (snap +2047) | 3 | 34 | pass, fill 14 |
| +2063 | -38:45 -37:92 (snap +2046) | 1 | 37 | pass, fill 14 | -38:18 -37:92 -36:27 (snap +2046) | 2 | 36 | pass, fill 14 | -38:8 -37:75 -36:53 -35:1 (snap +2046) | 3 | 35 | pass, fill 14 |
| +2064 | -39:27 -38:110 (snap +2045) | 1 | 38 | pass, fill 14 | -39:1 -38:54 -37:78 -36:4 (snap +2045) | 3 | 36 | pass, fill 14 | -39:8 -38:75 -37:53 -36:1 (snap +2045) | 3 | 36 | pass, fill 14 |
| +2065 | -40:18 -39:119 (snap +2044) | 1 | 39 | pass, fill 14 | -39:25 -38:85 -37:27 (snap +2044) | 2 | 37 | pass, fill 14 | -40:8 -39:75 -38:53 -37:1 (snap +2044) | 3 | 37 | pass, fill 14 |
| +2066 | -41:7 -40:130 (snap +2043) | 1 | 40 | pass, fill 14 | -41:8 -40:75 -39:53 -38:1 (snap +2043) | 3 | 38 | pass, fill 14 | -41:8 -40:75 -39:53 -38:1 (snap +2043) | 3 | 38 | pass, fill 14 |

## processor `c4cb84ff` (scratch parent, both patches)

Per history: the steady PDU ends per nearest-pop offset (taken minus the end beat's cycle; `(snap +n)` is the snap end's next pop, a tick away because prefill held the one before), the walk over the steady ends, the least clearance over every end (the snap included), and the outcome against the 8-cycle window (fill read where graded).

| Phase | Ascending (the leg's own scan) | walk | clear | outcome | Descending | walk | clear | outcome | Alone | walk | clear | outcome |
|---:|---|---:|---:|---|---|---:|---:|---|---|---:|---:|---|
| +1986 | +40:55 +41:79 +42:4 | 2 | 39 | pass, fill 14 | +40:102 +41:36 | 1 | 39 | pass, fill 14 | +39:9 +40:75 +41:53 +42:1 | 3 | 38 | pass, fill 14 |
| +1987 | +38:11 +39:88 +40:39 | 2 | 37 | pass, fill 14 | +39:120 +40:18 | 1 | 38 | pass, fill 14 | +38:9 +39:75 +40:53 +41:1 | 3 | 37 | pass, fill 14 |
| +1988 | +38:53 +39:81 +40:4 | 2 | 37 | pass, fill 14 | +38:134 +39:4 | 1 | 37 | pass, fill 14 | +37:9 +38:75 +39:53 +40:1 | 3 | 36 | pass, fill 14 |
| +1989 | +36:17 +37:94 +38:27 | 2 | 35 | pass, fill 14 | +37:138 | 0 | 36 | pass, fill 14 | +36:9 +37:75 +38:53 +39:1 | 3 | 35 | pass, fill 14 |
| +1990 | +35:1 +36:80 +37:57 | 2 | 34 | pass, fill 14 | +35:7 +36:131 | 1 | 34 | pass, fill 14 | +35:9 +36:75 +37:53 +38:1 | 3 | 34 | pass, fill 14 |
| +1991 | +35:51 +36:86 +37:1 | 2 | 34 | pass, fill 14 | +34:11 +35:127 | 1 | 33 | pass, fill 14 | +34:9 +35:75 +36:53 +37:1 | 3 | 33 | pass, fill 14 |
| +1992 | +34:34 +35:99 +36:5 | 2 | 33 | pass, fill 14 | +33:18 +34:120 | 1 | 32 | pass, fill 14 | +33:9 +34:75 +35:53 +36:1 | 3 | 32 | pass, fill 14 |
| +1993 | +32:23 +33:106 +34:9 | 2 | 31 | pass, fill 14 | +32:22 +33:116 | 1 | 31 | pass, fill 14 | +32:9 +33:75 +34:53 +35:1 | 3 | 31 | pass, fill 14 |
| +1994 | +31:21 +32:107 +33:10 | 2 | 30 | pass, fill 14 | +31:27 +32:111 | 1 | 30 | pass, fill 14 | +31:9 +32:75 +33:53 +34:1 | 3 | 30 | pass, fill 14 |
| +1995 | +30:21 +31:110 +32:7 | 2 | 29 | pass, fill 14 | +30:35 +31:103 | 1 | 29 | pass, fill 14 | +30:9 +31:75 +32:53 +33:1 | 3 | 29 | pass, fill 14 |
| +1996 | +29:28 +30:107 +31:3 | 2 | 28 | pass, fill 14 | +29:40 +30:98 | 1 | 28 | pass, fill 14 | +29:9 +30:75 +31:53 +32:1 | 3 | 28 | pass, fill 14 |
| +1997 | +29:43 +30:95 | 1 | 28 | pass, fill 14 | +28:46 +29:92 | 1 | 27 | pass, fill 14 | +28:9 +29:75 +30:53 +31:1 | 3 | 27 | pass, fill 14 |
| +1998 | +28:68 +29:70 | 1 | 27 | pass, fill 14 | +27:56 +28:82 | 1 | 26 | pass, fill 14 | +27:9 +28:75 +29:53 +30:1 | 3 | 26 | pass, fill 14 |
| +1999 | +27:101 +28:37 | 1 | 26 | pass, fill 14 | +26:65 +27:73 | 1 | 25 | pass, fill 14 | +26:9 +27:75 +28:53 +29:1 | 3 | 25 | pass, fill 14 |
| +2000 | +25:10 +26:119 +27:9 | 2 | 24 | pass, fill 14 | +25:75 +26:63 | 1 | 24 | pass, fill 14 | +25:9 +26:75 +27:53 +28:1 | 3 | 24 | pass, fill 14 |
| +2001 | +24:46 +25:92 | 1 | 23 | pass, fill 14 | +25:92 +26:46 | 1 | 24 | pass, fill 14 | +24:9 +25:75 +26:53 +27:1 | 3 | 23 | pass, fill 14 |
| +2002 | +24:96 +25:42 | 1 | 23 | pass, fill 14 | +24:109 +25:29 | 1 | 23 | pass, fill 14 | +23:9 +24:75 +25:53 +26:1 | 3 | 22 | pass, fill 14 |
| +2003 | +22:15 +23:120 +24:3 | 2 | 21 | pass, fill 14 | +23:117 +24:21 | 1 | 22 | pass, fill 14 | +22:9 +23:75 +24:53 +25:1 | 3 | 21 | pass, fill 14 |
| +2004 | +22:70 +23:68 | 1 | 21 | pass, fill 14 | +22:120 +23:18 | 1 | 21 | pass, fill 14 | +21:9 +22:75 +23:53 +24:1 | 3 | 20 | pass, fill 14 |
| +2005 | +20:4 +21:126 +22:8 | 2 | 19 | pass, fill 14 | +21:129 +22:9 | 1 | 20 | pass, fill 14 | +20:9 +21:75 +22:53 +23:1 | 3 | 19 | pass, fill 14 |
| +2006 | +20:66 +21:72 | 1 | 19 | pass, fill 14 | +20:138 | 0 | 19 | pass, fill 14 | +19:9 +20:75 +21:53 +22:1 | 3 | 18 | pass, fill 14 |
| +2007 | +18:5 +19:126 +20:7 | 2 | 17 | pass, fill 14 | +18:9 +19:129 | 1 | 17 | pass, fill 14 | +18:9 +19:75 +20:53 +21:1 | 3 | 17 | pass, fill 14 |
| +2008 | +18:76 +19:62 | 1 | 17 | pass, fill 14 | +17:19 +18:119 | 1 | 16 | pass, fill 14 | +17:9 +18:75 +19:53 +20:1 | 3 | 16 | pass, fill 14 |
| +2009 | +16:16 +17:122 | 1 | 15 | pass, fill 14 | +16:38 +17:100 | 1 | 15 | pass, fill 14 | +16:9 +17:75 +18:53 +19:1 | 3 | 15 | pass, fill 14 |
| +2010 | +16:99 +17:39 | 1 | 15 | pass, fill 14 | +15:52 +16:86 | 1 | 14 | pass, fill 14 | +15:9 +16:75 +17:53 +18:1 | 3 | 14 | pass, fill 14 |
| +2011 | +14:46 +15:92 | 1 | 13 | pass, fill 14 | +14:59 +15:79 | 1 | 13 | pass, fill 14 | +14:9 +15:75 +16:53 +17:1 | 3 | 13 | pass, fill 14 |
| +2012 | +13:2 +14:129 +15:7 | 2 | 12 | pass, fill 14 | +13:75 +14:63 | 1 | 12 | pass, fill 14 | +13:9 +14:75 +15:53 +16:1 | 3 | 12 | pass, fill 14 |
| +2013 | +13:87 +14:51 | 1 | 12 | pass, fill 14 | +13:84 +14:54 | 1 | 12 | pass, fill 14 | +12:9 +13:75 +14:53 +15:1 | 3 | 11 | pass, fill 14 |
| +2014 | +11:41 +12:97 | 1 | 10 | pass, fill 14 | +12:102 +13:36 | 1 | 11 | pass, fill 14 | +11:9 +12:75 +13:53 +14:1 | 3 | 10 | pass, fill 14 |
| +2015 | +10:3 +11:132 +12:3 | 2 | 9 | pass, fill 14 | +11:120 +12:18 | 1 | 10 | pass, fill 14 | +10:9 +11:75 +12:53 +13:1 | 3 | 9 | pass, fill 14 |
| +2016 | +10:100 +11:38 | 1 | 9 | pass, fill 14 | +10:129 +11:9 | 1 | 9 | pass, fill 14 | +9:9 +10:75 +11:53 +12:1 | 3 | 8 | not gradable |
| +2017 | +8:62 +9:76 | 1 | 7 | not gradable | +8:3 +9:135 | 1 | 7 | not gradable | +8:9 +9:75 +10:53 +11:1 | 3 | 7 | not gradable |
| +2018 | +7:25 +8:113 | 1 | 6 | not gradable | +7:24 +8:114 | 1 | 6 | not gradable | +7:9 +8:75 +9:53 +10:1 | 3 | 6 | not gradable |
| +2019 | +7:129 +8:9 | 1 | 6 | not gradable | +6:37 +7:101 | 1 | 5 | not gradable | +6:9 +7:75 +8:53 +9:1 | 3 | 5 | not gradable |
| +2020 | +6:98 +7:40 | 1 | 5 | not gradable | +5:56 +6:82 | 1 | 4 | not gradable | +5:9 +6:75 +7:53 +8:1 | 3 | 4 | not gradable |
| +2021 | +4:69 +5:69 | 1 | 3 | not gradable | +5:80 +6:58 | 1 | 4 | not gradable | +4:9 +5:75 +6:53 +7:1 | 3 | 3 | not gradable |
| +2022 | +3:37 +4:101 | 1 | 2 | not gradable | +4:102 +5:36 | 1 | 3 | not gradable | +3:9 +4:75 +5:53 +6:1 | 3 | 2 | not gradable |
| +2023 | +2:9 +3:129 | 1 | 1 | not gradable | +3:117 +4:21 | 1 | 2 | not gradable | +2:9 +3:75 +4:53 +5:1 | 3 | 1 | not gradable |
| +2024 | +2:121 +3:17 | 1 | 1 | not gradable | +1:3 +2:135 | 1 | 0 | not gradable | +1:9 +2:75 +3:53 +4:1 | 3 | 0 | not gradable |
| +2025 | +1:98 +2:40 | 1 | 0 | not gradable | +0:22 +1:116 | 1 | 0 | not gradable | +0:8 +1:75 +2:53 +3:1 (snap +2084) | 3 | 0 | not gradable |
| +2026 | -1:72 +0:65 (snap +2083) | 1 | 0 | not gradable | -1:49 +0:88 (snap +2083) | 1 | 0 | not gradable | -1:8 +0:75 +1:53 +2:1 (snap +2083) | 3 | 0 | not gradable |
| +2027 | -2:52 -1:85 (snap +2082) | 1 | 1 | not gradable | -2:70 -1:67 (snap +2082) | 1 | 1 | not gradable | -2:8 -1:75 +0:53 +1:1 (snap +2082) | 3 | 0 | not gradable |
| +2028 | -3:27 -2:110 (snap +2081) | 1 | 2 | not gradable | -2:98 -1:39 (snap +2081) | 1 | 1 | not gradable | -3:8 -2:75 -1:53 +0:1 (snap +2081) | 3 | 0 | not gradable |
| +2029 | -4:9 -3:128 (snap +2080) | 1 | 3 | not gradable | -3:124 -2:13 (snap +2080) | 1 | 2 | not gradable | -4:8 -3:75 -2:53 -1:1 (snap +2080) | 3 | 1 | not gradable |
| +2030 | -4:128 -3:9 (snap +2079) | 1 | 3 | not gradable | -5:18 -4:119 (snap +2079) | 1 | 4 | not gradable | -5:8 -4:75 -3:53 -2:1 (snap +2079) | 3 | 2 | not gradable |
| +2031 | -5:105 -4:32 (snap +2078) | 1 | 4 | not gradable | -6:48 -5:89 (snap +2078) | 1 | 5 | not gradable | -6:8 -5:75 -4:53 -3:1 (snap +2078) | 3 | 3 | not gradable |
| +2032 | -6:92 -5:45 (snap +2077) | 1 | 5 | not gradable | -6:80 -5:57 (snap +2077) | 1 | 5 | not gradable | -7:8 -6:75 -5:53 -4:1 (snap +2077) | 3 | 4 | not gradable |
| +2033 | -8:73 -7:64 (snap +2076) | 1 | 7 | not gradable | -7:113 -6:24 (snap +2076) | 1 | 6 | not gradable | -8:8 -7:75 -6:53 -5:1 (snap +2076) | 3 | 5 | not gradable |
| +2034 | -9:55 -8:82 (snap +2075) | 1 | 8 | not gradable | -9:10 -8:127 (snap +2075) | 1 | 8 | not gradable | -9:8 -8:75 -7:53 -6:1 (snap +2075) | 3 | 6 | not gradable |
| +2035 | -10:36 -9:101 (snap +2074) | 1 | 9 | pass, fill 14 | -10:49 -9:88 (snap +2074) | 1 | 9 | pass, fill 14 | -10:8 -9:75 -8:53 -7:1 (snap +2074) | 3 | 7 | not gradable |
| +2036 | -11:27 -10:110 (snap +2073) | 1 | 10 | pass, fill 14 | -10:90 -9:47 (snap +2073) | 1 | 9 | pass, fill 14 | -11:8 -10:75 -9:53 -8:1 (snap +2073) | 3 | 8 | not gradable |
| +2037 | -12:11 -11:126 (snap +2072) | 1 | 11 | pass, fill 14 | -12:1 -11:128 -10:8 (snap +2072) | 2 | 10 | pass, fill 14 | -12:8 -11:75 -10:53 -9:1 (snap +2072) | 3 | 9 | pass, fill 14 |
| +2038 | -12:128 -11:9 (snap +2071) | 1 | 11 | pass, fill 14 | -13:36 -12:101 (snap +2071) | 1 | 12 | pass, fill 14 | -13:8 -12:75 -11:53 -10:1 (snap +2071) | 3 | 10 | pass, fill 14 |
| +2039 | -13:119 -12:18 (snap +2070) | 1 | 12 | pass, fill 14 | -13:84 -12:53 (snap +2070) | 1 | 12 | pass, fill 14 | -14:8 -13:75 -12:53 -11:1 (snap +2070) | 3 | 11 | pass, fill 14 |
| +2040 | -14:110 -13:27 (snap +2069) | 1 | 13 | pass, fill 14 | -15:3 -14:127 -13:7 (snap +2069) | 2 | 13 | pass, fill 14 | -15:8 -14:75 -13:53 -12:1 (snap +2069) | 3 | 12 | pass, fill 14 |
| +2041 | -15:101 -14:36 (snap +2068) | 1 | 14 | pass, fill 14 | -16:48 -15:89 (snap +2068) | 1 | 15 | pass, fill 14 | -16:8 -15:75 -14:53 -13:1 (snap +2068) | 3 | 13 | pass, fill 14 |
| +2042 | -16:88 -15:49 (snap +2067) | 1 | 15 | pass, fill 14 | -16:104 -15:33 (snap +2067) | 1 | 15 | pass, fill 14 | -17:8 -16:75 -15:53 -14:1 (snap +2067) | 3 | 14 | pass, fill 14 |
| +2043 | -18:74 -17:63 (snap +2066) | 1 | 17 | pass, fill 14 | -18:25 -17:112 (snap +2066) | 1 | 17 | pass, fill 14 | -18:8 -17:75 -16:53 -15:1 (snap +2066) | 3 | 15 | pass, fill 14 |
| +2044 | -19:55 -18:82 (snap +2065) | 1 | 18 | pass, fill 14 | -18:87 -17:50 (snap +2065) | 1 | 17 | pass, fill 14 | -19:8 -18:75 -17:53 -16:1 (snap +2065) | 3 | 16 | pass, fill 14 |
| +2045 | -20:45 -19:92 (snap +2064) | 1 | 19 | pass, fill 14 | -20:15 -19:121 -18:1 (snap +2064) | 2 | 18 | pass, fill 14 | -20:8 -19:75 -18:53 -17:1 (snap +2064) | 3 | 17 | pass, fill 14 |
| +2046 | -21:38 -20:99 (snap +2063) | 1 | 20 | pass, fill 14 | -20:86 -19:51 (snap +2063) | 1 | 19 | pass, fill 14 | -21:8 -20:75 -19:53 -18:1 (snap +2063) | 3 | 18 | pass, fill 14 |
| +2047 | -22:34 -21:103 (snap +2062) | 1 | 21 | pass, fill 14 | -22:22 -21:114 -20:1 (snap +2062) | 2 | 20 | pass, fill 14 | -22:8 -21:75 -20:53 -19:1 (snap +2062) | 3 | 19 | pass, fill 14 |
| +2048 | -23:27 -22:110 (snap +2061) | 1 | 22 | pass, fill 14 | -22:101 -21:36 (snap +2061) | 1 | 21 | pass, fill 14 | -23:8 -22:75 -21:53 -20:1 (snap +2061) | 3 | 20 | pass, fill 14 |
| +2049 | -24:18 -23:119 (snap +2060) | 1 | 23 | pass, fill 14 | -24:45 -23:92 (snap +2060) | 1 | 23 | pass, fill 14 | -24:8 -23:75 -22:53 -21:1 (snap +2060) | 3 | 21 | pass, fill 14 |
| +2050 | +2059:1 (snap -24) | 0 | 24 | pass, fill 14 | -25:7 -24:119 -23:11 (snap +2059) | 2 | 23 | pass, fill 14 | -25:8 -24:75 -23:53 -22:1 (snap +2059) | 3 | 22 | pass, fill 14 |
| +2051 | -25:119 -24:18 (snap +2058) | 1 | 24 | pass, fill 14 | -25:90 -24:47 (snap +2058) | 1 | 24 | pass, fill 14 | -26:8 -25:75 -24:53 -23:1 (snap +2058) | 3 | 23 | pass, fill 14 |
| +2052 | -26:110 -25:27 (snap +2057) | 1 | 25 | pass, fill 14 | -26:52 -25:85 (snap +2057) | 1 | 25 | pass, fill 14 | -27:8 -26:75 -25:53 -24:1 (snap +2057) | 3 | 24 | pass, fill 14 |
| +2053 | -27:101 -26:36 (snap +2056) | 1 | 26 | pass, fill 14 | -28:22 -27:112 -26:3 (snap +2056) | 2 | 26 | pass, fill 14 | -28:8 -27:75 -26:53 -25:1 (snap +2056) | 3 | 25 | pass, fill 14 |
| +2054 | -28:96 -27:41 (snap +2055) | 1 | 27 | pass, fill 14 | -29:8 -28:114 -27:15 (snap +2055) | 2 | 27 | pass, fill 14 | -29:8 -28:75 -27:53 -26:1 (snap +2055) | 3 | 26 | pass, fill 14 |
| +2055 | -29:91 -28:46 (snap +2054) | 1 | 28 | pass, fill 14 | -30:3 -29:106 -28:28 (snap +2054) | 2 | 28 | pass, fill 14 | -30:8 -29:75 -28:53 -27:1 (snap +2054) | 3 | 27 | pass, fill 14 |
| +2056 | -31:83 -30:54 (snap +2053) | 1 | 30 | pass, fill 14 | -31:1 -30:98 -29:38 (snap +2053) | 2 | 29 | pass, fill 14 | -31:8 -30:75 -29:53 -28:1 (snap +2053) | 3 | 28 | pass, fill 14 |
| +2057 | -32:77 -31:60 (snap +2052) | 1 | 31 | pass, fill 14 | -32:1 -31:94 -30:42 (snap +2052) | 2 | 30 | pass, fill 14 | -32:8 -31:75 -30:53 -29:1 (snap +2052) | 3 | 29 | pass, fill 14 |
| +2058 | -33:73 -32:64 (snap +2051) | 1 | 32 | pass, fill 14 | -33:3 -32:96 -31:38 (snap +2051) | 2 | 31 | pass, fill 14 | -33:8 -32:75 -31:53 -30:1 (snap +2051) | 3 | 30 | pass, fill 14 |
| +2059 | -34:65 -33:72 (snap +2050) | 1 | 33 | pass, fill 14 | -34:7 -33:100 -32:30 (snap +2050) | 2 | 32 | pass, fill 14 | -34:8 -33:75 -32:53 -31:1 (snap +2050) | 3 | 31 | pass, fill 14 |
| +2060 | -35:61 -34:76 (snap +2049) | 1 | 34 | pass, fill 14 | -35:18 -34:102 -33:17 (snap +2049) | 2 | 33 | pass, fill 14 | -35:8 -34:75 -33:53 -32:1 (snap +2049) | 3 | 32 | pass, fill 14 |
| +2061 | -36:55 -35:82 (snap +2048) | 1 | 35 | pass, fill 14 | -35:39 -34:93 -33:5 (snap +2048) | 2 | 33 | pass, fill 14 | -36:8 -35:75 -34:53 -33:1 (snap +2048) | 3 | 33 | pass, fill 14 |
| +2062 | -37:49 -36:88 (snap +2047) | 1 | 36 | pass, fill 14 | -37:1 -36:73 -35:63 (snap +2047) | 2 | 35 | pass, fill 14 | -37:8 -36:75 -35:53 -34:1 (snap +2047) | 3 | 34 | pass, fill 14 |
| +2063 | -38:45 -37:92 (snap +2046) | 1 | 37 | pass, fill 14 | -38:18 -37:92 -36:27 (snap +2046) | 2 | 36 | pass, fill 14 | -38:8 -37:75 -36:53 -35:1 (snap +2046) | 3 | 35 | pass, fill 14 |
| +2064 | -39:27 -38:110 (snap +2045) | 1 | 38 | pass, fill 14 | -39:1 -38:54 -37:78 -36:4 (snap +2045) | 3 | 36 | pass, fill 14 | -39:8 -38:75 -37:53 -36:1 (snap +2045) | 3 | 36 | pass, fill 14 |
| +2065 | -40:18 -39:119 (snap +2044) | 1 | 39 | pass, fill 14 | -39:25 -38:85 -37:27 (snap +2044) | 2 | 37 | pass, fill 14 | -40:8 -39:75 -38:53 -37:1 (snap +2044) | 3 | 37 | pass, fill 14 |
| +2066 | -41:7 -40:130 (snap +2043) | 1 | 40 | pass, fill 14 | -41:8 -40:75 -39:53 -38:1 (snap +2043) | 3 | 38 | pass, fill 14 | -41:8 -40:75 -39:53 -38:1 (snap +2043) | 3 | 38 | pass, fill 14 |
