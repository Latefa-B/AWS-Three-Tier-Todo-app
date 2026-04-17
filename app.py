from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="todo-app-database.c1qkikkoozqc.us-east-1.rds.amazonaws.com",
    user="admin",
    password="sofiaamir20",
    database="ToDoApp"
)

@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    cursor = db.cursor()
    cursor.execute("INSERT INTO Tasks (task) VALUES (%s)", (task,))
    db.commit()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    cursor = db.cursor()
    cursor.execute("UPDATE Tasks SET status='Completed' WHERE id=%s", (task_id,))
    db.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
