import json
import sqlite3
from cgiserver import route, run
from cgiserver import GLOBAL_SETTING
from cgiserver.utils import html_file_loader


GLOBAL_SETTING.template_404 = "./static/404.html"
# 可以自定义错误代码界面的模板，可以是一个路径也可以是一个字符串
# GLOBAL_SETTING.template_400 = "./static/400.html"
# GLOBAL_SETTING.template_403 = "权限不足"


class DataBase:
    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.init_database()
        self.fill_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS STUDENT")
        cursor.execute(
            """
                    CREATE TABLE STUDENT
                    (
                        ID       TEXT     PRIMARY KEY     NOT NULL,
                        NAME     TEXT    NOT NULL,
                        CLASS    TEXT    NOT NULL
                    )
                    """
        )
        conn.commit()
        conn.close()

    def addto_database(self, id: str, name: str, cls: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO STUDENT (ID, NAME, CLASS) VALUES ('{id}', '{name}', '{cls}')"
        )
        conn.commit()
        conn.close()

    def fill_database(self):
        students = [
            ("709990845", "Sue", "class6"),
            ("393617759", "Thelma", "class8"),
            ("557948644", "Darrell", "class4"),
            ("1065334204", "Maria", "class10"),
            ("498022146", "Robert", "class2"),
            ("693113632", "Charles", "class7"),
            ("401090017", "Dewitt", "class10"),
            ("310667085", "Benjamin", "class6"),
            ("485798129", "Leslie", "class8"),
            ("570168538", "Carol", "class9"),
            ("631656174", "Joshua", "class9"),
            ("267808787", "Carrie", "class3"),
            ("344639076", "Jean", "class2"),
            ("184550698", "Herbert", "class5"),
            ("985725375", "Stephen", "class2"),
            ("426495546", "Bradley", "class9"),
            ("895973323", "William", "class5"),
            ("172760955", "Barbara", "class5"),
            ("1097803889", "Lyn", "class9"),
            ("252821386", "Derek", "class9"),
        ]
        for student in students:
            self.addto_database(*student)

    def query_by_id(self, id: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT ID, NAME, CLASS FROM STUDENT WHERE ID = '{id}'")
        query_result = []
        for student in cursor:
            query_result.append((student[0], student[1], student[2]))
        return query_result


@route("/", method="GET")
def hello():
    return "this is index.html"


@route("/log", method="GET")
def log_page():
    return html_file_loader("logs/server_log.html")


@route("/cgi-bin/calculator.py", method="GET")
def calculate_page(**args):
    return "This should return an HTML page capable of submitting the form"


@route("/cgi-bin/calculator.py", method="POST")
def calculate(**args):
    value1 = args.get("value1")
    value2 = args.get("value2")
    op = args.get("op")

    if any(arg is None for arg in (value1, value2, op)):
        return "argument error"

    try:
        value1 = float(value1)
        value2 = float(value2)
    except Exception:
        return "value1 or value2 is not a float or integer"

    if op == "+":
        return value1 + value2
    if op == "-":
        return value1 - value2
    if op == "*":
        return value1 * value2
    if op == "/":
        return value1 / value2

    return f"operation {op} not yet supported"


@route("/cgi-bin/query.py", method="GET")
def query_page(**args):
    return html_file_loader("static/query.html")


@route("/cgi-bin/query.py", method="POST")
def query(**args):
    response = {"ok": True, "message": None, "content": None}
    student_id = args.get("id")
    if student_id is None:
        response["ok"] = False
        response["message"] = "student id should be provided"
    query_result = db.query_by_id(student_id)
    if query_result:
        query_result = query_result[0]
        response["content"] = {
            "id": query_result[0],
            "name": query_result[1],
            "calss": query_result[2],
        }
    else:
        response["ok"] = False
        response[
            "message"
        ] = f"None of the students in the database have the id of {student_id}"
    return json.dumps(response)


if __name__ == "__main__":
    db = DataBase("student.db")
    run()
