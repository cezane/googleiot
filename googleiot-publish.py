import paho.mqtt.client as mqtt
import ssl, random, jwt_maker
from time import sleep

root_ca = './certs/roots.pem'
public_crt = './certs/rsa_cert.pem'
private_key = './certs/rsa_private.pem'

mqtt_url = "mqtt.googleapis.com"
mqtt_port = 8883
mqtt_topic = "/devices/sm1/events" #"projects/securesmartmetering/topics/sm1"
project_id   = "securesmartmetering"
cloud_region = "us-central1"
registry_id  = "sm1"
device_id    = "sm1"

connflag = False

def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return "Some error occurred. {}: {}".format(rc, mqtt.error_string(rc))

def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print("on_disconnect", error_str(rc))

def on_connect(client, userdata, flags, response_code):
    global connflag 
    connflag = True   
    print("Connected with status: {0}  --  msg: {1}".format(response_code,mqtt.connack_string(response_code)))

def on_publish(client, userdata, mid):
    print("User data: {0} -- mid: {1}".format(userdata, mid))
    #client.disconnect()

if __name__ == "__main__":
    print("Loaded MQTT configuration information.")
    print("Endpoint URL: {0}".format(mqtt_url))
    print("Root Cert: {0}".format(root_ca))
    print("Device Cert: {0}".format(public_crt))
    print("Private Key: {0}".format(private_key))   
 
    client = mqtt.Client("projects/{}/locations/{}/registries/{}/devices/{}".format(
                         project_id,
                         cloud_region,
                         registry_id,
                         device_id), protocol=mqtt.MQTTv311)

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
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    print("Connecting to Google IoT Broker...")
    client.connect(mqtt_url, mqtt_port, keepalive=60)
    client.loop_start()
    #client.loop_forever()

    while 1==1:
        sleep(2.5)
        print connflag
        if connflag == True:
            print("Publishing...")
            ap_measurement = random.uniform(25.0, 150.0)
            #payload = "sm1/sm1-payload-{}".format(ap_measurement)
            res = client.publish(mqtt_topic, ap_measurement, qos=1)
            print("---- {}".format(res.is_published()))
            if not res.is_published():
               print("Data not published!!")
            else:
               print("ActivePower published: %.2f" % ap_measurement)
        else:
            print("Waiting for connection...")


