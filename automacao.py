from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from tkinter import filedialog, messagebox

from time import sleep

class AutoClick:
    def __init__(self, driver):
        self.driver = driver

    def _encontrar_elemento(self, xpath: str, timeout: int, condition):
        locator = (By.XPATH,xpath)
        return WebDriverWait(self.driver, timeout).until(condition(locator))

    def click_elemento(self, xpath: str, timeout: int = 30):
        elemento = self._encontrar_elemento(xpath, timeout, EC.element_to_be_clickable)
        elemento.click()

    def enviar_keys(self, xpath: str, texto: str, timeout: int = 30):
        elemento = self._encontrar_elemento(xpath, timeout, EC.element_to_be_clickable)
        elemento.send_keys(texto)
    
    def pressionar_enter(self, xpath: str, timeout: int = 30):
        elemento = self._encontrar_elemento(xpath, timeout, EC.element_to_be_clickable)
        elemento.send_keys(Keys.RETURN)

    def clear_field(self, xpath: str, timeout: int = 30):
        elemento = self._encontrar_elemento(xpath, timeout, EC.element_to_be_clickable)
        elemento.clear()
    
    def selecionar(self, xpath: str, timeout: int = 30):
        elemento = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        print("Elemento encontrado:", elemento.text)
        return elemento.text
    def elemento_existe(self, xpath, timeout=5):
        """
        Verifica se um elemento existe na página dentro do tempo limite definido.

        :param xpath: O XPath do elemento a ser verificado.
        :param timeout: Tempo máximo (segundos) para aguardar o elemento aparecer.
        :return: True se o elemento existir, False caso contrário.
        """
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except:
            return False

    def encontrar_elemento_por_texto(self, seletor: str, texto: str, timeout: int = 30):
        elementos = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, seletor))
        )
        for elemento in elementos:
            if texto in elemento.text:
                return elemento
        return None
    
    def scroll_to_element(self, xpath):
        elemento = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Executa scroll até o elemento usando JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elemento)
        # sleep(1)

        return elemento
    
    def click_js(self, css_selector: str, timeout: int = 30):
        """
        Clica em um elemento usando JavaScript, dado um seletor CSS.
        :param css_selector: seletor CSS do elemento.
        :param timeout: tempo máximo de espera.
        """
        try:
            # Espera o elemento existir no DOM
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            
            # Executa o clique via JS
            self.driver.execute_script("arguments[0].click();", elemento)
            print(f"Clique realizado com sucesso em: {css_selector}")
            return True

        except Exception as e:
            print(f"Erro ao clicar via JS em {css_selector}: {e}")
            return False

