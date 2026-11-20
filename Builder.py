"""
Gera o executavel do app Loja de Pipas com PyInstaller.

Uso:
    python Builder.py

Resultado:
    dist/LojaPipas/LojaPipas.exe
"""

from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys


PASTA_PROJETO = Path(__file__).resolve().parent
NOME_APP = "LojaPipas"
ARQUIVO_PRINCIPAL = PASTA_PROJETO / "loja.py"
ARQUIVO_UI = PASTA_PROJETO / "loja.ui"
ARQUIVO_UI_PY = PASTA_PROJETO / "loja_ui.py"
ARQUIVO_BANCO = PASTA_PROJETO / "LojaDePipasUni9.db"
PASTA_DIST = PASTA_PROJETO / "dist"
PASTA_BUILD = PASTA_PROJETO / "build"


def executar(comando):
    print("$ " + " ".join(str(parte) for parte in comando))
    subprocess.run(comando, cwd=PASTA_PROJETO, check=True)


def instalar_pyinstaller():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller nao encontrado. Instalando...")
        executar([sys.executable, "-m", "pip", "install", "PyInstaller"])


def limpar_saida_anterior():
    destino = PASTA_DIST / NOME_APP
    if destino.exists():
        shutil.rmtree(destino)
    executavel = PASTA_DIST / f"{NOME_APP}.exe"
    if executavel.exists():
        executavel.unlink()

    pasta_spec = PASTA_BUILD / NOME_APP
    if pasta_spec.exists():
        shutil.rmtree(pasta_spec)


def criar_banco_local(pasta):
    banco = pasta / "LojaDePipasUni9.db"
    if banco.exists():
        return banco

    pasta.mkdir(parents=True, exist_ok=True)
    conexao = sqlite3.connect(banco)
    conexao.close()
    print(f"Banco criado: {banco}")
    return banco


def converter_ui():
    # O conversor transforma todos os componentes visuais do arquivo .ui em codigo Python.
    uic = Path(sys.executable).with_name("pyside6-uic.exe")
    if not uic.is_file():
        uic = PASTA_PROJETO / ".venv" / "Scripts" / "pyside6-uic.exe"
    if not uic.is_file():
        raise FileNotFoundError("Nao encontrei o pyside6-uic.exe.")

    executar([str(uic), str(ARQUIVO_UI), "-o", str(ARQUIVO_UI_PY)])


def principal():
    faltando = [
        str(arquivo.name)
        for arquivo in (ARQUIVO_PRINCIPAL, ARQUIVO_UI)
        if not arquivo.is_file()
    ]
    if faltando:
        print("Arquivos necessarios nao encontrados:", ", ".join(faltando))
        return 1

    instalar_pyinstaller()
    converter_ui()
    limpar_saida_anterior()

    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        NOME_APP,
        "--onefile",
        "--noconsole",
        "--clean",
        "--distpath",
        str(PASTA_DIST),
        "--workpath",
        str(PASTA_BUILD),
        "--specpath",
        str(PASTA_BUILD),
        str(ARQUIVO_PRINCIPAL),
    ]

    executar(comando)

    destino = PASTA_DIST
    destino.mkdir(parents=True, exist_ok=True)
    if ARQUIVO_BANCO.is_file():
        shutil.copy2(ARQUIVO_BANCO, destino / ARQUIVO_BANCO.name)
    else:
        criar_banco_local(destino)
    executavel = destino / f"{NOME_APP}.exe"
    print("\nExecutavel gerado com sucesso:")
    print(executavel)
    print("\nEste e um arquivo unico. Ao executar, o banco sera criado ao lado do .exe.")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())