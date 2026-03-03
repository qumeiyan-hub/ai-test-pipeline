import pytest
import pathlib
import datetime
import base64
from playwright.sync_api import sync_playwright

BASE_URL  = "https://qwerty-test.zhenguanyu.com"
DASHBOARD = "https://qwerty-test.zhenguanyu.com/#/dashboard"

SESSION_FILE   = pathlib.Path(__file__).parent.parent / "session_state.json"
SCREENSHOT_DIR = pathlib.Path(__file__).parent.parent / "reports" / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

# nodeid -> playwright page 对象
_page_registry: dict = {}
# nodeid -> [(label, base64_str), ...]  过程截图存储
_screenshots_store: dict = {}


# ─────────────────────────────────────────────
# 浏览器（session 级，整个会话只启动一次）
# ─────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()


# ─────────────────────────────────────────────
# 未登录页面 fixture
# ─────────────────────────────────────────────
@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context(viewport={"width": 1280, "height": 720}, locale="zh-CN")
    pg = context.new_page()
    _page_registry[request.node.nodeid] = pg
    yield pg
    _page_registry.pop(request.node.nodeid, None)
    context.close()


# ─────────────────────────────────────────────
# 已登录页面 fixture
# ─────────────────────────────────────────────
@pytest.fixture(scope="function")
def auth_page(browser, request):
    storage = str(SESSION_FILE) if SESSION_FILE.exists() else None
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="zh-CN",
        storage_state=storage,
    )
    pg = context.new_page()
    _page_registry[request.node.nodeid] = pg
    yield pg
    _page_registry.pop(request.node.nodeid, None)
    context.close()


# ─────────────────────────────────────────────
# 多截图 capture fixture
# 用法：capture(page, "步骤名称")
# ─────────────────────────────────────────────
@pytest.fixture(scope="function")
def capture(request):
    """过程截图辅助，测试中随时调用 capture(page, '步骤说明')"""
    store: list = []
    _screenshots_store[request.node.nodeid] = store

    def _snap(pg, label: str = ""):
        try:
            ts = datetime.datetime.now().strftime("%H%M%S_%f")
            safe = request.node.nodeid.replace("/", "_").replace("::", "__").replace(" ", "_")
            filename = SCREENSHOT_DIR / f"{safe}__{len(store):02d}_{ts}.png"
            pg.screenshot(path=str(filename), full_page=False)
            b64 = base64.b64encode(filename.read_bytes()).decode()
            store.append((label or f"步骤{len(store)+1}", b64))
        except Exception as e:
            print(f"\n[capture] 截图失败: {e}")

    yield _snap
    # 存储由钩子收集，不在此清理


# ─────────────────────────────────────────────
# pytest-html 钩子：call 阶段结束后收集所有截图
# ─────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    # 收集过程截图
    screenshots = list(_screenshots_store.pop(item.nodeid, []))

    # 追加最终状态全页截图
    pg = _page_registry.get(item.nodeid)
    if pg:
        try:
            img_bytes = pg.screenshot(full_page=True)
            b64 = base64.b64encode(img_bytes).decode()
            status = "❌ 失败" if report.failed else "✅ 通过"
            screenshots.append((f"最终页面 [{status}]", b64))
        except Exception:
            pass

    if not screenshots:
        return

    from pytest_html import extras as html_extras
    existing = list(getattr(report, "extras", []) or [])

    # 中文用例描述（取 docstring 第一行）
    doc = getattr(item.function, "__doc__", "") or ""
    desc = doc.strip().splitlines()[0].strip() if doc.strip() else ""
    if desc:
        existing.append(html_extras.html(
            f'<div style="padding:4px 8px;background:#eaf4ff;border-left:3px solid #3498db;'
            f'margin-bottom:6px;font-size:13px"><b>📋 用例说明：</b>{desc}</div>'
        ))

    # 注入每一步截图
    for i, (label, b64) in enumerate(screenshots):
        existing.append(html_extras.png(b64, name=f"[{i+1}] {label}"))

    report.extras = existing
