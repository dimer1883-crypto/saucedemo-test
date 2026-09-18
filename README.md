# saucedemo-test — UI-автотесты на Python (Selenium + pytest + Page Object)

Учебный проект: UI-автотесты для https://www.saucedemo.com — тренировочного
интернет-магазина, специально сделанного для практики тестирования.

Тесты покрывают авторизацию и корзину, написаны по паттерну Page Object:
селекторы и действия лежат в классах страниц, сами тесты читаются как шаги сценария.
Тесты запускаются автоматически в GitHub Actions на каждый push и pull request.

API-часть (requests + pytest) — в отдельном репозитории:
https://github.com/dimer1883-crypto/api-tests

## Стек

- Python 3.13
- pytest — раннер и параметризация
- Selenium WebDriver — управление браузером
- Page Object — структура тестового кода
- Allure — отчётность (аннотации `@allure.feature`, скриншот при падении)
- GitHub Actions — CI

## Что покрыто

| Тест | Сценарий |
| --- | --- |
| tests/test_login.py::test_login_page_load | Страница логина открывается, кнопка входа отображается |
| tests/test_login.py::test_successful_login | Успешный вход 4 разными типами пользователей (параметризация: standard, visual, problem, performance_glitch) — проверка, что открывается каталог товаров |
| tests/test_login.py::test_failed_login | Негативные сценарии: неверный пароль и заблокированный пользователь — проверка текста ошибки |
| tests/test_login.py::test_logout | Выход через бургер-меню возвращает на страницу логина |
| tests/test_cart.py::test_add_to_cart | Товар добавляется в корзину, счётчик на иконке становится 1 |
| tests/test_cart.py::test_cart_contains_added_item | Добавленный товар действительно лежит в корзине (проверка по названию) |

## Структура

```
saucedemo-test/
├── conftest.py                 # фикстура driver (headless в CI) + скриншот в Allure при падении
├── pytest.ini                  # testpaths = tests
├── requirements.txt
├── LESSONS.md                  # конспект курса: уроки и прогресс
├── pages/
│   ├── login_page.py           # вход, проверка ошибки, ожидание загрузки
│   ├── inventory_page.py       # каталог: добавление в корзину, счётчик, выход
│   └── cart_page.py            # корзина: список товаров
├── tests/
│   ├── test_login.py
│   └── test_cart.py
└── .github/workflows/tests.yml # CI: pytest в headless Chrome на каждый push
```

## Как запустить

Нужен Python 3.13, git и установленный Chrome (драйвер Selenium скачивает сам).

1. Клонировать репозиторий и перейти в него:

```
git clone https://github.com/dimer1883-crypto/saucedemo-test.git
cd saucedemo-test
```

2. Создать виртуальное окружение и активировать его:

```
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1     # PowerShell
.venv\Scripts\activate.bat       # cmd
```

3. Установить зависимости:

```
pip install -r requirements.txt
```

4. Запустить тесты:

```
pytest -v
```

Локально браузер открывается в обычном режиме. В CI переменная `CI` задана, поэтому
Chrome стартует в headless-режиме без окна — логика запуска в `conftest.py`.

## Отчёт Allure

При падении теста к отчёту автоматически прикладывается скриншот браузера
(хук `pytest_runtest_makereport` в `conftest.py`).

```
pytest --alluredir=allure-results
allure serve allure-results
```

## CI

Workflow `.github/workflows/tests.yml`: на каждый push запускается Ubuntu-раннер,
ставится Python 3.13 и Chrome, устанавливаются зависимости из `requirements.txt`
и выполняется `pytest`. Статус прогона виден во вкладке Actions.

## Заметки по курсу

Подробный конспект уроков и разбор ошибок — в [LESSONS.md](LESSONS.md).
