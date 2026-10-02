# Riviera Work Pt1.5 — Ruta complementaria Work para pendientes alcanzables

## 1. Marco y límite

La ruta histórica R1–R6 permanece cerrada en **12/12**. Esta planificación constituye un bloque complementario independiente `PW` y no reescribe el dictamen R6.

- **Máximo:** 5 iteraciones Work (`PW1`–`PW5`).
- **Carga prevista:** 4 iteraciones ordinarias; `PW5` solo se activa si existe un checkpoint tardío auténtico o si `PW3` deja la ruta a dos hitos reproducibles del objetivo.
- **Prohibido abrir PW6:** al terminar PW5 se emite estado final con `PASS`, `NOT_VALIDATED` o `DEFERRED` por puerta.
- **High Score:** permanece diferida por decisión previa y no consume presupuesto en esta ruta.
- **ROM objetivo:** S457 v0.110, SHA-256 `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`.
- **Base ya validada:** I21 Save/Load para partida nueva, DATA:1 y carga en frío. Los 49 checkpoints seleccionados acumulativos se preservan.

### Estado de ejecución — 2026-09-24

`PW1 COMPLETADA` — presupuesto consumido **1/5**. La reconstrucción y la aplicación directa del BPS producen S457 byte-exacto. `A364-ENVELOPE` y `RIBBON-22` pasan; `I04-6C-TECH` e `I05-READINGS` permanecen `NOT_VALIDATED` con sus límites documentados y sin modificar la ROM. La siguiente etapa autorizada por la ruta es `PW2 — Corpus 1.436 y auditoría automatizada`.

## 2. Alcance realista

| Puerta pendiente | Tratamiento en esta ruta | Expectativa |
| --- | --- | --- |
| I04-6C-TECH | Trazado estático y dinámico de dos residuos | `NOT_VALIDATED` en PW1: sin consumidor positivo ni prueba global de desuso |
| I05-READINGS | Búsqueda primaria acotada de tres nombres | Cierre solo si la identidad es inequívoca |
| CORPUS-1436 | Reconstrucción automatizada y conciliación con Bank66 | Cierre probable si las fuentes conservan punteros/ledger recuperable |
| A364-ENVELOPE | Llamadores, índices, límites y trazas dirigidas | `PASS` en PW1: 120/120 índices, cargador y único llamador identificados |
| RIBBON-22 | Propietarios y consumidores de 22 alias | `PASS` en PW1: 22/22 alias conciliados con propietarios y consumidor |
| I11-I18-GLOBAL-QA | Matriz automática completa más revisión visual representativa | Avance fuerte; cierre global depende de escenas no alcanzadas |
| I20-NATURAL-TEAM | Ruta natural corta desde DATA:1/checkpoint | Cierre posible dentro de PW3 |
| I22-LATE-SCENES | Solo con checkpoint auténtico o proximidad demostrada | Condicional PW5 |
| I23-ENDINGS | Solo si se recupera estado tardío auténtico | Fuera de carga ordinaria |
| I24-CREDITS-EXTRAS | Solo si se recupera estado tardío auténtico | Fuera de carga ordinaria |
| HIGH-SCORE | Sin ejecución | Diferida, `UNRESOLVED` |

## 3. Presupuesto común de ejecución

Cada iteración debe respetar estos topes:

- Máximo **3 familias de trabajo** y un único entregable consolidado.
- Máximo **3 rutas de emulación**, cada una hasta **20.000 fotogramas** o **20 minutos de tiempo real**, lo que ocurra primero.
- Máximo **2 reintentos por ruta** después de corregir entradas o sincronización.
- Máximo **12 checkpoints nuevos seleccionados** por iteración; los estados intermedios desechables no se incorporan al catálogo.
- Una herramienta que falle dos veces se sustituye por el siguiente método de UR-42; no se consume otra iteración repitiendo el mismo enfoque.
- Los análisis masivos deben ser automáticos. La revisión manual se limita a muestras estratificadas y a casos marcados por el auditor.
- Solo se modifica la ROM ante defecto demostrado. Toda corrección sigue: detectar → corregir → validar runtime/regresión → generar BPS acumulativo → informar.

## 4. Iteraciones

### PW1 — Recuperación, identidad y trazas técnicas

**Estado:** `COMPLETADA` el 2026-09-24. Resultado consolidado en `Riviera_PW1_Recuperacion_y_Trazas_Tecnicas.md`; no se generó una ROM ni un BPS nuevo.

**Objetivo:** dejar un entorno reproducible y resolver los faltantes que dependen de tablas, punteros y consumidores.

**Trabajo:**

1. Recuperar el paquete fuente S457, BPS acumulativo, ROM base, evidencia I21 y catálogo de 49 estados.
2. Verificar ROM base, S457, reconstrucción y BPS por SHA-256/checksum.
3. Trazar CP932-15939 y CP932-15968 con búsqueda de referencias, desensamblado y watchpoints dirigidos.
4. Enumerar llamadores, entradas, rango e índices del selector A364.
5. Localizar tablas propietarias y consumidores de los 22 alias Ribbon.
6. Ejecutar una búsqueda primaria acotada para 高津 利恵, 深尾 伸也 y 橋本 信之. Si no hay vínculo inequívoco con los créditos de Riviera, conservar kanji y `READING_UNVERIFIED`.

**Límites específicos:** dos pasadas estáticas y dos trazas dinámicas por familia técnica; máximo 30 minutos de búsqueda de fuentes primarias para los tres nombres.

