import paho.mqtt.client as mqtt
import ssl, random, jwt_maker
from time import sleep

root_ca = './certs/roots.pem'
public_crt = './certs/rsa_cert.pem'
private_key = './certs/rsa_private.pem'

pubsub_url = "pubsub.googleapis.com" #"mqtt.googleapis.com"
pubsub_port = 443
topic = "projects/myproject/topics/sm1"
subscription_name = "projects/myproject/subscriptions/sm1"
project_id   = "securesmartmetering"
cloud_region = "us-central1"
registry_id  = "sm1"
device_id    = "sm1"

def on_connect(client, userdata, flags, response_code):
    print("Connected with status: {0}".format(response_code))
    client.subscribe("subscription_name", 1)

def on_message(client, userdata, msg):
    print "------ON MESSAGE!!!!"
    print("Topic: {0} -- Payload: {1}".format(msg.topic, str(msg.payload)))

if __name__ == "__main__":
    print "Loaded MQTT configuration information."
    print("Endpoint URL: {0}".format(pubsub_url))
    print("Root Cert: {0}".format(root_ca))
    print("Device Cert: {0}".format(public_crt))
    print("Private Key: {0}".format(private_key))
    
    client = mqtt.Client("projects/{}/locations/{}/registries/{}/devices/{}".format(
                         project_id,
                         cloud_region,
                         registry_id,
                         device_id))
    
    client.username_pw_set(username='unused',
                           password=jwt_maker.create_jwt(project_id,
                                               private_key,
                                               algorithm="RS256"))
    client.tls_set(root_ca, 
                   certfile = public_crt, 
                   keyfile = private_key, 
                   cert_reqs = ssl.CERT_REQUIRED, 
                   tls_version = ssl.PROTOCOL_TLSv1_2, 
                   ciphers = None)

    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to Google IoT Broker...")
    client.connect(pubsub_url, pubsub_port, keepalive=60)
    client.loop_forever()

