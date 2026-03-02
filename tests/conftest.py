import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://qwerty-test.zhenguanyu.com/#/dashboard?tab=finished"
LOGIN_URL = "https://qwerty-test.zhenguanyu.com"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
    )
    page = context.new_page()
    yield page
    context.close()
