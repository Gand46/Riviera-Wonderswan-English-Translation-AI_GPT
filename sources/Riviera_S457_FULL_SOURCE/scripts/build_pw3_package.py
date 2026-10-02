#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PW3 = ROOT / "pw3"
PACKAGE_ROOT = PW3 / "package" / "Riviera_PW3_Rutas_Naturales_y_QA_Visual"
ZIP_PATH = PW3 / "package" / "Riviera_PW3_Rutas_Naturales_y_QA_Visual_FULL_PACKAGE.zip"


def cp(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


if PACKAGE_ROOT.exists():
    shutil.rmtree(PACKAGE_ROOT)
PACKAGE_ROOT.mkdir(parents=True)

# Full reproducible source chain from PW2, promoted and augmented for PW3.
source_in = ROOT / "pw2/package/Riviera_PW2_Corpus_y_Auditoria_Automatizada/fuentes/Riviera_S457_PW2_FULL_SOURCE"
source_out = PACKAGE_ROOT / "fuentes/Riviera_S457_PW3_FULL_SOURCE"
shutil.copytree(source_in, source_out)
cp(ROOT / "pw2/recovered_pw1/ruta/Riviera_Ruta_Complementaria_Work_Pendientes_Alcanzables.md", source_out / "Riviera_Ruta_Complementaria_Work_Pendientes_Alcanzables.md")
cp(PW3 / "build_pw3_results.py", source_out / "scripts/build_pw3_results.py")
cp(PW3 / "build_pw3_package.py", source_out / "scripts/build_pw3_package.py")
shutil.copytree(PW3 / "scripts/inputs", source_out / "scripts/pw3_inputs")
shutil.copytree(PW3 / "deliverables", source_out / "analysis/PW3")

# User-facing documentation and exact audits.
docs = PACKAGE_ROOT / "documentacion"
cp(ROOT / "pw2/recovered_pw1/resultados/Riviera_PW1_Recuperacion_y_Trazas_Tecnicas.md", docs / "Riviera_PW1_Recuperacion_y_Trazas_Tecnicas.md")
cp(ROOT / "pw2/deliverables/Riviera_PW2_Corpus_y_Auditoria_Automatizada.md", docs / "Riviera_PW2_Corpus_y_Auditoria_Automatizada.md")
cp(PW3 / "deliverables/Riviera_PW3_Rutas_Naturales_y_QA_Visual.md", docs / "Riviera_PW3_Rutas_Naturales_y_QA_Visual.md")
cp(ROOT / "pw2/recovered_pw1/ruta/Riviera_Ruta_Complementaria_Work_Pendientes_Alcanzables.md", docs / "Riviera_Ruta_Complementaria_Work_Pendientes_Alcanzables.md")
cp(ROOT / "pw2/r6/stage_r6_package/Riviera_R6_S457_Regresion_y_Dictamen_Final/DICTAMEN_R6.md", docs / "Riviera_R6_S457_Dictamen_Final.md")
cp(ROOT / "project_sources/17-WS_TRANSLATION_UNIVERSAL_RULES_v1.5.md", docs / "WS_TRANSLATION_UNIVERSAL_RULES_v1.5.md")

shutil.copytree(ROOT / "pw2/deliverables", PACKAGE_ROOT / "analisis/PW2")
shutil.copytree(PW3 / "deliverables", PACKAGE_ROOT / "analisis/PW3")
shutil.copytree(PW3 / "evidence", PACKAGE_ROOT / "evidencia/PW3_rutas")
shutil.copytree(PW3 / "scripts", PACKAGE_ROOT / "scripts/PW3")
cp(PW3 / "build_pw3_results.py", PACKAGE_ROOT / "scripts/build_pw3_results.py")
cp(PW3 / "build_pw3_package.py", PACKAGE_ROOT / "scripts/build_pw3_package.py")

# BPS direct from the clean Japanese ROM. No commercial ROM is packaged.
cp(ROOT / "pw2/recovered_pw1/patches/Riviera_CLEAN_JP_to_v0110_S457_cumulative.bps", PACKAGE_ROOT / "patches/Riviera_CLEAN_JP_to_v0110_S457_cumulative.bps")

# Verification outputs exclude the generated ROMs themselves.
for name in ("SHA256.txt", "source_rebuild.log", "bps_apply.log", "verification_result.txt"):
    cp(PW3 / "verification" / name, PACKAGE_ROOT / "verificacion" / name)

# Preserve the exact previous cumulative delivery for continuity.
cp(ROOT / "pw2/package/Riviera_PW2_Corpus_y_Auditoria_Automatizada_FULL_PACKAGE.zip", PACKAGE_ROOT / "entregas_previas/Riviera_PW2_Corpus_y_Auditoria_Automatizada_FULL_PACKAGE.zip")

readme = """# Riviera Work Pt1.5 — Paquete acumulativo PW3

- Etapa: `PW3 COMPLETADA` (`3/5`).
- ROM objetivo: S457 v0.110, SHA-256 `80ff36655d83956d96b634adafc685fa4379da326c3d45099dedcb73ef72a951`.
- BPS acumulativo directo desde la ROM japonesa limpia incluido en `patches/`.
- Fuentes reproducibles completas y cadena upstream incluidas en `fuentes/`.
- Documentación PW1–PW3, dictamen R6, matrices, scripts, capturas y estados incluidos.
- La entrega acumulativa PW2 exacta se preserva en `entregas_previas/`.
- La ROM japonesa comercial limpia no está incluida.

PW3 no modifica S457: no se demostró un defecto nuevo. La reconstrucción por fuentes y la aplicación del BPS siguen produciendo el mismo binario byte a byte. Team Edit natural permanece `NOT_VALIDATED`; High Score continúa diferido.
"""
(PACKAGE_ROOT / "README.md").write_text(readme, encoding="utf-8")

bad = [p for p in PACKAGE_ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".wsc", ".ws", ".rom"}]
if bad:
    raise SystemExit("Forbidden ROM files in package: " + ", ".join(str(p) for p in bad))

