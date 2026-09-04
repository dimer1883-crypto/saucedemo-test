# Курс: автотесты Selenium + pytest (saucedemo)

Учебный проект UI-автотестов для saucedemo.com (паттерн Page Object).
Репозиторий: https://github.com/dimer1883-crypto/saucedemo-test

---

## Установка на новый ПК (или переустановка с нуля)

Нужно: Python 3.13 (запускается командой `py`), git, Google Chrome.

1. Клонировать репозиторий:
```
git clone https://github.com/dimer1883-crypto/saucedemo-test.git
cd saucedemo-test
```

2. Создать виртуальное окружение (важно: команда `py`, а не `python`):
```
py -3.13 -m venv .venv
```

3. Активировать его:
- PowerShell: `.\.venv\Scripts\Activate.ps1`
- cmd: `.venv\Scripts\activate.bat`

4. Установить зависимости:
```
pip install -r requirements.txt
```

5. Проверить, что всё работает:
```
pytest
```
Должно быть `5 passed`.

## Очистка / пересоздание окружения

Если окружение сломалось или нужно всё пересоздать — удали папку `.venv`
(и при желании `__pycache__`, `.pytest_cache`), затем повтори шаги 2–5.

В cmd: `rmdir /s .venv`  (или просто удали папку `.venv` в проводнике).

---

## Прогресс по урокам

- [x] Урок 1 — окружение + первый тест
- [x] Урок 2 — фикстура (conftest.py) + Page Object
- [x] Урок 3 — сценарий входа (позитивный) + InventoryPage
- [x] Урок 4 — негативный тест (неверный пароль)
- [x] Урок 5 — параметризация (@pytest.mark.parametrize)
- [ ] Урок 6 — locked_out_user (негативный)
- [ ] Урок 7 — явные ожидания (WebDriverWait)
- [ ] Урок 8 — корзина и выход из аккаунта
- [ ] Урок 9 — Allure-отчёты
- [ ] Урок 10 — CI (GitHub Actions) + pytest.ini

---

## Урок 1. Окружение + первый тест

Что изучили: venv, установка selenium + pytest, Selenium Manager (сам качает
chromedriver), первый запуск браузера.

Ключевое: на ПК `python` ведёт на Python из Hermes (3.11), поэтому окружение
создаём через `py -3.13 -m venv .venv`.

```python
# tests/test_login.py (первая версия, без фикстуры)
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_login_page_load():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com")

    login_button = driver.find_element(By.ID, "login-button")
    assert login_button.is_displayed()

    driver.quit()
```

---

## Урок 2. Фикстура + Page Object

Что изучили: фикстура pytest (yield = подготовка + уборка, браузер закрывается
всегда), паттерн Page Object (страница = класс, селекторы в одном месте).

`conftest.py`:
```python
import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()
```

`pages/__init__.py` — пустой файл (делает `pages` пакетом).

`pages/login_page.py`:
```python
from selenium.webdriver.common.by import By


class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def login_button(self):
        return self.driver.find_element(By.ID, "login-button")
```

---

## Урок 3. Сценарий входа (позитивный)

Что изучили: `send_keys` (ввод текста), `click`, `.text` (чтение текста),
вторая страница InventoryPage, проверка результата действия.

`pages/login_page.py` (добавился метод `login`):
```python
def login(self, username, password):
    self.driver.find_element(By.ID, "user-name").send_keys(username)
    self.driver.find_element(By.ID, "password").send_keys(password)
    self.login_button().click()
```

`pages/inventory_page.py`:
```python
from selenium.webdriver.common.by import By


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, driver):
        self.driver = driver

    def title(self):
        return self.driver.find_element(By.CLASS_NAME, "title").text
```

`tests/test_login.py` (добавился позитивный тест):
```python
def test_successful_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"
```

---

## Урок 4. Негативный тест (неверный пароль)

Что изучили: негативный сценарий, атрибут `data-test` (стабильный селектор),
поиск по CSS, проверка части строки через `in`.

`pages/login_page.py` (добавился метод `error_message`):
```python
def error_message(self):
    return self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
```

`tests/test_login.py` (добавился негативный тест):
```python
def test_failed_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "wrong_password")

    error_text = login_page.error_message()
    assert "Username and password do not match" in error_text
```

---

## Урок 5. Параметризация

Что изучили: `@pytest.mark.parametrize` — один тест прогоняется несколько раз
с разными данными (вместо копирования теста под каждого пользователя).

```python
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.parametrize(
    "username",
    ["standard_user", "visual_user", "problem_user"],
)
def test_successful_login(driver, username):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, "secret_sauce")

    inventory_page = InventoryPage(driver)
    assert inventory_page.title() == "Products"
```

После запуска каждый набор данных — отдельный кейс в отчёте:
`test_successful_login[standard_user]`, `test_successful_login[visual_user]` и т.д.

---

## Итоговая структура проекта

```
saucedemo-test/
├── conftest.py           # фикстура driver
├── pages/
│   ├── __init__.py
│   ├── login_page.py     # LoginPage (open, login, login_button, error_message)
│   └── inventory_page.py # InventoryPage (title)
├── tests/
│   └── test_login.py
├── requirements.txt
├── README.md
├── LESSONS.md            # этот файл
└── .gitignore
```

## Шпаргалка по saucedemo

- Пароль у всех пользователей: `secret_sauce`.
- Пользователи: `standard_user`, `visual_user`, `problem_user`,
  `performance_glitch_user` (медленный), `error_user`, `locked_out_user`.
- `locked_out_user` — заблокирован, НЕ входит (ошибка «Sorry, this user has been locked out»).
- Селекторы: `#user-name`, `#password`, `#login-button`, `[data-test="error"]`, `.title`.