class Automation():
    def __init__(self, wait: int = 30):
        self.wait = wait
        self.driver = None
        
    def setup_driver(self, link: str = "https://viavp-auth.sce.manh.com/auth/realms/maactive/protocol/openid-connect/auth?scope=openid&client_id=zuulserver.1.0.0&redirect_uri=https://viavp.sce.manh.com/login&response_type=code&state=SB6a0O"):
        options = webdriver.ChromeOptions()
        options.add_argument("--force-device-scale-factor=0.8")  # 80% de zoom
        
        # cria o driver já com as opções
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(link)

        vav_user = "/html/body/div[1]/div[2]/div/div/div/div[2]/ul/li[2]/a/span"
        AutoClick(self.driver).click_elemento(vav_user, timeout=self.wait)


    def menu(self, texto: str):
        try:
            auto_click = AutoClick(self.driver)
            aguardando = Automation(self.driver)
            menu = "//ion-menu-toggle"
            barra = "//*[@id='ion-input-0']"
            aguardando.popup_please_wait()
            auto_click.click_elemento(menu, self.wait)
            auto_click.click_elemento(barra, self.wait)
            auto_click.enviar_keys(barra,texto, self.wait)
            sleep(1)
        except Exception as e:
            messagebox.showerror("ERRO", f"Erro ao acessar o Menu {e}")

    def selecionar_tela_inventory_details(self):
        try:
            auto_click = AutoClick(self.driver)
            inventory_details_menu = "//button[@id='inventoryDetails']"
            self.menu("Inventory Details")
            auto_click.click_elemento(inventory_details_menu, self.wait)
            self.popup_please_wait()
        except Exception as e:
            print(f"Verificar o erro {e}")

    def selecionar_asn(self):
        try:
            auto = AutoClick(self.driver)
            selecao_asn = "//*[@id='ASN']"
            self.menu("ASN")
            auto.click_elemento(selecao_asn, self.wait)
            self.popup_please_wait()
        except Exception as e:
            print(f"[ERRO] verificar {e}")

    def selecionar_wm_mobile(self):
        try:
            auto = AutoClick(self.driver)
            select_wm_mobile = "//button[@id='wmMobile']"
            tela_ead_cross = "/html/body/app-root/ion-app/ion-router-outlet/app-menu/ion-content/div/ion-list/app-menu-node[5]/ion-item/ion-label"
            receb_asn = "/html/body/app-root/ion-app/ion-router-outlet/app-menu-details/ion-content/ion-list/ion-item[2]/ion-label"
            dock_door = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[1]/input"
            stg_1302 = "1302"
            got_to_asn  ="/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[2]/ion-button"
            self.menu("WM Mobile")
            auto.click_elemento(select_wm_mobile, self.wait)
            self.popup_please_wait()
            self.driver.switch_to.window(self.driver.window_handles[1])
            # self.popup_please_wait()
            auto.click_elemento(tela_ead_cross, 30)
            auto.click_elemento(receb_asn, 30)
            auto.enviar_keys(dock_door,stg_1302, 30)
            auto.click_elemento(got_to_asn, 30)
            try:
                validar_asn_field = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'button-label') and text()='Associate Additional Asn']")))
                auto.click_elemento(validar_asn_field, 30)
            except:
                print("Button Associate Additional ASN n not find")
                pass
        except Exception as e:
            print(f"[ERRO] verificar {e}")

    def popup_please_wait(self):
        if self.driver:
            try:
                please_wait = "//*[@id='loading-2-msg']"
                WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH,please_wait)))
                print("Elemento foi encontrado, passou pelo código e esperou até ficar invisivel")
            except Exception as e:
                print(f"Elemento não foi encontrado ou não ficou visivel{e}")    

    def executar_script(self, script: str, texto: str, timeout=30):
        """
        Executa um script JavaScript no browser para preencher campos Angular/Ionic.
        :param script: Código JavaScript que deve retornar o input nativo.
        :param texto: Texto a ser enviado para o campo.
        :param timeout: Tempo máximo de espera.
        """
        try:
            # Aguarda até que o transfer-popup esteja no DOM
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    'return document.querySelector("transfer-popup")') is not None
            )

            # Busca o input pelo script informado
            input_element = self.driver.execute_script(script)

            if input_element:
                print("Campo encontrado! Enviando texto...")
                # Define o valor e dispara o evento input para Angular/Ionic reconhecer
                self.driver.execute_script(
                    """
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    """,
                    input_element, texto
                )
                return True
            else:
                print("Erro: Input não encontrado!")
                return False

        except TimeoutException:
            print("Erro, elemento não apareceu dentro do tempo limite")
            return False
        except Exception as e:
            print(f"Erro ao executar o script: {e}")
            return False


    def auto_wm_mobile(self, df):
        auto_click = AutoClick(self.driver)
        feedback = []

        loading_popup_full_path = '/html/body/app-root/ion-app/ion-loading/div[2]/div[2]'
        loading_popup_partial = "//*[@id='loading-3-msg']"
        loading_element = '<div class="loading-content sc-ion-loading-md" id="loading-3-msg">Loading....</div>'
        # XPaths dos elementos
        asn_campo_1 = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div[2]/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[1]/input"
        go_receiving_1 = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div[2]/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[2]/ion-button"
        associate_button = "//span[contains(@class, 'button-label') and text()='Associate Additional Asn']"
        # ion_backdrop = "/html/body[@class='backdrop-no-scroll']"  # Corrigido para XPath correto
        # seta_voltar = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/wm-action/ion-footer/wm-action-bar/ion-footer/ion-toolbar/ion-buttons/ion-button"
        stg_1302 = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[1]/input"
        go_stg = "/html/body/app-root/ion-app/ion-router-outlet/app-workflow/ion-content/div/wm-workflow-list/ion-list/div/div/div/div/text-input/ion-item/ion-grid/ion-row[2]/ion-col[2]/ion-button"
        recebimento_tela = "/html/body/app-root/ion-app/ion-router-outlet/app-menu-details/ion-content/ion-list/ion-item[2]/ion-label"
        pop = "/html/body/app-root/ion-app/ion-popover/error-popover/ion-content/div"
        if auto_click.elemento_existe(associate_button, 2):
            auto_click.click_elemento(associate_button, 2)
            # sleep(1)
            # self.popup_please_wait()
        else:
            print("Botão 'Associate Additional ASN' não encontrado. Continuando...")  # Se der erro aqui, seguimos adiante

        lista_de_dados = self.loop_lendo_planilha(df)
        if not lista_de_dados or all(x[0] is None and x[1] is None and x[2] is None for x in lista_de_dados):
            print("Erro: Nenhum dado válido encontrado na planilha. Verifique o arquivo!")
            return df

        for ilpn, item, asn in lista_de_dados:
            print(f"Processando ASN: {asn}, {item}, {ilpn}")
            sucesso = False  

            try:
                # Clica no campo, limpa e insere o ASN
                if auto_click.elemento_existe(asn_campo_1, 1):
                    print("Campo ASN encontrado, clicando...")
                    auto_click.click_elemento(asn_campo_1, 1)
                    auto_click.clear_field(asn_campo_1, 1)
                    auto_click.enviar_keys(asn_campo_1, asn, 1)
                else:
                    print(f"Campo ASN não encontrado para {asn}, pulando...")
                    feedback.append(f"Erro: Campo ASN não encontrado para {asn}")
                    continue

                # Clica no botão "Go Receiving"
                auto_click.click_elemento(go_receiving_1, 1)
                try:
                    WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, asn_campo_1))
                    )
                except:
                    pass

                # **Se o pop-up de erro aparecer, pressionar ESC e continuar**
                if auto_click.elemento_existe(pop, 1):
                    print(f"Pop-up de erro detectado ao processar ASN {asn}. Fechando...")
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    feedback.append(f"Erro: ASN {asn} já recebida")
                    continue

                print(f"ASN {asn} processado e verificado com sucesso!")
                feedback.append(f"ASN {asn} recebido com sucesso")
                sucesso = True

            except Exception as e:
                print(f"Erro ao processar ASN {asn}: {e}")

                # **Se o pop-up ainda existir, tentar fechar com ESC novamente**
                if auto_click.elemento_existe(pop, 2):
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

                feedback.append(f"Erro ao processar ASN {asn}, verificar.")

                # **Voltar ao menu principal apenas se der erro**
                self.driver.back()
                auto_click.click_elemento(recebimento_tela, 2)
                auto_click.click_elemento(stg_1302, 2)
                auto_click.enviar_keys(stg_1302, "1302", 2)
                auto_click.click_elemento(go_stg, 2)

                try:
                    if auto_click.elemento_existe(associate_button, 2):
                        auto_click.click_elemento(associate_button, 2)
                        # sleep(1)
                        # self.popup_please_wait()
                    else:
                        print("Botão 'Associate Additional ASN' não encontrado. Continuando...")  # Se der erro aqui, seguimos adiante
                        # sleep(2)
                except:
                    pass 


            finally:
                # **Garante que o campo seja limpo antes do próximo loop**
                auto_click.clear_field(asn_campo_1, 2)

        df['Feedback'] = feedback
        return df

    def auto_verify(self, df):
        auto_click = AutoClick(self.driver)
        feedback = []
        menu = 'button > span'
        asn_field = "//*[@id='ion-input-2']"
        selecionar_asn = "/html/body/app-root/ion-app/div/ion-split-pane/ion-router-outlet/screen-page/div/div/div[2]/div/ion-content/card-panel/div[1]/div/card-view/div"
        botao_verify = "/html/body/app-root/ion-app/div/ion-split-pane/ion-router-outlet/screen-page/div/div/div[2]/div/footer-actions/ion-grid/ion-row/ion-col[3]/div/div/dm-action[8]/ion-button"
        confirma_verify = "/html/body/app-root/ion-app/ion-modal/verify-popup/ion-footer/ion-toolbar/ion-row/ion-col[2]/ion-button[2]"
        lista_de_dados = self.loop_lendo_planilha(df)
        self.popup_please_wait()
        
        # try:
        #     """Apenas em telas pequenas, ou se for executar sem diminuir o zoom"""
        #     sleep(5)
        #     auto_click.click_js("ion-button.toggle-button")
        #     auto_click.click_js('ion-button[data-component-id="ASN-ASN-chevron-down"]')
        #     # input("Elemento do Menu foi encontrado")
        # except:
        #     # input("Não foi encontrado o elemento do Menu")
        #     print("Não foi encontrado o elemento do Menu")
        
        auto_click.click_elemento(asn_field, 30)        

        for ilpn, item, asn in lista_de_dados:
            feedback_msg = "Erro na automação"  # Valor padrão

            try:
                self.processar_asn(auto_click, asn_field, selecionar_asn, botao_verify, confirma_verify, asn, item, ilpn)
                feedback_msg = "ASN verificado com sucesso"
            except Exception as e:
                print(f"Erro inesperado na automação: {e}")

                # Se a exceção já contém o status, usa ela
                if "não está em In Receiving" in str(e):
                    feedback_msg = str(e)  # aqui já vai vir com "ASN XXXX não está In Receiving - Status: YYY"
                else:
                    # fallback: tenta pegar o status na tela
                    status = "//*[@id='main']/screen-page/div/div/div[2]/div/ion-content/card-panel/div/div/card-view/div/div[1]/div[1]"
                    try:
                        desc = auto_click.selecionar(status, 30).strip()
                        feedback_msg = f"Analisar ASN manualmente status: {desc}"
                    except:
                        feedback_msg = "Erro inesperado sem status visível"

                # Tenta fechar popup se existir
                try:
                    cancel = "/html/body/app-root/ion-app/ion-modal/verify-popup/ion-footer/ion-toolbar/ion-row/ion-col[1]/ion-button"
                    auto_click.click_elemento(cancel, 30)
                except:
                    pass

                # feedback_msg = f"Analisar ASN manualmente status: {desc}"

            feedback.append(feedback_msg)

        # Ajustando a lista de feedback
        while len(feedback) < len(df):
            feedback.append("Erro: ASN não processado")

        print(f"Tamanho do DataFrame: {len(df)}, Tamanho da lista feedback: {len(feedback)}")

        df['Feedback'] = feedback
        return df

    def processar_asn(self, auto_click, asn_field, selecionar_asn, botao_verify, confirma_verify, asn, item, ilpn):
        print(f"Processando ASN: {asn}, {item}, {ilpn}")
        auto_click.clear_field(asn_field,10)
        auto_click.click_elemento(asn_field, 10)
        auto_click.enviar_keys(asn_field, asn, 10)
        auto_click.pressionar_enter(asn_field, 10)
        # self.popup_please_wait()

        # Capturar o elemento novamente para evitar stale element reference
        for tentativa in range(3):
            try:
                selecionar_asn_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selecionar_asn))
                )
                selecionar_asn_element.click()
                break
            except StaleElementReferenceException:
                print(f"Tentativa {tentativa+1}: Stale Element Reference, tentando novamente...")
                # sleep(1)
            except Exception as e:
                print(f"[ERRO] Não consegui selecionar ASN: {e}")
                raise RuntimeError("Erro ao selecionar ASN")

        # Verificar status da ASN
        try:
            selecao_status_asn = "//*[@id='main']/screen-page/div/div/div[2]/div/ion-content/card-panel/div/div/card-view/div/div[1]/div[1]"
            status_asn_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, selecao_status_asn))
            )
            status = status_asn_element.text.strip()
            print(f"Status da ASN {asn}: {status}")

            if status.lower() != "in receiving":
                print(f"[AVISO] ASN {asn} não está em In Receiving. Status: {status}. Status: {status}\n\n Fechando Execução do Verify atualizar planilha por segurança")
                raise RuntimeError(f"ASN {asn} não está In Receiving - Status: {status}")

            # Se chegou aqui, o status era "In Receiving", então continua com a verificação
            auto_click.scroll_to_element(botao_verify)
            auto_click.click_elemento(botao_verify, 10)
            auto_click.click_elemento(confirma_verify, 10)
            # self.popup_please_wait()
            auto_click.clear_field(asn_field, 10)

        except Exception as e:
            print(f"Erro ao verificar status do ASN: {e}")
            self.close_driver()
            return

    def reason_code_auto(self, df, reason_code, status, filial, comentario1, comentario2):
        auto_click = AutoClick(self.driver)
        feedback = []
        # Definição dos XPaths
        inventory_container_path = '//*[@id="ion-input-1"]'
        checkbox = "//*[@id='main']/inventory-grid/dm-list-layout/div/div/div[3]/div[2]/div[1]/ion-content/grid-view/div/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/datatable-row-wrapper[1]/datatable-body-row/div[1]/datatable-body-cell/div/label/input"
        more_options = "//*[@id='main']/inventory-grid/dm-list-layout/div/div/div[3]/div[2]/footer-actions/ion-grid/ion-row/ion-col[3]/div/div/more-actions/ion-button"
        reidentify_item = "//*[@id='mat-menu-panel-2']/div/div[2]/button"
        reidentify_item_2 = "/html/body/div/div[2]/div/div/div/div[2]/button"
        elementos = "driver.find_elements_by_css_selector('span.row-action-label')"
        lupa = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[1]/div/button"
        checkbox_sku = "/html/body/app-root/ion-app/ion-modal[2]/lookup-dialogue/modal-container/div/div/modal-content/ion-row[3]/grid-view/div/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/datatable-row-wrapper/datatable-body-row/div[1]/datatable-body-cell/div/input"
        submit_sku = "/html/body/app-root/ion-app/ion-modal[2]/lookup-dialogue/modal-container/div/modal-footer/div/div[2]/ion-button"
        script_input_item_Name = '''return document.querySelector("transfer-popup").querySelectorAll("input")[0];'''
        reasoncode_field = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[1]/autocomplete/div/ion-input/input"
        ref1 = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[2]/input"
        ref2 = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[3]/input"
        attribute1 = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[3]/ion-item[1]/input"
        inventory_type = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[2]/popup-dropdown[1]/ion-label/div"
        product_status = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[2]/ion-col[2]/popup-dropdown[2]/ion-label/div"
        product_status_021 = "/html/body/app-root/ion-app/ion-popover/generic-dropdown/ion-list/ion-item[8]/ion-label/div"
        confir_reidentify_item = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-footer/button[1]"
        inv_0014 = "/html/body/app-root/ion-app/ion-popover/generic-dropdown/ion-list/ion-item[1]/ion-label/div"
        inv_1401 = "/html/body/app-root/ion-app/ion-popover/generic-dropdown/ion-list/ion-item[2]/ion-label/div"
        cancel = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-footer/button[2]"
        inv_type = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[1]/div/ion-row/ion-col/div/ion-row/ion-col/div[4]/ion-row[2]/span"
        dismiss = "/html/body/app-root/manh-overlay-container/toast/div/ion-grid/ion-row/ion-col[3]/ion-button"
        att1_source = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[1]/div/ion-row/ion-col/div/ion-row/ion-col/div[12]/ion-row[2]/span"

        lista_dados = self.loop_lendo_planilha(df)

        # try:
        #     sleep(5)
        #     auto_click.click_js('ion-button[data-component-id="filter-count-btn"]')
        #     auto_click.click_js('ion-button[data-component-id="InventoryGrid-Inventorycontainer-chevron-down"]')
        #     # auto_click.click_js('ion-button[data-component-id="InventoryGrid-Inventoryattribute1-chevron-down"]')
        #     # input("Elemento do Menu foi encontrado")
        # except:
        #     # input("Não foi encontrado o elemento do Menu")
        #     print("Não foi encontrado o elemento do Menu")

        for ilpn, item, asn in lista_dados:
            feedback_msg = "Erro: Não processado"  # Inicializa com um valor padrão
            
            try:
                print(f"Processando ILPN: {ilpn}, Item: {item}, ASN: {asn}")
                auto_click.click_elemento(inventory_container_path, 30)
                auto_click.clear_field(inventory_container_path, 30)
                sleep(2)
                auto_click.enviar_keys(inventory_container_path, ilpn, 30)
                auto_click.pressionar_enter(inventory_container_path, 10)
                auto_click.click_elemento(checkbox, 10)

                try:
                    auto_click.click_elemento(more_options, 30)
                    sleep(1)
                    elemento_desejado = auto_click.encontrar_elemento_por_texto('span.row-action-label', 'ReIdentify Item', 30)

                    if elemento_desejado:
                        sleep(1)
                        elemento_desejado.click()
                        print("ReIdentify Item encontrado")
                    else:
                        print("Elemento não encontrado")
                        feedback_msg = "[ERRO] Elemento não encontrado"
                        feedback.append(feedback_msg)
                        continue
                except Exception as e:
                    print(f"Erro ao identificar elemento: {e}")
                    feedback_msg = f"[ERRO] {e}"
                    feedback.append(feedback_msg)
                    continue

                # self.popup_please_wait()
                sleep(3)

                # --- Validação de segurança do item exibido na tela ---
                try:
                    # XPATH preciso com base na estrutura real do HTML
                    xpath_item = (
                        "//transfer-popup//ion-row[@data-component-id='itemName']"
                        "/following-sibling::ion-row//span[@appuniqueiddirective and normalize-space(text())!='']"
                    )

                    # Espera o item aparecer dentro do modal
                    elemento_item_tela = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, xpath_item))
                    )

                    # Captura e normaliza o texto exibido
                    item_tela = elemento_item_tela.text.strip()
                    print(f"[DEBUG] Texto capturado do item: '{item_tela}'")

                    # Garante que só números sejam considerados e preenche zeros à esquerda
                    item_tela = ''.join(filter(str.isdigit, item_tela)).zfill(9)
                    item = str(item).zfill(9)

                    print(f"[CHECK] Item exibido na tela: {item_tela} | Item esperado: {item}")

                    # Validação de consistência
                    if not item_tela.isdigit() or item_tela == "":
                        print("[ERRO] Item capturado inválido (vazio ou não numérico). Abortando execução por segurança.")
                        auto_click.click_elemento(cancel, 10)
                        feedback_msg = "[ABORTADO] Item capturado inválido ou vazio"
                        feedback.append(feedback_msg)
                        continue

                    # Se o item da tela for diferente do importado → aborta
                    if item_tela != item:
                        print(f"[ABORTADO] Divergência detectada! Esperado: {item}, Encontrado: {item_tela}")
                        auto_click.click_elemento(cancel, 10)
                        feedback_msg = f"[ABORTADO] Item divergente (esperado {item}, encontrado {item_tela})"
                        feedback.append(feedback_msg)
                        continue

                    print("[OK] Item validado com sucesso — prosseguindo com reason code.")

                except TimeoutException:
                    print("[ERRO] Não foi possível localizar o item dentro do modal.")
                    auto_click.click_elemento(cancel, 10)
                    feedback_msg = "[ERRO] Item não visível — execução abortada"
                    feedback.append(feedback_msg)
                    continue

                except Exception as e:
                    print(f"[ERRO] Falha ao validar item: {e}")
                    auto_click.click_elemento(cancel, 10)
                    feedback_msg = f"[ERRO] Validação do item falhou: {e}"
                    feedback.append(feedback_msg)
                    continue
                # --------------------------------------------------------


                # Verificar condição de filial e status
                for tentativas in range(3):
                    try:
                        inv_type_value = auto_click.selecionar(inv_type, 30)
                        # auto_click.scroll_to_element(att1_source)
                        att1_source_value = auto_click.selecionar(att1_source)
                        print(f"Passou de primeira ILPN:{ilpn}")
                        break
                    except:
                        print(f"Erro ao selecionar inv_type_value ILPN{ilpn}, Tentando novamente... Tentativa {tentativas + 1}")
                        feedback_msg = "[ERRO] Erro ao selecionar inv_type_value"
                        feedback.append(feedback_msg)
                        if tentativas == 2:
                            break

                if filial == inv_type_value and status == att1_source_value:
                    feedback_msg = "ILPN com filial e status igual"
                    print("ILPN com filial e status igual")
                    auto_click.click_elemento(cancel, 30)
                    sleep(1)
                    feedback.append(feedback_msg)  # Adiciona antes do continue
                    continue

                elif filial != inv_type_value and reason_code == "M1" and filial == "1401":
                    if len(item) < 9:
                        item = item.zfill(9)
                    # self.executar_script(script_input_item_Name, item, 30)
                    self.executar_script('return document.querySelector("transfer-popup").querySelectorAll("input")[0];',item)   # aqui o valor vem da sua planilha/loop

                    auto_click.click_elemento(lupa, 30)
                    auto_click.click_elemento(checkbox_sku, 30)
                    auto_click.click_elemento(submit_sku, 30)
                    
                    self.executar_script('return document.querySelector("transfer-popup").querySelectorAll("input")[1];',reason_code,30)
                    sleep(1)
                    ActionChains(self.driver).send_keys(Keys.RETURN).perform()

                    # Preenchendo os campos adicionais
                    # auto_click.scroll_to_element(ref1)
                    auto_click.click_elemento(ref1, 30)
                    auto_click.enviar_keys(ref1, comentario1, 30)
                    auto_click.enviar_keys(ref2, comentario2, 30)
                    auto_click.enviar_keys(attribute1, status, 30)
                    auto_click.click_elemento(inventory_type, 30)
                    auto_click.click_elemento(inv_1401, 30)
                    auto_click.scroll_to_element(product_status)
                    auto_click.click_elemento(product_status)
                    auto_click.scroll_to_element(product_status_021)
                    auto_click.click_elemento(product_status_021)
                    auto_click.click_elemento(confir_reidentify_item)

                    feedback_msg = f"Reason Code {reason_code} Feito"
                    print(feedback_msg, "M1")
                    self.popup_please_wait()

                elif filial == inv_type_value and status != att1_source_value:
                    if len(item) < 9:
                        item = item.zfill(9)
                    # self.executar_script(script_input_item_Name, item, 30)
                    self.executar_script('return document.querySelector("transfer-popup").querySelectorAll("input")[0];', item)# aqui o valor vem da sua planilha/loop
                    auto_click.click_elemento(lupa, 30)
                    auto_click.click_elemento(checkbox_sku, 30)
                    auto_click.click_elemento(submit_sku, 30)
                    # auto_click.click_elemento(reasoncode_field, 30)
                    # auto_click.enviar_keys(reasoncode_field, reason_code, 30)
                    # auto_click.pressionar_enter(reasoncode_field, 30)
                    self.executar_script('return document.querySelector("transfer-popup").querySelectorAll("input")[1];',reason_code,30)
                    sleep(1)
                    # Se precisar Enter, pode simular:
                    
                    ActionChains(self.driver).send_keys(Keys.RETURN).perform()

                    # Preenchendo os campos adicionais
                    # auto_click.scroll_to_element(ref1)
                    auto_click.click_elemento(ref1, 30)
                    auto_click.enviar_keys(ref1, comentario1, 30)
                    auto_click.enviar_keys(ref2, comentario2, 30)
                    auto_click.enviar_keys(attribute1, status, 30)
                    auto_click.click_elemento(inventory_type, 30)

                    if inv_type_value == "1401":
                        auto_click.click_elemento(inv_1401, 30)
                    else:
                        auto_click.click_elemento(inv_0014, 30)

                    auto_click.scroll_to_element(product_status)
                    auto_click.click_elemento(product_status)
                    auto_click.scroll_to_element(product_status_021)
                    auto_click.click_elemento(product_status_021)
                    auto_click.click_elemento(confir_reidentify_item)
                    feedback.append(f"Reason Code {reason_code} Feito")

                    feedback_msg = f"Reason Code {reason_code} Feito"
                    print(feedback_msg)
                    self.popup_please_wait()

                else:
                    auto_click.click_elemento(cancel, 30)
                    feedback_msg = "Verificar"
                    feedback.append(feedback_msg)
                    continue

                print(f"ILPN {ilpn} processado com sucesso")

            except Exception as e:
                print(f"Erro ao processar ILPN {ilpn}: {e}")
                feedback_msg = f"[ERRO] Verificar"

            feedback.append(feedback_msg)  # Adiciona o feedback ao final da iteração

        # Garantir que `feedback` tenha o mesmo tamanho do `df`
        while len(feedback) < len(df):
            feedback.append("Erro: Não processado")  
            print(f"Tamanho do DataFrame: {len(df)}, Tamanho da lista feedback: {len(feedback)}")

        df['Feedback'] = feedback[:len(df)]
        return df

    def importar_planilha(self):
        try:
            file = filedialog.askopenfilename(title="Selecione o Arquivo", filetypes=[("Excel Files", "*.csv;*.xlsm")])
            if file:
                if file.endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                messagebox.showinfo("Arquivo Selecionado", f"Arquivo selecionado: {file}")
                self.loop_lendo_planilha(df)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar planilha: {e}")
            
    def loop_lendo_planilha(self, df):
        dados = []
        for index, row in df.iterrows():
            ilpn = str(row.get('ILPN'))
            item = str(row.get('Item'))
            asn = row.get('ASN')
            
            if isinstance (asn, float):
                asn = str(int(asn))
            else:
                asn = str(asn)

            dados.append((ilpn, item, asn))
            print(f"ILPN: {ilpn}, Item: {item}, ASN: {asn}")
        return dados

    def close_driver(self):
        if self.driver:
            self.driver.quit()

