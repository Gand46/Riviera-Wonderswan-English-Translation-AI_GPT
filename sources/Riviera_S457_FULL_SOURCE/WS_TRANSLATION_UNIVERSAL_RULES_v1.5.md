---
title: "WonderSwan Translation Projects — Universal Rules"
version: "1.5"
date: "2026-09-20"
scope: "All WonderSwan / WonderSwan Color translation and localization projects"
language: "en"
status: "MANDATORY_BASELINE"
machine_readable_sections: true
---

# WonderSwan / WonderSwan Color Translation Projects
## Universal Rules, Translation Quality and Integrated Quality Gate
### Version 1.5 — Mandatory Project Source

## 0. PURPOSE AND AUTHORITY

This document is the universal baseline for all WonderSwan and WonderSwan Color translation/localization projects.

It is intended to be consumed by:
- GPT/LLM agents;
- ChatGPT Work projects;
- coding agents;
- QA agents;
- translation agents;
- human contributors;
- automated build/verification pipelines.

Project-specific rules MAY add stricter constraints, but MUST NOT weaken, bypass, or contradict this baseline.

Version 1.3 formalizes two mandatory release-quality requirements:

1. **Native typography continuity:** localized text must use the same in-game typographic system/style as the corresponding original game surface, unless a project-specific redesign is explicitly documented and validated.
2. **Rendered-content legibility:** a `PASS` requires the actual on-screen content to be readable. Source code, decoded strings, ROM bytes, tables, or an expected word are evidence of intent/content, but are not evidence that the rendered result is legible.

Version 1.5 strengthens two additional mandatory safeguards:

3. **Context-independent recognition / anti-false-pass:** OCR, GPT vision, a human reviewer or any automated recognizer MUST NOT obtain a legibility `PASS` primarily by reconstructing an expected word from language context, dictionaries, filenames, source strings, prior knowledge or semantic plausibility. The rendered glyphs themselves must support the reading.
4. **Font preservation and glyph integrity:** the project MUST preserve the native font identity and must verify glyph completeness, repeated-glyph consistency and cross-glyph style continuity. A correct decoded string rendered with malformed, mixed, incomplete or non-native glyphs is not typography- or legibility-approved.

The quality model is:

```text
FINAL QUALITY
=
UR PASS
+
TQ PASS
+
QG PASS
```

Where:

```text
UR = Universal technical/project rules
TQ = Translation and linguistic quality rules
QG = Integrated product/release quality rules
```

The desired end result is not merely "Japanese text replaced with English".

The target is:

> A coherent English-language version that looks, reads and behaves as if it could have been an official WonderSwan/WonderSwan Color release, while preserving the original game's design, functionality, constraints and artistic identity.

---

# PART I — UR: UNIVERSAL PROJECT RULES

## UR-01 — Identify the original ROM
Every project MUST identify the original Japanese ROM using, at minimum:
- expected filename;
- exact byte size;
- SHA-256;
- WonderSwan checksum when applicable.

Never assume two ROMs with the same filename are byte-identical.

## UR-02 — Use a clean base
Official cumulative patches MUST be generated from a clean, known original ROM.

## UR-03 — Commercial ROM handling
A commercial ROM may be used privately for development and validation, but it is NOT required to be distributed with the project package.

The package MUST include sufficient metadata/hashes for the user to provide the correct base ROM.

## UR-04 — Never silently change the base
If a project changes to a different original ROM revision, that change MUST be explicitly documented and the validation chain rebuilt.

## UR-05 — Complete cumulative sources
Every formal version MUST include the complete cumulative source state needed to reproduce the current build.

Do not ship only files changed in the last phase.

## UR-06 — Mandatory cumulative BPS
Every playable formal version MUST include:

```text
Original Japanese ROM -> Current Version
```

as a cumulative BPS patch.

## UR-07 — No patch chains
Users MUST NOT need:

```text
v0.1 -> v0.2 -> v0.3 -> v0.4
```

to obtain the current version.

## UR-08 — Incremental patches are supplemental
Incremental BPS/IPS patches may be retained for:
- auditing;
- debugging;
- historical comparison;
- regression analysis.

They are NOT the primary installation method.

## UR-09 — IPS is optional/supplemental
A cumulative IPS may be included for compatibility, but it does NOT replace the mandatory cumulative BPS.

## UR-10 — Self-contained delivery
Formal packages SHOULD include, when applicable:
- full source;
- scripts;
- tables;
- dictionaries/glossaries;
- builders;
- patchers;
- verifiers;
- inventories;
- reports;
- evidence;
- documentation;
- changelog;
- hashes.

The project MUST NOT depend solely on prior chat context.

## UR-11 — Reproducible build
There MUST be a documented procedure equivalent to:

```text
Known Original ROM + Project Sources/Scripts -> Current ROM
```

## UR-12 — BPS round-trip verification
For every RC/final or other formally distributed playable version, applying the cumulative BPS to the correct original ROM MUST produce a ROM byte-identical to the project build.

Required validation:

```text
SHA256(builder_output) == SHA256(BPS_output)
```

## UR-13 — WonderSwan checksum
After ROM modification, validate and rebuild the WonderSwan checksum when required.

## UR-14 — Output hashes
At minimum record SHA-256 for:
- original ROM;
- current ROM;
- cumulative BPS.

## UR-15 — Explain binary changes
Relevant binary modifications SHOULD be attributable to intended project changes.

## UR-16 — Validate allowed ranges
For bounded modifications, compare actual changed ranges against expected ranges.

Preferred result:

```text
unexpected_changed_offsets = 0
```

## UR-17 — Preserve neighboring data
Do not arbitrarily alter:
- code;
- pointers;
- opcodes;
- padding;
- tables;
- graphics;
- icons;
- terminators;
- metadata;
- neighboring resources.

## UR-18 — No blind global replacements
Do not globally replace byte sequences merely because they decode as Japanese text.

The resource context MUST be understood first.

---

# PART II — TEXT DISCOVERY AND STRUCTURAL VALIDATION

## UR-19 — Shift-JIS/CP932 is only candidate evidence
A valid Shift-JIS/CP932 sequence is NOT proof that it is real in-game text.

## UR-20 — Prefer structural confirmation
When possible, connect candidate text to:
- consumer;
- pointer;
- descriptor;
- table;
- decoder;
- renderer;
- script;
- index;
- resource structure;
- runtime execution.

## UR-21 — No destructive candidate filtering
Do not permanently discard uncertain candidates solely because of:
- entropy;
- proximity;
- apparent noise;
- length;
- unusual characters;
- lack of obvious references.

## UR-22 — Use explicit unresolved states
Allowed states include:

```text
UNRESOLVED
UNKNOWN
NEEDS_TRACE
NEEDS_CONTEXT
NEEDS_REVIEW
SOURCE_UNCLEAR
```

