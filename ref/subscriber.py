import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Create a pubsub object
pubsub = r.pubsub()

# Subscribe to the channel
channel = 'my_channel'
pubsub.subscribe(channel)

print(f"Subscribed to channel: {channel}")

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received message: {message['data'].decode('utf-8')} from channel: {message['channel'].decode('utf-8')}")
