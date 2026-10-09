# Actualización vigente — S457 v0.110 · B4 parcial · 23/09/2026

Se corrigió la ambigüedad `I/l` en cuatro nombres de créditos sin modificar la fuente global de ROM. La `I` compilada conserva el tallo nativo y añade barras de tres píxeles. Las trece páginas pasan guardas de registros y escrituras; solo cambian las cuatro páginas previstas. Once de once glifos aislados se reconocieron antes de consultar la clave.

La regresión conserva 83/83 capturas de combate y 15/15 del prólogo. Team Edit se validó por entrada nativa controlada, sin mutar la ROM. Esto no cierra la progresión natural, la lectura ciega de palabras completas ni la matriz global de diálogos, tutoriales, menús y gráficos.

B4 queda **entregado parcialmente**. I15–I18 continúan EN CURSO. El contador es 4/8; quedan B5, B6 y dos reservas, máximo cuatro iteraciones. Próxima etapa: **B5 — recorridos funcionales y contenido tardío**.

---

## Historial conservado — programa S456

# Riviera — ruta consolidada de finalización

Actualizada el 23/09/2026. Base de continuación: **S456 v0.109**.

**Presupuesto: seis entregas previstas y dos reservas; máximo de planificación: ocho.** B1, B2 y B3 han consumido tres entregas. Quedan tres bloques previstos (B4–B6) y dos reservas: máximo restante **cinco**. B2 y B3 se entregaron con resultados parciales y NO están cerrados: el corpus narrativo y la revisión lingüística global siguen pendientes; tres lecturas, dos candidatos técnicos y brechas de cobertura conservan su condición pendiente. Las 26 etapas originales siguen siendo controles de aceptación.

S455 integra dos lecturas adicionales, corrige el espaciado de dos nombres y amplía la comprobación técnica a 1.766 recursos conocidos, 3.325 usos directos, 662 descompresiones nativas y 76 textos del manual. Los 93 usos sin propietario directo en el inventario no son 93 traducciones faltantes; requieren reconciliación contextual.

S456 corrige dos identidades de habilidad en Rapier y verifica 76 textos nativos y diez fichas de menú por versión. El índice y glosario entregados cubren el manual; B3 no está cerrado globalmente.

Una iteración es un bloque sustancial de trabajo y entrega; puede contener múltiples compilaciones, verificaciones y llamadas a herramientas. No equivale a una llamada, una respuesta breve ni un reinicio de contexto. Los cambios solicitados que amplíen el alcance deben registrarse aparte.

| Bloque | Etapas cubiertas | Resultado exigido | Estado |
|---|---|---|---|
| B1 · Lote consolidado de créditos | I01, I02, I03, I05, I06, I08 | 26 nombres integrados; 13 páginas y reconstrucción verificadas. Cinco lecturas y puertas visuales trasladadas con evidencia a B2/B4/B5. | ENTREGADO_CON_PENDIENTES_TRAZADOS |
| B2 · Cobertura e integridad | I04, I05, I06, I07, I08, I09, I10 | Resolver cinco lecturas, CP932-15939/15968; cerrar inventario de recursos visibles, punteros, límites, controles, compresión y correspondencias. Investigar acceso a escenas tardías desde este bloque. | ENTREGADO PARCIAL, PENDIENTES ABIERTOS |
| B3 · Revisión lingüística integral | I09, I11, I12, I13, I14 | Cotejar todo el corpus trazable, glosario y variantes iniciales, intermedias y finales; corregir e integrar por lotes. | ENTREGADO PARCIAL, RESTO LINGÜÍSTICO ABIERTO |
| B4 · Tipografía y superficies | I15, I16, I17, I18 | Resolver I/l y espaciado; revisar prólogo, combate, menús, Team Edit, diálogos, tutoriales y gráficos a escala nativa con lectura sin contexto. | SIGUIENTE |
| B5 · Recorridos funcionales y contenido tardío | I19, I20, I21, I22, I23, I24 | Validar combate, equipo, guardado/carga, sesiones, escenas tardías, rutas, finales, créditos naturales y desbloqueables; conservar accesos reproducibles. | PENDIENTE |
| B6 · Regresión y entrega final | I25, I26 | Regresión sobre una sola ROM candidata, cero bloqueadores, dictamen conforme al reglamento, fuentes acumulativas y BPS desde JP limpios idénticos. | PENDIENTE |
| R1 | Etapas que fallen antes de B6 | Corregir defectos sustanciales y repetir únicamente las pruebas afectadas. | Reserva 1 |
| R2 | Regresión final y bloqueadores persistentes | Último lote de reparación, verificación y dictamen. | Reserva 2 |

## Cómo economizar iteraciones

- Ejecutar revisión, corrección, compilación y validación del bloque en la misma entrega; evitar una sesión por nombre o por informe.
- Agrupar cambios por recurso y dependencia. Investigar las rutas tardías en B2 y preparar checkpoints antes de B5.
- Reutilizar evidencia solo cuando coincidan bytes, dependencias y entorno; registrar su alcance y procedencia. Repetir pruebas por impacto y realizar una regresión integral en B6.
- Consolidar un paquete acumulativo por bloque. Mantener fuentes reproducibles y un BPS directo desde la ROM japonesa limpia.
- Registrar cada defecto una vez, con responsable de bloque, evidencia y condición de cierre. Los bloqueos de una fuente no detienen tareas independientes.
- Actualizar contador consumido/restante al terminar cada bloque; no reiniciar las reservas ni renumerar para ocultar iteraciones extra.

## Puertas que no se pueden omitir

I01–I03 conservan cierre histórico. I04–I11 siguen en curso e I12–I26 pendientes, con pruebas parciales donde existen. B1 no cierra I05, I06 ni I08 globalmente. Los 1.590 recursos son un censo conocido; no demuestran todavía cobertura exhaustiva del juego. No se calculará un porcentaje global a partir del número de etapas ni de nombres.

La aprobación final exige todos los criterios originales, corpus y variantes trazables, controles técnicos, legibilidad y comportamiento validados, rutas tardías cubiertas y ausencia de bloqueadores. Las sondas controladas de créditos no sustituyen su reproducción natural. Los nombres sin lectura confirmada permanecen pendientes y los defectos visuales no se resuelven por contexto o por mera conservación de píxeles.

