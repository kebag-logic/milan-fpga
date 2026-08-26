# AVDECC model tools

The shipping entity model is generated from `configs/endstation_*.yaml` by
`sw/builder/endstation_builder.py`. The builder emits an AEM overlay and packs
it into the `aem_desc.bin` image that is paired with the gateware.

The files in this directory provide the model packer, image wrapper, setup
helpers, and a small controller used for protocol validation:

| File | Purpose |
|---|---|
| `gen_aem_store.py` | Build descriptor bytes from a builder overlay. |
| `gen_aemi_image.py` | Wrap and validate the descriptor-memory image. |
| `milan_controller.py` | Exercise discovery and AEM commands from a measurement peer. |
| `aecp_csr_setup.sh` | Configure the remaining fabric-visible control registers. |

Generated descriptor data is not edited by hand. Start with
[`docs/ENDSTATION_BUILDER.md`](../docs/ENDSTATION_BUILDER.md) for the build
pipeline and [`docs/testing/TESTING.md`](../docs/testing/TESTING.md) for the
validation entry points.
