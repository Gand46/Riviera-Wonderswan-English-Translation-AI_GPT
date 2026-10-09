> Historical report for its stated version. Current I04/I05 status: [S463](10_S463_ASTRA_I04_I05.md).

# S462 / RC6 — corrección de la regresión del selector compacto

## Resultado

`R01_COMPACT_SELECTOR_PARENT_RANGE_LOSS = PASS`.

S460 sustituyó el salto que conservaba la tabla de rangos compactos de `ES=C000`. Como consecuencia, 22 streams ingleses almacenados en `[0x7CB227,0x7CB529)` y `[0x7CDBE1,0x7CDC00)` pasaron por la ruta nativa y aparecieron como glifos japoneses. S462 restaura la tabla previa y conserva el nuevo tramo S460 `[0x7CED22,0x7D0000)`.

## Cambio binario

- Base RC5: `2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf`.
- RC6: `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204`.
- Preimagen `0x75EAF1`: `EB0081FF22ED7299EBE1`.
- Postimagen: `81FF22ED73E5EBCBFFFF`.
- Diff RC5→RC6: 12 bytes: diez del selector y dos del checksum.
- Los 22 streams son byte-idénticos entre RC5 y RC6.

## Validación

- 18 casos de límites y los 801 offsets de los rangos perdidos pasaron el intérprete de las instrucciones reales.
- Mesen 2.1.1 reprodujo RC5 y RC6 desde checkpoints existentes, sin escrituras a ROM.
- Control RC5 `0x7CB227`: ruta `NATIVE`, glifos japoneses.
- RC6 `0x7CB227`: ruta `COMPACT`, “Use selected / items only.”.
- RC6 `0x7CDBE1`: ruta `COMPACT`, “We wasted time. / We must hurry.”.
- Las cuatro líneas coinciden exactamente con 581 píxeles de primer plano de la fuente nativa; cero diferencias, recorte o solapamiento.
- La aprobación visual nueva es representativa: 2/22, una entrada natural de cada rango. Los otros 20 tienen prueba estructural de integración, no un nuevo PASS visual individual.

## Release

- Build acumulativo S441→S462: `PASS_BYTE_EXACT`.
- BPS acumulativo directo JP→RC6: `PASS_BYTE_EXACT`.
- BPS SHA-256: `2a36c3ada7d4448fc629957854b3c8885ac7e58a0979fd64d52940bff15f2b4f`.
- Checksum WonderSwan RC6: `289A`.

`FINAL_APPROVED=false`. I04 continúa `NOT_VALIDATED`; I05 conserva `Shinya Fukao = PASS` y dos lecturas `NOT_VALIDATED`. High Score y la segunda revisión humana siguen como seguimientos separados.