**El máximo de ocho es un presupuesto de planificación, no una cantidad necesaria demostrada ni una garantía de terminación.** La cobertura global y el acceso tardío siguen abiertos. Si al agotar R2 quedan bloqueadores, el resultado será NO APROBADO con evidencia, causa, alcance restante y estimación revisada explícita; no se declarará terminado ni se ampliará el contador silenciosamente.

Siguiente acción: **B4 — tipografía y superficies**, incluyendo distinción I/l y revisión de abreviaturas del manual. B3 deja 147 entradas/736 filas trazadas y dos errores de Rapier corregidos en S456; el resto lingüístico se mantiene abierto para contexto B5 y reparación R1. B2 conserva tres lecturas, dos candidatos y brechas. B5 conserva persistencia, rutas y créditos naturales.

---

## Historial conservado — la ruta S456 al inicio prevalece

# Riviera — ruta consolidada de finalización

Actualizada el 23/09/2026. Base de continuación: **S455 v0.108**.

**Presupuesto: seis entregas previstas y dos reservas; máximo de planificación: ocho.** B1 y B2 han consumido dos entregas. Quedan cuatro bloques previstos (B3–B6) y dos reservas: máximo restante **seis**. B2 se entregó con resultados parciales y NO está cerrado: tres lecturas, dos candidatos técnicos y brechas de cobertura conservan su condición pendiente. Las 26 etapas originales siguen siendo controles de aceptación.

S455 integra dos lecturas adicionales, corrige el espaciado de dos nombres y amplía la comprobación técnica a 1.766 recursos conocidos, 3.325 usos directos, 662 descompresiones nativas y 76 textos del manual. Los 93 usos sin propietario directo en el inventario no son 93 traducciones faltantes; requieren reconciliación contextual.

Una iteración es un bloque sustancial de trabajo y entrega; puede contener múltiples compilaciones, verificaciones y llamadas a herramientas. No equivale a una llamada, una respuesta breve ni un reinicio de contexto. Los cambios solicitados que amplíen el alcance deben registrarse aparte.

| Bloque | Etapas cubiertas | Resultado exigido | Estado |
|---|---|---|---|
| B1 · Lote consolidado de créditos | I01, I02, I03, I05, I06, I08 | 26 nombres integrados; 13 páginas y reconstrucción verificadas. Cinco lecturas y puertas visuales trasladadas con evidencia a B2/B4/B5. | ENTREGADO_CON_PENDIENTES_TRAZADOS |
| B2 · Cobertura e integridad | I04, I05, I06, I07, I08, I09, I10 | Resolver cinco lecturas, CP932-15939/15968; cerrar inventario de recursos visibles, punteros, límites, controles, compresión y correspondencias. Investigar acceso a escenas tardías desde este bloque. | ENTREGADO PARCIAL, PENDIENTES ABIERTOS |
| B3 · Revisión lingüística integral | I09, I11, I12, I13, I14 | Cotejar todo el corpus trazable, glosario y variantes iniciales, intermedias y finales; corregir e integrar por lotes. | SIGUIENTE |
| B4 · Tipografía y superficies | I15, I16, I17, I18 | Resolver I/l y espaciado; revisar prólogo, combate, menús, Team Edit, diálogos, tutoriales y gráficos a escala nativa con lectura sin contexto. | PENDIENTE |
| B5 · Recorridos funcionales y contenido tardío | I19, I20, I21, I22, I23, I24 | Validar combate, equipo, guardado/carga, sesiones, escenas tardías, rutas, finales, créditos naturales y desbloqueables; conservar accesos reproducibles. | PENDIENTE |
| B6 · Regresión y entrega final | I25, I26 | Regresión sobre una sola ROM candidata, cero bloqueadores, dictamen conforme al reglamento, fuentes acumulativas y BPS desde JP limpios idénticos. | PENDIENTE |
| R1 | Etapas que fallen antes de B6 | Corregir defectos sustanciales y repetir únicamente las pruebas afectadas. | Reserva 1 |
| R2 | Regresión final y bloqueadores persistentes | Último lote de reparación, verificación y dictamen. | Reserva 2 |

## Cómo economizar iteraciones

- Ejecutar revisión, corrección, compilación y validación del bloque en la misma entrega; evitar una sesión por nombre o por informe.
- Agrupar cambios por recurso y dependencia. Investigar las rutas tardías en B2 y preparar checkpoints antes de B5.
- Reutilizar evidencia solo cuando coincidan bytes, dependencias y entorno; registrar su alcance y procedencia. Repetir pruebas por impacto y realizar una regresión integral en B6.
- Consolidar un paquete acumulativo por bloque. Mantener fuentes reproducibles y un BPS directo desde la ROM japonesa limpia.
- Registrar cada defecto una vez, con responsable de bloque, evidencia y condición de cierre. Los bloqueos de una fuente no detienen tareas independientes.
- Actualizar contador consumido/restante al terminar cada bloque; no reiniciar las reservas ni renumerar para ocultar iteraciones extra.

## Puertas que no se pueden omitir

I01–I03 conservan cierre histórico. I04–I10 siguen en curso e I11–I26 pendientes, con pruebas parciales donde existen. B1 no cierra I05, I06 ni I08 globalmente. Los 1.590 recursos son un censo conocido; no demuestran todavía cobertura exhaustiva del juego. No se calculará un porcentaje global a partir del número de etapas ni de nombres.

La aprobación final exige todos los criterios originales, corpus y variantes trazables, controles técnicos, legibilidad y comportamiento validados, rutas tardías cubiertas y ausencia de bloqueadores. Las sondas controladas de créditos no sustituyen su reproducción natural. Los nombres sin lectura confirmada permanecen pendientes y los defectos visuales no se resuelven por contexto o por mera conservación de píxeles.

**El máximo de ocho es un presupuesto de planificación, no una cantidad necesaria demostrada ni una garantía de terminación.** La cobertura global y el acceso tardío siguen abiertos. Si al agotar R2 quedan bloqueadores, el resultado será NO APROBADO con evidencia, causa, alcance restante y estimación revisada explícita; no se declarará terminado ni se ampliará el contador silenciosamente.

Siguiente acción: **B3 — revisión lingüística integral** y reconciliación JP–inglés–ROM. Se continúan tareas independientes; los pendientes de B2 conservan responsables y evidencias para R1. B4 conserva I/l; el espaciado quedó corregido en S455. B5 conserva créditos naturales y rutas tardías.


