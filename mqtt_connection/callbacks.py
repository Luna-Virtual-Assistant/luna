from datetime import datetime
from core import Core
from keywords import keyword_mapping
from mqtt_publisher.publisher import publish
import os
from dotenv import load_dotenv
import json

load_dotenv(override=True)


REQ_TOPIC = os.getenv("REQ_TOPIC")
core = Core()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} connected to broker sucessfully")
        client.subscribe(REQ_TOPIC)
        client.subscribe("/luna/duplicated")
        client.subscribe("/luna/select_contact")
        
    else:
        print(f"Connection failed with code {rc}")
        
def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] {client._client_id.decode()} subscribed to topic with mid {mid} and QOS {granted_qos} on {REQ_TOPIC}")
    

def on_message(client, userdata, message):
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] Received a message on topic {message.topic}")
    
    if core._is_selecting_contact:
        if message.topic == "/luna/select_contact":
            message_as_string = message.payload.decode()
            message_as_number = int(message_as_string)
            selected_contact = core._contacts[message_as_number - 1]
            data = {
                "contact": selected_contact,
                "message": core._message_to_send
            }
            stringified_data = json.dumps(data)
            publish(stringified_data, "/whatsapp/duplicated")
            core._is_selecting_contact = False
            return;
        return;
    
    if message.topic == "/luna/duplicated":
        message_as_string = message.payload.decode()
        message_as_dict = json.loads(message_as_string)
        core.run("duplicated_contacts", message_as_dict)
        return;
    
    
    message_payload = message.payload.decode()
    splitted_message_payload = message_payload.split(" ")
    action = keyword_mapping.get(splitted_message_payload[0])        
    message_payload_no_action = " ".join(splitted_message_payload[1:])
    if message_payload_no_action:
        core.run(action, message_payload_no_action)
    else:
        core.run(action)
    print(f"[{datetime.now().strftime('%Y-%m-%d - %H:%M:%S')}] Message payload: {message.payload.decode()}")
    