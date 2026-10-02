# Riviera: The Promised Land — WonderSwan Color English v0.112 / S459 / RC3

This is the supplied S459 source and cumulative BPS prepared for GitHub. The patch targets the Japanese 8 MiB WonderSwan Color release. **Status: experimental manual-testing RC3; `FINAL_APPROVED=false`.** This packaging does not incorporate later checkpoints or fix remaining translation defects.

| File | SHA-256 / provenance |
|---|---|
| Required clean Japanese ROM, 8,388,608 bytes | `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921` (documented, not measured in this packaging run) |
| English S459 output, 8,388,608 bytes | `c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd` (documented; WonderSwan checksum `BF7D`) |
| Direct JP→S459 BPS | `0d90bce872e7383497b90ef6051bf197260eb2ddc1ea4dd9c2d63c36c0e40504` (measured from both supplied packages) |

## Patch your copy

Provide your own clean Japanese ROM matching the size and SHA-256 above. Use a BPS patcher with it as the **source** and `patches/Riviera_EN_v0.112_S459_RC3_CUMULATIVE_FROM_JP.bps` as the patch. The bundled Python 3 patcher is also available:

```sh
python3 apply_patch.py path/to/clean-jp.wsc build/Riviera-English-RC3.wsc
```

`APPLY_PATCH.bat` and `APPLY_PATCH.command` call that script on Windows and macOS. Verify the output SHA-256 above. Do not patch an earlier translated ROM or chain older BPS files. No ROM or BIOS is distributed.

## Build from the actual cumulative sources

```sh
python3 build.py path/to/clean-jp.wsc build/Riviera-English-RC3.wsc
```

`BUILD.bat` and `BUILD.command` wrap the same Python builder. Its S459→S458→S457→S456→historical source chain rebuilds the translation from the user-provided original, without applying the included BPS as its build step. Python 3.9+ and approximately 1 GB temporary space are recommended by the supplied documentation. The sanitized nested archive still has four ordered chunks under `source/Riviera_S457_FULL_SOURCE/upstream/`; they are **required** build inputs. See [build and reproducibility](docs/BUILD_AND_REPRODUCIBILITY.md) for the precise validation boundary and a byte-comparison procedure.

## Technical architecture

- The S455/S457 credit graphics run through a guarded hook at ROM `0x761124`, a dispatch stub at `0x7FDC40` and RLE/packed graphics beginning at `0x7FDE80`. The global native font remains unchanged; S457 extends the capital I in four compiled credit graphics.
- S456 corrects two Rapier ability names in the item/manual integration. It retains a bounded inventory of 1,766 known resources and manual tables of 147 records and 76 unique texts.
- S458 repairs LaLa termination and three owners, adds the first Fia Chapter 8 line, and fixes an epilogue spelling error. S459 redirects seven Hades dialogue owners to `0x7FFC34..0x7FFDFC` and rebalances four bank 0x66 epilogue streams by moving control bytes.
- The current dialogue encoding uses two-byte `0xA2` glyph references, `0xA9` for line breaks, `0xFE00` for page breaks and `0xFF` for termination. S459 checks length and allocation bounds and recalculates the WonderSwan footer checksum.

These are ROM **file offsets**, not CPU addresses. See [the findings register](docs/TECHNICAL_FINDINGS.md) for individual evidence, buffer/codec details, historical scope and unresolved cases. The [consumer table](docs/TEXT_CONSUMERS.csv) gives every S459 owner and stream offset while recording unknown CPU entries explicitly. Original reports and analyses remain in the source chain.

## Validation and open issues

The supplied RC3 gate matrix has 11 PASS, six PASS_SYNTHETIC, two NOT_VALIDATED and one FAIL. Earlier source rebuild and BPS round-trip reports refer to the original supplied source archive; the cleaned source chain has passed structural/hash checks, but **a fresh clean-ROM build and source/BPS byte comparison were NOT_RUN** because no clean ROM was supplied for this packaging. The patch bytes and CRC are unchanged.

Japanese remains visible in a later ending scene (`FAIL` for global linguistic QA). The ninth icon consumer and three Japanese credit-name readings remain `NOT_VALIDATED`; an independent context-free review of all 32 fullscreen epilogue pages is also incomplete. Synthetic passes describe their tested screens and access method, not a natural full playthrough. See [status](docs/STATUS.md), [validation](docs/VALIDATION.md) and the [gate matrix](validation/RC3_GATE_MATRIX.json).

## Repository contents

| Path | Purpose |
|---|---|
| `build.py`, `source/` | Guarded cumulative source builders and historical archive chain |
| `patches/`, `apply_patch.py` | Direct BPS and local applicator |
| `validation/`, `evidence/` | Supplied bounded reports and selected screen captures |
| `docs/` | Technical findings, consumer offsets, build scope, status and organization decisions |
| `scripts/verify_repository.py` | Package identity, file-limit and forbidden-extension checks |

No project-wide license was supplied; preservation of existing credits and tool sources does not grant rights in the commercial game. See [NOTICE.md](NOTICE.md) and the historical reports for the credited evidence and tools. Contributors should consult [CONTRIBUTING.md](CONTRIBUTING.md). Original tool authorship/licensing should be confirmed before changing redistribution terms.
