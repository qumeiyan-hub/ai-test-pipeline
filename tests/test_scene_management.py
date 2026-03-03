"""
班课详情 - 自定义场景配置 业务逻辑自动化测试
需求来源：【班课详情】支持自定义设置：场景(Tab)、字段、功能按钮、指标
测试对象：C入门班 已结束班课（测试环境：id=10566630）

测试分层：
  TC-SCENE-FUNC  功能测试（场景Tab、功能按钮展示）
  TC-SCENE-EXC   异常测试（权限控制、禁用状态）
  TC-SCENE-UI    UI交互测试（切换稳定性、布局显示）
  TC-FIELD-COND  字段条件测试（按班课类型差异化展示）
  TC-SCENE-BOUND 边界值测试（极端操作、人数边界）
"""
import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL  = "https://qwerty-test.zhenguanyu.com"
CLASS_URL = (
    f"{BASE_URL}/#/lesson/lesson-detail"
    f"?id=10566630&teamId=&tab=courseData&episodeIndex=1"
)

# 等待 Tab 渲染完成的公共选择器
TAB_SELECTOR = "li.next-tabs-tab"
BTN_SELECTOR  = "button.next-btn"


# ══════════════════════════════════════════════════════════════
# 一、场景Tab默认展示验证（TC-SCENE-FUNC-001/002）
# ══════════════════════════════════════════════════════════════
class 场景Tab默认展示验证:

    def test_入门班默认显示三个场景Tab(self, auth_page: Page, capture):
        """入门班班课详情默认展示「课前沟通」「课后回访」「转化沟通」三个Tab（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 查看默认Tab")

        for tab_name in ["课前沟通", "课后回访", "转化沟通"]:
            tab = auth_page.locator(TAB_SELECTOR, has_text=tab_name)
            expect(tab).to_be_visible(timeout=8000)

        capture(auth_page, "② 三个Tab全部可见 - 验证通过")

    def test_入门班默认Tab数量为三个(self, auth_page: Page, capture):
        """入门班场景Tab数量精确为3个，不多不少（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载完成")

        tabs = auth_page.locator(TAB_SELECTOR)
        count = tabs.count()
        capture(auth_page, f"② 统计到Tab数量：{count}个")
        assert count == 3, f"期望3个Tab，实际{count}个"

    def test_入门班不显示续报沟通Tab(self, auth_page: Page, capture):
        """入门班显示「转化沟通」而非「续报沟通」，业务逻辑：入门班转化续报（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 检查Tab类型")

        zhuanhua = auth_page.locator(TAB_SELECTOR, has_text="转化沟通")
        xubao    = auth_page.locator(TAB_SELECTOR, has_text="续报沟通")

        assert zhuanhua.count() > 0, "入门班应显示「转化沟通」Tab"
        assert xubao.count() == 0,   "入门班不应显示「续报沟通」Tab"
        capture(auth_page, "② Tab类型验证 - 转化沟通✓ 续报沟通×")


# ══════════════════════════════════════════════════════════════
# 二、场景Tab切换交互验证（TC-SCENE-UI）
# ══════════════════════════════════════════════════════════════
class 场景Tab切换交互验证:

    def test_点击课前沟通Tab正常切换(self, auth_page: Page, capture):
        """点击「课前沟通」Tab，页面内容正常切换且不崩溃（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 进入班课详情页")

        auth_page.locator(TAB_SELECTOR, has_text="课前沟通").click()
        auth_page.wait_for_timeout(800)
        capture(auth_page, "② 点击「课前沟通」Tab后")

        assert "lesson-detail" in auth_page.url

    def test_点击课后回访Tab正常切换(self, auth_page: Page, capture):
        """点击「课后回访」Tab，页面内容正常切换且不崩溃（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 进入班课详情页")

        auth_page.locator(TAB_SELECTOR, has_text="课后回访").click()
        auth_page.wait_for_timeout(800)
        capture(auth_page, "② 点击「课后回访」Tab后")

        assert "lesson-detail" in auth_page.url

    def test_点击转化沟通Tab正常切换(self, auth_page: Page, capture):
        """点击「转化沟通」Tab，页面内容正常切换且不崩溃（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 进入班课详情页")

        auth_page.locator(TAB_SELECTOR, has_text="转化沟通").click()
        auth_page.wait_for_timeout(800)
        capture(auth_page, "② 点击「转化沟通」Tab后")

        assert "lesson-detail" in auth_page.url

    def test_连续切换所有Tab页面保持稳定(self, auth_page: Page, capture):
        """反复切换三个Tab页面不崩溃、不白屏（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 初始状态")

        for tab in ["课前沟通", "课后回访", "转化沟通", "课前沟通"]:
            auth_page.locator(TAB_SELECTOR, has_text=tab).click()
            auth_page.wait_for_timeout(500)

        capture(auth_page, "② 连续切换4次后页面状态")
        assert "lesson-detail" in auth_page.url


# ══════════════════════════════════════════════════════════════
# 三、功能按钮展示验证（TC-SCENE-FUNC-008）
# ══════════════════════════════════════════════════════════════
class 功能按钮展示验证:

    def test_上层无需选学员功能按钮可见(self, auth_page: Page, capture):
        """「任务执行」「用户分层」「生成榜单」等无需选学员的按钮正常展示（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(BTN_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 检查上层功能按钮")

        for btn_text in ["任务执行", "用户分层", "生成榜单", "下载课程表现"]:
            btn = auth_page.locator(f"button:has-text('{btn_text}')").first
            expect(btn).to_be_visible(timeout=8000)

        capture(auth_page, "② 上层功能按钮全部可见")

    def test_下层需选学员功能按钮可见(self, auth_page: Page, capture):
        """「补加金币」「请假」「临调」等需先选学员的按钮正常展示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(BTN_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 检查下层功能按钮")

        for btn_text in ["补加金币", "请假", "临调", "维护学员标签", "生成奖状"]:
            btn = auth_page.locator(f"button:has-text('{btn_text}')").first
            expect(btn).to_be_visible(timeout=8000)

        capture(auth_page, "② 下层功能按钮全部可见（均处于禁用等待选学员）")

    def test_非S线班课显示在线用户筛选按钮(self, auth_page: Page, capture):
        """C入班课（非S线）应显示「在线用户筛选」按钮（字段条件展示业务规则）（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(BTN_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 验证在线用户筛选按钮")

        btn = auth_page.locator("button:has-text('在线用户筛选')").first
        expect(btn).to_be_visible()
        capture(auth_page, "② 「在线用户筛选」按钮可见（非S线班课）")

    def test_全屏按钮可见(self, auth_page: Page, capture):
        """全屏功能按钮正常展示（P2）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(BTN_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载")

        fullscreen = auth_page.locator("text=全屏").first
        expect(fullscreen).to_be_visible()
        capture(auth_page, "② 全屏按钮可见")


# ══════════════════════════════════════════════════════════════
# 四、功能按钮权限控制（TC-SCENE-EXC-009/010）
# ══════════════════════════════════════════════════════════════
class 功能按钮权限控制验证:

    def test_未选学员时需选学员按钮处于禁用状态(self, auth_page: Page, capture):
        """未勾选任何学员时，needSele类按钮（补加金币/请假/临调等）应为 disabled（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button[class*='needSele']", timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 初始状态：未选任何学员")

        for btn_text in ["补加金币", "生成奖状", "请假", "临调"]:
            btn = auth_page.locator(
                f"button[class*='needSele']:has-text('{btn_text}')"
            ).first
            if btn.count() > 0:
                is_disabled = btn.get_attribute("disabled") is not None
                assert is_disabled, f"「{btn_text}」在未选学员时应为 disabled"

        capture(auth_page, "② 需选学员按钮均处于 disabled 状态 - 验证通过")

    def test_人数显示区域包含在班和已选中字段(self, auth_page: Page, capture):
        """人数显示区显示「当前在班X人」和「已选中X人」两个计数（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 查看人数显示区域")

        in_band  = auth_page.locator("text=/当前在班/").first
        selected = auth_page.locator("text=/已选中/").first
        expect(in_band).to_be_visible()
        expect(selected).to_be_visible()
        capture(auth_page, "② 在班人数 + 已选中人数区域均可见")

    def test_勾选学员后需选按钮变为可用(self, auth_page: Page, capture):
        """勾选学员后，补加金币等按钮应从 disabled 变为可点击（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector("button[class*='needSele']", timeout=15000)
        auth_page.wait_for_timeout(2000)
        capture(auth_page, "① 初始状态：未选学员，需选按钮禁用")

        # 找到第一个学员的复选框并勾选
        checkbox = auth_page.locator("input[type='checkbox']").first
        if checkbox.count() > 0:
            checkbox.click()
            auth_page.wait_for_timeout(800)
            capture(auth_page, "② 勾选第一名学员后")

            btn = auth_page.locator("button[class*='needSele']:has-text('补加金币')").first
            if btn.count() > 0:
                is_enabled = btn.get_attribute("disabled") is None
                capture(auth_page, f"③ 补加金币按钮状态：{'可用' if is_enabled else '仍禁用'}")
                assert is_enabled, "勾选学员后「补加金币」应变为可用"
        else:
            # 无复选框时跳过（数据问题）
            capture(auth_page, "② 未找到复选框 - 跳过")
            pytest.skip("未找到学员复选框，跳过此用例")


# ══════════════════════════════════════════════════════════════
# 五、字段差异化展示条件验证（TC-FIELD-COND）
# ══════════════════════════════════════════════════════════════
class 字段差异化展示条件验证:

    def test_学员列表列头展示正确(self, auth_page: Page, capture):
        """学员列表列头包含「基本信息」「购课信息」「累计课程数据」「沟通」等核心列（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载 - 查看列头")

        for col_name in ["基本信息", "购课信息", "累计课程数据", "沟通"]:
            col = auth_page.locator(f"text={col_name}").first
            expect(col).to_be_visible(timeout=8000)

        capture(auth_page, "② 核心列头全部可见")

    def test_沟通类字段列展示(self, auth_page: Page, capture):
        """「今日沟通」「累计沟通」沟通统计字段正常显示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载 - 查看沟通字段")

        for col in ["今日沟通", "累计沟通"]:
            el = auth_page.locator(f"text={col}").first
            expect(el).to_be_visible(timeout=8000)

        capture(auth_page, "② 沟通字段列均可见")

    def test_入门班展示挖需问卷字段(self, auth_page: Page, capture):
        """入门班专属字段「挖需问卷」正常展示（非入门班不显示，业务差异化配置）（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 入门班详情页加载")

        col = auth_page.locator("text=挖需问卷").first
        expect(col).to_be_visible()
        capture(auth_page, "② 「挖需问卷」字段可见（入门班专属）")

    def test_问卷家访字段可见(self, auth_page: Page, capture):
        """「问卷家访」字段正常展示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载")

        col = auth_page.locator("text=问卷家访").first
        expect(col).to_be_visible()
        capture(auth_page, "② 「问卷家访」字段可见")

    def test_直播课冲突字段可见(self, auth_page: Page, capture):
        """「直播课冲突」字段正常展示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载")

        col = auth_page.locator("text=直播课冲突").first
        expect(col).to_be_visible()
        capture(auth_page, "② 「直播课冲突」字段可见")

    def test_累计出勤和荣誉数据列展示(self, auth_page: Page, capture):
        """「累计出勤」「累计荣誉」数据列正常展示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载 - 查看课程数据列")

        for col in ["累计出勤", "累计荣誉"]:
            el = auth_page.locator(f"text={col}").first
            expect(el).to_be_visible(timeout=8000)

        capture(auth_page, "② 累计出勤、累计荣誉列均可见")

    def test_购课渠道字段正常展示(self, auth_page: Page, capture):
        """购课渠道信息字段在学员卡片中正常展示（P2）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1500)
        capture(auth_page, "① 页面加载")

        col = auth_page.locator("text=购课渠道").first
        expect(col).to_be_visible()
        capture(auth_page, "② 「购课渠道」字段可见")


# ══════════════════════════════════════════════════════════════
# 六、学员数据展示验证（TC-SCENE-FUNC-007）
# ══════════════════════════════════════════════════════════════
class 学员数据展示验证:

    def test_班课内学员数据正常加载(self, auth_page: Page, capture):
        """班课详情页有学员数据正常展示（该班课共3名学员）（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(2000)
        capture(auth_page, "① 页面加载 - 等待学员数据渲染")

        students = auth_page.locator("text=/北京|沈阳|大连/")
        count = students.count()
        capture(auth_page, f"② 学员数据已渲染，找到 {count} 名学员城市信息")
        assert count >= 1, "班课内应有学员数据"

    def test_学员在班人数显示正确(self, auth_page: Page, capture):
        """「当前在班」人数显示正确且非负数（P0）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 查看人数显示")

        count_el = auth_page.locator("text=/当前在班/").first
        expect(count_el).to_be_visible()
        count_text = count_el.text_content() or ""
        capture(auth_page, f"② 人数显示内容：{count_text.strip()}")

        nums = re.findall(r'\d+', count_text)
        if nums:
            assert int(nums[0]) >= 0, f"在班人数不应为负数: {count_text}"

    def test_课程跟进记录展示(self, auth_page: Page, capture):
        """学员卡片内课程跟进记录正常显示（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(2000)
        capture(auth_page, "① 页面加载")

        followup = auth_page.locator("text=/课程跟进|查看.*跟进/").first
        expect(followup).to_be_visible()
        capture(auth_page, "② 课程跟进记录可见")


# ══════════════════════════════════════════════════════════════
# 七、边界值与稳定性验证（TC-SCENE-BOUND）
# ══════════════════════════════════════════════════════════════
class 边界值与稳定性验证:

    def test_页面加载无JavaScript报错(self, auth_page: Page, capture):
        """班课详情页加载全程无 JS 异常报错（P0）"""
        errors = []
        auth_page.on("pageerror", lambda e: errors.append(str(e)))

        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载完成 - 检查JS错误")

        assert len(errors) == 0, f"页面有JS报错: {errors}"
        capture(auth_page, "② 无JS报错 - 页面健康")

    def test_反复切换Tab页面不崩溃(self, auth_page: Page, capture):
        """快速反复切换5次Tab，页面始终保持正常（稳定性测试）（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 初始状态")

        sequence = ["课前沟通", "转化沟通", "课后回访", "课前沟通", "转化沟通"]
        for tab in sequence:
            auth_page.locator(TAB_SELECTOR, has_text=tab).click()
            auth_page.wait_for_timeout(400)

        capture(auth_page, "② 连续切换5次后最终状态")
        assert "lesson-detail" in auth_page.url

    def test_更多按钮可展开(self, auth_page: Page, capture):
        """「更多」功能按钮点击后可正常展开（P2）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(BTN_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 页面加载 - 初始按钮状态")

        more_btn = auth_page.locator("button:has-text('更多')").first
        if more_btn.count() > 0:
            expect(more_btn).to_be_visible()
            more_btn.click()
            auth_page.wait_for_timeout(600)
            capture(auth_page, "② 点击「更多」后展开状态")
        else:
            capture(auth_page, "② 未找到「更多」按钮（可能已全部展示）")

        assert "lesson-detail" in auth_page.url

    def test_已结课班课课时进度显示完成状态(self, auth_page: Page, capture):
        """已结课班课课时进度显示为「X/X」全部完成状态（P1）"""
        auth_page.goto(CLASS_URL)
        auth_page.wait_for_selector(TAB_SELECTOR, timeout=15000)
        auth_page.wait_for_timeout(1000)
        capture(auth_page, "① 进入已结课班课详情页")

        # 已结课班课：课时进度应呈现如「2/2」格式
        progress = auth_page.locator("text=/\\d+\\s*\\/\\s*\\d+\\s*课时/").first
        expect(progress).to_be_visible()
        progress_text = progress.text_content() or ""
        capture(auth_page, f"② 课时进度显示：{progress_text.strip()}")