## UR-23 — Negative evidence is limited
Failure to find a reference with one tool does NOT prove a resource is unused.

---

# PART III — UNIVERSAL TRANSLATION STATES

The following states MUST be recorded separately:

```text
DISCOVERED
TRANSLATED
INTEGRATED
RUNTIME_CONFIRMED
LINGUISTIC_APPROVED
TYPOGRAPHY_APPROVED
LEGIBILITY_APPROVED
DESIGN_APPROVED
VISUAL_APPROVED
FUNCTIONAL_APPROVED
FINAL_APPROVED
```

All states except `FINAL_APPROVED` are independent evidence/status dimensions.

`FINAL_APPROVED` is a **derived state**. It MUST NOT be manually granted simply because one or more other states are true.

`FINAL_APPROVED` may only be true when every mandatory applicable gate required by this document is `PASS`, and any `N/A` is explicitly justified.

Never treat one state as automatically implying another.


### Universal validation outcomes

For any gate or dimension, use these meanings consistently:

```text
PASS           = tested with sufficient evidence and met the requirement
FAIL           = tested with sufficient evidence and did not meet the requirement
NOT_VALIDATED  = insufficient evidence; requirement has not been tested adequately
N/A            = genuinely not applicable, with explicit justification
```

Rules:

- `NOT_VALIDATED` is NOT equivalent to `FAIL`.
- `NOT_VALIDATED` is also NOT equivalent to `PASS`.
- Any mandatory gate in `FAIL` or `NOT_VALIDATED` blocks `FINAL_APPROVED`.
- `N/A` may only be used when the requirement truly does not apply and the reason is documented.
---

# PART IV — TQ: TRANSLATION / LINGUISTIC QUALITY

## TQ-01 — Preserve meaning
The translation MUST preserve the real meaning of the source.

## TQ-02 — Preserve intent
Maintain the communicative function:
- question;
- order;
- threat;
- request;
- joke;
- warning;
- explanation;
- implication;
- reaction;
- gameplay instruction.

## TQ-03 — No unsupported additions
Do not add information that is absent or not reasonably implied in the source.

## TQ-04 — No meaning loss
Do not omit meaning merely to make text fit.

Solve space pressure through better wording, layout, spacing, or technically valid extensions/adaptations of the game's native typography and text system. Do not replace the native typographic identity merely to gain space.

## TQ-05 — Preserve logic
Maintain:
- cause;
- consequence;
- condition;
- negation;
- comparison;
- temporal relation;
- subject/object;
- direction;
- possession.

## TQ-06 — Preserve gameplay information
Never accidentally alter:
- quantities;
- stats;
- percentages;
- damage;
- items;
- conditions;
- directions;
- objectives;
- hints;
- timers;
- turns;
- commands;
- requirements.

A stylistically attractive but functionally wrong translation is a FAIL.

## TQ-07 — Natural target language
Final English MUST read naturally and should not look like raw Japanese syntax transferred word-for-word.

## TQ-08 — No unreviewed MTL
Machine/LLM output may create a draft, but it MUST NOT be considered linguistically approved without review.

## TQ-09 — Grammar
Approved text MUST use correct grammar.

## TQ-10 — Spelling
Known spelling errors are not acceptable in approved text.

## TQ-11 — Punctuation consistency
Use project-wide conventions for:
- periods;
- commas;
- question/exclamation marks;
- apostrophes;
- quotes;
- dashes;
- ellipses.

## TQ-12 — Capitalization consistency
Define and preserve conventions for:
- names;
- titles;
- items;
- skills;
- menus;
- headings;
- places;
- commands.

## TQ-13 — Mandatory terminology memory/glossary
Any project with recurring names, terms, items, skills, locations, UI labels or other repeated terminology MUST maintain a central glossary/terminology memory covering, where relevant:
- characters;
- places;
- items;
- weapons;
- armor;
- spells;
- skills;
- statuses;
- enemies;
- factions;
- organizations;
- UI commands;
- system terminology;
- proper nouns.

A glossary may be marked `N/A` only for a genuinely trivial project with no recurring terminology, and that decision MUST be documented.

## TQ-14 — One entity, one approved name
The same entity SHOULD NOT receive different translations without a documented reason.

## TQ-15 — Document required abbreviations
When a technical limit requires a shorter variant, document it.

Example:

```text
Full: Restoration Potion
Menu: Restore Pot.
```

## TQ-16 — Preserve character voice
When applicable preserve:
- formality;
- rudeness;
- timidity;
- authority;
- age impression;
- humor;
- sarcasm;
- arrogance;
- innocence;
- military style;
- technical register.

## TQ-17 — Do not approve ambiguous text without context
When context materially affects meaning, identify:
- speaker;
- listener;
- scene;
- location;
- previous line;
- next line;
- game state.

Otherwise use:

```text
NEEDS_CONTEXT
```

## TQ-18 — Dialogue must work as dialogue
Review conversations as connected exchanges, not isolated strings.

## TQ-19 — UI wording must be functional
Menu labels and commands MUST prioritize clear function while preserving meaning.

## TQ-20 — Abbreviate only when necessary
When space is limited, prioritize:

```text
meaning
> clarity
> consistency
> naturalness
> compactness
```

## TQ-21 — Reference translations are semantic aids
Translations from SNES/PS1/other versions may guide:
- meaning;
- official terminology;
- names;
- intent.

They MUST NOT be assumed structurally identical to the WonderSwan version.

## TQ-22 — Do not invent context
If the correct interpretation cannot be supported, mark it unresolved instead of guessing.

---

# PART V — QG: INTEGRATED PRODUCT / RELEASE QUALITY

## QG-01 — Quality is multidimensional
Release quality requires all applicable dimensions:

```text
LINGUISTIC QUALITY
+
TECHNICAL INTEGRATION
+
VISUAL DESIGN
+
TYPOGRAPHY
+
LAYOUT
+
UI/UX QUALITY
+
GAMEPLAY INTEGRITY
+
ARTISTIC CONSISTENCY
+
RUNTIME STABILITY
+
REGRESSION CONTROL
+
CONTENT COVERAGE
+
REPRODUCIBILITY
```

## QG-02 — Translation must look native to the game
Localized content MUST feel integrated into the original game systems, not pasted on top.

## QG-03 — Respect the original architecture
Do not solve presentation problems with arbitrary hacks that damage:
- pointers;
- tables;
- code;
- memory;
- save behavior;
- control codes;
- nearby resources.

## QG-04 — No integration side effects
A valid change MUST NOT introduce:
- missing text;
- graphical corruption;
- new misalignment;
- crashes;
- gameplay changes;
- save failures;
- regressions in previously approved scenes.

---

# PART VI — DESIGN QUALITY