---

## Historial conservado — la ruta S455 anterior prevalece

# Riviera — ruta consolidada de finalización

Actualizada el 23/09/2026. Base de continuación: **S454 v0.107**.

**Objetivo: seis iteraciones de entrega, incluida esta, más dos de reserva; máximo de planificación: ocho.** B1 está entregado. Quedan cinco bloques previstos y, solo si hacen falta, dos reservas: máximo planificado restante **siete**. Las 26 etapas originales se mantienen como controles de aceptación, no como 26 conversaciones adicionales.

Una iteración es un bloque sustancial de trabajo y entrega; puede contener múltiples compilaciones, verificaciones y llamadas a herramientas. No equivale a una llamada, una respuesta breve ni un reinicio de contexto. Los cambios solicitados que amplíen el alcance deben registrarse aparte.

| Bloque | Etapas cubiertas | Resultado exigido | Estado |
|---|---|---|---|
| B1 · Lote consolidado de créditos | I01, I02, I03, I05, I06, I08 | 26 nombres integrados; 13 páginas y reconstrucción verificadas. Cinco lecturas y puertas visuales trasladadas con evidencia a B2/B4/B5. | ENTREGADO_CON_PENDIENTES_TRAZADOS |
| B2 · Cobertura e integridad | I04, I05, I06, I07, I08, I09, I10 | Resolver cinco lecturas, CP932-15939/15968; cerrar inventario de recursos visibles, punteros, límites, controles, compresión y correspondencias. Investigar acceso a escenas tardías desde este bloque. | SIGUIENTE |
| B3 · Revisión lingüística integral | I09, I11, I12, I13, I14 | Cotejar todo el corpus trazable, glosario y variantes iniciales, intermedias y finales; corregir e integrar por lotes. | PENDIENTE |
| B4 · Tipografía y superficies | I15, I16, I17, I18 | Resolver I/l y espaciado; revisar prólogo, combate, menús, Team Edit, diálogos, tutoriales y gráficos a escala nativa con lectura sin contexto. | PENDIENTE |
| B5 · Recorridos funcionales y contenido tardío | I19, I20, I21, I22, I23, I24 | Validar combate, equipo, guardado/carga, sesiones, escenas tardías, rutas, finales, créditos naturales y desbloqueables; conservar accesos reproducibles. | PENDIENTE |
| B6 · Regresión y entrega final | I25, I26 | Regresión sobre una sola ROM candidata, cero bloqueadores, dictamen conforme al reglamento, fuentes acumulativas y BPS desde JP limpios idénticos. | PENDIENTE |
| R1 | Etapas que fallen antes de B6 | Corregir defectos sustanciales y repetir únicamente las pruebas afectadas. | Reserva 1 |
| R2 | Regresión final y bloqueadores persistentes | Último lote de reparación, verificación y dictamen. | Reserva 2 |

## Cómo economizar iteraciones

- Ejecutar revisión, corrección, compilación y validación del bloque en la misma entrega; evitar una sesión por nombre o por informe.
- Agrupar cambios por recurso y dependencia. Investigar las rutas tardías en B2 y preparar checkpoints antes de B5.
- Reutilizar evidencia solo cuando coincidan bytes, dependencias y entorno; registrar su alcance y procedencia. Repetir pruebas por impacto y realizar una regresión integral en B6.
- Consolidar un paquete acumulativo por bloque. Mantener fuentes reproducibles y un BPS directo desde la ROM japonesa limpia.
- Registrar cada defecto una vez, con responsable de bloque, evidencia y condición de cierre. Los bloqueos de una fuente no detienen tareas independientes.
- Actualizar contador consumido/restante al terminar cada bloque; no reiniciar las reservas ni renumerar para ocultar iteraciones extra.

## Puertas que no se pueden omitir

I01–I03 conservan cierre histórico. I04–I06 siguen en curso e I07–I26 pendientes, con pruebas parciales donde existen. B1 no cierra I05, I06 ni I08 globalmente. Los 1.590 recursos son un censo conocido; no demuestran todavía cobertura exhaustiva del juego. No se calculará un porcentaje global a partir del número de etapas ni de nombres.

La aprobación final exige todos los criterios originales, corpus y variantes trazables, controles técnicos, legibilidad y comportamiento validados, rutas tardías cubiertas y ausencia de bloqueadores. Las sondas controladas de créditos no sustituyen su reproducción natural. Los nombres sin lectura confirmada permanecen pendientes y los defectos visuales no se resuelven por contexto o por mera conservación de píxeles.

**El máximo de ocho es un presupuesto de planificación, no una cantidad necesaria demostrada ni una garantía de terminación.** La cobertura global y el acceso tardío siguen abiertos. Si al agotar R2 quedan bloqueadores, el resultado será NO APROBADO con evidencia, causa, alcance restante y estimación revisada explícita; no se declarará terminado ni se ampliará el contador silenciosamente.

Siguiente acción: **B2 — cobertura e integridad**, incorporando en el mismo bloque las cinco lecturas pendientes, los dos candidatos I04 y los controles estructurales I06–I10. B4 conserva las incidencias I/l y espaciado; B5 conserva créditos naturales.

---

## Historial del programa; la ruta anterior prevalece sobre la planificación antigua

# Actualización vigente — S453 v0.106 · I05.2f · 23/09/2026

Assist Work/Marketing/Sales: seis nombres integrados en tres entradas, sin abreviaturas, cambios de línea ni fuente. Quedan **cuatro entradas de créditos por localizar**: Tuning y tres grupos Special Thanks.

QA técnico: 13 páginas; solo cambia el índice 7, las otras doce permanecen idénticas. Tablas de animación sin cambios, 1.590 recursos intactos, 83 capturas de combate iguales a S452 y reconstrucción/BPS idénticos. 79 apariciones de glifos nativos exactas y 22/22 glifos aislados reconocidos. Se corrigió el compositor diagnóstico para que el fondo vacío de un rótulo no recorte la tinta del campo vecino; no fue un defecto de bytes de ROM.

I/l sigue abierto en nombres de etapas anteriores. No se extiende el PASS de glifos aislados a lectura ciega de palabras, reproducción natural o aprobación global. I01–I03 conservan cierre histórico; I04–I06 continúan en curso; I07–I26 pendientes.

