# Building RC3

## Requirements

- Python 3.9 or newer.
- A clean 8 MiB Japanese ROM with SHA-256 `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.
- Approximately 1 GB of temporary free space for extraction and intermediate builds.

No third-party Python package is required.

## Full cumulative build

Linux/macOS:

```bash
python3 build.py clean-jp.wsc build/Riviera-English-RC3.wsc
```

Windows:

```bat
BUILD.bat clean-jp.wsc build\Riviera-English-RC3.wsc
```

Expected output:

- size: 8,388,608 bytes;
- SHA-256: `c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd`;
- WonderSwan checksum: `BF7D`.

The build path is:

```text
clean Japanese ROM -> S456 cumulative source -> S457 -> S458 -> S459 RC3
```

No intermediate BPS is used by the source build.

## Direct BPS application

```bash
python3 apply_patch.py clean-jp.wsc Riviera-English-RC3.wsc
```

The script rejects an incorrect base ROM, a modified patch and an existing output path.

## Source archive chunks

The historical S456 archive is exactly 145,694,256 bytes and is stored as four numbered chunks below GitHub's per-file hard limit. `rebuild_s457.py` concatenates them in lexical order inside a temporary directory and verifies the original archive SHA-256 before extraction.

Expected reconstructed archive SHA-256:

`1e2f381ef0186d5763dc762047db1978f8eff520351f3cdd70db5eb3d78db9b7`

The build deletes temporary extracted data automatically. The historical archive was sanitized to remove savestates and bytecode; see BUILD_AND_REPRODUCIBILITY.md. A fresh clean-ROM rebuild after sanitization was NOT_RUN.
