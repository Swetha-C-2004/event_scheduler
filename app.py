from flask import Flask, render_template, request, redirect, url_for
from models import db, Event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Use a flag to ensure initialization code runs only once
first_request = True

@app.before_request
def initialize():
    global first_request
    if first_request:
        db.create_all()
        first_request = False

@app.route('/')
def index():
    events = Event.query.order_by(Event.priority.desc()).all()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        priority = request.form['priority']
        description = request.form['description']

        new_event = Event(title=title, date=date, priority=priority, description=description)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
