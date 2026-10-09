# Riviera WSC English — v0.116 S463 RC7

This test build adds **Nobuyuki Hashimoto** to the native Special Thanks credit page and closes the two I04 Japanese-text candidates as **non-text pixels in a building graphic**, with documented synthetic native DMA/PPU evidence reviewed by Astra.

**高津利恵 remains Japanese: its reading has not been established for this person.** This is `INTERNAL_TEST_NOT_FINAL`; `FINAL_APPROVED=false`. The full game is not globally approved. See [the current report](docs/10_S463_ASTRA_I04_I05.md) and [the roadmap](docs/04_HOJA_DE_RUTA_Y_PENDIENTES.md).

## What changed

Only the compressed page-09 credit graphic and checksum differ from RC6. The full name uses two lines of unchanged native glyphs. An improved lossless encoder fits the graphic into the existing allocation; runtime font, decoder, hooks, animation and gameplay code are unchanged. RC6's compact-selector regression fix and all earlier translations are retained.

Sources, the cumulative BPS, hashes, documentation, native screenshots and versioned savestates are included. No commercial ROM or BIOS is included. Historical stage reports retain their original scope; S463 is the current report.

## Apply the patch

Use the clean Japanese original, not a previously patched ROM:

```text
python apply_patch.py Riviera_JP_CLEAN.wsc Riviera_EN_v0.116_S463_RC7.wsc
```

## Rebuild from cumulative sources

Windows:

```text
BUILD.bat Riviera_JP_CLEAN.wsc build\Riviera_EN_v0.116_S463_RC7.wsc
```

macOS/Linux:

```text
./BUILD.command Riviera_JP_CLEAN.wsc build/Riviera_EN_v0.116_S463_RC7.wsc
```

The Python build chain runs from clean JP through S441–S463; no patch chain is required. The current source rebuild and BPS produce exactly the same ROM. The Windows launcher is provided; Windows execution was not available in this Linux validation environment.

## Identity and verification

- Original SHA-256: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`
- RC7 SHA-256: `933cfcd5ea40f0f1d960338e78dc60ead6d8e5c280ea28bc69007f55ed2cc7aa`
- RC7 checksum: `2564`
- BPS SHA-256: `c70c704ddd0f9e67646ea4bcb67c38be725648b1893b55b540ff07f0f37ade0f`
- Package: `python verify_package.py`

Astra approved the changed credit page; the native decoder output matched all 4,608 graphic bytes. All 76 screenshot pairs outside that page were pixel-identical to RC6 in the 6,000-frame bounded replay. These checks do not imply a complete playthrough, hardware validation or global language approval.