## QG-10 — Preserve composition
Maintain the original visual logic:
- hierarchy;
- margins;
- alignment;
- distribution;
- grouping;
- relationship between text and icons.

## QG-11 — "It fits" is not enough
A string is not design-approved merely because it remains inside a box.

Evaluate:
- breathing room;
- balance;
- distance from borders;
- relation to neighboring elements.


## QG-13 — Preserve hierarchy
Maintain clear distinction between:
- titles;
- subtitles;
- body text;
- values;
- commands;
- names;
- secondary information.

## QG-14 — Localized redesign is allowed when necessary
The English version may require a layout/design adaptation, but it MUST look intentional and coherent with the original game.

---

# PART VII — TYPOGRAPHY QUALITY

## QG-20 — Native in-game typography is mandatory
Localized text MUST use the same typographic system or a visually faithful extension of the typography used by the original game on the corresponding surface.

A translation MUST NOT introduce a generic, unrelated, substitute or stylistically inconsistent font merely because the text technically fits or is easier to implement.

Typography approval requires consistency with the game's actual visual language.

## QG-20.1 — Preserve the original font identity
When the original game already provides the required Latin glyphs/font resources, localized text MUST use them unless a demonstrated technical limitation makes that impossible.

When new or replacement glyphs are technically required, they MUST be designed to match the native font in all applicable characteristics, including:
- pixel construction;
- stroke thickness;
- glyph height;
- baseline;
- proportions;
- visual weight;
- edge treatment;
- spacing behavior;
- platform-appropriate raster style.

## QG-20.2 — Typography continuity across the same interface
Text added to an existing menu, dialog, label, title card, status area or other surface MUST visually belong to the same typographic family as the surrounding original game content.

A localized word that looks as if it came from a different font, tool, platform or graphic source MUST NOT receive `TYPOGRAPHY = PASS`.

## QG-20.3 — No typography substitution as a shortcut
Do NOT solve translation/integration problems by replacing the original visual typography with a different or generic font.

A broader typography adaptation is permitted only when technically necessary, and it MUST:
- preserve the original game's typographic identity;
- remain visually faithful to the native font family/style;
- be documented;
- explain why the native resources alone are insufficient;
- revalidate all affected surfaces;
- preserve or improve legibility without introducing stylistic discontinuity.

No typography redesign may be used as an exemption from native-style fidelity.

## QG-20.4 — Font mismatch blocks approval
If the localized text does not visually match the typography expected for that game surface:

```text
TYPOGRAPHY = FAIL
VISUAL_APPROVED = false
FINAL_APPROVED = false
status = NEEDS_TYPOGRAPHY_FIX
```

Correct spelling, correct ROM bytes or successful rendering do not override a typography mismatch.

## QG-20.5 — Font reference and provenance are mandatory
Before approving typography for a modified text family or surface, the project MUST identify the native font reference actually used by that surface whenever technically recoverable.

The reference SHOULD record, as applicable:
- font/tile bank or resource;
- glyph table / codepoint mapping;
- tile or cell dimensions;
- bits-per-pixel / palette behavior;
- glyph height and baseline;
- stroke thickness;
- width or VWF metrics;
- spacing/kerning behavior;
- renderer/consumer;
- representative original glyphs;
- hashes or offsets when useful for reproducibility.

When the native game already contains a required Latin glyph, that native glyph MUST be reused unless a documented technical reason prevents it.

A newly designed glyph MUST be a faithful extension of the same native system. It MUST NOT be treated as approved merely because it resembles a generic "retro" or "8-bit" font.

If the native font reference cannot yet be established:

```text
FONT_PRESERVATION = NOT_VALIDATED
TYPOGRAPHY_APPROVED = false
FINAL_APPROVED = false
```

until sufficient evidence is obtained or a technically justified, documented alternative is validated.

## QG-20.6 — Glyph integrity and completeness
Every localized glyph MUST be structurally complete according to the active native font design.

Do not accept:
- missing stems;
- missing crossbars;
- incomplete bowls/counters;
- broken diagonals;
- accidental extra strokes;
- fragments belonging to another glyph/tile;
- malformed joins;
- truncated top/bottom rows;
- corrupted internal whitespace;
- a glyph whose identity depends on knowing the intended word.

Examples such as `A`, `P`, `R`, `W`, `M`, `N`, `S`, `5`, `O` and `0` require particular care because a small pixel defect may change or obscure their identity.

Connected-component counts, edge counts, OCR confidence and similar image metrics MAY be used diagnostically, but no single metric is a universal proof of glyph correctness. The glyph MUST be compared against the native font/reference and its actual rendered form.

A malformed required glyph results in:

```text
GLYPH_INTEGRITY = FAIL
TYPOGRAPHY = FAIL
LEGIBILITY = FAIL when recognition is materially affected
VISUAL_APPROVED = false
FINAL_APPROVED = false
```

## QG-20.7 — Cross-glyph and repeated-glyph consistency
A localized surface MUST NOT mix unrelated glyph construction styles inside the same typographic family.

Characters that belong to the same font family MUST remain coherent in:
- grid;
- pixel scale;
- stroke weight;
- cap height;
- baseline;
- diagonal construction;
- corner treatment;
- counters/openings;
- width logic;
- spacing;
- visual weight.

Repeated instances of the same glyph rendered under the same state SHOULD have the same pixel construction. Unexpected differences between repeated letters (for example the two `S` glyphs in `PASSWORD`) MUST be investigated for:
- wrong tile mapping;
- mixed font banks;
- partial tile overwrite;
- renderer state;
- per-string graphic corruption;
- unintended font substitution.

A one-off hand-edited word MUST NOT receive `TYPOGRAPHY = PASS` if its letters no longer belong to the same coherent font system used by the surrounding interface.

## QG-20.8 — Canonical glyph reference set for modified fonts
If any font graphics, glyph mappings or replacement glyphs are modified, the project MUST maintain a canonical reference set for every affected glyph used by the translation.

The reference set MAY be an extracted atlas, tile sheet, bitmap matrix, documented glyph table or equivalent reproducible representation.

For each affected glyph, the project SHOULD be able to answer:

```text
What is the expected native/approved shape?
Where does it come from?
Which codepoint/tile maps to it?
Does runtime rendering match that approved shape?
```

A glyph that cannot be traced to a native or explicitly approved extension remains `NOT_VALIDATED`.

## QG-21 — Evaluate glyph width
Character count alone does not determine whether text fits.

## QG-22 — Validate spacing
Check:
- letter spacing;
- word spacing;
- icon/text spacing;
- number/symbol spacing;
- accidental double spaces;
- missing spaces.

## QG-23 — Baseline and height
Do not accept:
- vertically floating glyphs;
- clipped glyphs;
- inconsistent baseline;
- malformed glyph height.