Próximo lote: **I05.2g — Tuning**. Revisar capacidad antes de ampliar: quedan 1.143 bytes antes del arranque. Estado de las 26 etapas y dependencias actualizado. Versión de pruebas, no RC.

---

## Historial previo — S452

# Actualización vigente — S452 v0.105 · I05.2e · 23/09/2026

Graphic/Sound: once nombres japoneses localizados y dos alias latinos preservados. Quedan **siete entradas de créditos por localizar**, no siete personas. Kazuko Yamaguchi ocupa dos líneas para mantener la fuente nativa sin recortar trazos.

La reserva S451 se reorganiza con compresión RLE sin pérdida: 17.856 bytes crudos en 5.783 bytes, más rutina de 197 bytes. Produce/Scenario permanecen idénticos en ejecución. Quedan 2.889 bytes antes del arranque. Todas las 13 páginas pasan QA técnico; solo cambian 5/6. Referencia nativa de animación ampliada, 1.590 recursos, 83 capturas de combate, reconstrucción y BPS verificados.

La puerta visual sigue abierta por I/l nativo, ahora también Fumie Ishinaka. Se corrige la gravedad de la incidencia a MAJOR conforme al reglamento, sin inventar una aprobación. Créditos naturales y tiempos finales siguen pendientes; I04 conserva dos casos indeterminados. I01–I03 mantienen cierre histórico; I04–I06 en curso; I07–I26 pendientes.

Próximo lote: **I05.2f — Assist Work/Marketing/Sales**. No hay RC ni cierre global.

---

## Historial previo — S451

# Actualización vigente — S451 v0.104 · I05.2d · 23/09/2026

Se integran siete nombres de Produce y Scenario en dos grupos, con nombre y apellido en líneas consecutivas. Quedan **nueve entradas de créditos por localizar**, no nueve personas. Kazuki Yamanobe se corrobora mediante su lectura en CEDEC y metadatos editoriales; no se copia la variante Ikki de otra versión.

Las 13 páginas pasan la prueba técnica controlada: solo cambian 0/3, y ambas tablas ampliadas coinciden con referencias del motor nativo. 1.590 recursos conocidos intactos; 83 capturas de batalla iguales a S450; reconstrucción y BPS idénticos. Se preservan arranque y cabecera.

La puerta visual sigue abierta: los glifos nativos I/l son idénticos; ahora también afecta Takeo Isogai. Se conservan transcripción, clave y evidencia sin convertir la ambigüedad en PASS. I05.2d queda integrada y confirmada técnicamente, pendiente de cierre visual. El recorrido natural sigue pendiente en I24 y los dos casos de I04 siguen indeterminados.

Siguiente lote: **I05.2e — Graphic/Sound**. Antes de ampliar, resolver el espacio: la reserva actual de banco 7F deja ocho bytes antes del código de arranque; no expandirla a ciegas. No hay RC ni aprobación global. Estado y dependencias de las 26 etapas en el JSON y `analysis/ETAPAS_26.csv`.

---

## Historial previo — S450

# Actualización vigente — S450 v0.103 · I05.2c · 23/09/2026

Se integran ocho nombres en cuatro entradas de Program, Script, Character Design y Event BG Design. Quedan **11 entradas de créditos por localizar**, no once personas: cada entrada puede contener varios nombres. Los nueve grupos sustituidos gráficamente en S449/S450 conservan sus streams originales como entrada del motor.

QA técnico: 13 páginas controladas; solo páginas 2/4 modificadas (índice cero), última página S449 intacta; tablas de animación extendidas cotejadas con ejecución nativa independiente; 1.590 recursos conocidos intactos; 83 capturas de combate idénticas; reconstrucción y BPS idénticos.

La prueba de reconocimiento aislado identificó 28 de 29 glifos. `I` y `l` son idénticos ya en la ROM japonesa original. Se registra **RIV-CREDIT-I-L**, fallo del reconocimiento aislado y cierre visual abierto; no se modifica el glifo nativo sin un rediseño justificado. I05.2c queda integrada y confirmada técnicamente, con su puerta visual pendiente. No hay RC ni aprobación global.

Siguiente lote independiente: **I05.2d**, Produce/Scenario, manteniendo la incidencia de glifo para I15 y el recorrido natural para I24. I01–I03 conservan cierre histórico; I04–I06 siguen en curso; I07–I26 mantienen sus dependencias. Véanse `INFORME_S450_I05_2c.md` y `analysis/ETAPAS_26.csv`.

---

## Historial previo — S449

# Actualización vigente — S449 v0.102 · I05.2b · 23/09/2026

Esta actualización prevalece sobre el historial conservado a continuación. I05.2b integra Development, Tuning, Debug, Sarugakucho y Studio Stat en la última página de créditos. La fuente nativa se conserva; el espaciado horizontal de los dos nombres se adapta sin modificar sus píxeles.

Las 13 páginas pasan la prueba controlada; las otras doce son idénticas a S448. Se verificaron límites y registros de la rutina, 1.590 recursos conocidos intactos y 83 capturas de combate idénticas durante 2.500 frames. Los cinco streams japoneses originales permanecen como entrada del compositor nativo y sus bloques visibles se sustituyen antes del retorno: esto no equivale a eliminar sus bytes de la ROM.

Quedan **15 entradas visibles de créditos por localizar**, dos candidatos I04 indeterminados y las puertas posteriores de auditoría. I01–I03 conservan cierre histórico; I04–I06 siguen en curso; I07–I26 permanecen pendientes, con evidencia parcial donde se indica. No se declara RC ni aprobación global. El recorrido natural de los créditos sigue sin validarse.

Siguiente acción: **I05.2c**, corroborar e integrar el próximo grupo de las 15 entradas pendientes. El estado JSON y `analysis/ETAPAS_26.csv` contienen dependencias y criterios; `INFORME_S449_I05_2b.md` contiene las pruebas de esta versión.

---

## Historial previo — S448

# Actualización vigente — S448 v0.101 · I05.2a · 23/09/2026

Esta actualización prevalece sobre el estado S447 conservado abajo como historial. I01–I03 permanecen completadas en su alcance histórico. I04 e I05 continúan abiertas; I06 pasa a EN_CURSO por comprobaciones estructurales acotadas. I07–I26 no reciben cierre global por estas pruebas.

