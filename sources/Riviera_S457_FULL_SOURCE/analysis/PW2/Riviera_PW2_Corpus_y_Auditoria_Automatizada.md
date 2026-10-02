# Riviera Work Pt1.5 — PW2 Corpus y auditoría automatizada

**Fecha:** 2026-09-25  
**Estado:** `PW2 COMPLETADA` — presupuesto consumido `2/5`  
**Binario modificado:** no  
**Siguiente etapa:** `PW3 — Rutas naturales cortas y QA visual dirigida`

## 1. Resultado ejecutivo

PW2 reconstruyó la mayor matriz defendible a partir de direcciones, intervalos, propietarios y consumidores reales: **1.766 recursos**, **3.418 usos** y **3.325 comprobaciones de puntero**. Los 1.766 intervalos coinciden byte a byte con S457. No se generó ninguna ROM ni un BPS nuevo.

El contador histórico `1.436/1.436` no pudo convertirse legítimamente en 1.436 filas editables. La cadena de fuentes conserva una fila agregada denominada `Main indexed text` y la afirmación agregada de que Bank66 `595/595` es un subconjunto, pero no conserva las claves, direcciones, punteros ni pares de texto de aquellas filas. Conforme a la regla de detención de PW2, no se fabricaron identificadores `HIST-0001…HIST-1436`.

| Puerta | Resultado PW2 | Evidencia |
| --- | --- | --- |
| Identidad S457 | `PASS` | SHA-256 exacto y aplicación BPS desde la ROM japonesa limpia. |
| Matriz real de recursos | `PASS_STATIC` | 1.766/1.766 hashes de intervalo coinciden. |
| Punteros/propietarios | `PASS_STATIC_SCOPED` | 3.325/3.325 comprobaciones heredadas y 147/147 registros crudos cotejados sobre S457. |
| Residuos 47 | `45 CLASSIFIED / 2 NOT_VALIDATED` | No se confirmó deuda de traducción; I04 conserva dos casos técnicos. |
| CORPUS-1436 | `NOT_VALIDATED` | Falta el índice fila-a-fila de v0.25 o un equivalente reproducible. |
| BANK66-595 | `NOT_VALIDATED_KEY_LEVEL` | La relación de subconjunto solo está documentada a nivel agregado. |
| QA visual global | `NOT_VALIDATED` | La matriz prioriza la ejecución posterior; una coincidencia binaria no concede aprobación visual. |

High Score permanece `DEFERRED` y fuera del presupuesto de esta ruta.

## 2. Identidad binaria

| Elemento | SHA-256 |
| --- | --- |
| ROM japonesa limpia | `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921` |
| S457 aplicada desde el BPS | `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951` |
| BPS acumulativo vigente | `e4bda7c628316fb92978f33ffc136c7f480f2a885f0b606be46e09b7c2335cef` |

La aplicación BPS produjo 8 MiB y el hash objetivo exacto. La ROM comercial no forma parte del paquete entregado.

## 3. Matriz real recuperada

`RESOURCE_MATRIX_1766.csv/json` contiene por recurso:

- identificador estable, clase, banco, dirección física e intervalo;
- hash del intervalo y comparación con S457;
- etiqueta integrada disponible y procedencia documental;
- usos, propietarios y consumidores enlazados;
- estados lingüístico, integración, runtime y visual;
- cola de contexto y estimación conservadora de riesgo de ancho.

Distribución del universo: 931 `TEXT`, 662 `LZ`, 76 `SCRIPT`, 59 `RAW` y 38 `CREDIT_STREAM`. Existen 1.590 recursos con al menos una arista I03 y 176 sin arista I03: 79 LZ, 59 RAW y 38 streams de créditos. Estos 176 casos se clasifican como **vínculo de consumidor ausente**, no como recursos huérfanos ni desusados demostrados.

No existen intervalos duplicados. Hay ocho grupos de contenido binario idéntico en direcciones distintas; se conservan porque pueden ser propietarios legítimamente distintos.

## 4. Punteros y contexto

Las 3.325 comprobaciones familiares heredadas permanecen `match=true`. Además, los 147 registros que conservan sus bytes crudos de tabla fueron cotejados directamente contra S457: 147 coincidencias y cero discrepancias.