class Login():
    def __init__(self, driver, login: str, senha: str):
        self.driver = driver
        self.login = login
        self.senha = senha

    def logando(self):
        
        email= "//input[@id='i0116']"
        senha= "//input[@id='i0118']"
        avancar = "//input[@id='idSIButton9']"
        home = "//button[@value='Home']"
        auto_click = AutoClick(self.driver)

        def tentar_acao(acao,descricao,tentativas=3):
            for tentativa in range(tentativas):
                try:
                    acao()
                    return True
                except Exception as e:
                    print(f"[Erro] {descricao} na tentativa {tentativa + 1}: {e}")
            return False
        try:
            if not tentar_acao(lambda: auto_click.click_elemento(email, 10), "Tentando clicar no Label do e-mail"):
                return
            if not tentar_acao(lambda:auto_click.enviar_keys(email, self.login, 10), "Tentando enviar o e-mail"):
                return
            if not tentar_acao(lambda: auto_click.click_elemento(avancar,10), "Tentando avançar"):
                return
        except Exception as e:
            print("Encerrando")
            
        
        try:
            if not tentar_acao(lambda: auto_click.click_elemento(senha, 10),"Tentando clicar no Label da senha"):
                return
            if not tentar_acao(lambda:auto_click.enviar_keys(senha, self.senha, 10),"Tentando enviar a senha"):
                return
            if not tentar_acao(lambda: auto_click.click_elemento(avancar,10), "Tentando clicar em avançar"):
                return
        except Exception as e:
            print(f"Encerrando {e}")
            
        
        
        sleep(1)
        if not tentar_acao(lambda: auto_click.click_elemento(avancar, 10), "Tentando clicar em avançar"):
            return
        if not tentar_acao(lambda: auto_click.click_elemento(home, 10), "Tentando clicar no home"):
            return

# if __name__ == "__main__":