## QG-24 — Font changes require global regression testing
If the font, glyph mapping, font graphics, spacing routine or shared text renderer changes, revalidate other surfaces affected by the same typography.

A fix for one word MUST NOT degrade typography or legibility elsewhere.

---

# PART VIII — LAYOUT QUALITY

## QG-30 — No clipping
No approved text may be cut off.

## QG-31 — No overflow
Text MUST NOT invade:
- frames;
- portraits;
- icons;
- numbers;
- other fields;
- reserved regions.

## QG-32 — Good line breaks
Line breaks SHOULD preserve semantic and visual units.

Avoid unnecessary separation of:
- article + noun;
- auxiliary + verb;
- proper names;
- number + unit;
- inseparable expressions.

## QG-33 — Window modifications must remain coherent
If a window is resized or altered, preserve:
- visual style;
- borders;
- symmetry;
- tile consistency;
- reuse compatibility.

## QG-34 — Avoid destructive one-off fixes
Do not fix one string by changing a reusable component in a way that breaks other strings/screens.

## QG-35 — UNIVERSAL LEGIBILITY RULE
All localized text MUST be immediately and correctly readable from the actual rendered game output under realistic viewing conditions.

A legibility `PASS` is a property of the **visible rendered content**, not of:
- source code;
- translation tables;
- decoded ROM bytes;
- expected strings;
- script output;
- disassembly;
- a reviewer already knowing what the word is intended to say.

The absence of clipping, corruption or overflow does NOT by itself prove legibility.

To obtain `LEGIBILITY = PASS`, `LEGIBILITY_APPROVED = true` and `VISUAL_APPROVED = true`, all applicable conditions MUST be satisfied:

- every required character is visibly recognizable;
- the complete word or message can be read correctly from the rendered output;
- words do not require guessing ambiguous/missing letters from prior knowledge;
- glyphs are not excessively merged or visually confused;
- spacing allows clear separation of characters and words;
- baseline and glyph height remain coherent;
- contrast and composition permit reliable reading;
- borders, icons, portraits and graphics do not interfere with recognition;
- abbreviations remain understandable;
- the text remains readable at a scale reasonably representative of actual WonderSwan/emulator output, not only in a heavily enlarged diagnostic capture.

### QG-35.1 — Rendered content is the authority for legibility
Static/source analysis may prove what the program **intends** to display.

It cannot by itself prove what a player can actually read.

Example:

```text
source/decoded value = "PASSWORD"
rendered screen       = ambiguous or malformed glyphs
```

Result:

```text
CONTENT_INTENT = CONFIRMED
LEGIBILITY = FAIL
VISUAL_APPROVED = false
FINAL_APPROVED = false
```

The fact that the code contains the correct word MUST NOT convert the visual result into a pass.

### QG-35.2 — No inferred readability
A GPT, reviewer or QA agent MUST NOT declare a word readable merely because it knows:
- the source Japanese;
- the intended English translation;
- the expected label;
- the underlying decoded string.

The rendered pixels must independently support the claimed reading.

### QG-35.3 — Context-free recognition
All player-visible text, including labels, names, item names, commands, statistics and headings, MUST be recognizable from what is actually rendered on screen without requiring the reviewer to reconstruct the intended word.

Examples:

```text
ARTHUR
PASSWORD
ITEM
CONTINUE
```

If the visible result requires the evaluator to think "this must say PASSWORD because the code says PASSWORD", the result is NOT legibility-approved.

### QG-35.4 — Native-scale validation
Diagnostic zoom may be used to inspect pixels, glyphs and corruption.

However, an enlarged 4x/8x screenshot alone does NOT prove real-world legibility.

Whenever practical, evaluate the text at a size representative of:
- native WonderSwan output;
- normal emulator display;
- intended handheld viewing.

### QG-35.5 — Letterform discrimination
The active font MUST preserve sufficient visual distinction between potentially confusable glyphs when they occur, including cases such as:

```text
I / l / 1
O / 0
S / 5
B / 8
R / P
C / G
U / V
```

The exact pairs depend on the font; this list is not exhaustive.

### QG-35.6 — Shared-font regression
If a glyph, font table, spacing routine, VWF rule or shared renderer is changed to improve one word or screen, all materially affected surfaces MUST be considered for regression testing.

A local readability fix is not approved if it damages readability elsewhere.

### QG-35.7 — Readability uncertainty blocks approval
If rendered evidence is insufficient to decide whether the content is readable:

```text
LEGIBILITY = NOT_VALIDATED
LEGIBILITY_APPROVED = false
VISUAL_APPROVED = false
FINAL_APPROVED = false
status = NEEDS_VISUAL_REVIEW
```

Use `FAIL` only when sufficient rendered evidence exists and the content is actually unreadable, ambiguous or materially difficult to read.

Use `NOT_VALIDATED` when the evidence is missing or inadequate.

Neither state may be silently converted to `PASS`.
### QG-35.8 — Readability is functional quality, not optional polish
A word that is technically present, semantically correct and inside its available display area can still be a quality failure if a normal player cannot read it quickly and reliably.

Readability defects MUST be classified according to impact:
- `BLOCKER` when they prevent required gameplay understanding or progression;
- `MAJOR` when important text cannot be reliably read;
- `MINOR` when readability is reduced but meaning remains clear;
- `POLISH` only when the text is already clearly readable and the change is purely aesthetic.

### QG-35.9 — OCR is corroborating evidence, not an authority
OCR MAY be used to assist QA, but OCR output alone MUST NOT grant:

```text
LEGIBILITY = PASS
LEGIBILITY_APPROVED = true
VISUAL_APPROVED = true
FINAL_APPROVED = true
```

OCR systems may use:
- language models;
- dictionaries;
- lexical priors;
- spell correction;
- word-frequency priors;
- surrounding UI context;
- neighboring characters;
- expected labels;
- post-processing.

Those mechanisms can reconstruct the *likely intended word* even when one or more rendered glyphs are malformed.

Therefore:

```text
OCR_MATCH == EXPECTED_TEXT
```

does **not** imply:

```text
GLYPH_INTEGRITY = PASS
CONTEXT_FREE_RECOGNITION = PASS
LEGIBILITY = PASS
```

If the OCR engine cannot disable or expose contextual correction, its result MUST be classified as `OCR_CONTEXT_ASSISTED` and used only as supporting evidence.

### QG-35.10 — Mandatory context-independent recognition
A legibility `PASS` requires the rendered pixels to support the reading independently of the expected translation.

For every modified text element used as direct evidence for `LEGIBILITY = PASS`, the evaluator MUST first be capable of producing a literal visible transcription without using the expected source/translation as a correction key.

For text whose font/glyph graphics were modified, or whenever glyph integrity is in doubt, a formal blind/context-masked check is mandatory when practical:

