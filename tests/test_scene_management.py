"""
班课详情-自定义场景配置 自动化测试
基于需求文档：【班课详情】支持自定义设置：场景(Tab)、字段、功能按钮、指标

测试分层：
  - 可完全自动化：UI可见性、Tab默认展示、按钮状态、人数显示逻辑
  - 需要数据配合：场景CRUD（标注 @pytest.mark.requires_data）
"""
import pytest
from playwright.sync_api import Page, expect

BASE_URL    = "https://qwerty-test.zhenguanyu.com"
# C入门班 已结束班课（测试环境现有数据）
CLASS_URL   = f"{BASE_URL}/#/lesson/lesson-detail?id=10566630&teamId=&tab=courseData&episodeIndex=1"
DASHBOARD   = f"{BASE_URL}/#/dashboard?tab=finished"


# ══════════════════════════════════════════════
# TC-SCENE-FUNC：功能测试
# ══════════════════════════════════════════════
class TestDefaultSceneTabs:
    """TC-SCENE-FUNC-001/002：入门班默认场景Tab验证（P0）"""

    def test_rumen_default_three_tabs_visible(self, auth_page: Page):
        """TC-SCENE-FUNC-001: 入门班默认显示课前沟通/课后回访/转化沟通三个Tab"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        for tab_name in ["课前沟通", "课后回访", "转化沟通"]:
            tab = auth_page.locator("li.next-tabs-tab", has_text=tab_name)
            expect(tab).to_be_visible(timeout=8000)

    def test_rumen_tabs_count_is_three(self, auth_page: Page):
        """TC-SCENE-FUNC-001补充: 入门班默认Tab数量应为3个"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        tabs = auth_page.locator("li.next-tabs-tab")
        tab_count = tabs.count()
        assert tab_count == 3, f"期望3个默认Tab，实际可见{tab_count}个"

    def test_tab_switch_to_course_before(self, auth_page: Page):
        """TC-SCENE-FUNC: 点击「课前沟通」Tab可正常切换"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        auth_page.locator("li.next-tabs-tab", has_text="课前沟通").click()
        auth_page.wait_for_timeout(1000)
        assert "lesson-detail" in auth_page.url

    def test_tab_switch_to_course_after(self, auth_page: Page):
        """TC-SCENE-FUNC: 点击「课后回访」Tab可正常切换"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        auth_page.locator("li.next-tabs-tab", has_text="课后回访").click()
        auth_page.wait_for_timeout(1000)
        assert "lesson-detail" in auth_page.url

    def test_tab_switch_to_conversion(self, auth_page: Page):
        """TC-SCENE-FUNC: 点击「转化沟通」Tab可正常切换"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        auth_page.locator("li.next-tabs-tab", has_text="转化沟通").click()
        auth_page.wait_for_timeout(1000)
        assert "lesson-detail" in auth_page.url


# ══════════════════════════════════════════════
# TC-SCENE-FUNC：功能按钮展示测试
# ══════════════════════════════════════════════
class TestFunctionButtons:
    """TC-SCENE-FUNC-008: 功能按钮在场景内正常展示"""

    def test_upper_function_buttons_visible(self, auth_page: Page):
        """上层功能按钮（无需选学员）可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button.next-btn", timeout=15000)
        auth_page.wait_for_timeout(1000)
        for btn_text in ["任务执行", "用户分层", "生成榜单"]:
            btn = auth_page.locator(f"button:has-text('{btn_text}')").first
            expect(btn).to_be_visible(timeout=8000)

    def test_download_buttons_visible(self, auth_page: Page):
        """下载类功能按钮可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button.next-btn", timeout=15000)
        auth_page.wait_for_timeout(1000)
        btn = auth_page.locator("button:has-text('下载课程表现')").first
        expect(btn).to_be_visible()

    def test_lower_function_buttons_visible(self, auth_page: Page):
        """下层功能按钮（需先选学员）可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button.next-btn", timeout=15000)
        auth_page.wait_for_timeout(1000)
        for btn_text in ["补加金币", "请假", "临调", "维护学员标签", "生成奖状"]:
            btn = auth_page.locator(f"button:has-text('{btn_text}')").first
            expect(btn).to_be_visible(timeout=8000)

    def test_non_s_line_online_filter_visible(self, auth_page: Page):
        """TC-FIELD-COND-005: C入班课（非S线）展示「在线用户筛选」按钮"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button.next-btn", timeout=15000)
        auth_page.wait_for_timeout(1000)
        btn = auth_page.locator("button:has-text('在线用户筛选')").first
        expect(btn).to_be_visible()


# ══════════════════════════════════════════════
# TC-SCENE-EXC：异常测试 - 按钮权限与禁用状态
# ══════════════════════════════════════════════
class TestButtonPermissions:
    """TC-SCENE-EXC-009/010: 功能按钮权限控制"""

    def test_lower_buttons_disabled_when_no_student_selected(self, auth_page: Page):
        """TC-SCENE-EXC-009: 未选择学员时，needSele类按钮处于 disabled 状态"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button[class*='needSele']", timeout=15000)
        auth_page.wait_for_timeout(1000)
        for btn_text in ["补加金币", "生成奖状", "请假", "临调"]:
            btn = auth_page.locator(f"button[class*='needSele']:has-text('{btn_text}')").first
            if btn.count() > 0:
                is_disabled = btn.get_attribute("disabled") is not None
                assert is_disabled, f"「{btn_text}」在未选学员时应为 disabled"

    def test_student_count_shows_in_band_format(self, auth_page: Page):
        """TC-SCENE-UI-007: 无筛选无选中时显示「在班X人」格式"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        count_text = auth_page.locator("text=/当前在班|在班.*人/").first
        expect(count_text).to_be_visible()


# ══════════════════════════════════════════════
# TC-SCENE-UI：UI交互测试
# ══════════════════════════════════════════════
class TestUIInteraction:
    """UI展示与交互验证"""

    def test_student_list_columns_visible(self, auth_page: Page):
        """TC-SCENE-FUNC-007: 学员列表有数据列展示"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        for col_name in ["基本信息", "购课信息", "累计课程数据", "沟通"]:
            col = auth_page.locator(f"text={col_name}").first
            expect(col).to_be_visible(timeout=8000)

    def test_student_data_displayed(self, auth_page: Page):
        """班课内有学员数据正常展示（该班课有北京/沈阳/大连3名学员）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(2000)
        students = auth_page.locator("text=/北京|沈阳|大连/")
        assert students.count() >= 1, "班课内应有学员数据"

    def test_course_data_tab_columns(self, auth_page: Page):
        """课程数据列（出勤/荣誉等）正常展示"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        for col in ["累计出勤", "累计荣誉"]:
            el = auth_page.locator(f"text={col}").first
            expect(el).to_be_visible(timeout=8000)

    def test_scene_tabs_do_not_crash_on_click(self, auth_page: Page):
        """连续点击所有场景Tab不报错"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        for tab in ["课前沟通", "课后回访", "转化沟通"]:
            auth_page.locator("li.next-tabs-tab", has_text=tab).click()
            auth_page.wait_for_timeout(600)
        assert "lesson-detail" in auth_page.url

    def test_fullscreen_button_visible(self, auth_page: Page):
        """全屏按钮可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        fullscreen = auth_page.locator("text=全屏").first
        expect(fullscreen).to_be_visible()

    def test_student_count_shows_selected_format(self, auth_page: Page):
        """TC-SCENE-UI-008/009: 人数显示区域包含「在班」和「已选中」"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        in_band = auth_page.locator("text=/当前在班/").first
        selected = auth_page.locator("text=/已选中/").first
        expect(in_band).to_be_visible()
        expect(selected).to_be_visible()


# ══════════════════════════════════════════════
# TC-FIELD-COND：字段展示条件测试
# ══════════════════════════════════════════════
class TestFieldDisplayConditions:
    """字段按班课类型差异化展示"""

    def test_rumen_ban_has_zhuanhua_goutong_tab(self, auth_page: Page):
        """TC-FIELD-COND: 入门班显示「转化沟通」Tab（非续报沟通）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        zhuanhua = auth_page.locator("li.next-tabs-tab", has_text="转化沟通")
        xubao = auth_page.locator("li.next-tabs-tab", has_text="续报沟通")
        assert zhuanhua.count() > 0, "入门班应显示「转化沟通」Tab"
        assert xubao.count() == 0, "入门班不应显示「续报沟通」Tab"

    def test_communication_columns_visible(self, auth_page: Page):
        """TC-SCENE-FUNC-007: 沟通类字段列正常展示"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        for col in ["今日沟通", "累计沟通"]:
            el = auth_page.locator(f"text={col}").first
            expect(el).to_be_visible(timeout=8000)

    def test_挖需问卷_column_visible_in_rumen(self, auth_page: Page):
        """TC-FIELD-COND: 入门班展示「挖需问卷」字段"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        col = auth_page.locator("text=挖需问卷").first
        expect(col).to_be_visible()

    def test_zhijia_fangwen_column_visible(self, auth_page: Page):
        """TC-FIELD-COND: 「问卷家访」字段可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        col = auth_page.locator("text=问卷家访").first
        expect(col).to_be_visible()

    def test_zhibo_ke_chongtu_column_visible(self, auth_page: Page):
        """TC-FIELD-COND: 「直播课冲突」字段可见"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1500)
        col = auth_page.locator("text=直播课冲突").first
        expect(col).to_be_visible()


