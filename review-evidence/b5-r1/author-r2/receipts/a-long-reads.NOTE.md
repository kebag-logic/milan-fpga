# a-long-reads.u16: the byte-identical record

The archive step's text redaction masked 3 bytes of `a-long-reads.u16` (offsets 114032-114034 replaced by `###`). Those bytes were read-interval data that happened to match a redaction pattern. So the published `a-long-reads.u16` hashes to `8897abce...`, not the page's `2183d57f...` (R425-2 F1).

`a-long-reads.u16.gz` holds the original record unchanged. Restore it with `gunzip -k a-long-reads.u16.gz`, then check:

    sha256sum a-long-reads.u16
    2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961

`tools/b5_attrib.py` accepts the restored file unmodified. The masked copy is kept only as history. The archive tool now refuses to mask any binary file.
