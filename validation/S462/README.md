# S462 / RC6 — compact selector regression fix

Result: `PASS` for R01. `FINAL_APPROVED=false` because I04 and two I05 readings remain open.

S462 restores the two compact ranges accidentally bypassed in S460 while preserving the new S460 tail. The 22 stored streams remain byte-identical. Mesen A/B evidence naturally reproduces RC5 Japanese glyphs and RC6 English for `0x7CB227`; a second natural route validates `0x7CDBE1`. Both representative captures match native ROM glyph pixels exactly with no clipping.

This validation does not extend visual approval to the other 20 streams or globally to the project. See `S462_VALIDATION.json`.
