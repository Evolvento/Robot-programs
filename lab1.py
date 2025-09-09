from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Вариант В, Б, Г, А, В - Microsoft Edge, locked_out_user / secret_sauce, Сортировка по цене (high to low), Добавить первый товар из списка., Добавить товар в корзину, перейти в корзину и продолжить покупки (вернуться в каталог).

driver = webdriver.Edge()

driver.get("https://www.saucedemo.com/")

driver.implicitly_wait(2)


usernames = ["locked_out_user", "standard_user"]
cur_user = 0
password = "secret_sauce"


field_username = driver.find_element(By.ID, "user-name")
field_password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.ID, "login-button")


field_username.send_keys(usernames[cur_user])
field_password.send_keys(password)

login_button.click()

try:
    error_button = driver.find_element(By.CLASS_NAME, "error-button")
    error_button.click()

    field_username.clear()
    field_password.clear()
    cur_user += 1


    field_username.send_keys(usernames[cur_user])
    field_password.clear()
    field_password.send_keys(password)

    login_button.click()
    
except NoSuchElementException:
    print("Элемент error-button не найден на странице. Пользователь успешно вошел в систему.")


select_container = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))

select_container.select_by_visible_text("Price (high to low)")

button_in_card_product = driver.find_element(By.ID, "add-to-cart-sauce-labs-fleece-jacket")

button_in_card_product.click()

basket_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")

basket_button.click()

cart_footer = driver.find_element(By.CLASS_NAME, "cart_footer")
button_return = cart_footer.find_element(By.TAG_NAME, "button")

button_return.click()

driver.quit()