Quedan 93 usos con `NO_DIRECT_OWNER_FIELD_IN_INVENTORY`. Se mantienen en `NEEDS_CONTEXT`; no son fallos de puntero. La matriz conserva la identidad del recurso y sus consumidores conocidos para que PW3 pueda priorizar únicamente casos alcanzables.

## 5. Residuos y búsqueda japonesa

La conciliación de los 47 residuos produce:

- 40 `CLASSIFIED_GRAPHIC_DATA`;
- 4 `CLASSIFIED_VM_METADATA`;
- 1 `CLASSIFIED_GRAPHIC_TEXT_ALREADY_ENGLISH`;
- 2 `UNRESOLVED_TECHNICAL_NOT_CONFIRMED_TEXT`: `CP932-15939` y `CP932-15968`.

No se confirmó ningún residuo como deuda lingüística. Las pasadas CP932 acotadas a Bank66, Bank7A y Bank7C se conservaron solo como triage: los datos gráficos y la fuente personalizada generan falsos positivos, por lo que esos resultados no conceden PASS lingüístico.

## 6. Ancho y revisión manual

La estimación de ancho marcó nueve etiquetas TEXT cuyo tramo de línea supera un proxy conservador de 96 píxeles. El proxy no conoce el rectángulo de cada consumidor y, por tanto, solo alimenta `NEEDS_VISUAL`; no se declara overflow.

`MANUAL_REVIEW_60.csv` respeta el máximo fijado e incluye:

- 7 casos críticos: corpus, Bank66, dos residuos y tres lecturas;
- 18 propietarios que requieren contexto;
- 20 muestras estratificadas sin arista I03;
- 15 casos priorizados por riesgo de ancho/longitud.

La decisión manual no cerró falsamente ninguno: los casos se asignaron a `NEEDS_CONTEXT`, `NEEDS_CONSUMER_EDGE`, `NEEDS_VISUAL` o `NOT_VALIDATED` con la evidencia requerida.

## 7. Dictamen CORPUS-1436/595

PW2 aplicó la condición de detención prevista. Para conceder PASS hacen falta uno de estos insumos equivalentes:

1. el índice editable fila-a-fila de v0.25;
2. un volcado reproducible con clave estable, propietario físico, texto original e integrado para cada fila;
3. la lista de 595 claves Bank66 cruzada contra esas mismas 1.436 claves.

El contador agregado sí permite conservar la afirmación histórica de subconjunto, pero no demostrarla por claves. Por ello `CORPUS-1436` y `BANK66-595` permanecen abiertos sin ampliar el número de iteraciones.

## 8. Entrada precisa para PW3

PW3 debe comenzar por la matriz y las colas generadas, no por una nueva búsqueda masiva. Prioridad:

1. nueve banderas de ancho en sus consumidores reales;
2. casos `NEEDS_CONTEXT` alcanzables en diálogo, menús, tutorial, inventario, equipo y combate;
3. ruta natural desde DATA:1 hacia Team Edit, conservando estados antes/dentro/después;
4. hasta tres rutas de 20.000 fotogramas y máximo doce checkpoints seleccionados;
5. corrección inmediata únicamente si se demuestra un defecto visual o funcional.

La salida de PW3 deberá distinguir `runtime-confirmed` de `visual-approved`; OCR o presencia de texto no bastan para aprobar legibilidad.

## 9. Entregables

- `RESOURCE_MATRIX_1766.csv/json`
- `CORPUS_1436_RECONCILIATION.json`
- `POINTER_AUDIT.json`
- `INVENTORY_ORPHAN_DUPLICATE_AUDIT.json`
- `RESIDUAL_AUDIT_47.json`
- `QA_QUEUES.json`
- `MANUAL_REVIEW_60.csv`
- `TEXT_AUDIT_INTERPRETATION.json`
- `PW2_GATE_RESULTS.json` y `PW2_SUMMARY.json`

El paquete acumulativo incluye este informe, la ruta actualizada, toda la fuente S457 reproducible, el BPS directo desde la ROM japonesa, los scripts de PW2 y el paquete PW1 previo. No incluye ninguna ROM comercial.
