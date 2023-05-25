from flask import Flask, jsonify, request, render_template
import mysql.connector
from dotenv import load_dotenv
import os
import sys
import logging
import simplejson as json


logging.basicConfig(level=logging.DEBUG)

load_dotenv()

S2_HOST = os.getenv('S2_HOST')
S2_USER = os.getenv('S2_USER')
S2_PASS = os.getenv('S2_PASS')
S2_DB = os.getenv('S2_DB')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def init_connection():
    return mysql.connector.connect(**app.config["MYSQL"])

app = Flask (__name__)
app.config["MYSQL"] = {
    "host": S2_HOST,
    "user": S2_USER,
    "password": S2_PASS,
    "database": S2_DB
}

def db_query(query,payload):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        if query == 'get_current_invoice_count':
            query_payload = "SELECT COUNT(*) FROM accounts_receivable;"
            cursor.execute(query_payload)
            rows = cursor.fetchone()[0]
            return rows
        elif query == 'get_payment_stats':
            query_payload = "SELECT * FROM accounts_receivable"
            cursor.execute(query_payload)
            rows = cursor.fetchall()
            PIF = 0
            PARTIAL = 0
            NA = 0
            for r in rows:
                if 'PIF' in r:
                    PIF = PIF + 1
                elif 'PARTIAL' in r:
                    PARTIAL = PARTIAL + 1
                elif 'NA' in r:
                    NA = NA + 1
            inv_stats = {'PIF': PIF, 'PARTIAL': PARTIAL, 'NA': NA}
            return inv_stats
        else:
            query_payload = ( "NOTHING YET")
        
        
        

        # for row in rows:
        #     row_json = json.dumps(row)
        #     app.logger.info(row_json)
        #     app.logger.info(type(row_json))

    except Exception as e:
        print(e)
        return "Error"

@app.route('/')
def home():
    payload = ''
    inv_count = db_query('get_current_invoice_count',payload)
    inv_stats = db_query('get_payment_stats',payload)
    app.logger.info(inv_count)
    if inv_count != "Error":
        return render_template('index.html', num_inv = inv_count, inv_stats = inv_stats)
    else:
        print('Error!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)