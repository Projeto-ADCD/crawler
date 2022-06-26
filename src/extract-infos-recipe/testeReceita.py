from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome()
driver.set_page_load_timeout(3)
try:
  driver.get("https://www.tudogostoso.com.br/receita/316996-pudim-fit.html")
except:
  pass
elementos = driver.find_elements(By.XPATH,'//div[@class="col-lg-8 ingredients-card"]//*')
ingredientes = defaultdict(list)
actual = 'DEFAULT'
for e in elementos:
  if e.tag_name == 'h3':
    actual = e.text
  if e.tag_name == 'li':
    ingredientes[actual].append(e.text)

elementos = driver.find_elements(By.XPATH,'//div[@class="directions-info col-lg-8 directions-card"]//*')
preparo = defaultdict(list)
actual = 'DEFAULT'
for e in elementos:
  if e.tag_name == 'h3':
    actual = e.text
  if e.tag_name == 'li':
    preparo[actual].append(e.text)

## time.sleep(3)
driver.close()

print(json.dumps(ingredientes,indent=2))
print(json.dumps(preparo,indent=2))