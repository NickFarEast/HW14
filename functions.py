import sqlite3


def get_result(sql, param=""):
    """ Функция подключения к базе данных

    :param param:
    :param sql: параметры запроса в базу данных
    :return:  возвращает список словарей из базы данных соответствующих параметрам запроса
    """
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []
        for item in con.execute(sql, param).fetchall():
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
    param = (f'%{name1}%', f'%{name2}%')
    sql = f"""SELECT `cast`
              FROM netflix n
              WHERE n.cast LIKE ? AND n.cast LIKE ?
              """

    actors_list = []
    names_list = set()
    result = get_result(sql, param)

    for item in result:
        for i in item.get("cast").split(","):
            actors_list.append(i)

    for name in actors_list:
        if actors_list.count(name) >= 2:
            names_list.add(name)

    return names_list


def search(type, date, genre):
    """ Функция для поиска фильмов в базе данных по заданным параметрам

    :param type: Тип(фильм или сериал)
    :param date: дата выпуска
    :param genre: Жанр
    :return: Возвращает список фильмов согласно заданным параметрам
    """
    param = (type, date, f'%{genre}%')
    sql = f"""SELECT *
           FROM netflix n
           WHERE type = ? AND release_year = ? AND listed_in LIKE ?
           """

    result = get_result(sql, param)

    return result



