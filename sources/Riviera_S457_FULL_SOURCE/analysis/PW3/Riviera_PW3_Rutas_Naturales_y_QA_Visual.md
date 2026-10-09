# Riviera Work Pt1.5 — PW3 Rutas naturales cortas y QA visual dirigida

**Fecha:** 2026-09-25  
**Estado:** `PW3 COMPLETADA` — presupuesto consumido `3/5`  
**ROM modificada:** no  
**Siguiente etapa:** `PW4 — Consolidación y dictamen de alcance Work`

## Resultado ejecutivo

PW3 agotó las tres rutas acotadas y sus reintentos útiles. La progresión natural reproducible avanzó desde el checkpoint descendiente de `DATA:1` hasta el segundo combate de `Start 1-1`. Se validaron en ejecución y por lectura directa las superficies alcanzables de guardado, Start, mapa, diálogos, tutorial, selección de objetos, combate, victoria, Quest y diálogo de NPC.

No apareció Team Edit por progresión ordinaria. La captura controlada heredada sigue siendo legible, pero no concede el cierre natural: `I20-NATURAL-TEAM = NOT_VALIDATED`. El hito alcanzado no deja I22 a dos hitos reproducibles, por lo que PW5 no se activa.

No se demostró ningún defecto nuevo de traducción o renderizado. S457 permanece byte idéntica y se conserva el mismo BPS acumulativo.

## Presupuesto ejecutado

| Ruta | Resultado | Presupuesto |
| --- | --- | --- |
| 1 · arranque en frío | La SRAM de 32 KiB cargó byte a byte; la automatización del menú saltó dos filas y abrió Extra Contents. Se clasifica como sincronización de entrada, no defecto de ROM. | 3 intentos acotados; sin exceder 20.000 cuadros por intento |
| 2 · DATA:1/Start 1-1 | Start → mapa → diálogo → tutorial → Item Select → primer combate → victoria → diálogo posterior. | 5.200 + 14.800 = 20.000 cuadros |
| 3 · continuación natural | Quest, Hector, segundo Item Select y segundo combate. | 20.000 cuadros; un reintento de 20.000 |

Se seleccionaron cuatro estados nuevos y se copió el checkpoint de entrada heredado: cinco estados en el paquete, 53 seleccionados acumulativos. El límite era 12 nuevos.

## QA runtime

La matriz `RUNTIME_MATRIX_PW3.csv/json` registra 13 superficies naturales legibles y una referencia controlada de Team Edit. La aprobación es representativa y alcanzable, no global: la matriz PW2 de 1.766 recursos no se convierte artificialmente en 1.766 PASS visuales.

Las cadenas visibles `Lorelei`, `Einherjar`, `Potion` y `Devastator` caben en los cuadros alcanzados. Los diálogos, nombres de hablante, indicadores y transiciones antes/después permanecen estables. No hubo escrituras de ROM; las rutas naturales registraron cero callbacks de escritura a SRAM durante los tramos observados.

## Puertas

| Puerta | Resultado PW3 | Motivo |
| --- | --- | --- |
| I20-NATURAL-TEAM | `NOT_VALIDATED` | Team Edit no apareció antes del segundo combate de 1-1. |
| I11-I18-GLOBAL-QA | `PARTIAL_RUNTIME_PASS` | 13 superficies naturales alcanzables pasan; no hay cobertura visual total. |
| I22-LATE-SCENES | `DEFERRED` | Sin checkpoint tardío auténtico ni proximidad a dos hitos. |
| HIGH-SCORE | `DEFERRED_UNCHANGED` | Fuera del presupuesto por decisión previa. |

## Verificación binaria

- ROM japonesa limpia: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.
- S457, reconstrucción por fuentes y aplicación BPS: `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`.
- BPS acumulativo: `e4bda7c628316fb92978f33ffc136c7f480f2a885f0b606be46e09b7c2335cef`.
- Checksum WonderSwan: `0xD44D`.

## Decisión

PW3 se cierra sin parche nuevo. PW4 debe consolidar la cadena reproducible, repetir BPS/Save/Continue/cold boot en el alcance ya demostrado y emitir el dictamen ordinario con cada puerta en `PASS`, `NOT_VALIDATED` o `DEFERRED`. PW5 permanece desactivada.
