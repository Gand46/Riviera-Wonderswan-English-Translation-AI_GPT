# Identidades y reconstrucción — S463 RC7

| Artefacto | SHA-256 |
|---|---|
| ROM JP original | `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921` |
| ROM RC6 base | `b8aa59568a860c229751f504e2b5e9cd81d21909507e9f685c6f3797f18c1204` |
| ROM RC7 resultante | `933cfcd5ea40f0f1d960338e78dc60ead6d8e5c280ea28bc69007f55ed2cc7aa` |
| BPS JP→RC7 | `c70c704ddd0f9e67646ea4bcb67c38be725648b1893b55b540ff07f0f37ade0f` |

Tamaño: 8388608 bytes. Checksum WonderSwan: 2564.

```text
python apply_patch.py ROM_JP_LIMPIA.wsc SALIDA_RC7.wsc
python build_rc7.py ROM_JP_LIMPIA.wsc --out SALIDA_RC7_REBUILT.wsc
```

La cadena completa S441–S463 no usa parches intermedios. Se ejecutó en Linux con Python; BUILD.bat y BUILD.command llaman al mismo punto de entrada. Las salidas coinciden byte por byte. El origen y el destino deben ser archivos distintos.
