from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os.path
from functions import bcolors, log_function
import time
import pandas as pd

class CrawlerSiteTudoGostoso:

  def __init__(self, 
    name_csv_save: str = "data_saved.csv", 
    name_last_url_file: str = "last_url.txt", 
    sleep_between_pages_seconds : int = 5, 
    timeout_load_page_seconds: int = 5, 
    url_start: str = None
  ):
    self.save_first = True
    if not(url_start is None):
      self.url_start = url_start
    elif os.path.isfile(name_last_url_file):
      with open(name_last_url_file,'r') as file:
        last_url_downloaded = file.read()
      self.url_start = last_url_downloaded
      self.save_first = False
      log_function(bcolors.WARNING,f"Arquivo {name_last_url_file} encontrado. irá começar apartir dele.")
    else:
      self.url_start = "https://www.tudogostoso.com.br/receitas"
    self.name_csv_save = name_csv_save
    self.name_last_url_file = name_last_url_file
    self.sleep_between_pages_seconds = sleep_between_pages_seconds
    self.timeout_load_page_seconds = timeout_load_page_seconds
  
  def run(self):
    self._extract()


  def _extract(self):
    while True:

      log_function(bcolors.OKGREEN,f"Fazendo crawler da pagina: {self.url_start}")

      driver = webdriver.Chrome()
      driver.set_page_load_timeout(self.timeout_load_page_seconds)

      try:
        driver.get(self.url_start)
      except:
        pass
    
      elementos = driver.find_elements(By.XPATH,'//div[@class="mb-3 recipe-card recipe-card-with-hover"]//a')
      urls = []
      for e in elementos:
        urls.append(e.get_attribute('href'))
      
      log_function(bcolors.OKGREEN,f"Achados {len(urls)} urls.")

      
      self._transform(self.url_start,urls)

      with open(self.name_last_url_file,'w') as file:
        file.write(self.url_start)
      
      try:
        button_next = driver.find_element(By.XPATH,'//a[@class="next"]')
        self.url_start = button_next.get_attribute('href')
      except:
        log_function(bcolors.OKBLUE,"Botão next não encontrado, crawler terminou de executar.")
        driver.close()
        break

      driver.close()
      time.sleep(self.sleep_between_pages_seconds)
  
  def _transform(self, url : str, urls: List[str]):
    dataAux = [(url,e) for e in urls]
    data = pd.DataFrame(dataAux,columns=['page','url'])
    self._load(data)
  
  def _load(self, data: pd.DataFrame):

    if not self.save_first:
      self.save_first = True
      log_function(bcolors.WARNING, "Página não salva. arquivo last_url guarda a ultima salva. a seguinte será salva")
    else:
      full_path_data = "data/"+self.name_csv_save
      if os.path.isfile(full_path_data):
        dataAlredySaved = pd.read_csv(full_path_data)
        data = pd.concat([dataAlredySaved, data],axis=0,ignore_index=True)
        data.to_csv(full_path_data,index=False)
        log_function(bcolors.OKBLUE,f"Arquivo {full_path_data} encontrado. {dataAlredySaved.shape[0]} URLS salvas.")
      else:
        data.to_csv(full_path_data,index=False)
        log_function(bcolors.WARNING,f"Arquivo {full_path_data} não encontrado. criando agora. {data.shape[0]} URLS salvas.")
    
    
        