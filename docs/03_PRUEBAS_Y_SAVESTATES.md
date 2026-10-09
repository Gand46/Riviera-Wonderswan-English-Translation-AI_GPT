# Pruebas añadidas en S463

- validation/S463/credits_S463_RC7/page09_stable.mss corresponde al SHA-256 RC7 933cfcd5ea40f0f1d960338e78dc60ead6d8e5c280ea28bc69007f55ed2cc7aa.
- El homónimo bajo credits_S462_RC6_build/ pertenece a RC6, no a RC7.
- Ambos proceden del checkpoint S460 de final sintético, seguido de 3300 frames del guion de créditos. No prueban persistencia del guardado del juego.
- El replay completo dura 6000 frames; las 76 capturas fuera de la página cambiada coinciden. Los comandos originales y hashes están en RUN.json.
- I04 utiliza inyección de estado/registros y mapa BG sintético; prueba representación del gráfico, no acceso natural.

## Evidencia histórica S460 y anteriores

# Pruebas, capturas y savestates

## Entorno de ejecución

| Componente | Identidad |
|---|---|
| Mesen | 2.1.1 |
| SHA-256 del ejecutable usado | `ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41` |
| ROM RC4 requerida por los estados nuevos | `931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d` |

El emulador no se redistribuye. Los `.mss` suelen depender de la versión del emulador y del hash exacto del ROM.

## Rutas finales nuevas

La evidencia está en `validation/S460/final_routes/`:

- `final_route0_full`: ocho tramos encadenados, créditos comunes y retorno nativo.
- `final_route1_branch` a `final_route4_branch`: tres tramos por rama y retorno nativo.
- Cada tramo conserva `injected_anchor.mss`, checkpoints, `resume.mss`, capturas, lecturas de ROM y traza de CPU.
- Los estados `complete.mss` representan el retorno de cada secuencia.

La inyección coloca el secuenciador en la entrada nativa conocida y configura la rama; por ello acredita ejecución controlada y renderer real, no una llegada desde una partida completa sin asistencia.

## Mensajes condicionales

`validation/S460/optional_npc_synthetic/` conserva el estado inicial, trazas, 12 capturas y hoja de contacto de los ocho streams condicionados por flags. El ROM diagnóstico temporal no se incluye; su hash y las únicas redirecciones realizadas quedan documentados en `DIAGNOSTIC_BUILD.json`.

## High Score para revisión posterior

Los estados históricos solicitados se conservan en:

- `sources/QA_S458/astra_runtime/highscore/`
- `sources/QA_S458/astra_runtime/highscore_details/`
- `sources/QA_S458/astra_runtime/highscore_cold/`
- `sources/QA_S458/astra_runtime/highscore_cold_final/`
- `sources/QA_S458/astra_runtime/highscore_cold_jp/`
- `sources/QA_S458/astra_runtime/highscore_cold_rc1_control/`

La validación previa de escritura nativa y arranque en frío sigue archivada. La pantalla verde con artefactos queda como investigación comparativa de inicialización/emulador y no bloquea esta RC. Se excluyen los archivos SRAM `.sav` y `.srm` del paquete.

## Repetir la comparación actual

```text
python validation/S463/run_credit_qa.py --base-rom RC6.wsc --target-rom RC7.wsc --emulator /ruta/Mesen --out /ruta/QA_nueva
```

El estado fuente S460 se resuelve dentro del paquete; `--state` permite indicar otra ruta. El Lua no cambia bytes de ROM. Los registros RUN.json originales preservan los comandos ejecutados; el wrapper entregado permite configurar las rutas equivalentes.