Dos nombres de créditos integrados y corroborados; 13 composiciones nativas controladas y 578 comprobaciones de anchura; 83 capturas de combate idénticas. Quedan 16 cadenas del grupo previo de 18 y se añaden cuatro cadenas en katakana: 20 cadenas de créditos pendientes en el universo ampliado. Los dos candidatos I04 siguen indeterminados. La siguiente acción es I05.2b. Véase Riviera_S448_I05_2a_Informe.md para pruebas, límites y matriz completa.

---

## Historial del programa al cierre I05.1

# Riviera — programa de auditoría integral por iteraciones

Versión del programa: 6. Base inicial: **S447 v0.100**. Reglamento: **WS_TRANSLATION_UNIVERSAL_RULES v1.5**.

**Estado actualizado: I01–I03 completadas; I04 e I05 EN_CURSO.** I05.1 incorporó 176 recursos nuevos respecto de I03, entre ellos 38 cadenas únicas de créditos. Dieciocho cadenas de nombres conservan glifos japoneses y requieren lecturas verificadas. I04 mantiene 45 candidatos clasificados y 2 indeterminados. La siguiente acción es **I05.2**. S447 permanece sin cambios y no hay aprobación global.

## Objetivo y alcance

Auditar cobertura, integridad, calidad lingüística, tipografía, comportamiento y contenido tardío; corregir los defectos al detectarlos y conservar una cadena reproducible hasta un dictamen de publicación. El programa incluye **26 iteraciones base agrupadas en 9 fases**. No fija una fecha ni promete que 26 sesiones basten para cerrar todo el juego.

S447 es el punto de partida. Los 47 residuos son el lote técnico heredado, no 47 traducciones demostradas. Tras I04.2, 45 tienen clasificación técnica y 2 siguen abiertos. Team Edit en disposición natural, escenas tardías y revisión general siguen siendo frentes de trabajo. El censo determinará el universo real, incluidos capítulos y variantes; no se inventan cantidades para calcular un porcentaje.

## Orden de trabajo

Orden predeterminado: I01 → I26. Las dependencias detalladas permiten avanzar otro bloque cuando exista un bloqueo documentado. I14 puede necesitar el contexto obtenido en I22–I24: se mantiene pendiente mientras se accede a esas escenas y se retoma después, sin fingir cierre. Las correcciones urgentes interrumpen la secuencia y se integran en la iteración donde se detectan.

La siguiente acción es **I05.2**: verificar la lectura e integración de los nombres de los créditos detectados en I05.1. I05 depende de I03 completada. I04 conserva estado EN_CURSO con dos candidatos indeterminados y su requisito para I09 sigue vigente. La detección de nombres en el formato nativo de glifos demuestra una brecha que la búsqueda Shift-JIS no captaba; la romanización debe preservar la identidad de cada persona y comprobarse en el juego. Una iteración puede requerir varias sesiones; terminar una respuesta no equivale a terminarla.

## Mapa del programa

| Fase | Iteraciones | Resultado previsto |
|---|---|---|
| 0. Base reproducible | I01–I02 | Base identificada, reconstrucción y mapa de modificaciones |
| 1. Censo y residuos | I03–I05 | Universo inicial, clasificación de los 47 candidatos y búsqueda gráfica |
| 2. Integridad técnica | I06–I08 | Punteros, controles, buffers y memoria gráfica revisados |
| 3. Cobertura | I09–I10 | Correspondencia original–traducción–ROM y pendientes identificados |
| 4. Calidad lingüística | I11–I14 | Glosario y revisión contextual por bloques |
| 5. Tipografía e interfaz | I15–I18 | Fuentes, combate, menús, Team Edit y diálogos revisados |
| 6. Funcionamiento | I19–I21 | Flujos de combate/menús y persistencia probados |
| 7. Contenido tardío | I22–I24 | Accesos, finales, créditos y variantes documentados |
| 8. Regresión y entrega | I25–I26 | Pruebas consolidadas y dictamen sustentado de publicación |

## Forma de ejecutar cada iteración

1. Registrar ROM de entrada y hash; elegir un lote finito de IDs del censo y sus consumidores.
2. Examinar el lote y documentar hallazgos con evidencia y gravedad.
3. Corregir los defectos dentro de la misma iteración cuando la solución esté suficientemente determinada; no esperar a una fase futura para arreglar un fallo conocido.
4. Validar las correcciones en ejecución, lectura directa y regresión de los consumidores afectados. Un defecto semántico sin contexto suficiente conserva NEEDS_CONTEXT.
5. Si cambia la ROM, reconstruir, comprobar checksum/hash y entregar BPS acumulativo desde la japonesa limpia más fuentes acumulativas completas. El incremento es opcional y nunca sustituye el acumulativo.
6. Actualizar resultados, evidencias, incidencias, cobertura y próximo paso exacto. Si no cambia la ROM, entregar el informe y el estado de auditoría sin fabricar otra versión jugable.

Los lotes extensos se dividen en Ixx.01, Ixx.02, etc., por capítulo, consumidor o familia de recursos. Cada lote declara sus IDs incluidos y excluidos. La iteración matriz solo se cierra cuando todos sus lotes obligatorios y criterios de salida estén resueltos. Se ajusta el tamaño al trabajo real; no se rebaja el criterio de aprobación para encajar en una sesión.

Tras un intento natural acotado con una condición de parada registrada, usar checkpoints, Lua de Mesen, trazas de consumidores o inyección mínima. Separar los guardados de QA y etiquetar NATURAL / CHECKPOINT / SYNTHETIC. El acceso sintético demuestra comportamiento bajo ese estado; no demuestra que una ruta natural sea alcanzable.

## Iteraciones detalladas

### I01 — Identidad y congelación de la base

- **Fase:** 0 · Base reproducible.
- **Entrada/dependencias:** Sin dependencias; entrada S447.
- **Alcance:** Identificar ROM original, S447, BPS, fuentes y herramientas; registrar tamaños, hashes y checksum.
- **Trabajo:** Reutilizar manifiestos y contrastarlos con los archivos disponibles. Inventariar evidencia heredada sin extender su alcance.
- **Criterio de cierre:** Base inequívoca y registro de procedencia; cualquier discrepancia resuelta.
- **Entregable:** informe I01, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado actual:** COMPLETADA — PASS en el alcance de fase 0.

### I02 — Reproducibilidad y mapa de modificaciones