1. capture the actual rendered output;
2. preserve a native/representative-scale view;
3. make a diagnostic crop/zoom if needed;
4. hide or avoid the expected decoded string, filename, patch note and translation label during the first recognition pass;
5. transcribe only what the pixels visibly support;
6. mark uncertain characters explicitly (`?`, `AMBIGUOUS`, `BROKEN`, `MISSING`);
7. only after that transcription, compare against the intended string.

Example:

```text
expected_text        = PASSWORD
visible_transcription = P?SSW?RD
contextual_ocr        = PASSWORD
```

Result:

```text
CONTEXT_FREE_RECOGNITION = FAIL
LEGIBILITY = FAIL
VISUAL_APPROVED = false
FINAL_APPROVED = false
```

The expected word MUST NOT be used to fill uncertain letters and then retroactively claim that those letters were readable.

### QG-35.11 — Glyph-by-glyph identity must support word identity
A word-level reading is valid only when its required glyph sequence is visually supported.

For typography-modified or suspicious text, inspect the relevant glyphs individually and record, when practical:

```text
PASS
AMBIGUOUS
BROKEN
MISSING
WRONG_GLYPH
```

The evaluator SHOULD be able to derive:

```text
glyph identities -> word
```

rather than:

```text
expected word -> guessed glyph identities
```

A stylized native glyph does not need to resemble a generic computer font. It does, however, need to remain identifiable within the game's documented font system and distinguishable from other glyphs that could plausibly occur in the same context.

If a required glyph is materially ambiguous or malformed, the word MUST NOT receive a legibility `PASS` merely because the remaining letters make the intended word obvious.

### QG-35.12 — OCR anti-context protocol
When OCR is used as QA evidence, record the engine/method and distinguish raw visual recognition from contextual correction.

When the tool supports it, the first OCR pass SHOULD minimize semantic reconstruction by using appropriate settings such as:
- dictionary/language-model correction disabled;
- raw character recognition;
- constrained character set only when the character set is a real property of the game, not a way to force the expected word;
- no expected-word prompt;
- no filename/translation hint containing the answer;
- crop limited to the actual rendered text where appropriate.

A second context-enabled OCR pass MAY be used for comparison.

Interpretation:

```text
raw/context-minimized OCR correct + glyph review correct
    -> may corroborate legibility

context-enabled OCR correct but raw/glyph review ambiguous
    -> suspected contextual false positive; no legibility PASS

OCR disagreement with clearly readable native-font glyphs
    -> OCR failure; do not penalize the game solely for OCR weakness
```

OCR is never mandatory when direct rendered review provides stronger evidence.

### QG-35.13 — Semantic plausibility cannot repair visual ambiguity
Language plausibility is not visual evidence.

The following are prohibited as reasons to convert ambiguous pixels into a pass:
- "that menu normally says PASSWORD";
- "the source string says PASSWORD";
- "only PASSWORD makes sense here";
- "OCR autocorrected it to PASSWORD";
- "the other letters make the missing letter obvious";
- "the translation table proves the word".

Those facts may confirm `CONTENT_INTENT`, but not `GLYPH_INTEGRITY` or `LEGIBILITY`.

### QG-35.14 — Repeated-character comparison is a required diagnostic
When the same character appears more than once in a rendered word/line or in nearby text using the same font state, compare those instances when investigating suspected corruption.

Unexpected pixel-shape differences MUST be explained by a legitimate renderer/font behavior or treated as evidence of possible corruption.

This diagnostic is particularly useful for:
- repeated letters in one word;
- common UI labels;
- recurring names;
- digits;
- punctuation;
- shared menu commands.

The absence of pixel identity is not automatically a failure when legitimate state/kerning/compositing behavior changes the bitmap, but unexplained inconsistency blocks typography approval.

---

# PART IX — ARTISTIC QUALITY

## QG-40 — Preserve platform/game identity
Localization assets SHOULD remain consistent with:
- WonderSwan-era resolution;
- platform palette;
- original artistic direction;
- original pixel-art language.

## QG-41 — Pixel-art discipline
Localized graphics MUST respect:
- original resolution;
- pixel grid;
- tile size;
- color limits;
- pixel-art style;
- platform-appropriate anti-aliasing behavior.

## QG-42 — Logo localization
A localized logo SHOULD preserve:
- personality;
- proportions;
- visual weight;
- composition;
- intent.

Do not replace a distinctive logo with generic typography.

## QG-43 — Preserve iconography
Do not alter original icons unless localization requires it.

## QG-44 — Avoid visually foreign assets
Avoid modern-looking fonts, smoothing, Unicode glyphs or graphic elements that visibly clash with the original game.

---

# PART X — UI / UX QUALITY

## QG-50 — Immediate comprehension
The player MUST be able to understand:
- what is selected;
- what action will occur;
- what value is shown;
- how navigation works.

## QG-51 — Command consistency
The same action SHOULD keep the same name across interfaces unless a documented constraint requires otherwise.

## QG-52 — Preserve UI states
Validate:
- selected;
- unselected;
- active;
- inactive;
- disabled;
- highlighted.

## QG-53 — Navigation integrity
Localization MUST NOT accidentally alter:
- cursor positions;
- hitboxes;
- menu order;
- selection coordinates;
- navigation logic.

## QG-54 — Functional clarity beats decorative wording
A visually elegant but functionally ambiguous label is a quality failure.

---

# PART XI — GAMEPLAY INTEGRITY

## QG-60 — Localization must not alter gameplay
Do not accidentally change:
- damage;
- statistics;
- AI;
- collision;
- timers;
- spawn behavior;
- progression;
- flags;
- scripts;
- win/loss conditions.

## QG-61 — Save/load validation
When applicable validate:
- New Game;
- Save;
- Load;
- Continue;
- cold boot;
- existing save compatibility.

---

# PART XII — RUNTIME AND VISUAL QA

## QG-70 — Boot is only a minimum check
A successful boot is NOT equivalent to full QA.

## QG-71 — Representative runtime validation
Every modified family MUST receive representative runtime validation before RC/final approval, unless runtime validation is genuinely not applicable and `N/A` is explicitly justified.

## QG-72 — Cover late-game states
QA SHOULD include, when applicable:
- title;
- menus;
- options;
- gameplay;
- dialogue;
- inventory;
- equipment;
- battle UI;
- shops;
- tutorials;
- transitions;
- Stage Clear;
- Game Over;
- Continue;
- Save/Load;
- late-game areas;
- ending;
- credits.

## QG-73 — Visual review criteria
Visual review MUST evaluate the actual rendered output. Static code/string inspection cannot grant a visual or legibility pass.

Check:
- clipping;
- overflow;
- overlap;
- spacing;
- alignment;
- width;
- line breaks;
- corrupted glyphs;
- damaged icons;
- wrong tiles;
- legibility under `QG-35`.

