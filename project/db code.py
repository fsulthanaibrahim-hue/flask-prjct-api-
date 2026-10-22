# connect that app.py code to database(this page)
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 1. Configure the database file location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Initialize the database object
db = SQLAlchemy(app)

# 3. Define the Database Table Structure (Schema)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)

    # Helper method to convert database records into Python dictionaries (JSON)
    def to_dict(self):
        return {"id": self.id, "name": self.name, "image": self.image}

# 4. Create the actual database file and tables automatically on startup
with app.app_context():
    db.create_all()

# --- DATABASE CRUD OPERATIONS ---

# CREATE: Add a new item to the database
@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json or 'image' not in request.json:
        abort(400, description="Missing 'name' or 'image' in request body.")
    
    new_item = Item(name=request.json['name'], image=request.json['image'])
    db.session.add(new_item)
    db.session.commit() # Saves permanently to database.db
    return jsonify(new_item.to_dict()), 201

# READ ALL: Fetch all items from the database
@app.route('/api/items', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items]), 200

# READ ONE: Fetch a single item using its database ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found.")
    return jsonify(item.to_dict()), 200

# UPDATE: Edit an item's details in the database
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found.")
    if not request.json:
        abort(400, description="Invalid JSON payload.")
        
    item.name = request.json.get('name', item.name)
    item.image = request.json.get('image', item.image)
    
    db.session.commit() # Saves the updates permanently
    return jsonify(item.to_dict()), 200

# DELETE: Remove an item from the database
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found.")
    
    db.session.delete(item)
    db.session.commit() # Deletes permanently from database.db
    return jsonify({"message": f"Item {item_id} successfully deleted from database."}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