**Salida:** mapa técnico con direcciones/referencias, resultado por I04/A364/Ribbon/I05, hashes de identidad y lista exacta de insumos de PW2.

### PW2 — Corpus 1.436 y auditoría automatizada

**Objetivo:** reconstruir el universo editable y convertir la QA global en una matriz auditable.

**Trabajo:**

1. Extraer las 1.436 entradas con identificador estable, banco/dirección, puntero, texto origen, texto integrado, familia y estado.
2. Demostrar por claves que las 595 entradas Bank66 son subconjunto; no sumar denominadores.
3. Ejecutar búsquedas de Shift-JIS/japonés residual, cadenas sin contexto, overflow estimado, punteros fuera de rango, duplicados y recursos huérfanos.
4. Formar colas `PASS_STATIC`, `NEEDS_CONTEXT`, `NEEDS_VISUAL`, `TECHNICAL_DATA` y `UNRESOLVED`.
5. Revisar manualmente hasta 60 elementos: todos los críticos más una muestra estratificada de cada familia.

**Límite específico:** no revisar manualmente 1.436 filas. El proceso se detiene si no puede ligar cada fila a una dirección o identificador real; no se fabrica el índice desde el ledger agregado.

**Salida:** CSV/JSON editable de 1.436 filas, reconciliación Bank66, informe residual y matriz de cobertura para PW3.

### PW3 — Rutas naturales cortas y QA visual dirigida

**Objetivo:** cerrar I20 y validar en ejecución los casos prioritarios detectados en PW2.

**Trabajo:**

1. Partir de DATA:1 con carga en frío verificada.
2. Intentar hasta tres rutas naturales hacia Team Edit; conservar estado antes, dentro y después, con equipo base, variado y extremo disponible.
3. Reproducir los casos `NEEDS_VISUAL` de mayor riesgo: diálogos, menús, tutorial, inventario, equipo, combate y transiciones alcanzables.
4. Corregir en la misma iteración cualquier defecto demostrado y ejecutar regresión de la familia afectada.
5. Registrar el hito natural más lejano y si existe proximidad objetiva para I22.

**Cierre de I20:** acceso por progresión ordinaria, edición/confirmación del equipo, retorno estable y capturas legibles. Un acceso mediante inyección puede ayudar al diagnóstico, pero no concede el PASS natural.

**Salida:** matriz runtime, hasta 12 estados seleccionados, capturas comparativas, correcciones/BPS si aplican y decisión objetiva sobre activar PW5.

### PW4 — Consolidación y dictamen de alcance Work

**Objetivo:** cerrar el bloque ordinario sin prolongarlo por contenido de juego completo.

**Trabajo:**

1. Repetir reconstrucción y BPS acumulativo directo desde la ROM japonesa.
2. Verificar hashes, checksum, tamaño/mapeador, punteros y familias modificadas.
3. Repetir Save/Continue/cold boot con la ranura nativa.
4. Consolidar puertas como `PASS`, `NOT_VALIDATED` o `DEFERRED` y separar QA estática, runtime y visual.
5. Emitir un dictamen de candidatura de pruebas. `FINAL_APPROVED` solo procede si todas las puertas obligatorias aplicables pasan.

**Salida:** paquete fuente acumulativo depurado, BPS acumulativo, manifiesto, matriz final ordinaria y dictamen.

### PW5 — Condicional: escenas tardías, finales o créditos

**Activación obligatoria:** solo si antes de finalizar PW4 existe al menos una de estas condiciones:

- checkpoint auténtico de progresión tardía con SRAM válida; o
- ruta PW3 a un máximo de dos hitos reproducibles del contenido objetivo.

**Trabajo permitido:** hasta tres ramas de 20.000 fotogramas para I22 y, si quedan inmediatamente accesibles, I23/I24. Revisar escenas, variantes, créditos y extras alcanzados; conservar evidencia antes/después.

**Regla de salida:** si el objetivo no aparece dentro del presupuesto, clasificar la puerta como `DEFERRED_REQUIRES_LONG_PLAYTHROUGH_OR_AUTHENTIC_CHECKPOINT`. No usar banderas temporales o estados sintéticos para conceder PASS natural/visual.

## 5. Actividades excluidas del presupuesto

- Playthrough completo desde el comienzo para alcanzar todos los finales.
- Búsqueda abierta e indefinida de fuentes para lecturas personales.
- Revisión visual manual de las 1.436 entradas sin filtro automático.
- Repetición de pruebas con idéntico método después de dos fallos.
- High Score, conforme a su aplazamiento vigente.
- Compatibilidad con partidas antiguas hasta disponer de una muestra auténtica.

## 6. Resultado esperado y regla final

La meta razonable es cerrar **I04, CORPUS-1436, A364, RIBBON-22 e I20**, completar el tramo alcanzable de I11–I18 y determinar con evidencia si I05 e I22 pueden cerrarse. I23 e I24 solo entran mediante PW5. Esta ruta reduce once puertas sin prometer la finalización artificial de contenido que requiere un recorrido prolongado.

Al concluir PW4 o PW5, el proyecto recibe un único dictamen. Si quedan puertas obligatorias en `NOT_VALIDATED` o `DEFERRED`, continúa como versión de pruebas y el informe debe identificar exactamente qué evidencia externa o checkpoint falta. No se abre una sexta iteración.
