import sqlite3
import json


all_ing = []
with open('model/all_ingrediants_list.txt', 'r') as f:
    all_ing = json.loads(f.read())
print(f"All ingerdiants list: {all_ing}")


def insert_ing(all_ing):
    connection = sqlite3.connect('ingredients.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Ingredients
                (name TEXT)''')
    connection.commit()
    for ing in all_ing:
        print(f"Trying to insert: {ing}")
        cursor.execute(f'Insert into Ingredients values ("{ing}")')
        connection.commit()
        print(f"{ing} inserted sucessfully")
    connection.close()


def insert_counts():
    connection = sqlite3.connect('ingredients.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rating_count
                (id INT, count INT)''')
    connection.commit()
    cursor.execute(f'Insert into rating_count values (1, 0)')
    connection.commit()
    print(f"Inserted count sucessfully")
    connection.close()


insert_ing(all_ing=all_ing)
insert_counts()
