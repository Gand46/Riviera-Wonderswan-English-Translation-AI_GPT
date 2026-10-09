> Historical report for its stated version. Current I04/I05 status: [S463](10_S463_ASTRA_I04_I05.md).

# Astra reconciliation and bounded regression — 2026-10-07 UTC

## Outcome

The preceding audit was correct **for S459 RC3**. It was not a statement about the later S462 RC6 revision. This iteration recovered the later cumulative project, rebuilt it from the identified clean Japanese ROM, applied its existing BPS independently through the supplied patcher, and reconciled every owner from the audit against the generated ROM.

**All 94 confirmed ending-dialogue remnants are already English in RC6.** All 97 audited owner→stream pairs (including three punctuation-only strings) are covered by the S460 source layer retained in RC6. The broader source inventory has 102 streams / 139 pages. The source and built-ROM matches are exact, not inferred from version names.

**Shinya Fukao** is already integrated and was recaptured in the native credits renderer. The two other names remain Japanese because their readings cannot be established for these specific credited people. The current Astra research result is retained rather than inventing plausible readings. MusicBrainz does list a soundtrack candidate as “Hashimoto, Nobuyuki”; this narrows the missing evidence to identity linkage and authority. It does not establish the Riviera Special Thanks identity. A same-name web designer uses Kozu, illustrating why guessing Takatsu from kanji would be unsound.

No new ROM bytes or patch were manufactured. The delivered BPS is the existing, verified cumulative RC6 patch. The only source utility edit fixes `verify_package.py` to evaluate generated-directory names relative to the repository, so a checkout located beneath a folder named `work` is not falsely rejected.

## Binary integrity

| Check | Result |
| --- | --- |
| Complete source chain → RC6 | PASS, exact target SHA-256 |
| Existing BPS applied directly to clean JP | PASS, byte-identical to rebuilt RC6 |
| WonderSwan checksum | PASS, 289A |
| RC3→RC6 changes outside intended ranges | 0 |
| All 94 audited Japanese dialogue streams | English bytes and redirected owners verified |
| Incorrect source / truncated BPS / corrupted BPS | Rejected |
| New changes to ROM in this iteration | 0 |

RC3→RC6 changes 4,243 bytes, confined to the ending text allocation and 102 pointer fields, the compact selector at 0x75EAF1..0x75EAFB, the page 08 credit payload at 0x7FEDE0..0x7FF4EA, and checksum bytes. This is the already documented S460→S462 work, not a new global replacement. Game logic, damage/stat tables, save routines, font resources and unrelated graphics are outside these change ranges. The selector changes are text-dispatch code, not a claim that the entire ROM contains no code changes relative to RC3.

Original JP SHA-256: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.

RC6 SHA-256: `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204`.

BPS SHA-256: `2a36c3ada7d4448fc629957854b3c8885ac7e58a0979fd64d52940bff15f2b4f`.

## Fresh runtime and visual evidence

- **Opening:** identical scripted controller input from boot in RC3 and RC6; 16 image pairs are pixel-identical.
- **Combat:** the same historical PW3 second-battle state and 1,200 frames of input; four image pairs are pixel-identical and both corrected runners terminate normally. This tests a bounded battle segment and state compatibility, not cold-save persistence or a full playthrough.
- **Ending:** route 0 plus late subsets of routes 1–5, using explicitly synthetic entry and the native renderer. Six stable-capture runs terminate normally. 47 distinct owner screenshots were captured; 44 selected last-page views were directly reviewed (24 by the primary reviewer, 20 by Astra). All 44 reviewed views are legible English or punctuation, with no Japanese or clipping observed. This is not a new visual approval of every page in all 102 streams.
- **Credits:** replay from the S460 synthetic-ending checkpoint, 4,500 frames, native RC6 renderer. `Shinya Fukao` is visible and legible at `runtime/credits_rc6/credit_09_f2100.png`. `橋本信之` remains visible in the next page, as expected for the unresolved reading.
- **Dispatch traces:** all recorded native-path events in the allocated ending range correspond to the preserved space token 8A; actual compact English glyph events take the compact path.

The initial FF+1 capture timing omitted some final punctuation before the renderer completed its last blit. The QA script now waits six frames and pauses A for eight frames. Stable captures resolve these omissions; the ROM was not changed to repair a screenshot-timing artifact. Final contact sheets use exact 2× nearest-neighbor scaling of the 237×144 Mesen output, including its side input display. Native PNGs are retained.

The reviewers had earlier access to source material; the first image-reading pass did not consult the expected strings as a correction key. It would be inaccurate to describe the reviewers as completely unexposed or the sample as a global blind review.

## Limits and unsuccessful diagnostics

The final combat WRAM dumps differ at one byte of the engine counter at 0x02E4 (words C61C/C60A). The unchanged code at ROM 0x720312 increments this counter (`FF06E402`). The cause of the counter offset was not established; full WRAM identity is therefore not claimed. Final CPU snapshots otherwise agree apart from an internal IRQ-suppression timestamp. The screenshots and bounded progression tests pass, but these facts do not grant universal gameplay approval.

An initial battle script attempted to create a savestate in the endFrame callback and timed out. Moving the snapshot to a CPU-execution callback resolved the runner. Two optional write-watchpoint diagnostics were unsuccessful and abandoned; no result is inferred from them. The successful CPU-only diagnostic and the initial failures are recorded separately. The empty first frame after loading a state was excluded from image comparison.

No natural complete playthrough, hardware validation, cold save/load cycle or new universal Japanese census was performed. Prior 102-stream and 32-page evidence remains historical and scoped to byte-identical resources. Global visual, linguistic and functional approvals remain open. `FINAL_APPROVED=false`.

## Remaining work

1. Establish identity-linked readings for 高津利恵 and 橋本信之; then replace only their bounded credit rows with native Latin glyphs and recapture.
2. Resolve I04 usage for the ninth icon intervals; they are not proven Japanese text and must not be overwritten as such.
3. Continue separately documented manual/hardware, High Score and global-review follow-ups.

## Evidence and reproducibility

The `validation/ASTRA_2026_10_07/` directory contains reconciliation JSON, the 97-row current catalog, independent Astra notes, native screenshots, selected savestates, consumer traces, input scripts, source-build log and per-run commands/hashes. Original workspace paths in execution records are provenance, not portable dependencies. Use the included BUILD.bat/BUILD.command and build_rc6.py for a clean rebuild. The QA runners preserve their original layout assumptions and must be pointed to the extracted source, emulator and private ROM paths when reproduced elsewhere.

The existing S461 reading-closeout file is retained as historical evidence; the current Astra name report supersedes only its search-description wording, not the unresolved result. Source/ROM changes are not inferred from metadata changes. Token savings: not measured.
