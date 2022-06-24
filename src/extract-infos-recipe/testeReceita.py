from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.set_page_load_timeout(5)
try:
  driver.get("https://www.tudogostoso.com.br/receita/316950-cupcake-de-batata.html")
except:
  pass
elementos = driver.find_elements(By.XPATH,'//div[@class="col-lg-8 ingredients-card"]/ul/li')
for e in elementos:
  print(e.text)

time.sleep(3)
driver.close()