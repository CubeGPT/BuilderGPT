import re, time
import config
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(config.RENDERING_URL)

    time.sleep(10)

    page.get_by_text("File").click()
    with page.expect_file_chooser() as fc_info:
        page.locator("[id=\"\\31 2\"]").click()
        file_chooser = fc_info.value
        file_chooser.set_files("temp/waiting_for_upload.schem")
    page.get_by_text("File", exact=True).click()
    page.locator("[id=\"\\32 3\"] > div:nth-child(3)").click()
    with page.expect_download() as download_info:
        page.locator("[id=\"\\31 8\"]").click()

    download = download_info.value
    download.save_as("temp/screenshot.png")
    page.close()

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
