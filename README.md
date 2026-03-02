# AI 辅助自动化测试流水线

针对 https://qwerty-test.zhenguanyu.com 的自动化测试项目

## 项目结构

```
ai-test-pipeline/
├── tests/
│   ├── conftest.py          # 全局配置和 Fixture
│   └── test_login_page.py   # 登录页测试用例
├── reports/                 # 测试报告（本地运行后生成）
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions CI/CD 配置
├── requirements.txt         # Python 依赖
├── pytest.ini              # pytest 配置
└── README.md
```

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 安装浏览器
playwright install chromium

# 3. 运行测试
pytest

# 4. 查看报告
open reports/report.html
```

## 测试用例覆盖

| 模块 | 用例数 | 说明 |
|------|--------|------|
| 页面加载 | 3 | 标题、状态码、表单可见性 |
| Tab 切换 | 3 | 内部登录、短信登录、验证码 |
| 表单校验 | 3 | 空提交、错误账号、验证码刷新 |
| UI 完整性 | 4 | 忘记密码、飞连登录、备案号、移动端 |

## CI/CD 触发条件

- 推送到 main / develop 分支时自动触发
- 提交 PR 到 main 时自动触发
- 每天北京时间 09:00 定时触发
- 支持手动在 GitHub Actions 页面触发
