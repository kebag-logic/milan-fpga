# Enabled parent loopback integration

Run `make` with scratch supplied through `WORK`.
Both supported shapes come from their generated enabled configurations.
The test elaborates `milan_datapath` with split control enabled.
It links the production AECP command implementation and descriptor image.
Commands enter that implementation as Ethernet command bytes.
Its edit callback drives the real parent transaction server.
The mailbox transport and processor instruction execution are outside scope.

ADD, REMOVE, replacement, rejected edits, and no-ops are checked.
GET_AUDIO_MAP checks both pages against commanded mappings.
The parent GET interface is independently checked against those mappings.
A boot format change exercises the actual clipping writer.
An accepted edit is aligned inside a mapped copy.

Distinct received AAF samples identify stream, channel, and presentation frame.
The expected map comes exclusively from command intent.
The parent commit pulse establishes the edit time.
Neither stored mapping bits nor buffer samples supply expected values.
Every capture sample and transmitted sample is graded.
Silence and the first eligible new frame are included.
All 63 destinations and eight talkers run concurrently at 8x8.
The final unused channel must remain silent.
A walk deadline assertion covers the entire capture walk.

`python3 mutants.py --output <scratch>` runs controls and three plants.
Removing the edit invalidation or map connection must fail samples.
Reducing retention to four pages must fail at 1x1.
Compilation errors never count as successful detections.

The [wire fixture](../input_loopback/README.md) adds isolated leaf coverage.
Its five unisolated defensive guards remain explicitly untested.
