# Contributing

RC3 is an evidence-driven translation project. Changes should preserve the cumulative build and must not include commercial ROM data.

Before proposing a change:

1. Identify the clean Japanese base by SHA-256.
2. Record the resource, owner/pointer, expected bytes and allowed range.
3. Rebuild from source and verify the resulting ROM hash.
4. Generate a cumulative BPS directly from the clean Japanese ROM.
5. Test affected runtime surfaces and relevant regressions.
6. Keep linguistic, typography, legibility, visual and functional results separate.
7. Document synthetic access as synthetic; do not present it as natural progression.

Do not commit ROMs, BIOS files, emulator distributions, temporary build output, SRAM, or unreviewed savestates.
