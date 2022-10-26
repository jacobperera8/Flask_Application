#!/usr/bin/python
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE users''')
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        conn.close()


#  Events table
# def create_db_table2():
#     try:
#         conn = connect_to_db()
#         # conn.execute('''DROP TABLE events''')
#         conn.execute('''
#                CREATE TABLE events (
#                    event_id INTEGER PRIMARY KEY NOT NULL,
#                    event_name TEXT NOT NULL,
#                    host_id INTEGER NOT NULL,
#                    participant_id INTEGER NOT NULL,
#                    start_time TIMESTAMP NOT NULL,
#                    End_time TEXT NOT NULL
#                );
#            ''')
#
#         conn.commit()
#         print("Events table created successfully")
#     except:
#         print("Events table creation failed")
#     finally:
#         conn.close()

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone) VALUES (?, ?, ?)", (user['name'], user['email'], user['phone']) )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_user


# Event
# def insert_event(event):
#     inserted_event = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO events (event_name, host_id, participant_id, start_time, End_time) VALUES (?, ?, ?, ?, ?)", (event['event_name'], event['host_id'], event['participant_id'], event['start_time'], event['End_time']) )
#         conn.commit()
#         inserted_event = get_event_by_id(cur.lastrowid)
#     except:
#         conn().rollback()
#
#     finally:
#         conn.close()
#
#     return inserted_event


def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            users.append(user)

    except:
        users = []

    return users

# Event
# def get_events():
#     events = []
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM events")
#         rows = cur.fetchall()
#
#         # convert row objects to dictionary
#         for i in rows:
#             event = {"event_name": i["event_name"], "host_id": i["host_id"], "participant_id": i["participant_id"],
#                      "start_time": i["start_time"], "End_time": i["End_time"]}
#             events.append(event)
#     except:
#         events = []
#
#     return events

def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
    except:
        user = {}

    return user

# Event
# def get_event_by_id(host_id):
#     event = {}
#     try:
#         conn = connect_to_db()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM events WHERE host_id = ?", (host_id,))
#         row = cur.fetchone()
#
#         # convert row object to dictionary
#         event["event_name"] = row["event_name"]
#         event["host_id"] = row["host_id"]
#         event["participant_id"] = row["participant_id"]
#         event["start_time"] = row["start_time"]
#
#     except:
#         event = {}
#
#     return event

# User
def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ? WHERE user_id =?", (user["name"], user["email"], user["phone"], user["user_id"]))
        conn.commit()
        #return the user
        updated_user = get_user_by_id(user["user_id"])

    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()

    return updated_user

# Event
# def update_event(event):
#     updated_event = {}
#     try:
#         conn = connect_to_db()
#         cur = conn.cursor()
#         cur.execute("UPDATE events SET event_name = ?, host_id = ?, participant_id = ?, start_time = ?, End_time = ? WHERE host_id =?", (event["event_name"], event["host_id"], event["participant_id"], event["start_time"], event["End_time"],))
#         conn.commit()
#
#         # return the event
#         updated_event = get_event_by_id(event["host_id"])
#
#     except:
#         conn.rollback()
#         updated_event = {}
#     finally:
#         conn.close()
#
#     return updated_event

def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()

    return message


users = []
user0 = {
    "name": "Charles Effiong",
    "email": "charles@gamil.com",
    "phone": "067765665656",
}

user1 = {
    "name": "Sam Adebanjo",
    "email": "samadebanjo@gamil.com",
    "phone": "098765465",
}

user2 = {
    "name": "John Doe",
    "email": "johndoe@gamil.com",
    "phone": "067765665656",
}

user3 = {
    "name": "Mary James",
    "email": "maryjames@gamil.com",
    "phone": "09878766676",
}

users.append(user0)
users.append(user1)
users.append(user2)
users.append(user3)

create_db_table()

for i in users:
    print(insert_user(i))




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/users/add',  methods = ['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update',  methods = ['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>',  methods = ['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.run()