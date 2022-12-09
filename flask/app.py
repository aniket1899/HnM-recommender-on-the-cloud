from flask import Flask, request, jsonify
import json
import psycopg2

#command to connect gd = http://127.0.0.1:5000/getdata?article_id=706016002
#command to connect basic = http://127.0.0.1:5000/getProductsHomepageBasic?article_id=706016002

app = Flask(__name__)
app.config["DATABASE_NAME"] = "recc"
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "root"
app.config["DATABASE_HOST"] = "localhost"

# Connect to the database
conn = psycopg2.connect(database=app.config["DATABASE_NAME"],
                        user=app.config["DATABASE_USER"],
                        password=app.config["DATABASE_PASSWORD"],
                        host=app.config["DATABASE_HOST"])

cur = conn.cursor()

@app.route("/getdata", methods=["GET"])
def get_data():

  article_id = request.args.get("article_id")
  # Execute a SELECT query and retrieve the result set
  cur.execute('select article_id, "' + article_id + '" from contentbased order by 2 desc limit 10;')
  rows = cur.fetchall()
  payload = []
  content = {}
  for result in rows:
      content = {'article_id': result[0], 'score': result[1]}
      payload.append(content)
      content = {}
  return jsonify(payload)


@app.route("/getProductsHomepageBasic", methods = ['GET'])
def get_products_home_basic():
  _VOLUME_LINK = 'url'

  _ARGS = {
  'customer_id' : request.args.get("customer_id"),
  'article_id' : request.args.get("article_id"),
  'index_group_name' : request.args.get("index_group_name"),
  'product_group_name' : request.args.get("product_group_name"),
  'garment_group_name' : request.args.get("garment_group_name")
  }

  query = 'SELECT * FROM articles'
  where = []
  for arg, val in _ARGS.items():
      if val:
          where.append(f" {arg} = '{val}' ")
  if where:
      query = query + " WHERE " + " AND ".join(where)
  query += " ;"
  print(query)
  cur.execute(query)
  
  rows = cur.fetchall()
  payload = []
  content = {}
  _ARTICLE_MASTER_SCHEMA = ['article_id', 'detail_desc', 'index_group_name', 
  'product_group_name', 'prod_name', 'garment_group_name']
  for result in rows:
      content = {}
      for idx, col in enumerate(_ARTICLE_MASTER_SCHEMA):
        content[col] = result[idx]
        payload.append(content)
      content['URL'] = _VOLUME_LINK + f"/{result[-1]}/{content['article_id']}.jpg"
  return jsonify(payload)



      

if __name__ == '__main__':
  app.run(debug=True)