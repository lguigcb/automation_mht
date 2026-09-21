# Registro de correções — seletores instáveis em `automacao.py`

Data: 21/09/2026
Versão base: 1.6.2 (commit `659a19e`)
Arquivo afetado: `automacao.py` (nenhuma alteração em `interface.py`)

Este documento registra os problemas identificados nos seletores XPath da automação, o que foi corrigido, o que ainda está pendente e como validar no futuro.

---

## 1. Causa raiz comum

O Manhattan Active usa Ionic/Angular. Dois tipos de identificador **mudam a cada sessão/execução** e não podem ser usados em XPath:

| Padrão instável | Por que muda | Exemplo real |
|---|---|---|
| `id="ion-input-N"` | O Ionic numera cada `<ion-input>` na ordem em que é criado na sessão. Qualquer tela/modal aberto antes desloca a numeração. | Inventory container era `ion-input-1`; após o modal de perfil (3 ion-inputs) virou `ion-input-4`. |
| `id="ion-overlay-N"` | Mesmo mecanismo para overlays (modal, loading, toast, popover). | Modal de perfil aparecia como `ion-overlay-4`, mas varia. |
| `autocomplete-overlay[N]` (índice posicional) | Cada dropdown cria um overlay em `manh-overlay-container`; os anteriores ficam no DOM ocultos. O índice depende da ordem de abertura. | `autocomplete-overlay[1]`, `[2]`, `[3]` para org/profile/facility. |
| Full XPath (`/html/body/app-root/...`) | Qualquer mudança de layout, zoom ou versão do app quebra. | Vários em `reason_code_auto`, `auto_verify`, `auto_wm_mobile`. |

**Regra adotada:** preferir sempre o atributo `data-component-id` (definido pela aplicação, estável entre sessões) ou `title`/texto do elemento, com XPath relativo (`//tag[@data-component-id='...']`).

---

## 2. Corrigido

### 2.1 Login — seleção de Organization / Facility / Profile (DUQUEARM)

**Onde:** `Login.selecionar_perfil_duquearm()` e final de `Login.logando()`.

**Problema original (linhas antigas 733-809):**
- XPaths com `ion-overlay-4` e `autocomplete-overlay[1|2|3]` — falhavam por id/índice dinâmico.
- Bloco só executava **se o clique no Home falhasse** (`if not tentar_acao(home)`), gastando 3×10 s antes.
- `aguardando = Automation(self.driver)` passava o driver no parâmetro `wait`; `aguardando.driver` ficava `None` e `popup_please_wait()` não fazia nada.
- `messagebox.showinfo` bloqueante no meio do login.

**Correção aplicada:**
- Novo método `Login.selecionar_perfil_duquearm()`:
  - Espera o botão de perfil da navbar: `//profile-summary//button[contains(@class,'orgfacbu-container')]`
  - Se `//profile-summary//div[@data-component-id='DUQUEARM']` já existir → pula.
  - Abre o modal e usa:
    - `//core-profile-selection-modal//button[@data-component-id='autocomplete_open_dropdown_organization']`
    - `//core-profile-selection-modal//button[@data-component-id='autocomplete_open_dropdown_facility']`
    - `//core-profile-selection-modal//button[@data-component-id='autocomplete_open_dropdown_profile']`
    - Itens: `//autocomplete-overlay//ion-label[@title='DUQUEARM']` e `//autocomplete-overlay//ion-label[@title='PROV_PROF_DUQUEARM']`
    - Submit: `//core-profile-selection-modal//ion-button[@data-component-id='submit']`
  - Espera o modal sumir e confirma que a navbar mostra DUQUEARM; senão lança `RuntimeError`.
- Novo helper `AutoClick.click_elemento_visivel(xpath, timeout)`: entre todos os matches, clica no primeiro **visível** (necessário porque os `autocomplete-overlay` antigos ficam ocultos no DOM e `element_to_be_clickable` pegaria o primeiro oculto).
- `logando()` agora chama `selecionar_perfil_duquearm()` **sempre** após o login; se falhar, a exceção sobe e o `try/except` do `interface.py` interrompe a automação (não roda com Org errado). Home só é clicado se existir (5 s de checagem).

### 2.2 Reason Code — filtro "Inventory container"

**Onde:** `Automation.reason_code_auto()`.

**Problema:** `inventory_container_path = '//*[@id="ion-input-1"]'`. Parou de funcionar após a correção 2.1, porque o modal de perfil cria 3 ion-inputs e o campo passou a ser `ion-input-4` (e volta a `-1` quando o modal não abre).

**Correção aplicada:**
- `inventory_container_path = "//ion-input[@data-component-id='InventoryContainerId']//input"`
- Antes do loop: se existir `//ion-button[@data-component-id='InventoryGrid-Inventorycontainer-chevron-down']` (filtro recolhido), clica para expandir; depois `WebDriverWait` até o input ficar clicável.
- Substituiu o bloco comentado que tentava fazer isso via `click_js`.

---

## 3. Pendente (identificado, não corrigido)

