from zeroless import (Server, Client)

# Connects the client to as many servers as desired
client = Client()
client.connect_local(port=9876)

# Initiate a subscriber client
# Assigns an iterable to wait for incoming messages with the topic 'sh'
listen_for_pub = client.sub()

for x in listen_for_pub:
    print(x)