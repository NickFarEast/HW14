import json

from flask import Flask
import functions

app = Flask(__name__)


@app.route("/")
def get_all_title( ):

    sql = f"""SELECT *
          FROM netflix n 
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

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.route("/movie/<title>")
def get_by_title(title: str):
    param = (title, title)
    sql = f"""SELECT *
          FROM netflix n 
          WHERE n.title = ? AND n.date_added = (SELECT max(date_added)
          FROM netflix n 
          WHERE n.title = ?)
          AND n.type = 'Movie'
          """
    result = []
    for item in functions.get_result(sql, param):
        s = {
            "title": item.get("title"),
            "country": item.get("country"),
            "release_year": item.get("release_year"),
            "genre": item.get("listed_in"),
            "description": item.get("description")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")



@app.route("/movie/<year1>/to/<year2>")
def get_by_year(year1: str, year2: str):
    param = (year1, year2)
    sql = f"""SELECT *
          FROM netflix n
          WHERE n.release_year BETWEEN ? AND ?
          AND n.type = 'Movie'
          LIMIT 100
          """
    result = []
    for item in functions.get_result(sql, param):
        s = {
            "title": item.get("title"),
            "release_year": item.get("release_year"),
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")

@app.route("/rating/<value>")
def get_by_rating(value: str):
    sql = f"""SELECT *
          FROM netflix n
          WHERE n.type = 'Movie'"""

    if value == "children":
        sql += f""" AND rating = 'G'"""
    elif value == "family":
        sql += f""" AND rating LIKE '%G'"""
    elif value == "adult":
        sql += f""" AND rating = 'R' OR rating = 'NC-17'"""
    else:
        return app.response_class(response=json.dumps({}),
                                  status=200,
                                  mimetype="application/json")

    result = []
    for item in functions.get_result(sql):
        s = {
            "title": item.get("title"),
            "release_year": item.get("release_year"),
            "description": item.get("description")
        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


@app.route("/genre/<genre>")
def get_by_genre(genre: str):
    param = (f'%{genre}%', f'%{genre}%')
    sql = f"""SELECT *
          FROM netflix n
          WHERE n.listed_in LIKE ?
          AND n.release_year = (SELECT max(release_year)
          FROM netflix n
          WHERE n.listed_in LIKE ?)
          AND n.type = 'Movie'
          LIMIT 10
          """

    result = []
    for item in functions.get_result(sql, param):
        s = {
            "title": item.get("title"),
            "release_year": item.get("release_year"),
            "description": item.get("description")

        }
        result.append(s)

    return app.response_class(response=json.dumps(result),
                              status=200,
                              mimetype="application/json")


if __name__ == '__main__':
    app.run()
