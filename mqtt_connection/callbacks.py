from datetime import datetime
from core import Core
from keywords import keyword_mapping
from mqtt_publisher.publisher import publish
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv(override=True)


REQ_TOPIC = os.getenv("REQ_TOPIC")
core = Core()

DUPLICATED_CONTACT_HANDLER_TOPIC = f"{REQ_TOPIC}/duplicated"
SELECT_CONTACT_HANDLER_TOPIC = f"{REQ_TOPIC}/select_contact"

def send_message_to_contact(data: dict) -> None:
    headers = {'Content-Type': 'application/json'}
    requests.post(f"{os.getenv('WHATSAPP_REST_HOST')}/send-message?token={os.getenv('WHATSAPP_REST_SECRET')}", json=data, headers=headers)
    publish("stop", "/tts/stop")
    return;

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} connected to broker sucessfully")
        client.subscribe(REQ_TOPIC)
        client.subscribe(DUPLICATED_CONTACT_HANDLER_TOPIC)
        client.subscribe(SELECT_CONTACT_HANDLER_TOPIC)
        
    else:
        print(f"Connection failed with code {rc}")
        
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} subscribed to topic with mid {mid} and QOS {granted_qos} on {REQ_TOPIC}")
    

def on_message(client, userdata, message):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] Received a message on topic {message.topic}")
    
    if core._is_selecting_contact:
        if message.topic == SELECT_CONTACT_HANDLER_TOPIC:
            message_as_string = message.payload.decode()
            message_as_number = int(message_as_string)
            selected_contact = core._contacts[message_as_number - 1]
            data = {
                "chatName": selected_contact['chat_name'],
                "chatId": selected_contact['chat_id'],
                "sessionName": selected_contact['session_name'],
                "message": core._message_to_send
            }
            send_message_to_contact(data)
            core._is_selecting_contact = False
            return;
        return;
    
    if message.topic == DUPLICATED_CONTACT_HANDLER_TOPIC:
        message_as_string = message.payload.decode()
        message_as_dict = json.loads(message_as_string)
        core.run("duplicated_contacts", message_as_dict)
        return;
    
    
    message_payload = message.payload.decode()
    splitted_message_payload = message_payload.split(" ")
    action = keyword_mapping.get(splitted_message_payload[0].lower())        
    message_payload_no_action = " ".join(splitted_message_payload[1:])
    
    try:
        if message_payload_no_action:
            core.run(action, message_payload_no_action)
        else:
            core.run(action)
    except ValueError as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {e}")
        
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] Message payload: {message.payload.decode()}")
    