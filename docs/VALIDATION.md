# Validation record

## Binary and source

- Source rebuild from the identified clean Japanese ROM: `PASS`.
- BPS round-trip: `PASS_BYTE_EXACT`.
- Wrong source rejected: `PASS`.
- Truncated/corrupt patch rejected: `PASS`.
- WonderSwan checksum: `PASS` (`BF7D`).
- S458-to-S459 unexpected changed bytes: `0`.
- Overlap with 1,766 historical resource intervals: none.
- Independent BPS applicator: `NOT_VALIDATED`; the packaged `ws_patch_tools.bps` implementation was used.

## Runtime scope

- Seven corrected Chapter 8 streams were read and rendered by the native dialogue path from a documented savestate.
- The Hades encounter progressed to Team Edit under the tested input schedule.
- Ending route 0 completed all 13 credit pages and returned.
- Routes 1, 2 and 4 completed their tested late subsets and returned.
- The four modified epilogue streams reached their terminators and displayed the new line balance.

## Limits

- Runtime access is synthetic/savestate-based where the gate matrix says so.
- The visual inspection of the modified pages was source-aware; it does not replace blind recognition of the full 32-page universe.
- Japanese visible outside the corrected Hades encounter blocks global linguistic approval.
- A passing build or BPS does not grant visual, linguistic or final approval.

Machine-readable evidence is in `validation/S459/` and `validation/RC3_GATE_MATRIX.json`.
