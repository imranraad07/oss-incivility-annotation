import sqlite3


class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        c = self.conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_login TEXT UNIQUE not null, start_issue_id INTEGER not null, end_issue_id INTEGER not null, current_issue_id INTEGER not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS annotated_comments(id INTEGER PRIMARY KEY, issue_id INTEGER not null, comment_id INTEGER not null, user_login TEXT not null, tbdf TEXT not null);"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS annotated_issues(id INTEGER PRIMARY KEY, issue_id INTEGER not null, user_login TEXT not null, derailment_point TEXT not null, trigger TEXT not null, target TEXT not null, consequences TEXT not null, additional_comments TEXT not null);"
        )

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
        return c.lastrowid

    def close(self):
        self.conn.close()

    def create_user(self, user_login, start_issue, end_issue, current_issue):
        return self.execute(
            "INSERT INTO users (user_login, start_issue_id, end_issue_id, current_issue_id) VALUES (?, ?, ?, ?)",
            [user_login, start_issue, end_issue, current_issue],
        )

    def get_user(self, user_login):
        data = self.select("SELECT * FROM users WHERE user_login = ?;", [user_login])
        if data:
            d = data[0]
            retval = {
                "user_login": d[1],
                "start_issue_id": d[2],
                "end_issue_id": d[3],
                "current_issue_id": d[4]
            }
            return retval
        else:
            return None

    def update_current_issue(self, user_login, current_issue):
        return self.execute(
            "UPDATE users SET current_issue_id = ? WHERE user_login = ?;",
            [current_issue, user_login]
        )

    def get_all_users(self):
        data = self.select("SELECT * FROM users;")
        users = []
        for d in data:
            retval = {
                "user_login": d[1],
                "start_issue_id": d[2],
                "end_issue_id": d[3],
                "current_issue_id": d[4]
            }
            users.append(retval)
        return users

    def insert_comment_annotation(self, issue_id, comment_id, user_login, tbdf):
        return self.execute(
            "INSERT INTO annotated_comments (issue_id, comment_id, user_login, tbdf) VALUES (?, ?, ?, ?)",
            [issue_id, comment_id, user_login, tbdf],
        )

    def insert_issue_annotation(self, issue_id, user_login, derailment_point, trigger, target, consequences, additional_comments):
        return self.execute(
            "INSERT INTO annotated_issues (issue_id, user_login, derailment_point, trigger, target, consequences, additional_comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
            [issue_id, user_login, derailment_point, trigger, target, consequences, additional_comments],
        )

    def get_all_comment_annotations(self):
        data = self.select("SELECT * FROM annotated_comments;")
        comment_annotations = []
        for d in data:
            retval = {
                "issue_id": d[1],
                "comment_id": d[2],
                "user_login": d[3],
                "tbdf": d[4]
            }
            comment_annotations.append(retval)
        return comment_annotations

    def get_all_issue_annotations(self):
        data = self.select("SELECT * FROM annotated_issues;")
        annotated_issues = []
        for d in data:
            retval = {
                "issue_id": d[1],
                "user_login": d[2],
                "derailment_point": d[3],
                "trigger": d[4],
                "target": d[5],
                "consequences": d[6],
                "additional_comments": d[7]
            }
            annotated_issues.append(retval)
        return annotated_issues