manifest = []
for p in sorted(PACKAGE_ROOT.rglob("*")):
    if p.is_file() and p.name != "SHA256SUMS.txt":
        manifest.append((sha256(p), p.relative_to(PACKAGE_ROOT).as_posix(), p.stat().st_size))
(PACKAGE_ROOT / "SHA256SUMS.txt").write_text("".join(f"{h}  {name}\n" for h, name, _ in manifest), encoding="utf-8")

ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
if ZIP_PATH.exists():
    ZIP_PATH.unlink()
store_suffixes = {".zip", ".bps", ".ips", ".png", ".mss", ".sav", ".bin"}
with zipfile.ZipFile(ZIP_PATH, "w", allowZip64=True) as z:
    for p in sorted(PACKAGE_ROOT.rglob("*")):
        if not p.is_file():
            continue
        arc = (Path(PACKAGE_ROOT.name) / p.relative_to(PACKAGE_ROOT)).as_posix()
        compression = zipfile.ZIP_STORED if p.suffix.lower() in store_suffixes else zipfile.ZIP_DEFLATED
        z.write(p, arc, compress_type=compression)

with zipfile.ZipFile(ZIP_PATH) as z:
    bad_member = z.testzip()
    if bad_member is not None:
        raise SystemExit(f"ZIP CRC failure: {bad_member}")
    entries = len(z.infolist())
    direct_rom_entries = [n for n in z.namelist() if Path(n).suffix.lower() in {".wsc", ".ws", ".rom"}]
    if direct_rom_entries:
        raise SystemExit("Forbidden ROM entries in ZIP")

result = {
    "package": str(ZIP_PATH),
    "bytes": ZIP_PATH.stat().st_size,
    "sha256": sha256(ZIP_PATH),
    "entries": entries,
    "crc_test": "PASS",
    "direct_rom_entries": 0,
    "manifest_files": len(manifest),
}
(PW3 / "package/PACKAGE_VERIFICATION_PW3.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