- **Fase:** 0 · Base reproducible.
- **Entrada/dependencias:** I01
- **Alcance:** Reconstrucción desde fuentes acumulativas y aplicación del BPS a la ROM limpia; mapa de rangos modificados.
- **Trabajo:** Comprobar igualdad byte a byte y límites de 8 MiB/mapeador; reutilizar pruebas existentes solo si corresponden a los mismos archivos y entorno documentado.
- **Criterio de cierre:** Reconstrucción y parche idénticos; mapa de cambios y procedimiento reproducible.
- **Entregable:** informe I02, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado actual:** COMPLETADA — PASS en el alcance de fase 0.

### I03 — Censo de recursos y consumidores

- **Fase:** 1 · Censo y residuos.
- **Entrada/dependencias:** I02
- **Alcance:** Diálogos, UI, objetos, habilidades, tutoriales, gráficos con texto, rutas, finales y créditos.
- **Trabajo:** Cruzar extractores, tablas, bancos, recursos comprimidos y consumidores; asignar ID estable por recurso y por contexto de uso.
- **Criterio de cierre:** Censo inicial versionado con procedencia, familias y zonas sin resolver; sin declarar exhaustividad solo por resultados del extractor.
- **Entregable:** informe I03, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado actual:** COMPLETADA — censo inicial; brechas explícitas, universo global no demostrado.

### I04 — Clasificación de los 47 residuos

- **Fase:** 1 · Censo y residuos.
- **Entrada/dependencias:** I03
- **Alcance:** Los 47 candidatos técnicos heredados, sin presuponer que sean texto pendiente.
- **Trabajo:** Confirmar lista y direcciones contra S447; agrupar por consumidor; rastrear referencias y ejecutar casos dirigidos. Clasificar texto activo, datos, no utilizado demostrado o indeterminado.
- **Criterio de cierre:** Cada candidato con diagnóstico y evidencia. Los indeterminados mantienen esta iteración abierta; no se borran para reducir el contador.
- **Entregable:** informe I04, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado actual:** EN_CURSO — I04.1 e I04.2 ejecutadas en alcance acotado; 45 candidatos clasificados y 2 indeterminados. Ocho copias nativas verificadas; consumidor del noveno icono NOT_VALIDATED. Continúa I05 como bloque independiente; no se concede cierre de I04 ni global.

### I05 — Texto gráfico y japonés fuera del censo

- **Fase:** 1 · Censo y residuos.
- **Entrada/dependencias:** I03
- **Alcance:** Bancos secundarios, codificaciones alternativas, imágenes, mensajes especiales, finales y créditos.
- **Trabajo:** Combinar búsquedas de bytes y referencias con decodificación gráfica y lectura directa. Registrar duplicados por separado de usos.
- **Criterio de cierre:** Censo ampliado con cobertura de búsqueda, candidatos y límites; las zonas no interpretadas quedan registradas.
- **Entregable:** informe I05, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado actual:** EN_CURSO — I05.1 amplió el censo en 138 recursos gráficos y 38 cadenas de créditos nuevas respecto de I03. Dieciocho cadenas de nombres japoneses esperan lecturas verificadas e integración. Sigue I05.2; no hay cierre global.

### I06 — Punteros, bancos y límites

- **Fase:** 2 · Integridad técnica.
- **Entrada/dependencias:** I03
- **Alcance:** Referencias, destinos, solapamientos, rangos reservados y recursos reubicados.
- **Trabajo:** Validar cada formato conocido y sus consumidores; contrastar las regiones modificadas con sus reservas y tamaño real.
- **Criterio de cierre:** Ningún defecto técnico abierto en los rangos auditados; cobertura de formatos explícita.
- **Entregable:** informe I06, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I07 — Terminadores y controles de texto

- **Fase:** 2 · Integridad técnica.
- **Entrada/dependencias:** I06
- **Alcance:** Fin de cadena, saltos, esperas, nombres variables, números y códigos de presentación.
- **Trabajo:** Analizar flujos con sus reglas reales; comparar controles japoneses y traducidos; reproducir variantes de riesgo.
- **Criterio de cierre:** Cadenas del lote íntegramente parseables; controles y sustituciones funcionales, sin truncamientos detectados.
- **Entregable:** informe I07, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I08 — Descompresión y memoria gráfica

- **Fase:** 2 · Integridad técnica.
- **Entrada/dependencias:** I06, I07
- **Alcance:** Buffers, tiles, paletas, fuentes compartidas y limpieza entre pantallas.
- **Trabajo:** Instrumentar escrituras y límites; probar alternancia de cadenas largas/cortas y consumidores compartidos; incluir antecedentes OVER, RAGE, Attack y Magic.
- **Criterio de cierre:** Sin invasión ni residuos en los casos examinados; productores y consumidores afectados documentados.
- **Entregable:** informe I08, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I09 — Correspondencia japonés–inglés–ROM

- **Fase:** 3 · Cobertura de traducción.
- **Entrada/dependencias:** I04, I05, I07
- **Alcance:** Relacionar cada entrada original, su traducción y el recurso realmente integrado.
- **Trabajo:** Cruzar fuentes y compilación; detectar omisiones, versiones antiguas, traducciones no insertadas y usos sin referencia.
- **Criterio de cierre:** Matriz trazable para el censo vigente, con estados independientes y excepciones identificadas.
- **Entregable:** informe I09, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I10 — Barrido residual y variantes

- **Fase:** 3 · Cobertura de traducción.
- **Entrada/dependencias:** I09
- **Alcance:** Nuevas cadenas pendientes, alternativas, ayudas y recursos compartidos.
- **Trabajo:** Repetir búsquedas sobre la ROM construida; verificar candidatos en su consumidor y distinguir referencias japonesas legítimas.
- **Criterio de cierre:** Todo candidato nuevo resuelto o registrado; cobertura y traducción pendiente cuantificadas sin porcentaje global indefendible.
- **Entregable:** informe I10, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I11 — Glosario y textos de sistemas

- **Fase:** 4 · Calidad lingüística.
- **Entrada/dependencias:** I09
- **Alcance:** Personajes, lugares, objetos, habilidades, estadísticas, estados y comandos.
- **Trabajo:** Fijar glosario japonés–inglés; contrastar términos en todos sus usos y documentar abreviaturas justificadas.
- **Criterio de cierre:** Glosario versionado y coherencia del lote revisado; diferencias intencionales justificadas.
- **Entregable:** informe I11, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I12 — Narrativa inicial

