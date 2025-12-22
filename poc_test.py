from playwright.sync_api import sync_playwright
import re

def fetch_ffxiv_final_version():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. 列表頁抓取
        list_url = "https://www.ffxiv.com.tw/web/news/news_list.aspx?category=3"
        page.goto(list_url)

        page.wait_for_selector(".news_list .item")
        first_item = page.query_selector(".news_list .item")
        detail_link = "https://www.ffxiv.com.tw" + first_item.query_selector(".title a").get_attribute("href")

        # 2. 進入詳情頁
        page.goto(detail_link)

        try:
            # 根據你的反饋，這裡必須使用類別選擇器 .article
            page.wait_for_selector(".article", timeout=10000)

            # 抓取標題 (.news_title)
            title_el = page.query_selector(".news_title")
            title_text = title_el.inner_text().strip() if title_el else "未找到標題"

            # 抓取重點內文 (類別 .article)
            article_el = page.query_selector(".article")
            article_text = article_el.inner_text().strip() if article_el else "未找到內容"

            # 清理過多換行，讓輸出整潔
            cleaned_article = re.sub(r'\n\s*\n', '\n', article_text)

            print(f"【公告標題】: {title_text}")
            print("-" * 60)
            print(f"【重點內文】:\n{cleaned_article}")
            print("-" * 60)

        except Exception as e:
            print(f"抓取失敗，請確認頁面是否包含 .article 類別: {e}")

        browser.close()

if __name__ == "__main__":
    fetch_ffxiv_final_version()