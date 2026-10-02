# Riviera WSC English — v0.114 S461 RC5

Repositorio fuente depurado para GitHub y parche acumulativo directo desde la ROM japonesa original. No incluye ROM comercial, BIOS, emuladores, SRAM ni ejecutables.

## Estado

- Clasificación: `RELEASE_CANDIDATE_NOT_FINAL`
- `FINAL_APPROVED=false`
- ROM japonesa requerida, SHA-256: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`
- ROM RC5 esperada, SHA-256: `2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf`
- Checksum WonderSwan RC5: `2750`
- BPS acumulativo, SHA-256: `89e0ad8f6ccce32122e467be1211943b5641ad18ede44301fb1e4a6b1789eee4`

I04 continúa `NOT_VALIDATED`: no se identificó un consumidor auténtico del noveno recurso 6C ni se demostró desuso global. I05 continúa `NOT_VALIDATED`: `深尾伸也 → Shinya Fukao` está confirmado e integrado; `高津利恵` y `橋本信之` conservan sus píxeles japoneses al no existir lectura suficientemente respaldada.

La aprobación visual/lingüística se limita a Hades, escena posterior al final, cinco ramas, 32 páginas de epílogo y la fila modificada de la página 8 de créditos. No es una aprobación global del proyecto.

## Aplicar el BPS

Windows, macOS y Linux con Python 3:

```text
python apply_patch.py Riviera_JP_LIMPIA.wsc Riviera_EN_v0.114_S461_RC5.wsc
```

El aplicador rechaza una base incorrecta y verifica el SHA-256 de la salida.

## Reconstruir desde fuentes

Windows:

```text
BUILD.bat Riviera_JP_LIMPIA.wsc build\Riviera_EN_v0.114_S461_RC5.wsc
```

macOS o Linux:

```text
./BUILD.command Riviera_JP_LIMPIA.wsc build/Riviera_EN_v0.114_S461_RC5.wsc
```

La cadena reconstruye `S441 → S456 → S457 → S458 → S459 → S460 → S461` sin usar parches intermedios. El archivo fuente acumulativo S456 está dividido en tres partes menores de 100 MiB para ser compatible con GitHub. El constructor lo reensambla dentro de un directorio temporal y exige SHA-256 `f88217b6a17aa7b708167ada7b6741f2d3262bce063829506bbbe1ac7d8ee5f7`.

## Verificación del repositorio

```text
python verify_package.py
```

Comprueba archivos prohibidos, límite por archivo de GitHub, BPS, partes del archivo fuente y estado RC5. Los informes autoritativos están en `validation/S461/` y la documentación de cierre en `docs/`.

## Contenido

- `sources/`: fuentes acumulativas y overlays hasta S461.
- `patches/`: BPS acumulativo JP limpia → RC5.
- `validation/`: evidencia vigente de S460 y S461.
- `docs/`: cierre, alcance y pendientes.
- `release/RELEASE.json`: identidad y estado de release.
- `apply_patch.py`: aplicación verificada del BPS.
- `build_rc5.py`, `BUILD.bat`, `BUILD.command`: reconstrucción desde fuentes.