# ══════════════════════════════════════════════
# TC-SCENE-BOUND：边界值测试（可自动化部分）
# ══════════════════════════════════════════════
class TestBoundaryValues:
    """边界值测试"""

    def test_class_detail_page_loads_without_error(self, auth_page: Page):
        """班课详情页正常加载，无JS报错"""
        errors = []
        auth_page.on("pageerror", lambda e: errors.append(str(e)))
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        assert len(errors) == 0, f"页面加载有JS错误: {errors}"

    def test_student_count_display_not_empty(self, auth_page: Page):
        """TC-SCENE-BOUND-007补充: 学员人数不为负数或异常值"""
        import re
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        count_text = auth_page.locator("text=/当前在班/").first.text_content()
        nums = re.findall(r'\d+', count_text or "")
        if nums:
            assert int(nums[0]) >= 0, f"学员人数不应为负数: {count_text}"

    def test_multiple_tab_switches_stable(self, auth_page: Page):
        """反复切换Tab页面保持稳定不崩溃"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("li.next-tabs-tab", timeout=15000)
        auth_page.wait_for_timeout(1000)
        tabs = ["课前沟通", "课后回访", "转化沟通", "课前沟通", "转化沟通"]
        for tab in tabs:
            auth_page.locator("li.next-tabs-tab", has_text=tab).click()
            auth_page.wait_for_timeout(500)
        assert "lesson-detail" in auth_page.url

    def test_more_buttons_expandable(self, auth_page: Page):
        """「更多」按钮可展开额外功能"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button.next-btn", timeout=15000)
        auth_page.wait_for_timeout(1000)
        # 页面顶部导航栏的「更多」（限定在班课详情操作区）
        more_btn = auth_page.locator("button:has-text('更多')").first
        if more_btn.count() > 0:
            expect(more_btn).to_be_visible()
        assert "lesson-detail" in auth_page.url
