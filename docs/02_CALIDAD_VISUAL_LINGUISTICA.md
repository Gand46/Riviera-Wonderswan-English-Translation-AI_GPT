# Alcance actual añadido en S463

Astra aprobó la página 9 modificada: Nobuyuki Hashimoto completo en dos líneas, glifos nativos intactos, sin recorte. Los seis nombres vecinos conservan sus píxeles tras ajustar posición vertical. Evidencia y primera lectura: validation/S463/VISUAL_ASTRA_S463.json. La lectura se acredita mediante créditos originales de juegos Bandai y compañeros coincidentes; la relación de identidad es una inferencia documentada, no una lectura adivinada de kanji.

Los intervalos I04 son gráficos sin texto, con prueba sintética. 高津利恵 sigue sin lectura acreditada. No hay aprobación lingüística/visual global.

## Evidencia heredada S462, con su alcance original

# Aprobación visual y lingüística acotada — RC6

## Alcance heredado

Se conserva el PASS previo únicamente para Hades, la escena posterior al final, cinco ramas, 32 páginas fullscreen de epílogo y la fila modificada de la página 8 de créditos. Sus recursos y renderers correspondientes son byte-idénticos en RC6.

## Alcance nuevo S462

| Recurso | Acceso | Resultado visual |
|---|---|---|
| `0x7CB227` — “Use selected / items only.” | `SAVESTATE_REPLAY_WITH_SCRIPTED_INPUT` | `PASS` |
| `0x7CDBE1` — “We wasted time. / We must hurry.” | `SAVESTATE_REPLAY_WITH_SCRIPTED_INPUT` | `PASS` |

Ambos recursos fueron alcanzados por rutas de juego desde checkpoints documentados, sin escrituras a ROM. Sus cuatro líneas coinciden exactamente con los píxeles de la fuente nativa, son legibles y no presentan recorte ni solapamiento.

Los otros veinte streams afectados por el selector tienen `PASS` estructural de integración: datos intactos y selección compacta restaurada en todos los offsets aplicables. No reciben un PASS visual individual nuevo en esta iteración.

No existe aprobación visual o lingüística global del proyecto. `FINAL_APPROVED=false` por I04 e I05.