| # | Onde | Seletor atual | Risco | Correção sugerida |
|---|---|---|---|---|
| P1 | `Automation.auto_verify()` — `asn_field` | `//*[@id='ion-input-2']` | **Alto.** Mesmo problema de 2.2: vai deslocar para `ion-input-5` quando o modal de perfil abrir. Deve quebrar na próxima execução do Verify. | Capturar o `<ion-input>` do filtro ASN e usar seu `data-component-id` (`//ion-input[@data-component-id='...']//input`). Fallback: `//text-field-filter[.//span[@class='label' and @title='ASN']]//input`. |
| P2 | `Automation.menu()` — `barra` | `//*[@id='ion-input-0']` | Baixo. É o primeiro ion-input criado na sessão, então tende a ficar estável, mas segue o mesmo padrão frágil. | Trocar por `data-component-id` da barra de busca do menu quando for capturado. |
| P3 | `Automation.menu()` — `aguardando = Automation(self.driver)` | — | Médio. Mesmo bug da 2.1: o driver vai para `wait`, `aguardando.driver` fica `None` e `popup_please_wait()` é no-op. Hoje funciona "por acaso" porque o `click_elemento` seguinte tem timeout de 30 s. | Trocar por `self.popup_please_wait()` (o próprio objeto já tem o driver). Não alterado para não mudar timing dos 3 fluxos sem teste. |
| P4 | `reason_code_auto()` — `checkbox`, `more_options`, `lupa`, `checkbox_sku`, `submit_sku`, `ref1/ref2`, `attribute1`, `inventory_type`, `product_status`, `product_status_021`, `inv_0014/inv_1401`, `cancel`, `inv_type`, `att1_source`, `confir_reidentify_item` | Full XPaths | Médio. Funcionam hoje, mas dependem de posição (`ion-item[8]`, `div[12]`, `datatable-body-cell[5]`). `product_status_021` e `inv_1401` quebram se a ordem das opções do dropdown mudar. | Migrar gradualmente para `data-component-id`/texto quando cada elemento for capturado. Prioridade: os de dropdown por índice. |
| P5 | `auto_verify()` / `processar_asn()` — `selecionar_asn`, `botao_verify` (`dm-action[8]`), `confirma_verify`, `cancel`, `status` | Full XPaths | Médio. `dm-action[8]` depende da quantidade/ordem de ações no rodapé. | Idem P4. |
| P6 | `selecionar_wm_mobile()` / `auto_wm_mobile()` — `tela_ead_cross` (`app-menu-node[5]`), `receb_asn` (`ion-item[2]`), campos `dock_door`, `asn_campo_1`, `go_receiving_1` etc. | Full XPaths | Médio. `app-menu-node[5]` depende da ordem dos menus do usuário. | Usar texto do `ion-label` (ex.: `//ion-label[normalize-space()='EAD CROSS']`). |
| P7 | `popup_please_wait()` | `//*[@id='loading-2-msg']` | Baixo/Médio. `loading-N-msg` também é numerado pelo Ionic (em `auto_wm_mobile` já existe referência a `loading-3-msg`). | Usar `//ion-loading//div[contains(@class,'loading-content')]` ou `//ion-loading`. |
| P8 | `setup_driver()` — `vav_user` | `/html/body/div[1]/div[2]/.../li[2]/a/span` | Baixo. Página de login do Keycloak, muda pouco. | Usar texto do link quando capturado. |

---

## 4. Como validar no futuro

Checklist para rodar após qualquer alteração de seletor ou atualização do Manhattan:

1. **Import:** `python -c "import automacao"` sem erro.
2. **Login / perfil:**
   - Usuário em VIAV → console deve mostrar `Selecionando Organization/Facility/Profile` e `Perfil alterado para DUQUEARM com sucesso`; navbar passa a exibir `Org: DUQUEARM`.
   - Rodar de novo já em DUQUEARM → `Perfil já está em DUQUEARM, pulando seleção de facility`.
   - Teste negativo: trocar temporariamente `PROV_PROF_DUQUEARM` por valor inexistente → messagebox de erro do `interface.py` e a automação **não** prossegue. Reverter.
3. **Reason Code:** rodar com 1-2 ILPNs nos dois cenários acima (modal abre / não abre). O campo Inventory container deve receber a ILPN e filtrar com Enter em ambos. Se possível, recolher o filtro manualmente antes → `Filtro Inventory container recolhido, expandindo...`.
4. **Verify (P1):** enquanto não corrigido, esperar falha em `asn_field`. Ao corrigir, validar nos dois cenários de perfil.
5. **Receiving EAD:** sanidade — login completa e a navegação inicial acontece.
6. **Auditoria rápida de seletores frágeis:**
   ```powershell
   Select-String -Path automacao.py -Pattern "ion-input-\d|ion-overlay-\d|loading-\d-msg|autocomplete-overlay\[" 
   ```
   Qualquer match novo deve ser justificado ou trocado por `data-component-id`.
7. Só distribuir o instalador depois de validar os três fluxos. Build: `venv\Scripts\python.exe build.py` (gera `dist\Automações Manhattan\` e `dist\Automações Manhattan_setup_<versão>.exe`; versão em `version.py` — 1.7.0 é a primeira com estas correções).

---

## 5. Como capturar um seletor estável (para as pendências)

No Chrome, com a tela aberta: F12 → selecionar o elemento → copiar o `outerHTML` do `<ion-input>`, `<ion-button>` ou `<button>` mais próximo. Procurar nesta ordem:

1. `data-component-id="..."` → `//ion-input[@data-component-id='X']//input` ou `//ion-button[@data-component-id='X']`
2. `title="..."` → `//ion-label[@title='X']`
3. Texto visível → `//ion-label[normalize-space()='X']` ou `//span[contains(@class,'button-label') and text()='X']`
4. Só em último caso: XPath relativo a partir de um componente nomeado (`//core-profile-selection-modal//...`, `//transfer-popup//...`), nunca `/html/body/...`.
