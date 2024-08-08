import requests
from flask import Flask, request

app = Flask(__name__)

SHOPIFY_API_KEY = 'your_api_key'
SHOPIFY_PASSWORD = 'your_api_password'
SHOPIFY_STORE_NAME = 'your_shop_name'
SHOPIFY_API_VERSION = '2024-01'  # Replace with the desired API version
SHOPIFY_API_URL = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_NAME}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}/products.json"

@app.route('/')
def index():
    return '''
        <h2>Product Form</h2>
        <form action="/submit" method="POST">
            <label for="productName">Product Name:</label><br>
            <input type="text" id="productName" name="productName"><br><br>

            <label for="productDescription">Description:</label><br>
            <input type="text" id="productDescription" name="productDescription"><br><br>

            <label for="productPrice">Price:</label><br>
            <input type="text" id="productPrice" name="productPrice"><br><br>

            <label for="productSKU">SKU:</label><br>
            <input type="text" id="productSKU" name="productSKU"><br><br>

            <label for="productInventory">Inventory:</label><br>
            <input type="text" id="productInventory" name="productInventory"><br><br>

            <input type="submit" value="Submit">
        </form>
    '''

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect form data
    product_name = request.form['productName']
    product_description = request.form['productDescription']
    product_price = request.form['productPrice']
    product_sku = request.form['productSKU']
    product_inventory = request.form['productInventory']

    # Prepare data to be sent to Shopify
    product_data = {
        "product": {
            "title": product_name,
            "body_html": f"<strong>{product_description}</strong>",
            "vendor": "Your Brand",
            "product_type": "Widget",
            "variants": [
                {
                    "option1": "Default",
                    "price": product_price,
                    "sku": product_sku,
                    "inventory_quantity": int(product_inventory)
                }
            ]
        }
    }

    # Send data to Shopify
    headers = {"Content-Type": "application/json"}
    response = requests.post(SHOPIFY_API_URL, json=product_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:
        return f"Product created successfully! Response: {response.json()}"
    else:
        return f"Failed to create product. Error: {response.status_code} - {response.text}"

if __name__ == '__main__':
    app.run(debug=True)
