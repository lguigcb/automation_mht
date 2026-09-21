r"""
Instalador do Automações Manhattan.

Substitui o SFX do WinRAR usado até a 1.6.x, reproduzindo o mesmo comportamento:
  - Telas "Sobre" (readme.txt) e "Licença" (LICENSE.txt)
  - Extrai o app (onedir do PyInstaller, zipado em app.zip) em %APPDATA%\Automações Manhattan
  - Roda install.bat após a extração (equivalente ao "Setup=" do WinRAR)
  - Cria atalhos na área de trabalho e no menu iniciar
  - Registra em HKCU a entrada de desinstalação (só usuário atual, sem admin)

Empacotado com installer\setup.spec (onefile). Não exige privilégios de administrador.
"""

import os
import sys
import glob
import shutil
import zipfile
import logging
import threading
import subprocess
import traceback
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from version import APP_NAME, VERSION
except ImportError:  # rodando congelado: version.py vai como data
    exec(open(os.path.join(getattr(sys, "_MEIPASS", "."), "version.py"), encoding="utf-8").read())

EXE_NAME = f"{APP_NAME}.exe"
UNINSTALL_KEY = "AutomacoesManhattan"
CREATE_NO_WINDOW = 0x08000000

LOG_PATH = os.path.join(os.environ.get("TEMP", "."), "AutomacoesManhattan_setup.log")
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8")


def resource_path(nome: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, nome)


