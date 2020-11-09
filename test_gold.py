import pytest
import gold
import xlrd


def test_current_date():
    date = gold.get_current_date()
    assert type(date) == str, "Current date is not a string"
    assert len(date) == len("DD.MM.YYYY"), "Current date has a wrong length"


def test_current_month():
    month = gold.get_current_month("07.11.2020")
    assert type(month) == int, "Current month is not an integer"
    assert 0 <= month <= 11, "Current month has an unreal number"


def test_current_year():
    year = gold.get_current_year("07.11.2020")
    assert type(year) == int, "Current year is not an integer"
    assert len(str(year)) == 4, "Current year is too short to be true"


def test_bank_url():
    month = 5
    year = 2020
    bank_url = gold.compile_bank_url(month, year)
    assert type(bank_url) == str, "Bank url is not a string"
    assert len(bank_url) > 110, "Bank url is too short"
    assert "sberbank" in bank_url, "Bank url content is wrong"
    

def test_check_web_page_is_available():
    month = 5
    year = 2020
    request_result = gold.request_price_files(month, year)
    assert request_result is not False, "Request is not successful"
    assert type(request_result) == bytes, "Type of requst result isn't bytes"


def test_check_xls_file_is_downloaded():
    month = 5
    year = 2020
    price_files = gold.request_price_files(month, year)
    min_contents_size = 3 # '[]' for empty response
    if len(price_files) < min_contents_size:
        while current_month > 0:
            current_month -= 1
            price_files = gold.request_price_files(month, year)
            if len(price_files) > min_contents_size:
                break
    file_with_prices = gold.download_gold_bar_prices(price_files)
    assert file_with_prices is not False, "File was not downloaded"


def test_received_price():
    month = 5
    year = 2020
    price_files = gold.request_price_files(month, year)
    min_contents_size = 3 # '[]' for empty response
    if len(price_files) < min_contents_size:
        while current_month > 0:
            current_month -= 1
            price_files = gold.request_price_files(month, year)
            if len(price_files) > min_contents_size:
                break
    file_content = gold.download_gold_bar_prices(price_files)
    xls_file_name = 'test_gold.xls'
    open(xls_file_name, 'wb').write(file_content)
    gold_bar_price = gold.gold_bar_price_from_xls(xls_file_name)
    assert type(gold_bar_price) == int, "Gold bar price is not an integer"
    assert gold_bar_price > 0, "Gold bar price is negative"

    book = xlrd.open_workbook('test_gold.xls', encoding_override="cp1252")
    sheet = book.sheet_by_index(0)
    bar_material = sheet.cell_value(8, 0)
    assert bar_material.strip() == "Золото", "The price is not for a gold bar"
    bar_weight = sheet.cell_value(11, 0)
    assert int(bar_weight) == 10, "The price weight is wrong"


test_current_date()
test_current_month()
test_current_year()
test_bank_url()
test_check_web_page_is_available()
test_check_xls_file_is_downloaded()
test_received_price()