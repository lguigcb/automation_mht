# automacoes_manhattan
Software para automação de tarefas

- Atumoatização de Recebimento EAD Faturado na stage AUT-DIV (1302)
- Automatização da execução do Verify das ASN's que se encontram em Receiving
- Automatização da execução dos Reason Code's pelo Inventory Details

Para EAD Faturado, necessário ter acesso ao WM Mobile

Registro de correções de seletores (o que foi corrigido, pendências e checklist de validação): [CORRECOES_SELETORES.md](CORRECOES_SELETORES.md)

## Como gerar o instalador

1. Alterar a versão em `version.py` (aparece no título da janela, no nome do setup e em "Aplicativos instalados").
2. Rodar na raiz do projeto: `venv\Scripts\python.exe build.py`
3. Saídas em `dist\`:
   - `Automações Manhattan\` — app compilado em modo onedir (exe + `_internal`)
   - `Automações Manhattan_setup_<versão>.exe` — instalador para distribuir

O instalador (`installer\setup_app.py`) não pede administrador: mostra o `readme.txt` e a `LICENSE.txt`, instala em `%APPDATA%\Automações Manhattan` substituindo a versão anterior, executa o `installer\install.bat` após a extração e cria os atalhos "Automações Manhattan" na área de trabalho e no menu iniciar.