- **Fase:** 4 · Calidad lingüística.
- **Entrada/dependencias:** I11
- **Alcance:** Prólogo y primer bloque narrativo definido por el censo, incluidos tutoriales y decisiones.
- **Trabajo:** Revisión contextual contra japonés: voz, intención, naturalidad, números y pistas. Subdividir por escena si hace falta.
- **Criterio de cierre:** Todas las entradas del bloque revisadas; ambigüedades NEEDS_CONTEXT resueltas para cerrarlo.
- **Entregable:** informe I12, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I13 — Narrativa intermedia y alternativas

- **Fase:** 4 · Calidad lingüística.
- **Entrada/dependencias:** I12
- **Alcance:** Bloques narrativos intermedios y variantes asociadas que identifique el censo.
- **Trabajo:** Subiteraciones por capítulo/escena y ruta; comprobar continuidad terminológica, personajes y respuestas alternativas.
- **Criterio de cierre:** Cada bloque identificado cubierto o pendiente explícito; no extrapolar una muestra a todos los diálogos.
- **Entregable:** informe I13, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I14 — Narrativa tardía y textos sensibles

- **Fase:** 4 · Calidad lingüística.
- **Entrada/dependencias:** I13
- **Alcance:** Escenas finales, desenlaces, créditos y descripciones con efectos/condiciones de juego.
- **Trabajo:** Preparar revisión lingüística con contexto; usar evidencia de I22–I24 si falta. Comparar números, restricciones y consecuencias.
- **Criterio de cierre:** Revisión lingüística completa del lote; sin dudas semánticas críticas. Si falta contexto, volver tras I22–I24.
- **Entregable:** informe I14, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I15 — Fuentes, glifos y prólogo

- **Fase:** 5 · Tipografía e interfaz.
- **Entrada/dependencias:** I08, I11
- **Alcance:** Familias tipográficas; prólogo S447 y extensiones aprobadas.
- **Trabajo:** Comparar glifos con referencias nativas; revisar escala nativa e íntegra, baseline, grosor y puntuación. Transcribir píxeles antes de cotejar el texto esperado cuando sea práctico.
- **Criterio de cierre:** Legibilidad y fidelidad aprobadas en cada familia modificada; evidencias separadas de intención y OCR.
- **Entregable:** informe I15, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I16 — Interfaz de batalla

- **Fase:** 5 · Tipografía e interfaz.
- **Entrada/dependencias:** I08, I11
- **Alcance:** Comandos, objetos, objetivos, nombres de acciones, OVER/OverDrive, RAGE/MAX, Attack y Magic.
- **Trabajo:** Matriz de longitudes extremas, niveles y combinaciones válidas; observar entrada, actualización y salida de cada cuadro.
- **Criterio de cierre:** Sin recortes, colisiones o texto fantasma en la matriz; rótulos y condiciones funcionales confirmados.
- **Entregable:** informe I16, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I17 — Menús, inventario y Team Edit

- **Fase:** 5 · Tipografía e interfaz.
- **Entrada/dependencias:** I08, I11
- **Alcance:** Estados, equipamiento, inventario, ayudas y formaciones.
- **Trabajo:** Revisar todas las disposiciones identificadas, nombres largos y cambios de selección; incluir Team Edit en disposición natural con los miembros necesarios.
- **Criterio de cierre:** Matriz visual legible. El acceso sintético no cierra el pendiente de disposición natural.
- **Entregable:** informe I17, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I18 — Diálogos, tutoriales y gráficos

- **Fase:** 5 · Tipografía e interfaz.
- **Entrada/dependencias:** I10, I12, I15
- **Alcance:** Cajas narrativas, elecciones, mensajes ambientales, cartelas e imágenes con texto.
- **Trabajo:** Casos por consumidor y extremos de longitud; comprobar alineación nativa, saltos, tiempos y borrado.
- **Criterio de cierre:** Familias modificadas con evidencia visual/runtime y revisión directa; límites de muestreo declarados.
- **Entregable:** informe I18, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I19 — Flujo funcional de combate

- **Fase:** 6 · Funcionamiento y persistencia.
- **Entrada/dependencias:** I16
- **Alcance:** Selecciones, habilidades, objetos, objetivos y transiciones de batalla.
- **Trabajo:** Ejecutar secuencias válidas y casos límite; contrastar texto con acción, valor y condición reales.
- **Criterio de cierre:** Sin desajustes texto–efecto ni bloqueos detectados en las rutas probadas.
- **Entregable:** informe I19, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I20 — Flujo funcional de menús y equipo

- **Fase:** 6 · Funcionamiento y persistencia.
- **Entrada/dependencias:** I17
- **Alcance:** Equipo, inventario, miembros, formaciones y navegación entre pantallas.
- **Trabajo:** Validar cambios de estado, cancelar/confirmar, selecciones extremas y regreso a pantallas previas.
- **Criterio de cierre:** Estado del juego y etiquetas coherentes; comprobar el caso natural de Team Edit pendiente.
- **Entregable:** informe I20, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I21 — Persistencia y sesiones

- **Fase:** 6 · Funcionamiento y persistencia.
- **Entrada/dependencias:** I19, I20
- **Alcance:** Guardar/cargar, reinicio en frío, continuar y transiciones desde estados persistidos.
- **Trabajo:** Usar guardado nativo para demostrar persistencia; savestates solo como apoyo. Contrastar antes/después y probar recuperación de escenas.
- **Criterio de cierre:** Datos y textos correctos tras cold-Continue en los casos definidos; método de acceso registrado.
- **Entregable:** informe I21, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I22 — Acceso y cobertura de escenas tardías

- **Fase:** 7 · Contenido tardío.
- **Entrada/dependencias:** I03, I10
- **Alcance:** Localizar escenas y rutas finales identificadas por el censo.
- **Trabajo:** Intento natural acotado; después checkpoints, Lua, trazas o inyección mínima documentada. Mantener guardados de prueba separados.
- **Criterio de cierre:** Inventario de puntos de acceso y cobertura conseguida; lo no alcanzado permanece pendiente.
- **Entregable:** informe I22, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I23 — Finales, rutas y variantes

