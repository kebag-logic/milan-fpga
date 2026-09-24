#### What an adoption must prove

No result is claimed here: nothing is implemented.

| Arm | Expected evidence |
|---|---|
| Zero | Offset and PHC trajectory identical to today's build |
| Positive and negative | The offset moves by the configured value, in opposite directions |
| Sign | A sign-swapped mutation fails the suite |
| Limits | Out-of-range values are refused by the builder |
| Reset and update | Reset restores zero; no live change without an amendment |
| Peer delay | `neighborPropDelay` is unchanged by every value |
| Double correction | The I/E constants and `GPTP_LAT` are unchanged |
| Configuration to engine | The configured value reaches the engine input exactly |

An adoption is one bounded lane, tracked under issue #110.

It owes a reviewed durable donor pin and regenerated ROM.

It also owes donor `make`, `gptp_shadow` and root integration.

Every CONTRIBUTING gate runs at that candidate.

| Party | Owns |
|---|---|
| Parent | The product contract, REQ-PTP-06 constants, the builder refusal and this record |
| gPTP processor | Any asymmetry input and its arithmetic, under donor issue 58 |
| Donor bench | The UART Y/I/E tuner, never pinned into a product image |
| Issues #64 and #488 | Physical measurement of the split |
| Issue #110 | Integration tracking of any adopted donor pin |

