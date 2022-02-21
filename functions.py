import sqlite3
import json


def get_result(sql):
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []
        for item in con.execute(sql).fetchall():
            s = dict(item)

            result.append(s)

        return result
