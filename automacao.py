from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from tkinter import filedialog, messagebox

from time import sleep

class AutoClick:
    def __init__(self, driver):
        self.driver = driver

    def _encontrar_elemento(self, xpath: str, timeout: int, condition):
        return WebDriverWait(self.driver, timeout).until(condition((By.XPATH, xpath)))

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

    def scroll_to_element(self, xpath):
        elemento = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        # Executa scroll até o elemento usando JavaScript
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elemento)
        # sleep(1)

        return elemento
    

class Automation():
    def __init__(self, wait: int = 30):
        self.wait = wait
        self.driver = None

    def setup_driver(self, link: str = "https://viavp-auth.sce.manh.com/discover_user"):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(link)
        AutoClick(self.driver).click_elemento("//input[@id='discover-user-submit']", timeout=self.wait)

    def selecionar_tela(self):
        try:
            auto_click = AutoClick(self.driver)
            aguardando = Automation(self.driver)
            menu = "//ion-menu-toggle"
            barra = "/html/body/app-root/ion-app/div/ion-split-pane/ion-menu/ui-dm-hamburger/ion-header/ion-input/input"
            inventory_details_menu = "//button[@id='inventoryDetails']"
            aguardando.popup_please_wait()
            auto_click.click_elemento(menu, self.wait)
            auto_click.click_elemento(barra, self.wait)
            auto_click.enviar_keys(barra,"inventory details", self.wait)
            sleep(1)
            auto_click.click_elemento(inventory_details_menu, self.wait)
            aguardando.popup_please_wait()

        except Exception as e:
            print(f"Verificar o erro {e}")

    def popup_please_wait(self):
        if self.driver:
            try:
                please_wait = "//*[@id='loading-2-msg']"
                WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located((By.XPATH,please_wait)))
                print("Elemento foi encontrado, passou pelo código e esperou até ficar invisivel")
            except Exception as e:
                print(f"Elemento não foi encontrado ou não ficou visivel{e}")    

    def executar_script(self, script: str, texto: str, timeout = 30):
        """
        Executa um script JavaScript no browser e retorna o resultado.
        :param script: Código JavaScript a ser executado.
        :return: Retorno do script executado.
        """
        try:
        # Executa o script JavaScript no navegador
            WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script('return document.querySelector("transfer-popup")') is not None
        )
            # sleep(0.5)

            input_element = self.driver.execute_script(script)
        # Verifica se o campo de entrada foi encontrado
            if input_element:
                print("Campo encontrado! Enviando texto...")
                try:
                    input_element.click()
                    input_element.send_keys(texto)  # Envia o texto para o campo
                except:
                    input_element.click()
                    pass
            else:
                print("Erro: Input não encontrado!")

        except TimeoutException:
            print("Erro, elemento não apareceu dentro do tempo limite")
        except Exception as e:
            print(f"Erro ao executar o script: {e}")

    def reason_code_auto(self, df):
        #Label da ILPN
        auto_click = AutoClick(self.driver)
        inventory_container_path = "/html/body/app-root/ion-app/div/ion-split-pane/ion-router-outlet/inventory-grid/dm-list-layout/div/div/div[2]/dm-filter/div[2]/div/div[2]/div[2]/text-field-filter/div/ion-row/div/div/ion-input/input"
        checkbox = "//*[@id='main']/inventory-grid/dm-list-layout/div/div/div[3]/div[2]/div[1]/ion-content/grid-view/div/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/datatable-row-wrapper[1]/datatable-body-row/div[1]/datatable-body-cell/div/label/input"
        more_options = "//*[@id='main']/inventory-grid/dm-list-layout/div/div/div[3]/div[2]/footer-actions/ion-grid/ion-row/ion-col[3]/div/div/more-actions/ion-button"
        reidentify_item = "//*[@id='mat-menu-panel-2']/div/div[2]/button"
        lupa = "/html/body/app-root/ion-app/ion-modal/transfer-popup/ion-content/ion-row[2]/div/div/ion-row[2]/ion-col[2]/div/ion-row/ion-col/div/form/ion-row/ion-col/div/ion-row[1]/div/button"
        checkbox_sku = "/html/body/app-root/ion-app/ion-modal[2]/lookup-dialogue/modal-container/div/div/modal-content/ion-row[3]/grid-view/div/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/datatable-row-wrapper/datatable-body-row/div[1]/datatable-body-cell/div/input"
        submit_sku = "/html/body/app-root/ion-app/ion-modal[2]/lookup-dialogue/modal-container/div/modal-footer/div/div[2]/ion-button"
        script_input_item_Name = '''return document.querySelector("transfer-popup").querySelectorAll("input")[0];
        '''
        script_input_inventory_type = """return document.querySelector('#\\31 401');"""
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
        # copiar_sku =  self.loop_lendo_planilha(df= "item")
        # facility = self.loop_lendo_planilha(df= "facility")
        # ilpn = self.loop_lendo_planilha(df= "ilpn")
        #Criar Looping para ler as ILPN's
        # try:
        try:
            # df = self.importar_planilha()
            lista_dados = self.loop_lendo_planilha(df)
            
            for ilpn, item, facility in lista_dados:
                print(f"Processando ILPN: {ilpn}, Item: {item}, Facility: {facility}")
                auto_click.click_elemento(inventory_container_path, 30)
                auto_click.enviar_keys(inventory_container_path, ilpn, 30)
                auto_click.pressionar_enter(inventory_container_path, 10)
                auto_click.click_elemento(checkbox, 10)
                auto_click.click_elemento(more_options, 10)
                auto_click.click_elemento(reidentify_item, 10)
                self.popup_please_wait()
                self.executar_script(script_input_item_Name, f"00{item}", 30)
                auto_click.click_elemento(lupa, 30)
                auto_click.click_elemento(checkbox_sku, 30)
                auto_click.click_elemento(submit_sku, 30)
                auto_click.click_elemento(reasoncode_field, 30)
                auto_click.enviar_keys(reasoncode_field, "T3", 30)
                auto_click.pressionar_enter(reasoncode_field, 30)

                # Preenchendo os campos adicionais
                auto_click.scroll_to_element(ref1)
                auto_click.click_elemento(ref1, 30)
                auto_click.enviar_keys(ref1, "Adriano", 30)
                auto_click.enviar_keys(ref2, "Solicitação para o BOA", 30)
                auto_click.enviar_keys(attribute1, "BOA", 30)

                # Seleção do tipo de inventário
                auto_click.click_elemento(inventory_type, 30)
                auto_click._encontrar_elemento(inventory_type, 30, EC.visibility_of_element_located)
                
                try:
                    if facility == "0014":
                        auto_click.click_elemento(inv_0014, 30)
                    elif facility == "1401":
                        auto_click.click_elemento(inv_1401, 30)
                    else:
                        print(f"Facility divergente: {facility}")
                except Exception as e:
                    print(f"Erro ao validar Inventory Type: {e}")
                    self.driver.quit()
                
                auto_click.scroll_to_element(product_status)
                auto_click.click_elemento(product_status, 30)
                auto_click.scroll_to_element(product_status_021)
                auto_click.click_elemento(product_status_021, 30)
                input("Parando automação")
                auto_click.click_elemento(confir_reidentify_item, 30)
                auto_click.clear_field(inventory_container_path, 30)
            
        except Exception as e:
            print(f"Erro na automação: {e}")
             

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
            ilpn = str(row.get('ILPN', 'N/A'))
            item = str(row.get('Item', 'N/A'))
            facility = str(row.get('Facility', 'N/A'))
            dados.append((ilpn,item,facility))
            print(f"ILPN: {ilpn}, Item: {item}, Facility: {facility}")
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
            print("Encerrando")
            
        
        
        sleep(1)
        if not tentar_acao(lambda: auto_click.click_elemento(avancar, 10), "Tentando clicar em avançar"):
            return
        if not tentar_acao(lambda: auto_click.click_elemento(home, 10), "Tentando clicar no home"):
            return

# if __name__ == "__main__":