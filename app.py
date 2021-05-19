import sys
from flask import Flask, json, request, abort
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://adedejiabiola@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)

  def __repl__(self):
    return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route("/")
def index():
  result = Todo.query.all()
  return render_template("index.html", data = result)

@app.route("/todos/create", methods=['POST'])
def create_todo():
  error = False
  body = {}
  # description = request.form.get("description", '')
  try:
    description = request.get_json()['description']
    todo_instance = Todo(description=description)
    db.session.add(todo_instance)
    db.session.commit()
    body['description'] = todo_instance.description
  except:
    db.session.rollback()
    error = True
    print(sys.exec_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  if not error:
    return json.jsonify(body)