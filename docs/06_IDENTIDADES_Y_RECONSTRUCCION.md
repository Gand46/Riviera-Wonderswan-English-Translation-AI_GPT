# Identidades, aplicación y reconstrucción

| Artefacto | SHA-256 |
|---|---|
| ROM japonesa limpia requerida | `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921` |
| ROM RC4 base | `931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d` |
| ROM RC5 resultante | `2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf` |
| BPS JP→RC5 | `89e0ad8f6ccce32122e467be1211943b5641ad18ede44301fb1e4a6b1789eee4` |

Aplicación directa:

```bash
python3 apply_patch.py /ruta/Riviera_JP_limpia.wsc /ruta/Riviera_RC5.wsc
```

Reconstrucción completa:

```bash
python3 sources/Riviera_S461_OVERLAY/rebuild.py \
  /ruta/Riviera_JP_limpia.wsc --out /ruta/Riviera_RC5_rebuilt.wsc
```

La cadena ejecuta S441→S461 y produjo RC5 byte-exacto. Durante el cierre se sustituyó la copia truncada del ZIP fuente S456 que había quedado dentro del paquete RC4 por el archivo completo validado; la identidad nueva está fijada en `sources/Riviera_S457_FULL_SOURCE/source/RELEASE.json`.
