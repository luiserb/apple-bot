from contextlib import suppress
import time
import random
import re
import logging

from django.conf import settings

from backend.apps.core.models import Buyer
from backend.apps.order.models import Order

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


formatter = logging.Formatter('[ %(asctime)s ] %(levelname)s : %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(settings.BASE_DIR + '/logs/bot_logs.txt')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class AppleBot:
    def __init__(self, buyer:Buyer):
        self.buyer = buyer
        self.url:str = 'https://www.apple.com/shop/buy-iphone/iphone-16-pro'
        self.executable_path:str = settings.WEBDRIVER
        self.select_memory:int = settings.IPHONE_MEMORY
        self.exist_iphone:bool = False
        self.color:str = ''
        self.store:str = ''
        self.message:str = ''
        self.hour:str = ''
        self.horary:list = [
                                '12p.m.',
                                '12:30p.m.', 
                                '12:45p.m.', 
                                '1p.m.', 
                                '1:30p.m.', 
                                '2p.m.'
                            ]
        self.horary_select:list = [
            '12:00 p.m.',
            '12:30 p.m.',
            '12:45 p.m.',
            '1:00 p.m.',
            '1:30 p.m.',
            '2:00 p.m.'
        ]

        self.browser:WebDriver = self._get_browser()
        self.run()


    def _get_browser(self) -> WebDriver:
        service:Service = Service(executable_path=self.executable_path)
        options:ChromeOptions = ChromeOptions()
        options.headless=True
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        webdriver_browser:WebDriver = Chrome(service=service, options=options)
        webdriver_browser.set_window_size(1920, 1080)
        return webdriver_browser
    

    def _format_only_number(self, text:str) -> str:
        return re.sub(r'[^0-9]', '', text)


    def _scroll(self, value:int) -> None:
        self.browser.execute_script(f'window.scrollBy(0, {value})')
    
    
    def _get_message(self) -> bool:
        try:
            message:WebElement = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'is-error')))
            self.message = 'No se pudo finalizar la compra'
            success = False
        except:
            self.message = 'Se procedió la compra'
            success = True
        return success


    def _save_order(self) -> None:
        Order.objects.create(
                                buyer=self.buyer, 
                                color=self.color, 
                                store=self.store,
                                hour=self.hour,
                                message=self.message
                            )


    def select_iphone(self) -> bool:
        select_iphone:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[2]/div[2]/div/div[1]/fieldset/div/div[2]')))
        select_iphone.click()
        logging.info('Iphone seleccionado')
        total_colors:WebElement = self.browser.find_elements(By.XPATH, '//*[@id="root"]/div[3]/div[2]/div[2]/div/div[2]/fieldset/ul/li')
        color = random.randint(1, len(total_colors))
        select_color:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="root"]/div[3]/div[2]/div[2]/div/div[2]/fieldset/ul/li[{color}]')))
        select_color.click()
        name_color:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[2]/div[2]/div/div[2]/fieldset/div')))
        self.color = name_color.text
        logging.info('Color seleccionado: {}'.format(self.color))
        total_memory = len(self.browser.find_elements(By.XPATH, '//*[@id="root"]/div[3]/div[2]/div[2]/div/div[3]/fieldset/div/div'))
        exists_iphone:bool = False
        self._scroll(400)
        time.sleep(2)
        for i in range(1, total_memory+1):
            memory:WebElement = self.browser.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[4]/div[3]/div[2]/div[2]/div/div[3]/fieldset/div/div[{i}]/label/span/span[1]/span').text
            if self.select_memory == int(self._format_only_number(text=memory)):
                select_memory:WebElement = self.browser.find_element(By.XPATH, f'//*[@id="root"]/div[3]/div[2]/div[2]/div/div[3]/fieldset/div/div[{i}]')
                select_memory.click()
                logging.info('Memoria encontrada: {}'.format(self.select_memory))
                exists_iphone = True
                break
        return exists_iphone


    def section_trade(self) -> None:
        time.sleep(5)
        no_trade_button:WebElement = self.browser.find_element(By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[1]/div[2]/div[1]/div/div/div/div[3]')
        no_trade_button.click()
        time.sleep(2)
        buy_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[2]/div/div/div/div[1]/div[2]/div/div/fieldset/div/div[1]')))
        buy_button.click()
        logging.info('Forma de pago seleccionada')
        self._scroll(120)
        time.sleep(5)
        operator_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[3]/div/div/div[1]/fieldset/div/div[5]')))
        operator_button.click()
        logging.info('Operador seleccionado')


    def section_care(self) -> None:
        time.sleep(5)
        no_apple_care_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[5]/div/div/div[1]/div[1]/fieldset/div/div/div[5]')))
        no_apple_care_button.click()


    def add_to_bag(self) -> None:
        self._scroll(650)
        time.sleep(3)

        button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[10]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/span/form/div/span/button')))
        button.click()
        #button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[3]/div[3]/div[8]/div/div/div/div/div/div[3]/div/div/div/div[2]/div/div/span/form/div/span/button')))
        #button.click()
        
        review_bag_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/form/button')))
        review_bag_button.click()
        check_out_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="shoppingCart.actions.checkout"]')))
        check_out_button.click()
    

    def checkout(self) -> None:
        continue_as_guest_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="signIn.guestLogin.guestLogin"]')))
        continue_as_guest_button.click()
        time.sleep(2)
        if self.buyer.delivery:
            delivery_option:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[1]/fieldset/fieldset/div/div[1]/button')))
            delivery_option.click()
            input_zip_code:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.deliveryTab.delivery.deliveryLocation.address.postalCode"]')))
            input_zip_code.send_keys(self.buyer.zip_code)
            search_zip_code_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.deliveryTab.delivery.deliveryLocation.address.calculate"]')))
            search_zip_code_button.click()
        else:
            pickup_store_option:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[1]/fieldset/fieldset/div/div[2]/button')))
            pickup_store_option.click()
            input_zip_code:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.pickupTab.pickup.storeLocator.searchInput"]')))
            input_zip_code.send_keys(self.buyer.zip_code)
            time.sleep(2)
            search_zip_code_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.pickupTab.pickup.storeLocator.search"]')))
            search_zip_code_button.click()
    

    def select_pickup_store(self) -> bool:
        logging.info('Buscando tiendas')
        time.sleep(12)
        total_store:int = len(self.browser.find_elements(By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div[1]/div/fieldset/ul/li'))
        logging.info('Total de tiendas encontradas: {}'.format(total_store))
        store_available:bool = False
        if total_store >= 1:
            for i in range(1, total_store):
                name_store:str = self.browser.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div[1]/div/fieldset/ul/li[{i}]/label/span/span[1]/span/span/span[1]').text
                available:str = self.browser.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div[1]/div/fieldset/ul/li[{i}]/label/span/span[2]/span/span[1]').text
                if not 'unavailable' in available.lower():
                    time.sleep(4)
                    store_button:WebElement = self.browser.find_element(By.XPATH, f'//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div[1]/div/fieldset/ul/li[{i}]')
                    store_button.click()
                    self.store = name_store
                    logging.info('Tienda disponible encontrada: {}'.format(name_store))
                    WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.pickupTab.pickup.timeSlot.dateTimeSlots.timeSlotValue"]')))
                    select_options_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.fulfillment.pickupTab.pickup.timeSlot.dateTimeSlots.timeSlotValue"]')))
                    select_options_input.click()
                    select = Select(self.browser.find_element(By.XPATH, '//*[@id="checkout.fulfillment.pickupTab.pickup.timeSlot.dateTimeSlots.timeSlotValue"]'))
                    all_options = self.browser.find_elements(By.TAG_NAME, 'option')
                    for index, option in enumerate(all_options):
                        for horary in self.horary_select:
                            if horary in option.text:
                                select.select_by_index(index)
                                self.hour = option.text
                                logging.info('Horario seleccionado: {}'.format(option.text))
                                store_available = True
                                break
                        if store_available:
                            break
                if store_available:
                    break
            if store_available:
                continue_to_shipping_address:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')))
                continue_to_shipping_address.click()
            else:
                logging.info('No se ha encontrado tienda disponible')
        return store_available
    
    
    def delivery_options(self) -> bool:
        select:bool = False
        WebDriverWait(self.browser, 7).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[2]/div/fieldset/div/fieldset/div/div[2]')))
        total_options:int = len(self.browser.find_elements(By.XPATH, '//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[2]/div/fieldset/div/fieldset/div/div[2]/div'))
        if total_options >= 1:
            for i in range(1, total_options+1):
                label:str = self.browser.find_element(By.XPATH, f'//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[2]/div/fieldset/div/fieldset/div/div[2]/div[{i}]/div/label/span/span').text
                option:WebElement = self.browser.find_element(By.XPATH, f'//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[2]/div/fieldset/div/fieldset/div/div[2]/div[{i}]/div')
                for horary in self.horary:
                    if horary in label:
                        logging.info('Delivery seleccionado: {}'.format(label))
                        option.click()
                        select = True
                        break
                if select:
                    break
        return select
        

    def select_delivery(self) -> bool:
        logging.info('Buscando delivery')
        time.sleep(15)
        total_options:int = len(self.browser.find_elements(By.XPATH, '//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div'))
        logging.info('Total de delivery disponibles: {}'.format(total_options))
        select:bool = False
        if total_options >= 1:
            for i in range(1, total_options):
                option:WebElement = self.browser.find_element(By.XPATH, f'//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[{i}]/label')
                value:str = self.browser.find_element(By.XPATH, f'//*[@id="checkout-container"]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[3]/fieldset/div/div[{i}]/label/span/span[2]').text
                option.click()
                delivery = self.delivery_options()
                if delivery:
                    select = True
                    break
                if select:
                    break
            if select:
                button_continue:WebElement = self.browser.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
                button_continue.click()
                return True
            else:
                return False
        else:
            return False
    

    def verify_modal(self) -> bool:
        try:
            time.sleep(3)
            logging.info('Esperando model de verificación')
            WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="portal"]/div/div/div/div')))
            button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressVerification.selectedAddress.continueWithSelectedAddress"]')))
            button.click()
            return True
        except:
            return False
        
    
    
    def form_delivery(self) -> None:
        first_name:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressSelector.newAddress.address.firstName"]')))
        first_name.send_keys(self.buyer.first_name)
        last_name:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressSelector.newAddress.address.lastName"]')))
        last_name.send_keys(self.buyer.last_name)
        street_address:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressSelector.newAddress.address.street"]')))
        street_address.send_keys(self.buyer.street_address)
        email:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressContactEmail.address.emailAddress"]')))
        email.send_keys(self.buyer.email)
        phone:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.shipping.addressContactPhone.address.fullDaytimePhone"]')))
        phone.send_keys(self.buyer.phone)
        button_continue = self.browser.find_element(By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')
        button_continue.click()
        if self.verify_modal():
            logging.info('Presionando botón de continuación de compra')
            time.sleep(10)
            with suppress(Exception):
                button_continue.click()
    

    def order(self) -> None:
        with suppress(Exception):
            first_name_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.pickupContact.selfPickupContact.selfContact.address.firstName"]')))
            first_name_input.send_keys(self.buyer.first_name)
            last_name_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.pickupContact.selfPickupContact.selfContact.address.lastName"]')))
            last_name_input.send_keys(self.buyer.last_name)
            email:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.pickupContact.selfPickupContact.selfContact.address.emailAddress"]')))
            email.send_keys(self.buyer.email)
            phone:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.pickupContact.selfPickupContact.selfContact.address.fullDaytimePhone"]')))
            phone.send_keys(self.buyer.phone)
        self._scroll(value=500)
        button_continue:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')))
        button_continue.click()
        logging.info('Orden realizada con éxito')
        time.sleep(20)
    

    def pay(self) -> None:
        success:bool = False
        if self.buyer.payment_card and self.buyer.payment_card_status is True:
            debit_card_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingoptions.credit-selector"]')))
            debit_card_button.click()
            time.sleep(3)
            logging.info('Procediendo a introducir datos de la tarjeta')

            debit_card_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.cardInputs.cardInput-0.cardNumber"]')))
            debit_card_input.send_keys(self.buyer.payment_card.number)
            debit_card_expiration_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.cardInputs.cardInput-0.expiration"]')))
            debit_card_expiration_input.send_keys(self.buyer.payment_card.expiration)
            debit_card_cvv_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.cardInputs.cardInput-0.securityCode"]')))
            debit_card_cvv_input.send_keys(self.buyer.payment_card.cvv)
            
            if not self.buyer.delivery:
                self._scroll(200)
                logging.info('Rellenando datos Billing')
                billing_first_name:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.billingAddress.address.firstName"]')))
                billing_first_name.send_keys(self.buyer.first_name)
                billing_last_name:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.billingAddress.address.lastName"]')))
                billing_last_name.send_keys(self.buyer.last_name)
                billing_street:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.billingAddress.address.street"]')))
                billing_street.send_keys(self.buyer.street_address)
                billing_zip_code:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.creditCard.billingAddress.address.zipLookup.postalCode"]')))
                billing_zip_code.send_keys(self.buyer.zip_code)
                time.sleep(4)
            button_continue:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')))
            button_continue.click()
            success = True
        elif self.buyer.gift_card and self.buyer.payment_card_status is False:
            logging.info('Procediendo a introducir datos de la tarjeta de regalo')
            gift_card_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.giftCard.giftCardInput.resetFields"]')))
            gift_card_button.click()
            gift_card_input:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.giftCard.giftCardInput.giftCard"]')))
            gift_card_input.send_keys(self.buyer.gift_card.number)
            send_gift_card_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout.billing.billingOptions.selectedBillingOptions.giftCard.giftCardInput.applyGiftCard"]')))
            send_gift_card_button.click()
            success = self._get_message()
            if success is False:
                self._save_order()
        if success:
            self._scroll(500)
            logging.info('Procediendo a finalizar el pedido')
            time.sleep(12)
            continue_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[3]/div/div')))
            continue_button.click()

            logging.info('Esperando factura')
            time.sleep(12)
            pay_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[3]/div/div')))
            pay_button.click()
            self._scroll(500)
            with suppress(Exception):
                checkout_continue_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkout-container"]/div[1]/div[2]/div/div[1]/div[5]/div/div/div')))
                checkout_continue_button.click()
                checkout_continue_button:WebElement = WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rs-checkout-continue-button-bottom"]')))
                checkout_continue_button.click()
                logging.info('Finalizando pedido')
            time.sleep(30)
            success = self._get_message()
            self._save_order()

    
    def run(self) -> None:
        self.browser.get(url=self.url)
        exists_iphone = self.select_iphone()
        if exists_iphone:
            self.section_trade()
            self.section_care()
            self.add_to_bag()
            self.checkout()
            if self.buyer.delivery:
                if self.select_delivery():
                    self.form_delivery()
                    self.pay()
                    self.order()
            else:
                if self.select_pickup_store():
                    self.order()
                    self.pay()
        self.browser.close()
