# Informe de cierre — Riviera Work Pt1.5, v0.115 S462 RC6

## Dictamen

RC6 corrige la regresión del selector compacto introducida en S460/RC4 e incluida en S461/RC5. Veintidós streams continuaban almacenados en inglés, pero dos rangos habían sido derivados a los glifos japoneses. S462 recupera la ruta compacta anterior y mantiene el tramo añadido por S460.

`R01_COMPACT_SELECTOR_PARENT_RANGE_LOSS = PASS`. El diff RC5→RC6 se limita a diez bytes del selector y dos bytes de checksum. Los 22 streams permanecen byte-idénticos.

La reproducción A/B en Mesen 2.1.1 confirma `NATIVE` en RC5 y `COMPACT` en RC6. Dos streams alcanzados naturalmente, uno de cada rango, pasaron fidelidad de fuente nativa, integridad de glifos, reconocimiento independiente exacto, legibilidad, layout y regresión. Los otros veinte no reciben un PASS visual individual nuevo.

| Métrica | Resultado |
|---|---:|
| Streams afectados con integración estructural restaurada | 22/22 `PASS` |
| Representantes visuales naturales de ambos rangos | 2/2 `PASS` |
| Offsets de rangos perdidos comprobados | 801/801 |
| Build fuente acumulativo | `PASS_BYTE_EXACT` |
| BPS acumulativo | `PASS_BYTE_EXACT` |
| I04 | `NOT_VALIDATED` |
| Lecturas I05 confirmadas | 1/3 |

`FINAL_APPROVED=false`: I04 y dos lecturas I05 continúan abiertas. La ausencia de evidencia no se convirtió en PASS. La evidencia previa de 102 owners y 32 páginas de epílogo se conserva dentro de su alcance byte-idéntico; no constituye aprobación global.

## Identidad

- ROM RC6: `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204`.
- Checksum WonderSwan: `289A`.
- BPS JP→RC6: `2a36c3ada7d4448fc629957854b3c8885ac7e58a0979fd64d52940bff15f2b4f`.
- ROM JP requerida: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.
