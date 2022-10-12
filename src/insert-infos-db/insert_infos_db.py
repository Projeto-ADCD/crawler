import psycopg2
from dotenv import load_dotenv
load_dotenv('.env')
import os
from sql_code import *
import glob
import json

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
    json_str = json.dumps(json.loads(file.read()),ensure_ascii=False)
  

  if os.path.exists(dir+ "/img.jpg"):
    sql_insert = build_insert(json_str, True, nome)
  else:
    sql_insert = build_insert(json_str, False, 'miau kiaralho')
  
  try:
    cur.execute(sql_insert) ## inserindo as receitas no db
    conn.commit()
  except:
    conn.commit()
    continue
  
  print(nome)

cur.close()