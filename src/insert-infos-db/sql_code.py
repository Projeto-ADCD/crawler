

create_table_recipes = """
CREATE TABLE IF NOT EXISTS receitas (
  id SERIAL NOT NULL PRIMARY KEY,
  recipe_json JSON NOT NULL,
  has_image BOOLEAN NOT NULL,
  directory_name TEXT NOT NULL,
  porcoes INTEGER NOT NULL,
  tempo INTEGER NOT NULL
);
"""

create_extension_unnaccent = "CREATE EXTENSION unaccent;"


create_inveted_index = """
CREATE INDEX index_gin ON receitas USING gin(to_tsvector('portuguese', recipe_json));
"""

create_column_porcoes = """
ALTER TABLE receitas ADD porcoes INTEGER;
"""

create_column_tempo = """
ALTER TABLE receitas ADD tempo INTEGER;
"""

def build_insert_porcoes_tempo(id: int, tempo: int, porcoes: int):
  sql_insert = f"""
  UPDATE receitas
  SET porcoes = {porcoes}, tempo = {tempo}
  WHERE id = {id};
  """
  return sql_insert

def build_insert(json: str, has_image: bool, directory_name: str, tempo: int, porcoes: int) -> str:
  has_image = "true" if has_image else "false"
  sql_insert = f"""
  INSERT INTO receitas (recipe_json,has_image,directory_name, tempo, porcoes) VALUES ('{json}','{has_image}','{directory_name}',{tempo},{porcoes});
  """
  return sql_insert