A visual review MUST NOT pass if the reviewer can identify a word only because the expected translation is already known.

## QG-74 — Evidence
A visual/legibility `PASS` MUST be based on actual rendered evidence from the game/emulator.

The evidence may be observed directly during QA. When practical, preserve reproducible evidence such as:
- screenshot;
- GIF;
- video;
- log;
- save state/checkpoint;
- reproducible route.

Preserving the artifact is strongly recommended, but the mandatory requirement is that the claimed visual/legibility pass was actually evaluated from rendered output.

---

# PART XIII — NATURAL VS SYNTHETIC QA

## UR-30 — Label access method
When relevant, distinguish:

```text
NATURAL
SCRIPTED_NATURAL
SAVESTATE
CHEAT
WRAM_POKE
FREEZE
SYNTHETIC_STATE
POINTER_INJECTION
STATIC_ONLY
NOT_VALIDATED
```

## UR-31 — Synthetic proof has limited scope
Synthetic validation may prove:
- resource existence;
- decoder behavior;
- renderer compatibility;
- consumer behavior.

It does NOT prove that the scene was naturally reached in normal gameplay.


### UR-31.1 — Rendered synthetic evidence can validate rendering, not natural reachability
If a synthetic state, pointer injection, WRAM manipulation or equivalent method causes the game's real renderer to draw the actual resource, that rendered output MAY be used to validate applicable properties such as:
- typography;
- glyph integrity;
- layout;
- clipping/overflow;
- legibility;
- visual composition.

It still does NOT prove:
- natural gameplay reachability;
- correct progression into that state;
- complete route coverage;
- full gameplay validation.

## UR-32 — Never misrepresent synthetic coverage
Do not report synthetic access as if it were a normal playthrough.

---

# PART XIV — UNIVERSAL ANTI-BLOCKING POLICY

## UR-40 — No test may block the project indefinitely
A hard-to-reach state MUST NOT stop development indefinitely.

## UR-41 — Bounded natural attempt
Whenever navigation or QA can block, loop or consume unbounded time, natural/manual/automated attempts MUST have a defined time, frame or attempt limit.

## UR-42 — Escalate methods
If natural access fails, progressively consider:
1. savestate/checkpoint;
2. scripted input;
3. cheats/flags;
4. WRAM poke/freeze;
5. breakpoints/watchpoints;
6. consumer tracing;
7. minimal pointer substitution;
8. controlled state injection;
9. static analysis.


### UR-42.1 — Fallback analysis does not grant visual approval
Static analysis, disassembly, decoder inspection, pointer tracing, table inspection or other non-rendered fallback methods may be used to continue development and to confirm content intent/structure.

They MUST NOT by themselves grant:

```text
LEGIBILITY = PASS
LEGIBILITY_APPROVED = true
VISUAL_APPROVED = true
FINAL_APPROVED = true
```

Those statuses require the corresponding rendered/runtime evidence defined elsewhere in this document.

## UR-43 — Do not repeat equivalent failures indefinitely
After repeated equivalent failures, change methodology.

## UR-44 — Use safeguards
Any task with a realistic risk of blocking, looping indefinitely, producing unbounded logs or losing significant progress MUST use appropriate safeguards, such as:
- timeout;
- watchdog;
- frame limit;
- log limit;
- checkpointing;
- partial-result persistence.

Use only the safeguards applicable to the task, but do not run potentially unbounded work without a control mechanism.

## UR-45 — Tool failure does not stop unrelated work
Document the failure, preserve evidence, switch to alternatives, and continue independent work.

---

# PART XV — METRICS AND COMPLETION PERCENTAGES

## UR-50 — No percentage without a defensible denominator
Never report a global completion percentage without a known total universe.

## UR-51 — Label the metric
Examples:

```text
inventory_coverage
confirmed_text_coverage
script_coverage
family_coverage
runtime_coverage
visual_coverage
global_coverage
```

## UR-52 — Inventory is not automatically global scope
`X translated / Y discovered candidates` is only an inventory percentage unless exhaustiveness is proven.

## UR-53 — Shift-JIS candidates are not a global denominator
Raw candidate counts MUST NOT automatically define project completion.

---

# PART XVI — REGRESSION CONTROL

## QG-80 — Validate against previous stable version
Every formal version that has a previous approved/stable version MUST perform regression comparison against that prior version for all materially affected areas.

## QG-81 — A fix may not create an equal-or-worse defect
A new correction is not accepted if it introduces an equivalent or more severe regression.

## QG-82 — Revalidate globally affected surfaces
Global changes to:
- font;
- renderer;
- common UI;
- shared tables;
- allocators;
- text engine

require revalidation of previously approved surfaces they may affect.

---

# PART XVII — TOOL AND EVIDENCE PROVENANCE

## UR-60 — Do not claim tools that were not used
Only attribute evidence to tools actually executed.

## UR-61 — Record methodology
Important results SHOULD record:
- tool;
- version;
- command;
- input;
- output;
- result.

## UR-62 — Tools are evidence sources, not unquestionable authorities
Automated output MUST be reconciled with structural/runtime evidence.

---

# PART XVIII — EVIDENCE PRESERVATION

## UR-70 — Preserve useful project history
When reasonable retain:
- CSV inventories;
- logs;
- rejected candidates;
- screenshots;
- save states;
- hashes;
- analyses;
- negative results;
- prior versions.

## UR-71 — Trace reclassification
If a candidate changes status, preserve:
- previous state;
- new state;
- reason;
- evidence;
- version.

## UR-72 — Negative results matter
Record disproven hypotheses to prevent future repetition.

---

# PART XIX — VERSIONING AND HANDOFF

## UR-80 — Versions must represent real changes
Do not increment versions without meaningful change in:
- ROM;
- sources;
- translation;
- tooling;
- QA;
- evidence.

## UR-81 — Changelog required
A formal version SHOULD state:
- what changed;
- what was fixed;
- what was validated;
- what remains pending.

## UR-82 — Explicit project state
Handoffs SHOULD identify:
- current version;
- original ROM;
- hashes;
- current phase;
- completed work;
- pending work;
- blockers;
- evidence;
- build instructions;
- patch instructions;
- recommended next step.

## UR-83 — Migration-ready project
Important work SHOULD be resumable in another chat/Work environment without relying exclusively on hidden prior context.

---

# PART XX — QUALITY GATE PER ELEMENT

An element may be considered FINAL_APPROVED only when all applicable checks pass:

