import asyncio
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import getUrls
import getData
from playwright.async_api import async_playwright
from SQLMangment import create_database, add_record,delete_record



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_links(url):
    async def main():
        async with async_playwright() as playwright:
            return await getUrls.run(playwright, url)

    return asyncio.run(main())

def fetch_data(url):
    async def main():
        async with async_playwright() as playwright:
            return await getData.run(playwright, url)

    data = asyncio.run(main())
    if data["قیمت پایه"] is not None:
        add_record(db_name="divar", table_name=table_name,
               brand_type=data["برند و تیپ"], fuel_type=data["نوع سوخت"],
               engine_status=data["وضعیت موتور"], front_chassis=data["شاسی جلو"],
               rear_chassis=data["شاسی عقب"], body_status=data["وضعیت بدنه"],
               insurance_deadline=data["مهلت بیمهٔ شخص ثالث"], gearbox=data["گیربکس"],
               base_price=data["قیمت پایه"], mileage=data["کارکرد"],
               model_year=data["مدل (سال تولید)"], color=data["رنگ"],
               location=data["مکان"], url=url)


if __name__ == "__main__":
    user_input = input("Have you already received the required data ?(Y/N) : ").capitalize()
    if user_input == "N":
        try:
            thread_number = int(input("Enter the number of program threads : "))
        except ValueError as e:
            logging.error(f"Invalid input for thread number: {e}")
            exit(1)

        try:
            with open("carurls.txt", "r") as f:
                for url in f:
                    try:
                        url = url.strip()
                        if not url:
                            continue
                        urlList = fetch_links(url)
                        table_name = url.split("https://divar.ir/s/iran/car/")[1]
                        create_database("divar", table_name)

                        with ThreadPoolExecutor(max_workers=thread_number) as executor:
                            for url_item in urlList:
                                executor.submit(fetch_data, "https://divar.ir" + url_item["href"])

                    except Exception as e:
                        logging.error(f"Error processing URL {url}: {e}")
        except FileNotFoundError as e:
            logging.error(f"File 'carurls.txt' not found: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
    else:
        try:
            delete_record("divar", "")
        except Exception as e:
            logging.error(f"Error deleting record: {e}")