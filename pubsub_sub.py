from google.cloud import pubsub

def callback(message):
    print(message.data)
    message.ack()

project_id = "securesmartmetering"
topic_name = "sm1"
subscription_name = "sm1"

subscriber = pubsub.SubscriberClient()
topic = "projects/{}/topics/{}".format(project_id, topic_name)

subscription_name = 'projects/{}/subscriptions/{}'.format(project_id, subscription_name)

subscription = subscriber.subscribe(subscription_name)
future = subscription.open(callback)

try:
    future.result()
except Exception as ex:
    subscription.close()
    raise
