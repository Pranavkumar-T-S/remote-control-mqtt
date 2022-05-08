import paho.mqtt.client as mqtt
import logging
import state_handler as js 
import gpio_handler
from  credentials import *


Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logger = logging.basicConfig(filename="logfile.log",
                             filemode="a",
                             format=Log_Format,
                             level=logging.INFO)
logger = logging.getLogger()


def is_connected(client):
    client.publish("emblab/iotremote/rpi/statusreply",
                   payload="yes, rpi is connected ", qos=1)


def change_state(lvl1, lvl2, thing, value):
    state = js.retrieve_state()
    try:
        state[lvl1][lvl2][thing] = value
        gpio_handler.switch_state(thing,state[thing])
        logger.critical(f'{thing} state changed to {value}')
    except ValueError:
        logger.error("invalid thing")
        pass
    js.save_state(state)


def status(client, lvl1, lvl2, thing):
    state = js.retrieve_state()
    try:
        thing_status = state[lvl1][lvl2][thing]
        client.publish("emblab/iotremote/"+thing +
                       "/statusreply", thing_status, qos=1)
    except KeyError:
        client.publish("emblab/iotremote/"+thing + "/statusreply",
                       "thing not mentioned in state.json", qos=1)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("emblab/iotremote/#", qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" ", msg.payload)
    try:
        [lvl1, lvl2, thing, purpose] = msg.topic.split('/')
        pl = msg.payload.decode()
        print('payload', pl)
        if thing == 'rpi' and purpose == 'status':
            is_connected(client)
        elif purpose == 'status':
            status(client, lvl1, lvl2, thing)
        elif purpose == "state":
            change_state(lvl1, lvl2, thing, pl)
    except ValueError:
        # client.publish(msg.topic, payload="wrong topic",qos=1)
        pass

gpio_handler.initialize(js.state)
client = mqtt.Client(client_id=clientid, clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)
client.will_set("emblab/iotremote/rpi/statusreply",
                payload="raspberrypi disconnected", qos=1)

client.connect(cluster_url, 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
