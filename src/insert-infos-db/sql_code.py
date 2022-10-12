

create_table_recipes = """
CREATE TABLE IF NOT EXISTS receitas (
  id SERIAL NOT NULL PRIMARY KEY,
  recipe_json JSON NOT NULL,
  has_image BOOLEAN NOT NULL,
  directory_name TEXT NOT NULL
);
"""

create_extension_unnaccent = "CREATE EXTENSION unaccent;"


create_inveted_index = """
CREATE INDEX index_gin ON receitas USING gin(to_tsvector('portuguese', recipe_json));
"""

def build_insert(json: str, has_image: bool, directory_name: str) -> str:
  has_image = "true" if has_image else "false"
  sql_insert = f"""
  INSERT INTO receitas (recipe_json,has_image,directory_name) VALUES ('{json}','{has_image}','{directory_name}');
  """
  return sql_insert