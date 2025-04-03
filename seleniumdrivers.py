
# TODO:
# https://www.youtube.com/watch?v=eC841kSk-q0

def get_prompt() -> str:
    """"""
    from selenium import webdriver
    # from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    # from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    # import time
    from selenium.webdriver.support import expected_conditions as EC
    from pathlib import Path


    DB_FILE = 'db.json'
    THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    CSS_FILE = THIS_DIR / "Styles" / "main.css"


    PATH = "/Users/Derek/Code/ML/Selenium/chromedriver"
    cService = webdriver.ChromeService(executable_path=PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get("https://trends.google.com/trending?geo=US&sort=search-volume")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "mZ3RIc"))
    )

    trend = driver.find_element(By.CLASS_NAME, "mZ3RIc").get_attribute("innerText")
    driver.quit()
    all_trends = "Write a short, dry sarcasm, everyday language news report that contains bolded numbers and is accurate as of today on: " + str(trend)
    return all_trends


def get_images(topic: str) -> list:
    """"""
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from pathlib import Path
    from time import sleep


    DB_FILE = 'db.json'
    THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    CSS_FILE = THIS_DIR / "Styles" / "main.css"


    PATH = "/Users/Derek/Code/ML/Selenium/chromedriver"
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
