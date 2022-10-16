import psycopg2
from dotenv import load_dotenv
load_dotenv('.env')
import os
from sql_code import *
import glob
import json
import re

conn = psycopg2.connect(
    host=os.environ['HOST'],
    database=os.environ['DATABASE'],
    user=os.environ['USER_DB'],
    password=os.environ['PASSWORD'],
    port=os.environ['PORT']
)

cur = conn.cursor()


cur.execute(create_table_recipes) ## criando o db
conn.commit()

cur.execute(create_inveted_index) ## to create the inverted index
conn.commit()

cur.execute(create_extension_unnaccent) ## to create the inverted index
conn.commit()

list_receitas = list(glob.glob("../extract-infos-recipe/data/**"))
list_receitas.sort()

for dir in list_receitas:

  nome = dir.split('/')[-1]

  with open(dir+"/recipe.txt",'r') as file:
    file_readed = file.read()
    json_str = json.dumps(json.loads(file_readed),ensure_ascii=False)
    json_receita = json.loads(file_readed)

  try:
    porcoes = int(re.search("[0-9]+",json_receita['rendimento'])[0])
  except:
    porcoes = 0
  try:
    tempo = int(re.search("[0-9]+",json_receita['tempo_de_preparo'])[0])
  except:
    porcoes = 0
  
  if os.path.exists(dir+ "/img.jpg"):
    sql_insert = build_insert(json_str, True, nome, tempo, porcoes)
  else:
    sql_insert = build_insert(json_str, False, 'miau kiaralho', tempo, porcoes)

  try:
    cur.execute(sql_insert) ## inserindo as receitas no db
    conn.commit()
  except:
    conn.commit()
    continue
  
  print(nome)

cur.close()