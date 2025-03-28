from pywinauto import Application
from pywinauto.keyboard import send_keys
import time
import win32api
import win32con

# Caminho do arquivo de sessão
caminho_sessao = r"C:\ProgramData\IBM\Personal Communications\3270.ws"

# Abrir a sessão no IBM Personal Communications
win32api.ShellExecute(0, "open", caminho_sessao, "", "", win32con.SW_SHOWNORMAL)
# Definir o nome da sessão aberta no IBM PCOM
sessao_A = "Sessão A - [24 x 80]"
time.sleep(5)
app = Application(backend="win32").connect(title=sessao_A)
main_window = app.window(title=sessao_A)
main_window.type_keys("{ENTER}")
time.sleep(3)
main_window.send_keystrokes("+texto")
main_window.type_keys("{ENTER}")