```text
SOURCE_UNDERSTOOD       = PASS
SEMANTIC_ACCURACY       = PASS
TRANSLATION             = PASS
TERMINOLOGY             = PASS
LINGUISTIC_QUALITY      = PASS
INTEGRATION             = PASS
FONT_PRESERVATION       = PASS
GLYPH_INTEGRITY         = PASS
TYPOGRAPHY              = PASS
CONTEXT_FREE_RECOGNITION = PASS
LAYOUT                  = PASS
LEGIBILITY              = PASS
DESIGN                  = PASS
VISUAL                  = PASS
FUNCTIONAL              = PASS
RUNTIME                 = PASS or JUSTIFIED_N/A
REGRESSION              = PASS
EVIDENCE_SUFFICIENT     = PASS
```

If any applicable mandatory field is `FAIL` or `NOT_VALIDATED`:

```text
FINAL_APPROVED = false
```

`N/A` is permitted only with explicit justification.

`FINAL_APPROVED` is derived from the complete gate result; it MUST NOT be manually asserted.

---

# PART XXI — RELEASE QUALITY GATE

Before declaring a release candidate or final translation:

```text
ROM_INTEGRITY           = PASS
CHECKSUM                = PASS
BUILD                   = PASS
BPS_ROUNDTRIP           = PASS

LANGUAGE                = PASS
TERMINOLOGY             = PASS
DESIGN                  = PASS
FONT_PRESERVATION       = PASS
GLYPH_INTEGRITY         = PASS
TYPOGRAPHY              = PASS
CONTEXT_FREE_RECOGNITION = PASS
LAYOUT                  = PASS
LEGIBILITY              = PASS
UI_UX                   = PASS
GRAPHICS                = PASS
GAMEPLAY                = PASS
RUNTIME                 = PASS or JUSTIFIED_N/A
REGRESSION              = PASS

CONFIRMED_JP_PENDING    = 0
BLOCKER_ISSUES          = 0
MAJOR_ISSUES            = 0
```

MINOR/POLISH issues MAY remain only when explicitly documented and the build is not misrepresented as defect-free.

---

# PART XXII — ISSUE SEVERITY

## BLOCKER
Examples:
- ROM does not boot;
- crash;
- broken save/load;
- blocked progression;
- severe corruption;
- functionally wrong text that prevents correct play.

## MAJOR
Examples:
- mistranslation;
- important omission;
- significant clipping;
- broken layout;
- missing UI element;
- wrong proper name;
- important text that cannot be read reliably at realistic display scale;
- ambiguous or malformed glyphs that force the player to infer the intended word;
- substantially degraded screen.

## MINOR
Examples:
- spacing defect;
- punctuation;
- minor alignment;
- non-functional consistency issue.

## POLISH
Optional refinement:
- improved phrasing;
- minor pixel-art refinement;
- fine spacing adjustment.

---

# PART XXIII — GPT / AGENT OPERATING RULES

A GPT/agent working on these projects MUST treat quality as integrated product quality, not text replacement.

Before approving a change, evaluate:

```text
1. Is the meaning correct?
2. Is the terminology consistent?
3. Is it technically integrated correctly?
4. Does it preserve the original design intent?
5. Does the localized text use the same native typography/style as the corresponding original game surface?
6. Is the native font reference/provenance identified and preserved?
7. Is every required glyph structurally complete and individually identifiable within that font system?
8. Do repeated glyphs and neighboring glyphs remain internally consistent?
9. Is typography technically and visually consistent with surrounding in-game text?
10. Is layout balanced and readable?
11. Can the visible text be transcribed correctly before consulting the expected word/source string?
12. If OCR was used, was contextual reconstruction prevented or explicitly treated only as corroborating evidence?
13. Is every important word actually legible from the rendered pixels without relying on source code or prior knowledge of what it should say?
14. Was readability checked at a realistic display scale, not only under diagnostic zoom?
15. Is it visually professional?
16. Is UI behavior intact?
17. Is gameplay intact?
18. Was it actually tested?
19. Did it introduce regressions?
20. Is the evidence sufficient for the claimed status?
```

Additional agent rules:

- Do NOT invent missing context.
- Do NOT mark doubtful text as approved.
- Do NOT prefer shorter wording solely because it fits.
- Do NOT modify placeholders/control codes blindly.
- Do NOT equate "no Japanese found" with "translation complete".
- Do NOT equate "build succeeds" with "quality approved".
- Do NOT equate "boots" with "runtime QA complete".
- Do NOT equate "inside box" with "good design".
- Do NOT equate absence of clipping with legibility.
- Do NOT approve a word as readable merely because source code, a table, a decoder or prior knowledge identifies the intended word.
- Do NOT allow OCR/GPT/human semantic reconstruction to fill ambiguous or malformed letters and then count that reconstructed word as visual proof.
- Do NOT treat an OCR match as proof of glyph integrity.
- Do NOT prompt an OCR/vision step with the expected answer when that same step is intended to prove legibility.
- Do NOT hide uncertainty: transcribe ambiguous rendered characters explicitly as `?`/`AMBIGUOUS`/`BROKEN` before comparing with the expected string.
- Do NOT use static code/string inspection as a substitute for rendered legibility validation.
- Do NOT approve localized typography that visibly differs from the native font/style used by the game on that surface.
- Do NOT mix unrelated pixel-font construction styles within one native font family/surface.
- Do NOT approve malformed `A`, `P`, `R`, `W`, `M`, `N` or other glyphs simply because the word can be guessed from context.
- Do NOT substitute a generic font merely because it is technically easier to render.
- Do NOT use heavily enlarged screenshots as the sole proof of readability.
- Do NOT report synthetic validation as natural playthrough.
- Do NOT claim use of a tool that was not actually run.
- Preserve intermediate evidence and unresolved candidates.

- Use `FAIL` only when sufficient evidence demonstrates non-compliance.
- Use `NOT_VALIDATED` when evidence is insufficient.
- Never convert missing evidence into `PASS`.
- Never grant `FINAL_APPROVED` directly; derive it from all mandatory applicable gates.
- When blocked, change method instead of repeating indefinitely.

---

# PART XXIV — RECOMMENDED RECORD FORMAT

When practical, translation records SHOULD support:

```yaml
id:
offset:
resource:
consumer:
speaker:
context:

source_jp:
literal_gloss:
translation_en:

terminology_refs:
character_voice:

status:
confidence:

translated:
integrated:
runtime_confirmed:
linguistic_approved:
design_approved:
font_reference:
font_reference_provenance:
font_preservation_status: # PASS / FAIL / NOT_VALIDATED / N/A
glyph_integrity_status:   # PASS / FAIL / NOT_VALIDATED / N/A
typography_status:        # PASS / FAIL / NOT_VALIDATED / N/A
typography_approved:

expected_text:
visible_transcription:
context_free_recognition_status: # PASS / FAIL / NOT_VALIDATED / N/A
ocr_used:
ocr_engine_version:
ocr_mode:                 # RAW / CONTEXT_MINIMIZED / CONTEXT_ASSISTED / N/A
ocr_raw_output:
ocr_support_status:       # CORROBORATES / CONFLICTS / CONTEXTUAL_FALSE_POSITIVE / NOT_USED

legibility_status:        # PASS / FAIL / NOT_VALIDATED / N/A
legibility_approved:
visual_status:            # PASS / FAIL / NOT_VALIDATED / N/A
visual_approved:
functional_approved:
final_approved:

access_method:
issues:
notes:
evidence:
version:
```

