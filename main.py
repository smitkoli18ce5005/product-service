from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['product_database']
collection = db['product_collection']


@app.route('/product/add', methods=['POST'])
def product_add():
    try:
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_description')
        product_price = request.form.get('product_price')
        product_discount_percent = request.form.get('product_discount_percent')
        product_category = request.form.get('product_category')
        product_image = request.form.get('product_image')

        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400

        if collection.find_one({'product_id': product_id}):
            return jsonify({'error': 'Product ID already exists'}), 400

        product_object = {
            "product_id": product_id,
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price,
            "product_discount_percent": product_discount_percent,
            "product_category": product_category,
            "product_image": product_image
        }

        result = collection.insert_one(product_object)

        if result.inserted_id:
            return jsonify({'message': 'Data added successfully', 'product_id': product_id}), 201
        else:
            return jsonify({'error': 'Failed to add data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/list', methods=['GET'])
def product_list():
    try:
        documents = list(collection.find({}, {'_id': 0}))

        return jsonify(documents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/list/<product_id>', methods=['GET'])
def product_list_id(product_id):
    try:
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400

        product = collection.find_one({'product_id': product_id}, {'_id': 0})

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify(product), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400

        result = collection.delete_one({'product_id': product_id})

        if result.deleted_count == 0:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/update', methods=['PATCH'])
def update_product():
    try:
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_description')
        product_price = request.form.get('product_price')
        product_discount_percent = request.form.get('product_discount_percent')
        product_category = request.form.get('product_category')
        product_image = request.form.get('product_image')
        if not product_id:
            return jsonify({'error': 'Product ID is required'}), 400

        updated_data = {
            "product_id": product_id,
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price,
            "product_discount_percent": product_discount_percent,
            "product_category": product_category,
            "product_image": product_image
        }

        result = collection.update_one({'product_id': product_id}, {'$set': updated_data})

        if result.modified_count == 0:
            return jsonify({'error': 'Product contains same data or is not found'}), 404

        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()

