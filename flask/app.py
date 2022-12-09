from flask import Flask, request, jsonify
import json
import psycopg2

app = Flask(__name__)
app.config["DATABASE_NAME"] = "recc"
app.config["DATABASE_USER"] = "root"
app.config["DATABASE_PASSWORD"] = "root"
app.config["DATABASE_HOST"] = "localhost"

@app.route("/getdata", methods=["GET"])
def get_data():
  # Connect to the database
  conn = psycopg2.connect(database=app.config["DATABASE_NAME"],
                          user=app.config["DATABASE_USER"],
                          password=app.config["DATABASE_PASSWORD"],
                          host=app.config["DATABASE_HOST"])
  # Execute a SELECT query and retrieve the result set
  cur = conn.cursor()
  article_id = request.args.get("article_id")
  cur.execute('select article_id, "' + article_id + '" from contentbased order by 2 desc limit 10;')
  rows = cur.fetchall()
  payload = []
  content = {}
  for result in rows:
      content = {'article_id': result[0], 'score': result[1]}
      payload.append(content)
      content = {}
  return jsonify(payload)

  # Return the result set as a response to the client
  return rows


if __name__ == '__main__':
  app.run(debug=True)