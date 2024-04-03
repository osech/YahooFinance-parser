import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def get_tickers_list():
    try:
        print('Tickers collecting', '\n', 'Processing..')
        driver.set_window_size(1920, 1080)
        url = 'https://finance.yahoo.com/most-active/?offset=0&count=100'

        driver.get(url=url)

        driver.find_element(By.XPATH, '//*[@id="screener-criteria"]/div[2]/div[1]/div/button[1]').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/div/div').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/ul/li[9]/label/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/ul/li[20]/label/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/ul/li[28]/label/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/ul/li[29]/label/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/ul/li[52]/label/input').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="dropdown-menu"]/button').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]').click()
        time.sleep(0.5)

        tickers_count = int(
            driver.find_element(By.XPATH, '//*[@id="screener-criteria"]/div[2]/div[1]/div[2]/div/div[2]/div').text)

        tickers = driver.find_elements(By.CSS_SELECTOR, '[data-test="quoteLink"]')
        tickers_list = []
        for ticker in tickers:
            tickers_list.append(ticker.text)

        while len(tickers_list) < tickers_count:
            driver.find_element(By.XPATH, '//*[@id="scr-res-table"]/div[2]/button[3]').click()
            time.sleep(1)
            tickers = driver.find_elements(By.CSS_SELECTOR, '[data-test="quoteLink"]')
            for ticker in tickers:
                tickers_list.append(ticker.text)
            print(f'Processing({len(tickers_list)}/{tickers_count})..')

        with open('tickers.txt', 'w') as file:
            for ticker in tickers_list:
                file.write(f'{ticker}\n')

        print('Tickers collected successfully!')

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def get_data():
    tickers_list = []
    with open('tickers.txt', 'r') as file:
        for line in file:
            tickers_list.append(line.strip())

    data = {}

    try:
        # tickers_list = ['000100.S4Z', '000725.SZ', '513180.SS', '002340.SZ']
        k = 1
        print('Parsing processing..')
        driver.set_window_size(1920, 1080)

        for ticker in tickers_list:
            try:

                driver.get(url=f'https://finance.yahoo.com/quote/{ticker}')

                data[f'{ticker}'] = {}
                data[f'{ticker}']['name'] = driver.find_element(By.TAG_NAME, 'h1').text

                data[f'{ticker}']['Previous Close'] = driver.find_element(
                    By.XPATH, '//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]').text

                driver.get(url=f'https://finance.yahoo.com/quote/{ticker}/key-statistics')
                data[f'{ticker}']['Price/Book (mrq)'] = driver.find_element(
                    By.XPATH, '//*[@id="Col1-0-KeyStatistics-Proxy"]/section/div[2]/div[1]/div/div/div/div/table/tbody/tr[7]/td[2]').text

                driver.get(url=f'https://finance.yahoo.com/quote/{ticker}/financials')
                breakdown_list = driver.find_elements(By.CSS_SELECTOR, '[data-test="fin-row"]')

                if not breakdown_list:
                    data[f'{ticker}']['Total Revenue 2022'] = 'N/A'
                    data[f'{ticker}']['Total Revenue 2021'] = 'N/A'
                    data[f'{ticker}']['Total Revenue 2020'] = 'N/A'
                    data[f'{ticker}']['Research & Development 2022'] = 'N/A'
                    data[f'{ticker}']['Research & Development 2021'] = 'N/A'
                    data[f'{ticker}']['Research & Development 2020'] = 'N/A'
                    data[f'{ticker}']['EBITDA 2022'] = 'N/A'
                    data[f'{ticker}']['EBITDA 2021'] = 'N/A'
                    data[f'{ticker}']['EBITDA 2020'] = 'N/A'
                    data[f'{ticker}']['Total Assets 2022'] = 'N/A'
                    data[f'{ticker}']['Total Assets 2021'] = 'N/A'
                    data[f'{ticker}']['Total Assets 2020'] = 'N/A'
                    data[f'{ticker}']['Current Assets 2022'] = 'N/A'
                    data[f'{ticker}']['Current Assets 2021'] = 'N/A'
                    data[f'{ticker}']['Current Assets 2020'] = 'N/A'
                    data[f'{ticker}']['Net PPE 2022'] = 'N/A'
                    data[f'{ticker}']['Net PPE 2021'] = 'N/A'
                    data[f'{ticker}']['Net PPE 2020'] = 'N/A'
                    data[f'{ticker}']['Total Liabilities Net Minority Interest 2022'] = 'N/A'
                    data[f'{ticker}']['Total Liabilities Net Minority Interest 2021'] = 'N/A'
                    data[f'{ticker}']['Total Liabilities Net Minority Interest 2020'] = 'N/A'
                    data[f'{ticker}']['Current Liabilities 2022'] = 'N/A'
                    data[f'{ticker}']['Current Liabilities 2021'] = 'N/A'
                    data[f'{ticker}']['Current Liabilities 2020'] = 'N/A'
                    data[f'{ticker}']['Total Capitalization 2022'] = 'N/A'
                    data[f'{ticker}']['Total Capitalization 2021'] = 'N/A'
                    data[f'{ticker}']['Total Capitalization 2020'] = 'N/A'
                    data[f'{ticker}']['Share Issued 2022'] = 'N/A'
                    data[f'{ticker}']['Share Issued 2021'] = 'N/A'
                    data[f'{ticker}']['Share Issued 2020'] = 'N/A'

                    continue

                data[f'{ticker}']['Total Revenue 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[3]').text
                data[f'{ticker}']['Total Revenue 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[4]').text
                data[f'{ticker}']['Total Revenue 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[5]').text

                driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[1]/div[1]/div[1]/button').click()
                data[f'{ticker}']['Research & Development 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div[1]/div[3]').text
                data[f'{ticker}']['Research & Development 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div[1]/div[4]').text
                data[f'{ticker}']['Research & Development 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[2]/div[2]/div[1]/div[5]').text

                if len(breakdown_list) < 31:
                    data[f'{ticker}']['EBITDA 2022'] =driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[22]/div[1]/div[3]').text
                    data[f'{ticker}']['EBITDA 2021'] = driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[22]/div[1]/div[4]').text
                    data[f'{ticker}']['EBITDA 2020'] = driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[22]/div[1]/div[5]').text
                else:
                    data[f'{ticker}']['EBITDA 2022'] = driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[23]/div[1]/div[3]').text
                    data[f'{ticker}']['EBITDA 2021'] = driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[23]/div[1]/div[4]').text
                    data[f'{ticker}']['EBITDA 2020'] = driver.find_element(
                        By.XPATH,
                        '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[23]/div[1]/div[5]').text

                driver.get(url=f'https://finance.yahoo.com/quote/{ticker}/balance-sheet')

                data[f'{ticker}']['Total Assets 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[2]').text
                data[f'{ticker}']['Total Assets 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[3]').text
                data[f'{ticker}']['Total Assets 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[4]').text

                driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/button').click()

                data[f'{ticker}']['Current Assets 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]').text
                data[f'{ticker}']['Current Assets 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]').text
                data[f'{ticker}']['Current Assets 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[4]').text

                driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button').click()

                data[f'{ticker}']['Net PPE 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]').text
                data[f'{ticker}']['Net PPE 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]').text
                data[f'{ticker}']['Net PPE 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[4]').text

                data[f'{ticker}']['Total Liabilities Net Minority Interest 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]').text
                data[f'{ticker}']['Total Liabilities Net Minority Interest 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[3]').text
                data[f'{ticker}']['Total Liabilities Net Minority Interest 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[4]').text

                driver.find_element(By.XPATH, '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/button').click()

                data[f'{ticker}']['Current Liabilities 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]').text
                data[f'{ticker}']['Current Liabilities 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]').text
                data[f'{ticker}']['Current Liabilities 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[4]').text

                data[f'{ticker}']['Total Capitalization 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[1]/div[2]').text
                data[f'{ticker}']['Total Capitalization 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[1]/div[3]').text
                data[f'{ticker}']['Total Capitalization 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[4]/div[1]/div[4]').text

                data[f'{ticker}']['Share Issued 2022'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[13]/div[1]/div[2]').text
                data[f'{ticker}']['Share Issued 2021'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[13]/div[1]/div[3]').text
                data[f'{ticker}']['Share Issued 2020'] = driver.find_element(
                    By.XPATH,
                    '//*[@id="Col1-1-Financials-Proxy"]/section/div[3]/div[1]/div/div[2]/div[13]/div[1]/div[4]').text

            except Exception as ex:
                print(ex)
            finally:
                print(f'{k}/{len(tickers_list)}')
                k += 1
                continue

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=3)

        print('Complete!!!')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


# get_tickers_list()
get_data()
