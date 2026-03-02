"""
运行此脚本保存登录会话：
    python save_session.py

会打开浏览器，点击'一键登录'后自动保存 Cookie，
后续自动化测试直接复用，无需每次重新登录。
"""
from playwright.sync_api import sync_playwright
import json, pathlib

SESSION_FILE = pathlib.Path("session_state.json")
LOGIN_URL    = "https://qwerty-test.zhenguanyu.com"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page    = context.new_page()

        page.goto(LOGIN_URL)
        page.wait_for_load_state("networkidle")

        print("请在浏览器中点击【一键登录】按钮...")
        # 等待跳转到 dashboard（最多 60 秒）
        page.wait_for_url("**/dashboard**", timeout=60_000)
        page.wait_for_load_state("networkidle")

        # 保存完整会话状态（cookies + localStorage）
        context.storage_state(path=str(SESSION_FILE))
        print(f"✅ 会话已保存到 {SESSION_FILE}")

        browser.close()

if __name__ == "__main__":
    main()
