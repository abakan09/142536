from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Данные для API amoCRM
AMOCRM_DOMAIN = "https://abaertas01.amocrm.ru"
ACCESS_TOKEN = "ТВОЙ_ТОКЕН"

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
