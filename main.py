import json

from flask import Flask
import functions

app = Flask(__name__)


@app.route("/movie/<title>")
def get_by_title(title: str):
    sql = f"""SELECT *
          FROM netflix n 
          WHERE n.title = '{title}' AND n.date_added = (SELECT max(date_added)
          FROM netflix n 
          WHERE n.title = '{title}')
          """
    result = []
    for item in functions.get_result(sql):
        s = {
            "title": item.get("title"),
            "country": item.get("country"),
            "release_year": item.get("release_year"),
            "genre": item.get("listed_in"),
            "description": item.get("description")
            }
        result.append(s)

    print(result)
    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run()
