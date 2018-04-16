# googleiot
A basic pub/sub application to test the Google Cloud IoT Core and Pub/Sub services.

####Device registry:

  1. In the Google Cloud IoT Core page (GCP Console), click "Create device registry.";
  2. Enter "registry_id" for the Registry ID;
  3. Choose "us-central1" for the Cloud region;
  4. Choose "MQTT" for the Protocol;
  5. In the "Telemetry topic" dropdown list, select "Create a topic";
  6. In the "Create a topic" dialog, enter "topic_name" in the Name field;
  7. Click "Create" in the dialog;
  8. Leave the Device state topic and Certificate value fields blank, since they are optional.
  9. Click Create on the Cloud IoT Core page.

####Device addition:

  1. Click "Add device" on the Registry Details;
  2. Enter "device_id" for the Device ID;
  3. Select "Allow" for Device communication;
  4. Since Authentication and Device metadata are optional, leave them blank or use default values;
  5. Click Add.

####Associate a public key to a device

  1. To create an RSA256 key with 2048 bits, run the following command in the terminal (if you want to set your own information, just ommit the "-subj" param):

    openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes \
    -out rsa_cert.pem -subj "/CN=unused"

  2. On the Device details page, for your created device, click "Add public key";
  3. Choose Upload and select "RS256_X509". Search by your "rsa_cert.pem" file and select it;
  4. Click Add.

####MQTT Server

  * The GCP supports the MQTT protocol with a broker running on `mqtt.googleapis.com:8883`. The port `443` can also be used;
  * Unfortunately, according to Google Cloud documentation: "the managed MQTT bridge run by Cloud IoT Core does not support all publish/subscribe operations, such as creating arbitrary topics that devices can use to send messages between them";
  * To connect an MQTT client, the full device path must be specified:

    projects/{project-id}/locations/{cloud-region}/registries/{registry-id}/devices/{device-id}

  *
