import pytest
import pathlib
from playwright.sync_api import sync_playwright

BASE_URL  = "https://qwerty-test.zhenguanyu.com"
DASHBOARD = "https://qwerty-test.zhenguanyu.com/#/dashboard"

SESSION_FILE = pathlib.Path(__file__).parent.parent / "session_state.json"


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """未登录页面（用于登录页测试）"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
    )
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def auth_page(browser):
    """已登录页面（复用 session_state.json 中的会话）"""
    storage = str(SESSION_FILE) if SESSION_FILE.exists() else None
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
        storage_state=storage,
    )
    page = context.new_page()
    yield page
    context.close()
