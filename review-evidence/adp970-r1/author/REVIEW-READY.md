REVIEW READY 0ad0e518 (branch 970-discovery, three commits on dev-soft-core 5de21ff3 incl. a merge of c34e7d8b)

The ADP draw is seeded per IEEE 1722.1-2021 6.2.4.2.2 from the MAC address, the microsecond clock, the entity ID and the interface, at startup and at each qualified LINK_UP (Milan v1.2 5.6.3.5.2 and 5.6.3.5.3). The declared discovery time is unchanged (6.0 s). receipts/validation-r2 holds the gates.
