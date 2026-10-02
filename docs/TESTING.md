# Manual testing guide

Test only a ROM whose SHA-256 is `c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd`.

## Priority checks

1. Continue the late ending scene that still contains Japanese; record the full conversation, route and speaker order.
2. Review all 32 fullscreen epilogue pages without consulting expected strings first. Record unreadable or ambiguous glyphs before comparing with source.
3. Recheck Chapter 8 Hades dialogue for clipping, punctuation, portrait overlap and pacing.
4. Exercise Team Edit, Save/Load, Extras and High Score using legitimate saves where available.
5. Report any regression in previously approved battle, tutorial, menu or credit surfaces.

## Bug report data

- RC3 ROM SHA-256;
- emulator and version, or hardware/flash cartridge details;
- route/checkpoint and input sequence;
- save/SRAM provenance;
- native-resolution screenshot;
- expected and observed behavior;
- whether access was natural, scripted natural, savestate or synthetic.

Do not submit copyrighted ROM images with a report.
