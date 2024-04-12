from settings import valid_password, valid_phone
import  pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time



@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Firefox()
    # Переходим на страницу авторизации
    driver.get("https://my.rt.ru/")
    yield driver

    driver.quit()

@pytest.fixture(autouse=True)
def wait_open_page(driver):
    # ожидание 10 секунд пока не повятся форма авторизации
    driver.implicitly_wait(10)
    driver.find_element(By.ID, "card-title")


def test_login(driver):
    #позитивный тест на вход  в систему
    #поиск поля для ввода номера телефона
    driver.find_element(By.ID, "username").send_keys(valid_phone)
    #поиск поля для ввода пароля
    driver.find_element(By.ID, "password").send_keys(valid_password)
    driver.find_element(By.ID, "kc-login").click()
    assert driver.find_element((By.ID, "redirect_uri"))


def test_error_phone(driver):
    #тест при некорректном заполнении номера
    driver.find_element(By.ID, "username").send_keys("5986")
    # поиск поля для ввода пароля
    driver.find_element(By.ID, "password").send_keys(valid_password)
    driver.implicitly_wait(5)
    #поиск сообщения об ошибке
    driver.find_element(By.ID, "username-meta")


def test_error_password(driver):
    #тест при неверноем заполнении паролz
    driver.find_element(By.ID, "username").send_keys(valid_phone)
    # поиск поля для ввода пароля
    driver.find_element(By.ID, "password").send_keys("Tr1qwe")
    driver.find_element(By.ID, "kc-login").click()
    #ожидание сообщения об ошибке
    driver.implicitly_wait(5)
    driver.find_element(By.ID, "form-error-message")


def test_null_login(driver):
    #пустое поле логина выдает ошибку о необходимости ввести логин
    driver.find_element(By.ID, "password").send_keys(valid_password)
    #активация time.sleep для ручного ввода капчи
    #time.sleep(20)
    driver.find_element(By.ID, "kc-login").click()
    #ожидание сообщения об ошибки
    WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="username-meta"]')))


def test_null_password(driver):
    #пустое поле пароля выдает ошибку о необходимости ввести пароль
    driver.find_element(By.ID, "username").send_keys(valid_phone)
    #time.sleep(20)
    driver.find_element(By.ID, "kc-login").click()
    driver.implicitly_wait(5)
    #ожидание сообщения об ошибке
    driver.find_element(By.XPATH, "//*[@class='rt-input-container__meta rt-input-container__meta--error']")

def test_single_cocde(driver):
    driver.find_element(By.ID, 'back_to_otp_btn').click()
    WebDriverWait(driver,5).until(EC.text_to_be_present_in_element((By.ID, 'card-title'), ('Авторизация по коду')))
    driver.find_element(By.ID, 'address').send_keys(valid_phone)
    driver.find_element(By.ID, 'otp_get_code').click()
    #ожидание для ручного ввода временного кода
    time.sleep(15)
    driver.find_element((By.ID, "redirect_uri"))
    

def test_error_single_code(driver):
    driver.find_element(By.ID, 'back_to_otp_btn').click()
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, 'card-title'), ('Авторизация по коду')))
    driver.find_element(By.ID, 'address').send_keys(valid_phone)
    driver.find_element(By.ID, 'otp_get_code').click()
    driver.find_element(By.CLASS_NAME, 'rt-code-input rt-code-input--center code-input-container__code-input code-input').send_keys('456123')
    #ожидание сообщения об ошибке
    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.ID, 'form-error-message'), ('Неверный код. Повторите попытку')))


def test_time_single_code(driver):
    driver.find_element(By.ID, 'back_to_otp_btn').click()
    WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, 'card-title'), ('Авторизация по коду')))
    driver.find_element(By.ID, 'address').send_keys(valid_phone)
    driver.find_element(By.ID, 'otp_get_code').click()
    #ожидание для того чтобы код вручную ввести после истечения срока
    time.sleep(140)
    #ожидание сообщения об ошибке
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'form-error-message')))


def test_help(driver):
    #вспылвающее окно при нажатии на ссылку помощь
    driver.find_element(By.ID, 'faq-open').click()
    WebDriverWait(driver, 3).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "faq-modal__title"), ('Ваш безопасный ключ к сервисам Ростелекома')))
