import sqlite3 as sql

print("1 - добавление данных в БД\n2 - получение данных из БД\n3 - поиск по тексту\n4 - удаление по ID")
choice = int(input("> "))
con = sql.connect('search_system.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS `search_system` (`id` INT PRIMARY KEY,"
                " `rubrics` TEXT, 'text' TEXT, 'created_date' DATE)")


    if choice == 1:
        user_id = input("ID\n> ")
        rubrics = input("Rubrics\n> ")
        text = input("Text\n> ")
        date = input("Date\n> ")
        cur.execute(f"INSERT INTO `search_system` VALUES ('{user_id}', '{rubrics}', '{text}', '{date}')")

    elif choice == 2:
        cur.execute("SELECT * FROM `search_system`")
        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1], row[2], row[3])

    elif choice == 3:
        text_for_search = input("Text for search\n> ")
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS search_index using fts5(id, text);")
        cur.execute("SELECT * FROM `search_system`")
        rows = cur.fetchall()
        for row in rows:
            insert_id = row[0]
            insert_text = row[2]
            cur.execute(f"INSERT INTO `search_index` VALUES ('{insert_id}', '{insert_text}')")
        cur.execute(f"SELECT * FROM search_system JOIN (SELECT * FROM search_index WHERE "
                    f"search_index MATCH '{text_for_search}') si ON search_system.id = si.id ORDER BY created_date")
        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1], row[2], row[3])
        cur.execute(f"DELETE FROM 'search_index'")

    elif choice == 4:
        id_for_delete = input("ID for delete\n> ")
        cur.execute(f"DELETE FROM 'search_system' WHERE id='{id_for_delete}';")
    else:
        print("Вы ошиблись")

    con.commit()
    cur.close()
