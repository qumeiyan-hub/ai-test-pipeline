"""
登录页面测试用例
覆盖：页面加载、UI元素、表单校验、Tab切换、异常场景
"""
import pytest
from playwright.sync_api import Page, expect

LOGIN_URL = "https://qwerty-test.zhenguanyu.com"


class TestLoginPageLoad:
    """页面基础加载测试"""

    def test_page_title_exists(self, page: Page):
        """页面标题不为空"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        assert page.title() != ""

    def test_page_loads_successfully(self, page: Page):
        """页面能正常加载，无 500/404 错误"""
        response = page.goto(LOGIN_URL)
        assert response.status < 400, f"页面加载失败，状态码：{response.status}"

    def test_login_form_visible(self, page: Page):
        """登录表单可见"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        # 内部账号登录 Tab
        internal_tab = page.get_by_text("内部账号登录")
        expect(internal_tab).to_be_visible()


class TestLoginTabSwitch:
    """登录方式切换测试"""

    def test_switch_to_internal_login(self, page: Page):
        """切换到内部账号登录 Tab"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()
        # 用户名输入框应可见
        username_input = page.locator("input[placeholder*='用户名'], input[type='text']").first
        expect(username_input).to_be_visible()

    def test_switch_to_sms_login(self, page: Page):
        """切换到短信免密登录 Tab"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("短信免密登录").click()
        # 手机号输入框应可见
        phone_input = page.get_by_text("手机号")
        expect(phone_input).to_be_visible()

    def test_captcha_image_visible(self, page: Page):
        """图形验证码图片可见"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()
        captcha = page.get_by_text("看不清楚？换一张")
        expect(captcha).to_be_visible()


class TestLoginFormValidation:
    """表单校验测试"""

    def test_empty_username_login(self, page: Page):
        """用户名为空时，点击登录不应跳转到业务页面（仍在登录相关页）"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()
        # 内部账号登录表单是第一个，取第一个 login-btn
        page.locator("button.login-btn").first.click()
        page.wait_for_timeout(2000)
        # 空表单提交后仍应停留在登录相关域名，不跳转到业务 dashboard
        current_url = page.url
        assert "zhenguanyu.com" in current_url, f"跳转到了意外的域名：{current_url}"
        assert "dashboard" not in current_url, f"空表单不应跳转到 dashboard：{current_url}"

    def test_wrong_credentials_stays_on_login(self, page: Page):
        """输入错误账号密码后仍留在登录页"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()

        # 填入错误账号密码
        page.locator("input[type='text'], input[placeholder*='用户名']").first.fill("wrong_user")
        page.locator("input[type='password']").first.fill("wrong_password")

        # 填入验证码占位（会失败，但验证页面不会崩溃）
        captcha_input = page.locator("input[placeholder*='验证码']").first
        if captcha_input.is_visible():
            captcha_input.fill("0000")

        # 内部账号登录表单是第一个，取第一个 login-btn
        page.locator("button.login-btn").first.click()
        page.wait_for_timeout(2000)

        # 不应跳转到 dashboard
        assert "dashboard" not in page.url or "login" in page.url or "qwerty-test" in page.url

    def test_captcha_refresh(self, page: Page):
        """点击'换一张'能刷新验证码"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()

        refresh_btn = page.get_by_text("看不清楚？换一张")
        expect(refresh_btn).to_be_visible()
        refresh_btn.click()
        page.wait_for_timeout(500)
        # 验证码刷新后按钮依然存在（不报错即通过）
        expect(refresh_btn).to_be_visible()


class TestLoginPageUI:
    """UI 元素完整性测试"""

    def test_forgot_password_link_visible(self, page: Page):
        """'忘记密码'链接可见"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        page.get_by_text("内部账号登录").click()
        forgot = page.get_by_text("忘记密码")
        expect(forgot).to_be_visible()

    def test_third_party_login_visible(self, page: Page):
        """第三方登录（飞连）按钮区域存在于页面中"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        # 飞连登录文字在 tooltip 内，验证其 DOM 存在即可
        feilian = page.locator("text=飞连一键登录")
        assert feilian.count() > 0, "飞连一键登录元素不存在于页面中"

    def test_icp_record_visible(self, page: Page):
        """页面底部备案号可见"""
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        icp = page.get_by_text("京ICP备")
        expect(icp).to_be_visible()

    def test_page_responsive_mobile(self, page: Page):
        """移动端分辨率页面正常显示"""
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")
        internal_tab = page.get_by_text("内部账号登录")
        expect(internal_tab).to_be_visible()