- **Fase:** 7 · Contenido tardío.
- **Entrada/dependencias:** I22
- **Alcance:** Desenlaces y variantes identificados, con revisión lingüística, gráfica y de transición.
- **Trabajo:** Ejecutar cada variante censada; comprobar integridad, legibilidad y contexto; devolver hallazgos a I14/I18.
- **Criterio de cierre:** Evidencia por variante; sin sustituir finales no probados por un único final observado.
- **Entregable:** informe I23, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I24 — Créditos y contenido desbloqueable

- **Fase:** 7 · Contenido tardío.
- **Entrada/dependencias:** I22
- **Alcance:** Créditos completos, posjuego y opciones adicionales si existen.
- **Trabajo:** Recorrer inicio–fin del listado, entradas/salidas y desbloqueos identificados; justificar N/A solo con evidencia.
- **Criterio de cierre:** Recursos y comportamiento comprobados; nombres y roles legibles; contenido pendiente explícito.
- **Entregable:** informe I24, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I25 — Regresión consolidada

- **Fase:** 8 · Regresión y entrega.
- **Entrada/dependencias:** I01–I24
- **Alcance:** Todos los consumidores afectados por las correcciones y una muestra transversal del juego.
- **Trabajo:** Construcción candidata identificada por hash; repetir pruebas invalidadas y escenarios representativos. Comparar con la base apropiada.
- **Criterio de cierre:** Sin regresiones abiertas en la matriz; toda evidencia vinculada a una versión compatible.
- **Entregable:** informe I25, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

### I26 — Dictamen y paquete de entrega

- **Fase:** 8 · Regresión y entrega.
- **Entrada/dependencias:** I25
- **Alcance:** Decidir versión de pruebas, candidato a lanzamiento o continuidad de auditoría.
- **Trabajo:** Aplicar las puertas obligatorias del reglamento vigente; comprobar reconstrucción final, BPS acumulativo, fuentes completas y lista de incidencias.
- **Criterio de cierre:** Dictamen sustentado. RC solo si cumple requisitos aplicables; pendientes obligatorios impiden la aprobación, sin convertirlos artificialmente en N/A.
- **Entregable:** informe I26, registro de hallazgos y evidencias, cobertura actualizada y paquete acumulativo si hay cambios de ROM.
- **Estado inicial:** PENDIENTE.

## Registro de seguimiento y evidencia

El archivo `Riviera_Auditoria_Estado.json` conserva IDs, dependencias y estado del programa. Para una ejecución se completan hash de entrada/salida, hallazgos, pruebas, subiteraciones y evidencias. Las dependencias expresadas como I01–I24 significan todas las iteraciones de ese intervalo.

Estados de trabajo: **PENDIENTE**, **EN_CURSO**, **BLOQUEADA**, **COMPLETADA**. Un cierre administrativo no concede PASS a un recurso. Los resultados de cada comprobación son PASS / FAIL / NOT_VALIDATED / N/A con justificación cuando corresponda.

Por recurso se mantienen por separado: comprensión del original, traducción, integración, aprobación lingüística, preservación de fuente, integridad de glifos, reconocimiento sin contexto, legibilidad, ejecución, aprobación visual, función y regresión. FINAL_APPROVED se deriva de todas las puertas obligatorias aplicables; no se asigna manualmente.

Cada incidencia registra como mínimo:

- ID `RIV-AUD-0001`, iteración, familia, recurso/offset y consumidor.
- ROM/hash y procedimiento de reproducción; método de acceso.
- Resultado esperado, observado y evidencia original.
- Gravedad BLOCKER / MAJOR / MINOR / POLISH, causa y corrección.
- Prueba posterior, regresiones realizadas y estado; si no se resuelve, próximo paso concreto.

Las capturas deben conservar resolución nativa y ampliaciones enteras cuando hagan falta. Mantener EXPECTED_TEXT, VISIBLE_TRANSCRIPTION, GLYPH_REFERENCE, OCR_RAW y OCR_CONTEXT_ASSISTED separados. Si los píxeles no permiten reconocer una letra, el contexto no puede completar el resultado para otorgar PASS. La tipografía respeta cada familia nativa o rediseño expresamente aprobado; no se impone el centrado como regla universal.

## Métricas y criterios de publicación

Medir por familia y universo versionado: recursos censados, candidatos sin clasificar, traducciones pendientes, integraciones comprobadas, revisiones lingüísticas, consumidores probados, variantes vistas y fallos abiertos. No sumar unidades incompatibles ni convertir una muestra de capturas en cobertura total. Todo porcentaje debe indicar numerador, denominador y exclusiones. Si el universo crece, se actualiza el denominador y se explica el cambio.

La evidencia anterior puede conservarse cuando el recurso, consumidor y dependencias pertinentes no hayan cambiado y exista trazabilidad suficiente. Cambios en renderizadores, fuentes o recursos compartidos obligan a reconsiderar sus consumidores; no basta con que una cadena conserve sus bytes.

I26 puede concluir «versión de pruebas con pendientes», «continuar auditoría» o «candidato a lanzamiento aprobado». No hay avance automático a RC. FAIL o NOT_VALIDATED en una puerta obligatoria aplicable impide su aprobación según el reglamento. Los hallazgos no aplicables requieren una justificación comprobable; no se usan exclusiones para ocultar incertidumbre.

El paquete jugable incluirá fuentes completas acumulativas, BPS directo desde la ROM japonesa original, instrucciones, hashes, pruebas y pendientes. Los lanzadores Windows usarán `.bat`; se documentarán los entornos realmente probados. No es necesario redistribuir la ROM comercial.

## Formato de cierre de cada iteración

- Iteración y lote trabajados; ROM/hash de entrada y salida.
- Hallazgos y correcciones concretas.
- Pruebas ejecutadas y evidencia, separando natural y controlado.
- Resultado por criterio y pendientes, sin porcentajes globales no sustentados.
- Entregables y siguiente iteración o subiteración exacta.

## Identificación inicial

- ROM original: Riviera - Yakusoku no Chi Riviera (Japan).wsc; 8.388.608 bytes.
- SHA-256 original: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`.
- SHA-256 S447: `334a1d68f277279b3b5772fc26aa6f82b33984fd23b78857006ea29a1f389076`.
- Checksum S447 registrado: `AC25`.
- Fuentes de planificación: manifiesto S447, contexto de pendientes de esta conversación y reglamento universal v1.5. Actualización de fase 0: I01 e I02 ejecutadas y cerradas en su alcance técnico; no se concede aprobación global de traducción.

