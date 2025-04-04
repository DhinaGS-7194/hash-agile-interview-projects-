# Flask Login Application Documentation

## Overview
This Flask application provides a simple login page where users can enter their username and password. It connects to a PostgreSQL database to validate user credentials. The application includes basic SQL injection protection.

## Requirements
- Python 3
- Flask
- psycopg2 (PostgreSQL database adapter for Python)
- PostgreSQL

## Installation & Setup
### 1. Install Dependencies
```sh
pip install flask psycopg2
```

### 2. Configure PostgreSQL Database
- Ensure PostgreSQL is running.
- Create a database and a table:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    pass TEXT NOT NULL
);
```
- Insert test users:
```sql
INSERT INTO users (name, pass) VALUES ('user1', '1234');
INSERT INTO users (name, pass) VALUES ('user2', '5678');
```

### 3. Run the Application
```sh
python app.py
```

## Code Breakdown

### 1. Importing Required Modules
```python
from flask import Flask, render_template, request
import psycopg2 as pg
```
- `Flask` is used for creating the web application.
- `psycopg2` is used to interact with the PostgreSQL database.

### 2. Database Connection
```python
cur = pg.connect(host="localhost", dbname="postgres", user="postgres", password="1234", port=5432).cursor()
```
- Connects to a local PostgreSQL database using credentials.

### 3. SQL Injection Prevention
```python
def check(username, password):
    keywords = ["CREATE", "DROP", "ALTER", "INSERT", "UPDATE", "DELETE", "SELECT", "--", ";"]
    for keyword in keywords:
        if keyword in username or keyword in password:
            return True
    return False
```
- This function prevents SQL injection by rejecting inputs containing SQL keywords and special characters.

### 4. Flask Application
```python
app = Flask(__name__)
```
- Creates a Flask web application instance.

### 5. Login Route
```python
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check(username.upper(), password.upper()):
            return "<h1>Login Unsuccessful</h1>"
        cur.execute(f"SELECT * FROM users WHERE name='{username}' AND pass='{password}';")
        if cur.fetchall():
            return "<h1>Login Successful</h1>"
        else:
            return "<h1>Login Unsuccessful</h1>"
    return render_template("login.html")
```
- Handles both `GET` and `POST` requests.
- Takes user input, validates against SQL injection, and checks credentials in the database.

### 6. Running the Application
```python
if __name__ == '__main__':
    app.run()
```
- Runs the Flask application.

## HTML File (`login.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h1>Login</h1>
    <form method="POST">
        <label for="username">Username:</label>
        <input type="text" name="username">
        <br>
        <label for="password">Password:</label>
        <input type="password" name="password">
        <br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```
- Simple HTML form for username and password input.

## Security Issues
1. **SQL Injection Risk**: The query in `cur.execute()` uses string formatting, making it vulnerable to SQL injection. Use parameterized queries to prevent this:
    ```python
    cur.execute("SELECT * FROM users WHERE name=%s AND pass=%s;", (username, password))
    ```
2. **Plain Text Passwords**: Passwords should be stored securely using hashing (e.g., bcrypt or Argon2).
3. **Hardcoded Credentials**: Database credentials should be stored securely using environment variables.

## Improvements
- Use `Flask-WTF` for form validation.
- Implement Flask-Login for session management.
- Use hashed passwords with `bcrypt` or `argon2`.
- Implement proper error handling and logging.

## Conclusion
This Flask application provides a basic login functionality. However, for a production environment, security improvements are necessary to prevent SQL injection and secure user credentials properly.

