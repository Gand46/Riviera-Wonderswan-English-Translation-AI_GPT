# Aprobación visual y lingüística acotada — RC4/RC5

## Resultado

**PASS** sólo para el alcance probado: encuentro Hades ya integrado en RC3, conjunto completo de owners del diálogo posterior al final, cinco ramas de cierre y 32 páginas fullscreen de epílogo. RC5 añade únicamente la fila modificada de la página 8 de créditos. No es una aprobación global del proyecto.

| Comprobación | Resultado |
|---|---:|
| Streams posteriores al final | 102/102 validados |
| Ejecución por estado controlado (`SYNTHETIC_STATE`) | 94 |
| Inyección de puntero con renderer nativo (`POINTER_INJECTION`) | 8 |
| Páginas condicionales inspeccionadas sintéticamente | 12/12 |
| Capturas controladas únicas inspeccionadas | 167 |
| Hojas de contacto controladas inspeccionadas | 10/10 |
| Páginas de epílogo en segunda lectura ciega | 32/32 |
| Discordancias de lectura | 0 |
| Recortes, corrupción o ilegibilidad | 0 |
| Japonés visible en el alcance final | 0 |

## Recorridos posteriores al final

Las rutas 0..4 se ejecutaron en Mesen 2.1.1 contra el hash exacto de RC4 después de inyección controlada de estado. Todas retornaron desde el secuenciador nativo. El registro exige observar la dirección inicial exacta; no se afirma alcanzabilidad natural.

El estado controlado activó 94 de los 102 streams. Ocho mensajes de NPC dependen de banderas que no coexistían en ese estado; se probaron mediante inyección temporal de puntero en owners ejecutados de la misma escena. La prueba utilizó el renderer real, verificó las direcciones iniciales y produjo 12 capturas. La ROM diagnóstica se eliminó.

RC5 no modifica esos recursos ni su renderer, por lo que no repite esas pruebas. Sólo la página 8 de créditos se reejecutó; su reconocimiento independiente devolvió un único candidato, `Shinya Fukao`, con márgenes simétricos de 14 px, cero recorte, cero solapamiento y fuente nativa intacta.

## Segunda lectura de las 32 páginas

Las 32 capturas únicas se renombraron y barajaron con una semilla fija. La transcripción visible, legibilidad, recorte y presencia de japonés se registraron y se sellaron por SHA-256 antes de abrir la tabla que relacionaba cada captura con su stream y texto esperado.

La comparación posterior aceptó sólo equivalencias tipográficas visibles (`…`/`...`, `∼`/`~`, `—`/`-`). Letras, palabras y saltos de línea debían coincidir. Resultado: **32/32 PASS**. Es una segunda lectura ciega respecto de la tabla fuente; no se presenta como revisión de otra persona.

## Evidencia autoritativa

- `validation/S460/FINAL_DIALOG_COVERAGE.json`
- `validation/S460/DIALOG_VISUAL_REVIEW.json`
- `validation/S460/LINGUISTIC_REVIEW.json`
- `validation/S460/GLOBAL_VISUAL_LINGUISTIC_APPROVAL.json`
- `validation/S460/blind_epilogue_review/EPILOGUE_32_SECOND_READING.json`
- `validation/S460/optional_npc_synthetic/OPTIONAL_NPC_SYNTHETIC_VALIDATION.json`

La transcripción editorial consultada fue [Riviera: The Promised Land — Game Script (GBA)](https://gamefaqs.gamespot.com/gba/921257-riviera-the-promised-land/faqs/46447/epilogue).
