> Historical report for its stated version. Current I04/I05 status: [S463](10_S463_ASTRA_I04_I05.md).

# Cierre S461 / RC5

## Cambio binario único

La lectura confirmada `深尾伸也` → `Shinya Fukao` reemplaza la fila japonesa de “Tuning” en la página 8. El bloque comprimido `CREDIT-7A3C8D` se recompiló in situ en `0x7FEDE0..0x7FF4EA`; la nueva carga mide 1.777 bytes frente a 1.802. Fuente global, renderer, hooks, tablas de animación y otras páginas no cambiaron.

## Validación nueva

- Renderer real mediante arnés WRAM controlado y rutinas ROM nativas: `PASS`.
- Registros e integridad de escrituras: cero errores.
- Reconocimiento sin texto esperado como entrada: candidato único `Shinya Fukao`.
- Layout: 68 px, márgenes 14/14, sin recorte ni solapamiento.
- Diff RC4→RC5: 1.249 bytes, todos dentro del bloque comprimido autorizado y checksum.
- BPS directo JP→RC5: reaplicación byte-exacta.
- Reconstrucción S441→S461: byte-exacta.

## Pendientes

I04 permanece `NOT_VALIDATED`. I05 queda 1/3 `PASS`; 高津利恵 y 橋本信之 permanecen `NOT_VALIDATED`. En consecuencia `FINAL_APPROVED=false` y RC5 sigue siendo candidata, no aprobación final.
