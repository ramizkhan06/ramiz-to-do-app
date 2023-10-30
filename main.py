from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='remix'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

# Create the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() 
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Deleted Successfully', 'success')
    else:
        flash('Todo not found', 'error')
    return redirect('/')



@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() 
        todo.title = title
        todo.desc = desc
        todo.date_created = datetime.utcnow()
        db.session.add(todo)
        db.session.commit()
        flash('Updated Successfully')
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first() 
    return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
