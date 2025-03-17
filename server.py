from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/get_order_number", methods=["GET"])
def get_order_number():
    return jsonify({"order_number": 21000})  # Тестовый ответ

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Данные для API amoCRM
AMOCRM_DOMAIN = "https://abaertas01.amocrm.ru"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImY0ZmMxZTI3MjU2MDBkMzI0Y2VhNmIxODhkY2EwNGYzZjVkNjRlNmFmMDQ1NWJlZmRmMWUyOTQ1YWIwMzQxY2Q2M2RkYjBjZDgwZWRlYmQ4In0.eyJhdWQiOiI5ZWU0MjdkOS05ODM5LTRhYmUtODgzNy1jYjk5MGM1ZDc1YTQiLCJqdGkiOiJmNGZjMWUyNzI1NjAwZDMyNGNlYTZiMTg4ZGNhMDRmM2Y1ZDY0ZTZhZjA0NTViZWZkZjFlMjk0NWFiMDM0MWNkNjNkZGIwY2Q4MGVkZWJkOCIsImlhdCI6MTc0MjI1Mjk4MCwibmJmIjoxNzQyMjUyOTgwLCJleHAiOjE3NzUzNDcyMDAsInN1YiI6IjgzNDgxMzciLCJncmFudF90eXBlIjoiIiwiYWNjb3VudF9pZCI6MzA0MDkyMzEsImJhc2VfZG9tYWluIjoiYW1vY3JtLnJ1IiwidmVyc2lvbiI6Miwic2NvcGVzIjpbImNybSIsImZpbGVzIiwiZmlsZXNfZGVsZXRlIiwibm90aWZpY2F0aW9ucyIsInB1c2hfbm90aWZpY2F0aW9ucyJdLCJoYXNoX3V1aWQiOiJjY2ZmN2ViMy1hNmZkLTQwNzMtYTUyZC01MmU4OTAyMzllNjIiLCJhcGlfZG9tYWluIjoiYXBpLWIuYW1vY3JtLnJ1In0.HdfdJmSjjTpZpClXxcaYs6ZbRCoMqxFA_89ahmYLZJZzuoqu3CF9dywpp_xx-5v5Dl6Z17ylyoZr1xGQFmz5lIYh5dn-be6hS-EoiJ84STWNMk-XKn-Kah8B0PvlKuFoph7DfNzblqmDrLFplTKPyGRC1C2HxAUNPmY_gE81XfAUpm5NAYxvP5OOe2eQ6Uxy4jGp4XxLwJGZ6WwfH5aA2O9cPmEHX27n4DDnenGmX2Jm1uDwzy1ZEQ_uqTRhDgJXZN9UB6zn5x4kBPSK0r14esp63c9X1RTl8VnPPltSGDTS7_sbPZC0mE4D0WbtFlrhZ8rNb1Ru9VUPDnJpte8Bxw"

# ID сделки, где хранится глобальный счётчик
GLOBAL_LEAD_ID = 29908361
COUNTER_FIELD_ID = 1442913

def get_counter():
    """ Получаем текущее значение счётчика в amoCRM """
    url = f"{AMOCRM_DOMAIN}/api/v4/leads/{GLOBAL_LEAD_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for field in data.get("custom_fields_values", []):
            if field["field_id"] == COUNTER_FIELD_ID:
                return int(field["values"][0]["value"])
    return None

def update_counter(new_value):
    """ Обновляем значение счётчика в amoCRM """
    url = f"{AMOCRM_DOMAIN}/api/v4/leads/{GLOBAL_LEAD_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    
    payload = {
        "custom_fields_values": [
            {
                "field_id": COUNTER_FIELD_ID,
                "values": [{"value": str(new_value)}]
            }
        ]
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    return response.status_code == 200

@app.route("/get_order_number", methods=["GET"])
def get_order_number():
    """ API для получения и увеличения номера заказа """
    current_number = get_counter()
    if current_number is None:
        return jsonify({"error": "Ошибка получения счётчика"}), 400
    
    new_number = current_number + 1
    if update_counter(new_number):
        return jsonify({"order_number": new_number})
    else:
        return jsonify({"error": "Ошибка обновления счётчика"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
