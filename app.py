from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv
from flask_cors import CORS     #cors 
import json

app = Flask(__name__)
CORS(app)  # This will allow all domains by default

load_dotenv()
# MySQL Connection Function
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/getReports', methods=['POST'])
def get_reports():
    data = request.get_json()
    if not data or 'userId' not in data:
        return jsonify({"error": "No JSON data provided or userId missing"}), 400

    user_id = data['userId']
    print("user_id:", user_id)

    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to get results as dict
        query = "SELECT reportDetails FROM reports WHERE UserId = %s"
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        if not records:
            return jsonify({"message": "No records found for the given userId"}), 404
        
        # Clean up the data
        cleaned_records = []
        for record in records:
            # Assuming reportDetails is stored as a JSON string in the database
            try:
                report_details = json.loads(record['reportDetails'])
                cleaned_records.append(report_details)
            except json.JSONDecodeError:
                # Handle the case where JSON decoding fails
                return jsonify({"error": "Error decoding JSON data from the database"}), 500
        
        print("api response is:", cleaned_records)
        return jsonify(cleaned_records)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/getSummarizedReport', methods=['POST'])
def get_summarized_report():
    data = request.get_json()
    if not data or 'userId' not in data:
        return jsonify({"error": "No JSON data provided or userId missing"}), 400

    user_id = data['userId']
    print("user_id:", user_id)

    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to get results as dict
        query = "SELECT summarizedData FROM summarized_reports WHERE UserId = %s"
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        if not records:
            return jsonify({"message": "No records found for the given userId"}), 404
        
        # Clean up the data
        cleaned_records = []
        for record in records:
            # Assuming summarizedData is stored as a JSON string in the database
            try:
                summarized_data = json.loads(record['summarizedData'])
                cleaned_records.append(summarized_data)
            except json.JSONDecodeError:
                # Handle the case where JSON decoding fails
                return jsonify({"error": "Error decoding JSON data from the database"}), 500
        
        print("api response is:", cleaned_records)
        return jsonify(cleaned_records)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Default to port 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port, debug=True)