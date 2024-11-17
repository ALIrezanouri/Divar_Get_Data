import asyncio
import logging
from playwright.async_api import Playwright, async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run(playwright: Playwright, url) -> list:
    try:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(4000)
        all_links = []

        while True:
            try:
                # Scroll to the bottom of the page
                await page.evaluate('window.scrollBy(0, window.innerHeight);')
                await page.wait_for_timeout(5)  # Small delay to allow content to load

                # Extract links
                links = await page.query_selector_all('a')
                for link in links:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    if href and href.startswith('/v/') and {'href': href, 'text': text} not in all_links:
                        all_links.append({'href': href, 'text': text})

                # Check for "آگهی‌های بیشتر" button
                more_ads_button = await page.query_selector('button:has-text("آگهی‌های بیشتر")')
                if more_ads_button:
                    await more_ads_button.click()
                    await page.wait_for_timeout(4000)
                    continue

                # Check for "تلاش دوباره" button
                retry_button = await page.query_selector('button:has-text("تلاش دوباره")')
                if retry_button:
                    await retry_button.click()
                    await page.wait_for_timeout(4000)
                    continue

                # Check if we are at the bottom of the page
                is_bottom = await page.evaluate('window.scrollY + window.innerHeight >= document.documentElement.scrollHeight')
                if is_bottom:
                    break

            except Exception as e:
                logging.error(f"Error during page interaction: {e}")

        await context.close()
        await browser.close()
        return all_links

    except Exception as e:
        logging.error(f"Failed to run Playwright: {e}")