---

# PART XXV — FINAL COMPLETION CRITERIA

A project MUST NOT be called 100% complete merely because no obvious Japanese remains.

A final-quality release MUST satisfy:

```text
structural census reasonably closed
+
confirmed Japanese pending = 0
+
ambiguous candidates classified/documented
+
linguistic review complete
+
terminology review complete
+
design review complete
+
native typography continuity review complete
+
native font reference/provenance documented for modified font families
+
glyph integrity and repeated-glyph consistency review complete
+
typography/layout review complete
+
context-independent recognition review complete for modified/suspicious text
+
legibility review complete from actual rendered content at realistic display scale
+
representative runtime QA complete
+
late-game/ending/credits reviewed
+
save/load tested when applicable
+
critical regressions = 0
+
checksum valid
+
build reproducible
+
cumulative BPS verified
+
complete cumulative sources present
+
handoff/documentation complete
```

---

# PART XXVI — RULE HIERARCHY

```text
Universal Rules (this file)
        ↓
Project-specific technical rules
        ↓
Phase-specific instructions
        ↓
Individual implementation decisions
```

Project-specific rules MAY be stricter.

They MUST NOT weaken this file.

If old documentation conflicts with reproducible evidence, investigate, document the discrepancy, and update the project knowledge explicitly.

---


# PART XXVII — NORMATIVE CONSISTENCY RULES

## NR-01 — Mandatory keywords

Interpret normative keywords as follows:

```text
MUST / MUST NOT
    Mandatory requirement.

SHOULD / SHOULD NOT
    Strong recommendation. Deviation is permitted only when justified and documented.

MAY
    Optional behavior.

PASS
    Requirement was tested with sufficient evidence and satisfied.

FAIL
    Requirement was tested with sufficient evidence and not satisfied.

NOT_VALIDATED
    Evidence is insufficient to decide PASS/FAIL.

N/A
    Requirement does not apply; justification required.
```

A `SHOULD` MUST NOT be used to bypass a later mandatory release gate.

If a release gate requires a field to be `PASS`, the work needed to establish that `PASS` is mandatory for that release class.

## NR-02 — Evidence precedence

For different claims, use the appropriate evidence:

```text
Source/code/table evidence
    proves intended/static content or structure.

Rendered evidence
    proves what the game actually draws.

Legibility evidence
    proves that the rendered content can be read correctly without reconstructing the answer from expected text.

Glyph/font reference evidence
    proves whether the rendered characters preserve the approved native font identity and glyph structure.

OCR evidence
    may corroborate recognition, but does not independently prove legibility or glyph integrity when contextual correction may be involved.

Natural runtime evidence
    proves that the state can be reached/observed through the tested gameplay route.
```

One evidence class MUST NOT be silently substituted for another.

## NR-03 — Approval dependency

The approval hierarchy is:

```text
CONTENT/STRUCTURE CONFIRMATION
        ↓
TRANSLATION / INTEGRATION
        ↓
TYPOGRAPHY / LEGIBILITY / DESIGN / FUNCTION
        ↓
RUNTIME / VISUAL / REGRESSION
        ↓
FINAL_APPROVED
```

`FINAL_APPROVED` is never independent.

## NR-04 — Unknown is not failure, but still blocks release

```text
FAIL          = proven defect
NOT_VALIDATED = insufficient evidence
```

They are different diagnoses.

Both block any mandatory release gate until resolved or explicitly justified as `N/A`.

## NR-05 — Project-specific rules

Project-specific rules MAY be stricter than this document.

They MUST NOT:
- reduce a mandatory universal requirement to optional;
- convert `NOT_VALIDATED` into `PASS`;
- bypass rendered legibility requirements;
- bypass native typography fidelity;
- bypass release reproducibility;
- redefine synthetic access as natural gameplay.

## NR-06 — Anti-false-pass evidence separation
The following evidence categories MUST remain separate:

```text
EXPECTED_TEXT
    what the project intends to display

VISIBLE_TRANSCRIPTION
    what can actually be read from the rendered pixels before answer correction

GLYPH_REFERENCE
    what the native/approved glyph shape should be

OCR_RAW
    what an OCR system recognized before contextual post-correction, when available

OCR_CONTEXT_ASSISTED
    what an OCR/language model reconstructed with linguistic/contextual assistance
```

Rules:

- `EXPECTED_TEXT` MUST NOT overwrite or normalize `VISIBLE_TRANSCRIPTION`.
- `OCR_CONTEXT_ASSISTED` MUST NOT be promoted to `VISIBLE_TRANSCRIPTION`.
- A correct `EXPECTED_TEXT` plus a correct contextual OCR result cannot compensate for malformed glyphs.
- If `VISIBLE_TRANSCRIPTION` contains materially ambiguous characters, `CONTEXT_FREE_RECOGNITION` cannot be `PASS`.
- If glyph structure differs materially from the native/approved reference, `GLYPH_INTEGRITY` and/or `FONT_PRESERVATION` cannot be `PASS`.
- Automated pipelines MUST preserve raw/uncertain recognition results rather than silently autocorrecting them to the expected string.

A false positive caused by semantic reconstruction is a QA defect and MUST be corrected in the validation method, not accepted as evidence.

# FINAL OPERATING PRINCIPLE

Every project SHOULD follow this sequence:

```text
KNOWN BASE
→ STRUCTURAL ANALYSIS
→ SOURCE UNDERSTANDING
→ NATURAL LOCALIZATION
→ SAFE INTEGRATION
→ DESIGN/TYPOGRAPHY REVIEW
→ GLYPH/FONT INTEGRITY REVIEW
→ CONTEXT-INDEPENDENT LEGIBILITY REVIEW
→ RUNTIME QA
→ VISUAL QA
→ REGRESSION CONTROL
→ REPRODUCIBLE CUMULATIVE PATCH
→ PRESERVED EVIDENCE
→ RELEASE QUALITY GATE
```

Five non-negotiable principles:

```text
1. Integrated text is not automatically approved text.
2. Synthetic validation is not automatically a real playthrough.
3. Failure to find something is not proof that it does not exist.
4. Expected text or context-assisted OCR is not proof that rendered glyphs are readable.
5. A readable word is not typography-approved if its glyphs do not preserve the native font system.
```

And the final quality target is:

```text
NOT:
"Japanese game with English text inserted"

TARGET:
"A coherent English WonderSwan release that preserves the original game's
design, function, artistic identity and platform constraints."
```
