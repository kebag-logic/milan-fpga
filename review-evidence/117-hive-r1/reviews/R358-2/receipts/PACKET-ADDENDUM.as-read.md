# Packet addendum: probe include directory (R359-1 S3)

The probe build's `-I<probe>/include` directory holds 49 header files. Each is byte-identical to a file from the enumerating library's own source tree at the recorded revision.

| Subtree | Files | Source (byte-identical) |
|---|---:|---|
| `la/avdecc/` | 48 | the library's `include/la/avdecc/`, at `v4.3.1.1` (`6d61a92e7f264c69f23cdc38f50d31114e567aa0`) |
| `la/networkInterfaceHelper/` | 1 | the library's `externals/nih/include/la/networkInterfaceHelper/`, at the pinned submodule commit `d777db8b4d1947b1c63f4cb8aab03b0bec5f7e22` |

- `diff -rq` against both source directories reports no differing file and no file absent from the source. The directory is a subset: it omits SWIG `.i` files, the umbrella `avdecc.h`, `networkInterfaceHelper.h`, the Windows helper and one internal virtual-entity header, none of which the probe includes.
- The SHA-256 of the sorted per-file `sha256sum` list is `7711cedc9d4f84a45b99e3bcd1d9c997436b538de1db39889c9d65541b50f636`.
- There are no third-party headers in this directory.
- The recorded build command (`author/build-provenance.txt`) searches the library's `include/`, then its `externals/3rdparty/json/include/` (submodule `9cca280a`), then this directory. So this directory adds only the networkInterfaceHelper header that the library's own `include/` lacks. Its `la/avdecc` files duplicate the library's headers byte for byte.

The coordinator collected this read-only on 2026-09-27, because round 2 had no access to the controller host.
