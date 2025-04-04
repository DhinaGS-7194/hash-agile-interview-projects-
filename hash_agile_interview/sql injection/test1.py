from flask import Flask, render_template, request
import psycopg2 as pg

cur=pg.connect(host="localhost",dbname="postgres",user="postgres",password="1234",port=5432).cursor()

# cur.execute("""INSERT INTO users VALUES(4, 'user4', '3456');COMMIT;""")

def check(username, password):
    keywords=[
    "CREATE", "DROP", "ALTER", "TRUNCATE", "RENAME", "COMMENT",
    "INSERT", "UPDATE", "DELETE", "MERGE", "CALL",
    "GRANT", "REVOKE",
    "COMMIT", "ROLLBACK", "SAVEPOINT",
    "SELECT", "FROM", "WHERE", "GROUP", "HAVING", "ORDER", "LIMIT", "OFFSET",
    "UNION", "INTERSECT", "EXCEPT",
    "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS",
    "IN", "NOT IN", "EXISTS", "NOT EXISTS",
    "AND", "OR", "NOT", "IS NULL", "IS NOT NULL", "LIKE", "ILIKE", "SIMILAR TO",
    "BETWEEN", "ANY", "ALL", "SOME", "DISTINCT",

    "+", "-", "*", "/", "%", "**", "//",
    "=", "!=", "<", ">", "<=", ">=",
    ":=", "=",
    "&", "|", "^", "~", "<<", ">>",
    "(", ")", "[", "]", "{", "}", ",", ";","--"
    ]
    for keyword in keywords:
        if keyword in username or keyword in password:
            return True
    return False


app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if check(username.upper(), password.upper()):
            return "<h1>Login Unsuccessful</h1>"
        cur.execute(f"""SELECT * FROM users WHERE name='{username}' AND pass='{password}';""")
        if cur.fetchall():
            return "<h1>Login Successful</h1>"
        else:
            return "<h1>Login Unsuccessful</h1>"
    return render_template(r"login.html")

if __name__=='__main__':
    app.run()
