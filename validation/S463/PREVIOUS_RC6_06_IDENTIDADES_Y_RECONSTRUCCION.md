# Identidades, aplicación y reconstrucción

| Artefacto | SHA-256 |
|---|---|
| ROM japonesa limpia requerida | `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921` |
| ROM RC5 base | `2eaeb2c90ca2ef62d858a887fa1ee2091d680b17366bf5dd07d642d0fc8171bf` |
| ROM RC6 resultante | `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204` |
| BPS JP→RC6 | `2a36c3ada7d4448fc629957854b3c8885ac7e58a0979fd64d52940bff15f2b4f` |

Aplicación directa:

```bash
python3 apply_patch.py /ruta/Riviera_JP_limpia.wsc /ruta/Riviera_RC6.wsc
```

Reconstrucción completa:

```bash
python3 build_rc6.py /ruta/Riviera_JP_limpia.wsc --out /ruta/Riviera_RC6_rebuilt.wsc
```

La cadena S441→S462 produjo RC6 byte-exacto sin usar BPS intermedios. La fuente acumulativa S456 se reensambla desde partes con tamaño y SHA-256 verificados.
