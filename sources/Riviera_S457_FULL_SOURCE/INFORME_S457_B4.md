# Riviera S457 v0.110 — informe B4: tipografía y superficies

## Resultado

B4 queda **entregado parcialmente**. S457 corrige la colisión visual entre la `I` mayúscula y la `l` minúscula en cuatro nombres de créditos. La fuente global de ROM no cambia y no existe todavía aprobación visual ni final global.

- ROM S457: `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`
- Checksum WonderSwan: `D44D`
- Cambios respecto de S456: 7.361 bytes, todos dentro de cuatro gráficos compilados, el manejador reservado y el checksum.
- Reconstrucción desde fuentes: idéntica byte por byte.
- BPS e IPS acumulativos desde JP limpio: idénticos a S457.

## Corrección tipográfica

La fuente nativa almacenaba `I` y `l` con los mismos 50 bytes. S457 conserva el tallo nativo de un píxel y añade barras superior e inferior de tres píxeles solo al componer `I` en **Takeo Isogai, Tomofumi Ishida, Yoshinori Iwanaga y Fumie Ishinaka**. La fuente ROM de 52 glifos mantiene SHA-256 `56bbbae560868f39dcdc04f48023c829c8fad6e7f3d445154caff02daee84f19`.

La prueba sin palabras esperadas obtuvo 11/11 identificaciones correctas, incluidas cuatro `I` tomadas de ejecución. Este resultado no se extiende a lectura ciega de palabras completas.

## Validación ejecutada

| Área | Evidencia | Resultado |
|---|---:|---|
| Créditos | 13 páginas | Guardas limpias; solo cambian 0, 2, 4 y 5 |
| Combate | 83 capturas / 2.500 cuadros | Idénticas a S455 |
| Prólogo | 15 capturas / 4.800 cuadros | S456 y S457 idénticas |
| Team Edit | entrada nativa controlada | Textos y formaciones legibles; ROM no mutada |
| Reconstrucción | cadena S442–S457 | S457 exacta |
| Parches | BPS e IPS desde JP limpio | S457 exacta |

## Pendientes validados como abiertos

- Lectura sin contexto de palabras completas.
- Matriz contextual completa de diálogos, tutoriales, menús y gráficos.
- Team Edit por progresión natural y sus variantes.
- Créditos por progresión natural, tiempos y transición final.
- Pendientes heredados de B2 y B3: tres lecturas, dos candidatos técnicos, brechas de cobertura y resto narrativo/lingüístico.

## Ruta

Se consumieron 4 de 8 iteraciones máximas. Quedan B5, B6 y dos reservas: máximo cuatro. La siguiente etapa es **B5 — recorridos funcionales y contenido tardío**.
