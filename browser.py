import time
import config
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright, progress_bar: str=None) -> None:
    def set_progress(progress):
        if progress_bar is not None:
            progress_bar.set(progress)

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(config.RENDERING_URL)

    set_progress(40)

    for i in range(10):
        time.sleep(1)
        set_progress(40 + i)

    page.get_by_text("File").click()
    set_progress(55)

    with page.expect_file_chooser() as fc_info:
        page.locator("[id=\"\\31 2\"]").click()
        file_chooser = fc_info.value
        file_chooser.set_files("temp/waiting_for_upload.schem")
    page.get_by_text("File", exact=True).click()
    set_progress(60)

    page.locator("[id=\"\\32 3\"] > div:nth-child(3)").click()
    with page.expect_download() as download_info:
        page.locator("[id=\"\\31 8\"]").click()

    set_progress(70)

    download = download_info.value
    download.save_as("temp/screenshot.png")
    page.close()

    context.close()
    browser.close()

    set_progress(90)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
