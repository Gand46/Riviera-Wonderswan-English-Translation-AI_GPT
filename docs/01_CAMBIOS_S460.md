# S460 RC4 — cambios integrados

## Objetivo

Cerrar los tres puntos abiertos de calidad de la RC3: el diálogo japonés posterior al final, la lectura ciega de las 32 páginas de epílogo y la aprobación visual y lingüística agregada.

## Integración binaria

- Se repuntaron **102 streams** del evento posterior al combate final hacia **139 páginas** inglesas.
- Se cubrieron el reencuentro, los NPC de Elendia, la cena y las cinco ramas de cierre: Serene, Lina, Fia, Cierra y neutral/Asgard.
- El bloque nuevo ocupa `0x7CED22..0x7CF865`; termina antes de `0x7D0000`.
- Se amplió el despachador compacto existente para admitir el rango reservado `ED22..FFFF` del banco correspondiente.
- El constructor cambió 2.996 bytes respecto de RC3 y no detectó bytes fuera de sus owners, datos nuevos, extensión del despachador y checksum.

## Revisión editorial final

La revisión de capturas encontró y corrigió una puntuación partida en la rama de Serene. En la misma pasada se pulieron siete frases para que conservaran el sentido dentro del límite de 15 caracteres por línea:

| Antes | RC4 final |
|---|---|
| `Glad to see / tomorrow.` | `Glad we have a / tomorrow.` |
| `and warm. nya.` | `and warm. Nya.` |
| `From the mine / I cheered.` | `I cheered from / the mine.` |
| `No, you do not!` | `No, not yet!` |
| `Magic may jump / ten years.` | `A ten-year leap / for magic!` |
| `Demons remain. / across Riviera.` | `Demons remain / in Riviera.` |
| `Okay. We will / do what we can.` | `Okay. We should / do what we can.` |

La transcripción inglesa de la versión GBA se usó como referencia editorial de contexto y terminología; la redacción se adaptó al cuadro de texto de WonderSwan.

## Identidad final

| Dato | Valor |
|---|---|
| Versión | `v0.113 S460 RC4` |
| SHA-256 de ROM resultante | `931e5cfec6e60fe3ad2b48b192b38bfd071d1a3b2453ddac3e1c271fb8da3c7d` |
| Tamaño | 8.388.608 bytes |
| Checksum WonderSwan | `22D1` |
| SHA-256 de base RC3 | `c79079537ea5f66cf74f94d48afc3da14dd9db1f8458156d337f5e0107c111dd` |

El paquete no incluye ROM, BIOS, emulador ni SRAM.
