from flask import Flask, jsonify, request, abort

app = Flask(__name__)

items_db = {
    1: {"id": 1, "name": "Laptop", "image": "https://example.com"},
    2: {"id": 2, "name": "Smartphone", "image": "https://example.com"}
}
current_id = 2

# --- CRUD OPERATIONS ---

# 1. CREATE: Add a new item
@app.route('/api/items', methods=['POST'])
def create_item():
    global current_id
    if not request.json or 'name' not in request.json or 'image' not in request.json:
        abort(400, description="Missing 'name' or 'image' in request body.")
    
    current_id += 1
    new_item = {
        "id": current_id,
        "name": request.json['name'],
        "image": request.json['image']
    }
    items_db[current_id] = new_item
    return jsonify(new_item), 201

# 2. READ All: Get all items
@app.route('/api/items', methods=['GET'])
def get_all_items():
    return jsonify(list(items_db.values())), 200

# 3. READ One: Get a specific item by ID
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = items_db.get(item_id)
    if not item:
        abort(404, description="Item not found.")
    return jsonify(item), 200

# 4. UPDATE: Modify an existing item completely
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = items_db.get(item_id)
    if not item:
        abort(404, description="Item not found.")
    if not request.json:
        abort(400, description="Invalid JSON body.")
        
    item['name'] = request.json.get('name', item['name'])
    item['image'] = request.json.get('image', item['image'])
    
    return jsonify(item), 200

# 5. DELETE: Remove an item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in items_db:
        abort(404, description="Item not found.")
    del items_db[item_id]
    return jsonify({"message": f"Item {item_id} successfully deleted."}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
