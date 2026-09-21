"""
Pipeline de build da aplicação + instalador.

Uso (na raiz do projeto):
    venv\\Scripts\\python.exe build.py

Saídas:
    dist\\Automações Manhattan\\                       -> app em modo onedir (exe + _internal)
    dist\\Automações Manhattan_setup_<VERSION>.exe     -> instalador (onefile) para distribuir

Para nova versão: alterar apenas VERSION em version.py e rodar de novo.
"""

import os
import sys
import shutil
import zipfile
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
from version import APP_NAME, VERSION  # noqa: E402

PYINSTALLER = os.path.join(ROOT, "venv", "Scripts", "pyinstaller.exe")
if not os.path.exists(PYINSTALLER):
    PYINSTALLER = "pyinstaller"  # fallback: usa o do PATH

APP_SPEC = os.path.join(ROOT, f"{APP_NAME}.spec")
SETUP_SPEC = os.path.join(ROOT, "installer", "setup.spec")
INSTALL_BAT = os.path.join(ROOT, "installer", "install.bat")

DIST = os.path.join(ROOT, "dist")
APP_DIR = os.path.join(DIST, APP_NAME)
BUILD_INSTALLER = os.path.join(ROOT, "build_installer")
APP_ZIP = os.path.join(BUILD_INSTALLER, "app.zip")
VERSION_INFO = os.path.join(BUILD_INSTALLER, "version_info.txt")
SETUP_EXE = os.path.join(DIST, f"{APP_NAME}_setup_{VERSION}.exe")

# arquivos que interface.py lê em tempo de execução (raiz de _internal)
ARQUIVOS_OBRIGATORIOS = [
    f"{APP_NAME}.exe",
    "install.bat",
    os.path.join("_internal", "github.png"),
    os.path.join("_internal", "linkedin.png"),
    os.path.join("_internal", "help.png"),
    os.path.join("_internal", "icone.png"),
    os.path.join("_internal", "mini_icon.ico"),
    os.path.join("_internal", "icons", "mini_icon.ico"),
    os.path.join("_internal", "icons", "github.ico"),
    os.path.join("_internal", "icons", "help.ico"),
    os.path.join("_internal", "icons", "linkedin_1.ico"),
]


def etapa(titulo: str):
    print(f"\n=== {titulo} ===", flush=True)


def rodar(cmd):
    print(" ".join(f'"{c}"' if " " in c else c for c in cmd), flush=True)
    subprocess.run(cmd, check=True)


def mb(caminho: str) -> str:
    return f"{os.path.getsize(caminho) / 1024 / 1024:.1f} MB"


def gerar_version_info():
    partes = [int(p) for p in VERSION.split(".")] + [0] * 4
    tupla = tuple(partes[:4])
    conteudo = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={tupla},
    prodvers={tupla},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable('041604B0', [
        StringStruct('CompanyName', 'Luiz Guilherme'),
        StringStruct('FileDescription', 'Instalador do {APP_NAME}'),
        StringStruct('FileVersion', '{VERSION}'),
        StringStruct('InternalName', '{APP_NAME}_setup'),
        StringStruct('OriginalFilename', '{APP_NAME}_setup_{VERSION}.exe'),
        StringStruct('ProductName', '{APP_NAME}'),
        StringStruct('ProductVersion', '{VERSION}')
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1046, 1200])])
  ]
)
"""
    with open(VERSION_INFO, "w", encoding="utf-8") as f:
        f.write(conteudo)


def main():
    print(f"Build {APP_NAME} v{VERSION}")

    etapa("1/6 PyInstaller - aplicação (onedir)")
    rodar([PYINSTALLER, "--noconfirm", "--clean", APP_SPEC])

    etapa("2/6 Copiando install.bat")
    shutil.copy2(INSTALL_BAT, os.path.join(APP_DIR, "install.bat"))

    etapa("3/6 Checando arquivos obrigatórios")
    faltando = [a for a in ARQUIVOS_OBRIGATORIOS if not os.path.exists(os.path.join(APP_DIR, a))]
    if faltando:
        print("ERRO: arquivos ausentes em dist:\n  " + "\n  ".join(faltando))
        sys.exit(1)
    print("OK")

    etapa("4/6 Zipando aplicação")
    os.makedirs(BUILD_INSTALLER, exist_ok=True)
    if os.path.exists(APP_ZIP):
        os.remove(APP_ZIP)
    total = 0
    with zipfile.ZipFile(APP_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for pasta, _, arquivos in os.walk(APP_DIR):
            for nome in arquivos:
                caminho = os.path.join(pasta, nome)
                zf.write(caminho, os.path.relpath(caminho, APP_DIR))
                total += 1
    print(f"{total} arquivos -> {APP_ZIP} ({mb(APP_ZIP)})")

    etapa("5/6 Gerando version_info.txt")
    gerar_version_info()

    etapa("6/6 PyInstaller - instalador (onefile)")
    rodar([PYINSTALLER, "--noconfirm", "--clean", SETUP_SPEC])

    print("\n=== Concluído ===")
    print(f"App:        {APP_DIR}")
    print(f"Instalador: {SETUP_EXE} ({mb(SETUP_EXE)})")


if __name__ == "__main__":
    main()
