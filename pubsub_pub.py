from google.cloud import pubsub

project_id = "securesmartmetering"
topic_name = "sm1"

publisher = pubsub.PublisherClient()
topic = "projects/{}/topics/{}".format(project_id, topic_name)

#publisher.create_topic(topic)
publisher.publish(topic, "Testing pub/sub!", spam="eggs")
