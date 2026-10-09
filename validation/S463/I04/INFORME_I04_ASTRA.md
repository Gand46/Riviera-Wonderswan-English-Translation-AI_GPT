# I04 — cierre gráfico de dos candidatos CP932

**Resultado: PASS para la clasificación gráfica de ambos intervalos mediante consumidor nativo y presentación sintética documentada.** No se modificó la ROM. El alcance natural de este noveno recurso sigue sin demostrarse; no se afirma que esté usado o sin usar durante una partida.

ROM comprobada: `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204` (S462/RC6).

| Candidato | Intervalo, fin exclusivo | Bytes / píxeles | Clasificación |
|---|---|---:|---|
| CP932-15939 | 0x6CAE90..0x6CAE99 | 9 / 18 | CONFIRMED_GRAPHIC_NON_TEXT |
| CP932-15968 | 0x6CAD76..0x6CAD81 | 11 / 22 | CONFIRMED_GRAPHIC_NON_TEXT |

## Recurso y límites

`0x6CACBE..0x6CAEBE` contiene exactamente 512 bytes: dieciséis tiles 8×8, empaquetados a 4 bpp, cuatro por fila y cuatro filas; el nibble alto es el primer píxel. El conjunto forma un edificio/torre de 32×32, con cubierta, aberturas y estructuras laterales. Los dos candidatos corresponden a píxeles internos de ese dibujo, no a letras ni cadenas. `byte_pixel_mapping.csv` conserva el vínculo exacto entre cada byte ROM, byte WRAM, tile y par de píxeles; los subconjuntos también están en el JSON de cierre.

Tras los 512 bytes está una paleta de 32 bytes `0x6CAEBE..0x6CAEDE`. El inventario heredado identifica el siguiente recurso independiente `RIV-LZ-6CAEDE`, de 426 bytes. La frontera también coincide con el tamaño de transferencia nativo y la geometría completa mostrada por la PPU. No se deduce el límite de una decodificación CP932 ni se desechan intervalos vecinos en bloque.

## Consumidor realmente ejecutado

Se reutiliza la rama nativa que construye los descriptores gráficos para los ocho iconos conocidos. Su recorrido original inicia BP=9CBE, ejecuta ocho iteraciones y avanza BP en 0200; **por sí solo termina antes del noveno**. Esta limitación histórica no se oculta ni se vuelve a probar exhaustivamente.

El arnés coloca BP=ACBE y destino=4000 en WRAM, fija los bancos y entra en `5000:4A54`. Se ejecutan los opcodes originales de construcción del descriptor y el asignador `2000:377F`. El descriptor resultante es:

`04 00 BE AC 00 30 00 40 00 00 00 02 00 00`

Es decir: tipo 4, fuente 3000:ACBE, destino WRAM 4000, longitud 0200. El arnés salta al dispatcher nativo `2000:37AF`; la rama nativa tipo 4 `2000:384A..3878` programa y dispara GDMA. En el punto anterior al disparo, Mesen registra:

- `gdmaSrc=240830` = CPU 0x3ACBE.
- `gdmaDest=16384` = WRAM 0x4000.
- `gdmaLength=512`.
- banco C3=108 = 0x6C; la conversión de direcciones confirma ROM 0x6CACBE..0x6CAEBD.

La salida DMA es idéntica en **512/512 bytes** al recurso ROM. Por lo tanto incluye intactos los 9 y 11 bytes de ambos candidatos. Los bytes de píxeles no son copiados manualmente por Lua ni reescritos después del DMA.

**Limitación instrumental:** el callback `wsPrgRom/read` emitió cero eventos para GDMA. No se presenta ese contador como una traza positiva ni como ausencia de consumo. La evidencia positiva es la combinación de rama nativa ejecutada, registros hardware previos, mapeo de fuente y comparación íntegra de la salida DMA. `resource_reads.csv` conserva expresamente esta observación.

## Presentación real y acceso sintético

El arnés configura BG1 en modo packed 4bpp, sitúa los dieciséis tiles ya transferidos en una cuadrícula 4×4 y carga la paleta adyacente. Se captura la pantalla de Mesen tras cuatro frames: `screen.png`. El icono está en x=96..127, y=56..87. La franja derecha de 13 píxeles pertenece a indicadores del emulador; la pantalla de juego es 224×144.

Los **1024/1024 píxeles** del icono capturado coinciden con la reconstrucción independiente del recurso y la paleta, usando la cuantización nativa observada de Mesen (4 bits por canal ×16). `complete_resource_32x32.png` contiene el recurso completo; `runtime_crop8x.png` amplía la captura por vecino más próximo para inspección, y no sustituye la captura nativa.

Se ve un dibujo de edificio sin texto. Ambos intervalos quedan clasificados como gráficos; traducción, lingüística y tipografía de texto son N/A para estos dos candidatos. La confirmación de consumidor y PPU es **SYNTHETIC_NATIVE_DESCRIPTOR_DMA_PPU**, no una escena alcanzada jugando. El mapa BG1, posición y selección de recurso fueron impuestos por el arnés. No se identifica una escena natural ni se demuestra desuso universal. Tampoco se transfiere este PASS a otros recursos, a la partida completa o a la aprobación final del proyecto.

## Reproducir

```bash
python run_probe.py --rom /ruta/Riviera_S462_RC6_build.wsc --emulator /ruta/Mesen --out /ruta/evidencia
python verify_graphic.py --rom /ruta/Riviera_S462_RC6_build.wsc --evidence /ruta/evidencia
```

Requiere Mesen 2.1.1 Linux y Pillow. El runner fija `LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6` para este entorno, límite Mesen 15 s y watchdog del proceso 25 s. No contiene ni produce un parche. `RUN.json`, `RESULT.json`, `dma_state.txt`, `source_mapping.json`, `native_descriptor.bin`, `native_pixels.bin`, `executed_pcs.txt` y `mesen.log` conservan la procedencia. Las advertencias de lecturas WRAM no inicializadas durante el arranque quedan en el log; no alteraron la igualdad íntegra del descriptor, destino ni pantalla comprobados.

El estado anterior S461 `NOT_VALIDATED` queda preservado en el paquete padre. La transición actual es únicamente `UNRESOLVED_TECHNICAL_NOT_CONFIRMED_TEXT` → `CONFIRMED_GRAPHIC_NON_TEXT`, con alcance sintético explícito. No se repitieron los ocho hermanos cerrados ni los barridos de 65.536 selectores y 4.096 alias.