def ler_texto(nome: str) -> str:
    caminho = resource_path(nome)
    try:
        with open(caminho, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(caminho, encoding="latin-1") as f:
            return f.read()
    except FileNotFoundError:
        return f"(arquivo {nome} não encontrado no instalador)"


def pasta_destino() -> str:
    return os.path.join(os.environ["APPDATA"], APP_NAME)


class Instalador:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"Instalador - {APP_NAME} v{VERSION}")
        self.root.geometry("640x480")
        self.root.minsize(560, 420)
        self.root.resizable(True, True)
        try:
            self.root.iconbitmap(resource_path("mini_icon.ico"))
        except Exception:
            pass

        self.destino = pasta_destino()
        self.aceitou = tk.BooleanVar(value=False)
        self.abrir_ao_concluir = tk.BooleanVar(value=True)
        self.progresso = tk.DoubleVar(value=0)
        self.status = tk.StringVar(value="")
        self.instalando = False
        self.concluido = False

        self.container = ttk.Frame(root, padding=12)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.rodape = ttk.Frame(root, padding=(12, 0, 12, 12))
        self.rodape.pack(fill=tk.X)
        self.btn_cancelar = ttk.Button(self.rodape, text="Cancelar", command=self.cancelar)
        self.btn_cancelar.pack(side=tk.RIGHT)
        self.btn_avancar = ttk.Button(self.rodape, text="Avançar >")
        self.btn_avancar.pack(side=tk.RIGHT, padx=(0, 8))

        self.root.protocol("WM_DELETE_WINDOW", self.cancelar)
        self.tela_sobre()

    # ---------------- telas ----------------
    def _limpar(self):
        for w in self.container.winfo_children():
            w.destroy()

    def _texto_rolavel(self, titulo: str, conteudo: str):
        ttk.Label(self.container, text=titulo, font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 8))
        caixa = ScrolledText(self.container, wrap=tk.WORD, font=("Segoe UI", 9))
        caixa.pack(fill=tk.BOTH, expand=True)
        caixa.insert("1.0", conteudo)
        caixa.configure(state=tk.DISABLED)

    def tela_sobre(self):
        self._limpar()
        self._texto_rolavel("Sobre", ler_texto("readme.txt"))
        self.btn_avancar.configure(text="Avançar >", command=self.tela_licenca, state=tk.NORMAL)

    def tela_licenca(self):
        self._limpar()
        self._texto_rolavel("Licença", ler_texto("LICENSE.txt"))
        opcoes = ttk.Frame(self.container)
        opcoes.pack(anchor=tk.W, pady=(8, 0))
        ttk.Radiobutton(opcoes, text="Aceito os termos da licença", variable=self.aceitou, value=True,
                        command=self._atualizar_botao_licenca).pack(anchor=tk.W)
        ttk.Radiobutton(opcoes, text="Não aceito", variable=self.aceitou, value=False,
                        command=self._atualizar_botao_licenca).pack(anchor=tk.W)
        self.btn_avancar.configure(text="Instalar", command=self.tela_instalacao)
        self._atualizar_botao_licenca()

    def _atualizar_botao_licenca(self):
        self.btn_avancar.configure(state=tk.NORMAL if self.aceitou.get() else tk.DISABLED)

    def tela_instalacao(self):
        self._limpar()
        ttk.Label(self.container, text="Instalação", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 8))
        ttk.Label(self.container, text="Pasta de destino:").pack(anchor=tk.W)
        destino = ttk.Entry(self.container)
        destino.insert(0, self.destino)
        destino.configure(state="readonly")
        destino.pack(fill=tk.X, pady=(0, 12))

        ttk.Progressbar(self.container, variable=self.progresso, maximum=100).pack(fill=tk.X)
        ttk.Label(self.container, textvariable=self.status).pack(anchor=tk.W, pady=(4, 8))

        self.log_box = ScrolledText(self.container, height=8, font=("Consolas", 9), state=tk.DISABLED)
        self.log_box.pack(fill=tk.BOTH, expand=True)

        self.chk_abrir = ttk.Checkbutton(self.container, text=f"Abrir {APP_NAME} ao concluir", variable=self.abrir_ao_concluir)
        self.chk_abrir.pack(anchor=tk.W, pady=(8, 0))

        self.btn_avancar.configure(text="Concluir", command=self.concluir, state=tk.DISABLED)
        self.btn_cancelar.configure(state=tk.DISABLED)
        self.instalando = True
        threading.Thread(target=self._instalar_thread, daemon=True).start()

    # ---------------- utilidades de UI (thread-safe) ----------------
    def log(self, msg: str):
        logging.info(msg)

        def _ui():
            self.log_box.configure(state=tk.NORMAL)
            self.log_box.insert(tk.END, msg + "\n")
            self.log_box.see(tk.END)
            self.log_box.configure(state=tk.DISABLED)
            self.status.set(msg)
        self.root.after(0, _ui)

    def set_progresso(self, valor: float):
        self.root.after(0, lambda: self.progresso.set(valor))

    # ---------------- instalação ----------------
    def _instalar_thread(self):
        try:
            self._instalar()
            self.concluido = True
            self.log(f"{APP_NAME} v{VERSION} instalado com sucesso em {self.destino}")
            self.set_progresso(100)
            self.root.after(0, lambda: self.btn_avancar.configure(state=tk.NORMAL))
        except AppAbertoError as e:
            logging.warning(str(e))
            self.root.after(0, lambda: self._falha(str(e), fechar=True))
        except Exception as e:
            logging.error(traceback.format_exc())
            self.root.after(0, lambda: self._falha(f"{e}\n\nDetalhes em:\n{LOG_PATH}", fechar=True))
        finally:
            self.instalando = False

    def _falha(self, msg: str, fechar: bool):
        messagebox.showerror("Instalação não concluída", msg)
        self.btn_cancelar.configure(state=tk.NORMAL)
        if fechar:
            self.root.destroy()

    def _instalar(self):
        exe_destino = os.path.join(self.destino, EXE_NAME)

        # 1. App aberto? (exe em uso não pode ser aberto para escrita)
        self.log("Verificando se o aplicativo está fechado...")
        if os.path.exists(exe_destino):
            try:
                with open(exe_destino, "ab"):
                    pass
            except PermissionError:
                raise AppAbertoError(f"O {APP_NAME} está aberto.\n\nFeche o aplicativo e execute o instalador novamente.")

        # 2. Limpa a versão anterior (inclui a pasta aninhada deixada pelo SFX antigo)
        if os.path.isdir(self.destino):
            self.log("Removendo versão anterior...")
            self._rmtree_com_retry(self.destino)
        os.makedirs(self.destino, exist_ok=True)
        self.set_progresso(5)

        # 3. Extrai o app
        zip_path = resource_path("app.zip")
        self.log("Extraindo arquivos...")
        with zipfile.ZipFile(zip_path) as zf:
            membros = zf.infolist()
            total = max(len(membros), 1)
            for i, m in enumerate(membros, 1):
                zf.extract(m, self.destino)
                if i % 50 == 0 or i == total:
                    self.set_progresso(5 + 75 * i / total)
        self.log(f"{total} arquivos extraídos")

        # 4. readme / licença junto com o app
        for nome in ("readme.txt", "LICENSE.txt"):
            origem = resource_path(nome)
            if os.path.exists(origem):
                shutil.copy2(origem, os.path.join(self.destino, nome))

        # 5. install.bat (mesmo papel do "Setup=" do SFX antigo)
        bat = os.path.join(self.destino, "install.bat")
        if os.path.exists(bat):
            self.log("Executando install.bat...")
            env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
            try:
                r = subprocess.run(["cmd.exe", "/c", bat], cwd=self.destino, env=env,
                                   creationflags=CREATE_NO_WINDOW, timeout=60,
                                   capture_output=True, text=True)
                if r.returncode != 0:
                    self.log(f"Aviso: install.bat retornou {r.returncode}: {r.stderr.strip()}")
            except Exception as e:
                self.log(f"Aviso: falha ao executar install.bat: {e}")
        else:
            self.log("Aviso: install.bat não encontrado no pacote")
        self.set_progresso(85)

        # 6. Atalhos
        self.log("Criando atalhos...")
        self._criar_atalhos(exe_destino)
        self.set_progresso(95)

        # 7. Entrada de desinstalação (HKCU)
        self.log("Registrando instalação...")
        try:
            self._registrar_desinstalacao(exe_destino)
        except Exception as e:
            self.log(f"Aviso: não foi possível registrar a desinstalação: {e}")

    @staticmethod
    def _rmtree_com_retry(caminho: str, tentativas: int = 3):
        import time

        def _onerror(func, path, exc_info):
            try:
                os.chmod(path, 0o777)
                func(path)
            except Exception:
                raise

        for i in range(tentativas):
            try:
                shutil.rmtree(caminho, onerror=_onerror)
                return
            except Exception:
                if i == tentativas - 1:
                    raise
                time.sleep(1)

    def _criar_atalhos(self, exe_destino: str):
        import win32com.client  # pywin32

        shell = win32com.client.Dispatch("WScript.Shell")
        desktop = shell.SpecialFolders("Desktop")
        programas = shell.SpecialFolders("Programs")
        icone = os.path.join(self.destino, "_internal", "mini_icon.ico")
        if not os.path.exists(icone):
            icone = exe_destino

        # remove atalhos das versões antigas (Manhattan_Robo_1.6.x)
        for antigo in glob.glob(os.path.join(desktop, "Manhattan_Robo_*.lnk")):
            try:
                os.remove(antigo)
                self.log(f"Atalho antigo removido: {os.path.basename(antigo)}")
            except OSError as e:
                self.log(f"Aviso: não removeu {antigo}: {e}")

        for pasta in (desktop, programas):
            if not pasta:
                continue
            os.makedirs(pasta, exist_ok=True)
            atalho = shell.CreateShortCut(os.path.join(pasta, f"{APP_NAME}.lnk"))
            atalho.TargetPath = exe_destino
            atalho.WorkingDirectory = self.destino
            atalho.IconLocation = f"{icone},0"
            atalho.Description = f"{APP_NAME} v{VERSION}"
            atalho.Save()

    def _registrar_desinstalacao(self, exe_destino: str):
        import winreg

        desinstalar = os.path.join(self.destino, "desinstalar.bat")
        with open(desinstalar, "w", encoding="cp1252", errors="replace") as f:
            f.write(
                "@echo off\r\n"
                f"echo Removendo {APP_NAME}...\r\n"
                f'del /q "%USERPROFILE%\\Desktop\\{APP_NAME}.lnk" 2>nul\r\n'
                f'del /q "%USERPROFILE%\\OneDrive\\Desktop\\{APP_NAME}.lnk" 2>nul\r\n'
                f'del /q "%USERPROFILE%\\OneDrive\\Área de Trabalho\\{APP_NAME}.lnk" 2>nul\r\n'
                f'del /q "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{APP_NAME}.lnk" 2>nul\r\n'
                f'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{UNINSTALL_KEY}" /f >nul 2>&1\r\n'
                # o .bat não consegue apagar a própria pasta enquanto roda: delega para um cmd separado
                f'start "" /min cmd /c "timeout /t 2 >nul & rmdir /s /q "{self.destino}""\r\n'
            )

        chave = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                 rf"Software\Microsoft\Windows\CurrentVersion\Uninstall\{UNINSTALL_KEY}")
        valores = {
            "DisplayName": APP_NAME,
            "DisplayVersion": VERSION,
            "Publisher": "Luiz Guilherme",
            "InstallLocation": self.destino,
            "DisplayIcon": exe_destino,
            "UninstallString": f'cmd.exe /c ""{desinstalar}""',
        }
        for nome, valor in valores.items():
            winreg.SetValueEx(chave, nome, 0, winreg.REG_SZ, valor)
        winreg.SetValueEx(chave, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(chave, "NoRepair", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(chave)

    # ---------------- botões ----------------
    def concluir(self):
        if self.abrir_ao_concluir.get():
            exe = os.path.join(self.destino, EXE_NAME)
            try:
                env = dict(os.environ, __COMPAT_LAYER="RunAsInvoker")
                subprocess.Popen([exe], cwd=self.destino, env=env, close_fds=True)
            except Exception as e:
                messagebox.showwarning("Aviso", f"Instalado, mas não foi possível abrir o aplicativo:\n{e}")
        self.root.destroy()

    def cancelar(self):
        if self.instalando:
            return
        if self.concluido:
            self.root.destroy()
            return
        if messagebox.askyesno("Cancelar", "Deseja cancelar a instalação?"):
            self.root.destroy()


class AppAbertoError(Exception):
    pass


def main():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = tk.Tk()
    Instalador(root)
    root.mainloop()


if __name__ == "__main__":
    main()
