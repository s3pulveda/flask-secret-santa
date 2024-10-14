from flask import Flask, request, render_template, redirect, url_for
import html
import uuid

app = Flask(__name__)

# In-memory database for demonstration (replace with a real database in production)
db = {}

# Fetch participants and their gift lists from the in-memory db
def fetch_participants():
    participants = db
    return participants

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_person = request.args.get('selected_person')

    if request.method == 'POST':
        person = request.form.get('person')
        new_gift = request.form.get('new_gift')

        if person and new_gift:
            current_gifts = db.get(person, [])
            if new_gift not in [g['name'] for g in current_gifts]:
                gift_id = str(uuid.uuid4())  # Create a unique ID for each gift
                new_gift_object = {"name": html.escape(new_gift), "claimed": False, "id": gift_id}
                current_gifts.append(new_gift_object)
                db[person] = current_gifts

        return redirect(url_for('index', selected_person=person))

    participants = fetch_participants()
    participants = dict(sorted(participants.items()))  # Sort participants alphabetically
    return render_template('index.html', participants=participants, selected_person=selected_person)

@app.route('/claim_gift', methods=['POST'])
def claim_gift():
    person = request.form.get('person')
    gift_id = request.form.get('gift_id')

    current_gifts = db.get(person, [])
    gift_to_claim = next((gift for gift in current_gifts if gift['id'] == gift_id), None)

    if gift_to_claim is None:
        return "Gift not found", 404

    if gift_to_claim['claimed']:
        return "AlreadyClaimed", 409

    gift_to_claim['claimed'] = True
    db[person] = current_gifts
    return "Claimed"

@app.route('/delete_gift', methods=['POST'])
def delete_gift():
    person = request.form.get('person')
    gift_id = request.form.get('gift_id')

    current_gifts = db.get(person, [])
    gift_to_delete = next((gift for gift in current_gifts if gift['id'] == gift_id), None)

    if gift_to_delete is None:
        return "Gift not found", 404

    current_gifts = [gift for gift in current_gifts if gift['id'] != gift_id]
    db[person] = current_gifts
    return "Deleted"

@app.route('/init_names', methods=['GET'])
def init_names():
    initial_participants = ['Trish', 'Katelyn', 'Piotr', 'Albertico', 'Laura', 'Maria', 'Alberto',
                            'JP', 'Mackenzie', 'Pedro', 'Marissa', 'Orlando', 'Sonia', 
                            'Orlandito', 'Liz', 'Rossana', 'Jaime', 'Angelica', 'Italo', 
                            'Jorgito', 'Angie', 'Alicia']
    
    for participant in initial_participants:
        if participant not in db:
            db[participant] = []
    
    return "Names initialized!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
