import sqlite3

from flask import Flask
import requests
import csv
import pandas

app = Flask(__name__)


def create_users():
    # create table USERS in our database
    con = sqlite3.connect("projectDB.db")
    print("Database connected successfully")
    con.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           CHAR(50)    NOT NULL,
         CITY        CHAR(50)   NOT NULL);''')
    con.close()


def create_tasks():
    # create table TASKS in our database
    con = sqlite3.connect("projectDB.db")
    con.execute('''CREATE TABLE TASKS
         (ID INT PRIMARY KEY     NOT NULL,
         USERID INT     NOT NULL,
         TITLE           CHAR(50)    NOT NULL,
         COMPLETED        CHAR(50)   NOT NULL,
         FOREIGN KEY(USERID) REFERENCES USERS(ID));''')
    con.close()


def insert_users():
    # insert users to our database
    con = sqlite3.connect("projectDB.db")
    users = requests.get("https://jsonplaceholder.typicode.com/users")
    for x in users.json():
        userid = x["id"]
        username = x["username"]
        city = x["address"]["city"]
        query = f"INSERT INTO USERS VALUES ({userid}, '{username}', '{city}')"
        con.execute(query)
    con.commit()
    con.close()


def insert_tasks():
    # insert tasks to our database
    con = sqlite3.connect("projectDB.db")
    users = requests.get("https://jsonplaceholder.typicode.com/todos")
    for x in users.json():
        taskid = x["id"]
        userid = x["userId"]
        title = x["title"]
        completed = x["completed"]
        query = f"INSERT INTO TASKS VALUES ({taskid}, {userid}, '{title}', '{completed}')"
        con.execute(query)
    con.commit()
    con.close()


def configure_routes(app):

    @app.route('/')
    # basic route - just show Hello World to user
    def hello_world():
        return 'Hello World!'

    @app.route('/app/all')
    # take all needed information about task and write it in csv file on user hard drive
    def task_list():
        with open('task_list', mode='w') as csv_file:
            fieldnames = ['name', 'city', 'title', 'completed']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()

            con = sqlite3.connect("projectDB.db")

            name = ""
            city = ""
            check_id = ""

            task = con.execute(f"SELECT TITLE,COMPLETED,USERID from TASKS")
            for row in task:
                task = row[0]
                completed = row[1]
                user_id = row[2]
                if user_id != check_id:
                    check_id = user_id
                    user = con.execute(f"SELECT NAME,CITY from USERS WHERE ID={user_id}")
                    user_data = user.fetchall()
                    name = user_data[0][0]
                    city = user_data[0][1]

                writer.writerow({'name': name, 'city': city, 'title': task, 'completed': completed})

        return 'Saved'

    @app.route('/app/printall')
    # print csv file(needed create it first!) with tasks in terminal
    def print_all():
        try:
            data = pandas.read_csv('task_list')
            print(data)
            return 'Read'
        except FileNotFoundError:
            return 'You need to download file first'

    @app.route('/app/<task_id>')
    # show user information about specific task in web browser
    def user_task(task_id):
        con = sqlite3.connect("projectDB.db")
        task = con.execute(f"SELECT TITLE,COMPLETED,USERID from TASKS WHERE ID={task_id}")
        task_data = task.fetchall()
        title = task_data[0][0]
        completed = task_data[0][1]
        user_id = task_data[0][2]

        user = con.execute(f"SELECT NAME,CITY from USERS WHERE ID={user_id}")
        user_data = user.fetchall()
        name = user_data[0][0]
        city = user_data[0][1]

        con.close()

        answer = f"<b>Name</b> = {name} <b>City</b> = {city} <b>Task</b> = {title} <b>Completed</b> = {completed}"

        return answer


configure_routes(app)
if __name__ == '__main__':
    # start our app

    app.run(host='localhost', port=8080, debug=True)
