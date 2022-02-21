import sqlite3


def get_result(sql):
    """ Функция подключения к базе данных

    :param sql: параметры запроса в базу данных
    :return:  возвращает список словарей из базы данных соответствующих параметрам запроса
    """
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []
        for item in con.execute(sql).fetchall():
            s = dict(item)

            result.append(s)

        return result


def cast_search(name1, name2):
    """ Функция для получения списка актеров , которые снимались
    с указанными актерами 2 и более раза

    :param name1: имя первого актера
    :param name2: имя второго актера
    :return: возвращается множество с именами актеров
    """

    sql = f"""SELECT `cast`
              FROM netflix n 
              """
    t = []
    actors_list = []
    names_list = set()
    result = get_result(sql)

    for item in result:
        if name1 in item.get('cast') and name2 in item.get('cast'):
            t.append(item.get('cast'))
    print(t)

    for item in t:
        for i in item.split(","):
            actors_list.append(i)

    for name in actors_list:
        if actors_list.count(name) >= 2:
            names_list.add(name)

    return names_list



