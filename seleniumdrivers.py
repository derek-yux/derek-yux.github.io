import datetime
today = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S').split(" ")[0])
from newspaper import Article
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

def newspaper_text_extraction(article_url):
    article = Article(article_url)
    article.download()
    article.parse()
    return article.text


def get_prompt() -> str:
    """"""
    PATH = "/Users/derek/Code/ML/derek-yux.github.io/chromedriver"
    cService = webdriver.ChromeService(executable_path=PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get("https://trends.google.com/trending?geo=US&sort=search-volume")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mZ3RIc"))
    )

    trend = driver.find_element(By.CLASS_NAME, "mZ3RIc").get_attribute("innerText")
    driver.quit()
    return trend


def get_images(topic: str) -> list:
    """"""
    PATH = "/Users/derek/Code/ML/derek-yux.github.io/chromedriver"
    cService = webdriver.ChromeService(executable_path=PATH)
    driver = webdriver.Chrome(service=cService)
    url_p1 = "https://www.google.com/search?sca_esv=cd731438e95bc999&sxsrf=AHTn8zrMi6atrpzMrtDb1K9DOEKL0MQCVQ:1743542414604&q="
    url_p1 += topic.replace(" ", "+")
    if url_p1.endswith("+"):
        url_p1 = url_p1[:len(url_p1) - 1]
    url_p1 += "&udm=2&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpmDtIGL1r84kuKz6yAcD_igefx-eKq1gCPHF3zhthFol4Ng0BskIHiWtseitnxRUsdhuojFXPgEoHpG0GIfMKVPk2BkHblkxSI-tfKD1XmeeaqS5FHtrr8wsFXMuCe4QoMNCRPqH1YGzoZ9-eFehql3ssOZfjNPT2O6Pssj429Q7oCx7XuiHvC1mkqPCqfpKED5Tzqw&sa=X&ved=2ahUKEwjWxJfS4beMAxWUrokEHS93ABAQtKgLegQIIxAB&biw=1512&bih=784&dpr=2"
    driver.get(url_p1)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mNsIhb"))
    )
    images = driver.find_element(By.CLASS_NAME, "mNsIhb")
    images.click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YsLeY"))
    )
    middle = driver.find_element(By.CLASS_NAME, "YsLeY")
    final = middle.find_element(By.TAG_NAME, "img")
    result = [str(final.get_attribute("src"))]


    url_p2 = "https://www.google.com/search?sca_esv=cd731438e95bc999&sxsrf=AHTn8zrMi6atrpzMrtDb1K9DOEKL0MQCVQ:1743542414604&q="
    url_p2 += topic.replace(" ", "+")
    if url_p2.endswith("+"):
        url_p2 = url_p2[:len(url_p2) - 1]
    url_p2 += "+best+picture"
    url_p2 += "&udm=2&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpmDtIGL1r84kuKz6yAcD_igefx-eKq1gCPHF3zhthFol4Ng0BskIHiWtseitnxRUsdhuojFXPgEoHpG0GIfMKVPk2BkHblkxSI-tfKD1XmeeaqS5FHtrr8wsFXMuCe4QoMNCRPqH1YGzoZ9-eFehql3ssOZfjNPT2O6Pssj429Q7oCx7XuiHvC1mkqPCqfpKED5Tzqw&sa=X&ved=2ahUKEwjWxJfS4beMAxWUrokEHS93ABAQtKgLegQIIxAB&biw=1512&bih=784&dpr=2"
    driver.get(url_p2)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mNsIhb"))
    )
    images1 = driver.find_element(By.CLASS_NAME, "mNsIhb")
    images1.click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YsLeY"))
    )
    middle1 = driver.find_element(By.CLASS_NAME, "YsLeY")
    final1 = middle1.find_element(By.TAG_NAME, "img")
    result.append(str(final1.get_attribute("src")))


    url_p3 = "https://www.google.com/search?sca_esv=cd731438e95bc999&sxsrf=AHTn8zrMi6atrpzMrtDb1K9DOEKL0MQCVQ:1743542414604&q="
    url_p3 += topic.replace(" ", "+")
    if url_p3.endswith("+"):
        url_p3 = url_p3[:len(url_p3) - 1]
    url_p3 += "+funny+picture"
    url_p3 += "&udm=2&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpmDtIGL1r84kuKz6yAcD_igefx-eKq1gCPHF3zhthFol4Ng0BskIHiWtseitnxRUsdhuojFXPgEoHpG0GIfMKVPk2BkHblkxSI-tfKD1XmeeaqS5FHtrr8wsFXMuCe4QoMNCRPqH1YGzoZ9-eFehql3ssOZfjNPT2O6Pssj429Q7oCx7XuiHvC1mkqPCqfpKED5Tzqw&sa=X&ved=2ahUKEwjWxJfS4beMAxWUrokEHS93ABAQtKgLegQIIxAB&biw=1512&bih=784&dpr=2"
    driver.get(url_p3)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mNsIhb"))
    )
    images2 = driver.find_element(By.CLASS_NAME, "mNsIhb")
    images2.click()
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "YsLeY"))
    )
    middle2 = driver.find_element(By.CLASS_NAME, "YsLeY")
    final2 = middle2.find_element(By.TAG_NAME, "img")
    result.append(str(final2.get_attribute("src")))
    driver.quit()
    return result

def get_article(topic: str) -> str:
    """"""
    PATH = "/Users/derek/Code/ML/derek-yux.github.io/chromedriver"
    cService = webdriver.ChromeService(executable_path=PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get("https://www.google.com/search?q=" + topic.replace(" ", "+"))
    time.sleep(15)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "b8lM7"))
    )
    large_area = driver.find_element(By.CLASS_NAME, "b8lM7")
    search = large_area.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.quit()
    return search

def combine(topic: str, source_url: str) -> str:
<<<<<<< HEAD
    return "Write a short, informative, and quantitative news story on '" + topic + "' in the humor style of Dave Chappelle by summarizing this article: " + newspaper_text_extraction(source_url)
=======
    return "Write a short, informative, and quantitative news story on '" + topic + "' with a bolded title that does not contain quotation marks nor slashes and multiple twists and turns by summarizing this article: " + newspaper_text_extraction(source_url)
>>>>>>> ef70771 (html end test v2)
