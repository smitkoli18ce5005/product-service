from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://mongodb.default.svc.cluster.local:27017/')
db = client['product_database']
collection = db['product_collection']


@app.route('/', methods=['GET'])
def health():
    try:
        return 'Application is running!', 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/add', methods=['POST'])
def product_add():
    try:
        uniqueId = ObjectId()

        product_object = {
            "_id": uniqueId,
            "productId": uniqueId,
            "productName": request.form.get('productName'),
            "productDescription": request.form.get('productDescription'),
            "productPrice": request.form.get('productPrice'),
            "productDiscountPercent": request.form.get('productDiscountPercent'),
            "productCategory": request.form.get('productCategory'),
            "productImage": request.form.get('productImage')
        }

        result = collection.insert_one(product_object)

        if result.inserted_id:
            return jsonify({'message': 'Data added successfully', 'productId': str(uniqueId)}), 201
        else:
            return jsonify({'error': 'Failed to add data'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/list', methods=['GET'])
def product_list():
    try:
        products = list(collection.find())

        for product in products:
            product['_id'] = str(product['_id'])
            product['productId'] = str(product['productId'])

        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/list/<productId>', methods=['GET'])
def product_list_id(productId):
    try:
        if not productId:
            return jsonify({'error': 'Product ID is required'}), 400

        product = collection.find_one({'productId': ObjectId(productId)})

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product['_id'] = str(product['_id'])
        product['productId'] = str(product['productId'])
        return jsonify(product), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/delete/<productId>', methods=['DELETE'])
def delete_product(productId):
    try:
        if not productId:
            return jsonify({'error': 'Product ID is required'}), 400

        result = collection.delete_one({'productId': ObjectId(productId)})

        if result.deleted_count == 0:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/product/update/<productId>', methods=['PATCH'])
def update_product(productId):
    try:
        if not productId:
            return jsonify({'error': 'Product ID is required'}), 400

        product = collection.find_one({'productId': ObjectId(productId)})

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product['productName'] = request.form.get('productName') or product['productName']
        product['productDescription'] = request.form.get('productDescription') or product['productDescription']
        product['productPrice'] = request.form.get('productPrice') or product['productPrice']
        product['productDiscountPercent'] = request.form.get('productDiscountPercent') or product['productDiscountPercent']
        product['productCategory'] = request.form.get('productCategory') or product['productCategory']
        product['productImage'] = request.form.get('productImage') or product['productImage']

        result = collection.update_one({'productId': product['productId']}, {'$set': product})

        if result.modified_count == 0:
            return jsonify({'error': 'Product contains same data or is not found'}), 404

        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

