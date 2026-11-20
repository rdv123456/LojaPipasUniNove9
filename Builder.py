"""
Gera o executavel do app Loja de Pipas com PyInstaller.

Uso:
    python Builder.py

Resultado:
    dist/LojaPipas/LojaPipas.exe
"""

from pathlib import Path
import shutil
import subprocess
import sys


PASTA_PROJETO = Path(__file__).resolve().parent
NOME_APP = "LojaPipas"
ARQUIVO_PRINCIPAL = PASTA_PROJETO / "loja.py"
ARQUIVO_UI = PASTA_PROJETO / "loja.ui"
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

    pasta_spec = PASTA_BUILD / NOME_APP
    if pasta_spec.exists():
        shutil.rmtree(pasta_spec)


def principal():
    faltando = [
        str(arquivo.name)
        for arquivo in (ARQUIVO_PRINCIPAL, ARQUIVO_UI, ARQUIVO_BANCO)
        if not arquivo.is_file()
    ]
    if faltando:
        print("Arquivos necessarios nao encontrados:", ", ".join(faltando))
        return 1

    instalar_pyinstaller()
    limpar_saida_anterior()

    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        NOME_APP,
        "--onedir",
        "--noconsole",
        "--clean",
        "--distpath",
        str(PASTA_DIST),
        "--workpath",
        str(PASTA_BUILD),
        "--specpath",
        str(PASTA_BUILD),
        "--add-data",
        f"{ARQUIVO_UI};.",
        "--hidden-import",
        "PySide6.QtUiTools",
        str(ARQUIVO_PRINCIPAL),
    ]

    executar(comando)

    destino = PASTA_DIST / NOME_APP
    shutil.copy2(ARQUIVO_BANCO, destino / ARQUIVO_BANCO.name)
    shutil.copy2(ARQUIVO_UI, destino / ARQUIVO_UI.name)

    executavel = destino / f"{NOME_APP}.exe"
    print("\nExecutavel gerado com sucesso:")
    print(executavel)
    print("\nExecute o arquivo .exe dentro da pasta; mantenha o banco e o .ui na mesma pasta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())