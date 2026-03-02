"""
登录后功能测试用例
覆盖：Dashboard、导航菜单、Tab切换、班课数据、页面跳转
"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL  = "https://qwerty-test.zhenguanyu.com"
DASHBOARD = f"{BASE_URL}/#/dashboard"


class TestDashboardAccess:
    """Dashboard 基础访问测试"""

    def test_dashboard_loads_after_login(self, auth_page: Page):
        """登录后能正常访问 Dashboard"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        assert "dashboard" in auth_page.url, "未跳转到 dashboard 页面"

    def test_user_info_visible(self, auth_page: Page):
        """登录用户信息可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        # 用户名 qumeiyan 应出现在页面中
        user = auth_page.get_by_text("qumeiyan")
        expect(user.first).to_be_visible()

    def test_not_redirect_to_login(self, auth_page: Page):
        """携带会话访问不应被重定向到登录页"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        assert "login" not in auth_page.url, "会话失效，被重定向到登录页"


class TestNavigationMenu:
    """顶部导航菜单测试"""

    def test_main_nav_items_visible(self, auth_page: Page):
        """主导航菜单项全部可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        for nav_text in ["我的带班", "AI课跟课", "小课堂"]:
            item = auth_page.get_by_text(nav_text).first
            expect(item).to_be_visible(timeout=10000)

    def test_nav_click_ai_lesson(self, auth_page: Page):
        """点击 AI课跟课 能正常跳转"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        auth_page.get_by_text("AI课跟课").first.click()
        auth_page.wait_for_load_state("networkidle")
        assert "lesson-following-system" in auth_page.url, "AI课跟课页面未正常跳转"

    def test_nav_click_mini_lesson(self, auth_page: Page):
        """点击 小课堂 能正常跳转"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        auth_page.get_by_text("小课堂").first.click()
        auth_page.wait_for_load_state("networkidle")
        assert "mini-lesson" in auth_page.url, "小课堂页面未正常跳转"

    def test_back_to_dashboard(self, auth_page: Page):
        """从子页面点击'我的带班'能返回 Dashboard"""
        auth_page.goto(f"{BASE_URL}/#/lesson-following-system")
        auth_page.wait_for_load_state("networkidle")
        auth_page.get_by_text("我的带班").first.click()
        auth_page.wait_for_load_state("networkidle")
        assert "dashboard" in auth_page.url


class TestDashboardTabs:
    """Dashboard Tab 切换测试"""

    def test_tab_in_progress_visible(self, auth_page: Page):
        """'进行中' Tab 可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        tab = auth_page.get_by_text("进行中").first
        expect(tab).to_be_visible()

    def test_tab_not_started_visible(self, auth_page: Page):
        """'待开始' Tab 可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        tab = auth_page.get_by_text("待开始").first
        expect(tab).to_be_visible()

    def test_tab_finished_visible(self, auth_page: Page):
        """'已结束' Tab 可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        tab = auth_page.get_by_text("已结束").first
        expect(tab).to_be_visible()

    def test_switch_to_finished_tab(self, auth_page: Page):
        """切换到'已结束' Tab 后内容正常加载"""
        auth_page.goto(f"{DASHBOARD}?tab=finished")
        auth_page.wait_for_load_state("networkidle")
        # 已结束 tab 下有班课数据
        finished_count = auth_page.get_by_text("已结束").first
        expect(finished_count).to_be_visible()

    def test_tab_counts_visible(self, auth_page: Page):
        """各 Tab 下的数量统计可见"""
        auth_page.goto(DASHBOARD)
        auth_page.wait_for_load_state("networkidle")
        # 进行中、待开始、已结束 后面的数量应存在于页面
        counts = auth_page.locator("text=/进行中|待开始|已结束/").all()
        assert len(counts) >= 3, "Tab 数量统计未正确显示"


class TestClassCardData:
    """班课卡片数据测试"""

    def test_finished_class_card_visible(self, auth_page: Page):
        """已结束 Tab 下班课卡片正常显示"""
        auth_page.goto(f"{DASHBOARD}?tab=finished")
        auth_page.wait_for_load_state("networkidle")
        auth_page.wait_for_timeout(2000)
        # 应该有已结课的班课卡片
        card = auth_page.get_by_text("已结课").first
        expect(card).to_be_visible()

    def test_class_card_contains_teacher(self, auth_page: Page):
        """班课卡片包含主讲信息"""
        auth_page.goto(f"{DASHBOARD}?tab=finished")
        auth_page.wait_for_load_state("networkidle")
        auth_page.wait_for_timeout(2000)
        teacher_label = auth_page.get_by_text("主讲：").first
        expect(teacher_label).to_be_visible()

    def test_class_card_contains_student_count(self, auth_page: Page):
        """班课卡片包含学员人数"""
        auth_page.goto(f"{DASHBOARD}?tab=finished")
        auth_page.wait_for_load_state("networkidle")
        auth_page.wait_for_timeout(2000)
        count_label = auth_page.get_by_text("人").first
        expect(count_label).to_be_visible()

    def test_download_ranking_button_visible(self, auth_page: Page):
        """'下载排行榜' 按钮可见"""
        auth_page.goto(f"{DASHBOARD}?tab=finished")
        auth_page.wait_for_load_state("networkidle")
        auth_page.wait_for_timeout(2000)
        btn = auth_page.get_by_text("下载排行榜")
        expect(btn).to_be_visible()
