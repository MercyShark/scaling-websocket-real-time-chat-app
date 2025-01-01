import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Publish a message to a channel
channel = 'my_channel'
message = 'Hello, Redis!'
r.publish("channel_1", message)

print(f"Published message: {message} to channel: {channel}")
