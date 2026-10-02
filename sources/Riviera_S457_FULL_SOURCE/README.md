# Riviera S457 v0.110 — fuentes completas

Este paquete contiene el cambio B4, evidencia acotada y el parche acumulativo. No incluye una ROM comercial.

## Identidades

- JP limpia: `62f3886d3bae02105e56677ae7f5efe77ff7cb47036d2955ca46ea4a3f712921`
- S456 base: `b6ae03cda1be9d1742ca7aae3cfc32fe389c3fd51e9e3bc5b4929ff3653dcdc1`
- S457 destino: `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`

## Reconstrucción

```bash
python scripts/rebuild_s457.py /ruta/Riviera_JP_limpia.wsc --out build/Riviera_v0110_S457.wsc
```

El proceso reconstruye primero S456 desde su paquete de fuentes y luego aplica el constructor formal de S457. También puede aplicarse el BPS acumulativo:

```bash
python scripts/apply_s457.py /ruta/Riviera_JP_limpia.wsc --out build/Riviera_v0110_S457.wsc
```

## Verificación

Tras disponer de la JP limpia, S456, S457 candidata y S457 reconstruida:

```bash
python scripts/verify_s457.py JP.wsc S456.wsc S457.wsc S457_rebuilt.wsc
```

El verificador cubre hashes, checksum, compilación, BPS/IPS, rangos, fuente, tablas de animación y la evidencia B4 incluida. El PASS es acotado; consulte `analysis/B4/OPEN_ISSUES.json`.

Para repetir la entrada controlada de Team Edit con Mesen:

```bash
python scripts/run_route.py team_controlled qa/checkpoints/S446_CONTROLLED_TEAM_HEADER.mss 360 '[["a",20,28]]' --rom /ruta/S457.wsc --mesen /ruta/Mesen --access controlled_native_screen_entry
```
