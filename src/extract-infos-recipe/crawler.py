import os
from textwrap import indent
from typing import Dict, List
import pandas as pd
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import re
import json
import time
from functions import bcolors,log_function,process_text
from selenium.common.exceptions import NoSuchElementException,TimeoutException

class CrawlerSiteTudoGostosoReceita:


  def __init__(self,
    name_last_recipe_file: str = "last_recipe.txt",
    sleep_between_pages_seconds: int = 5,
    timeout_load_page_seconds: int = 5,
    file_urls: str = "../extract-urls-tudo-gostoso/data/data_saved.csv"
  ):
    self.name_last_recipe_file = name_last_recipe_file
    self.sleep_between_pages_seconds = sleep_between_pages_seconds
    self.timeout_load_page_seconds = timeout_load_page_seconds
    self.file_urls = file_urls

    if os.path.isfile(name_last_recipe_file):
      with open(name_last_recipe_file) as file:
        self.start_index = int(file.read())
    else:
      self.start_index = 0
  
  def run(self):
    self._extract()

  def _extract(self):
    dataframe = pd.read_csv(self.file_urls)
    dataframe = dataframe[self.start_index:]
    for index,line in dataframe.iterrows():
      while True:
        log_function(bcolors.OKGREEN,f"começando o crawler na receita {index}")
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(self.timeout_load_page_seconds)
        try:
          driver.get(line['url'])
        except:
          pass
        
        try:
          nome_receita = driver.find_element(By.XPATH, '//div[@class="recipe-title"]//h1').text
        except TimeoutException:
          continue
        
        ingredientes = self._get_json(driver,'//div[@class="col-lg-8 ingredients-card"]//*')
        passos = self._get_json(driver,'//div[@class="directions-info col-lg-8 directions-card"]//*')
        tempo_preparo = driver.find_element(By.XPATH,'//time[@class="dt-duration"]').text
        rendimento =  driver.find_element(By.XPATH,'//data[@class="p-yield num yield"]').text
        autor = driver.find_element(By.XPATH,'//a[@class="author-name"]//span').text

        try:
          url_image = driver.find_element(By.XPATH,'//img[@class="pic"]').get_attribute('src')
        except NoSuchElementException:
          url_image = None

        driver.close()

        name_recipe_save = process_text(nome_receita)
        name_directory = f"{index}-{name_recipe_save}"

        try:
          os.mkdir("data/"+name_directory)
        except FileExistsError:
          pass
        
        if not url_image is None:
          img_data = requests.get(url_image).content


          with open(f"data/{name_directory}/img.jpg", 'wb') as handler:
              handler.write(img_data)
      
        self._transform(nome_receita, ingredientes, passos, tempo_preparo, rendimento, autor, name_directory, line['url'])


        with open(self.name_last_recipe_file,'w') as file:
          file.write(str(index))
        
        log_function(bcolors.OKBLUE,f"crawler rodou ok na receita {index} - {nome_receita}.")
        time.sleep(self.sleep_between_pages_seconds)
        break
    
  def _transform(self, nome_receita : str, 
    ingredientes : Dict[str, List], 
    passos : Dict[str, List], 
    tempo_preparo : str, 
    rendimento : str, 
    autor : str,
    name_directory: str,
    url_receita: str
  ) -> str:
    str_para_salvar = {
      "nome_receita": nome_receita,
      "ingredientes" : ingredientes,
      "passos" : passos,
      "tempo_de_preparo":tempo_preparo,
      "rendimento" : rendimento,
      "autor" : autor,
      "url_receita": url_receita
    }
    str_para_salvar = json.dumps(str_para_salvar,indent = 2, ensure_ascii=False)
    self._load(str_para_salvar,name_directory)

  def _load(self, str_para_salvar: str, name_directory: str):
    with open(f"data/{name_directory}/recipe.txt","w") as file:
      file.write(str_para_salvar)

  def _get_json(self, driver, xpath : str) -> Dict:
    elementos = driver.find_elements(By.XPATH,xpath)
    json_output = defaultdict(list)
    actual = 'DEFAULT'
    for e in elementos:
      if e.tag_name == 'h3':
        actual = e.text
      if e.tag_name == 'li':
        json_output[actual].append(e.text)
    return json_output
