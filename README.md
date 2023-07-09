# A FastAPI, Kafka, and Faust mini-project
A basic use case for how to leverage [Kafka](https://developer.confluent.io/quickstart/kafka-on-confluent-cloud/?_gl=1*54cy62*_ga*MTMzMjc1NjEyOS4xNjg4NDA2MDIx*_ga_D2D3EGKSGD*MTY4ODg0MjE5NC4xMC4xLjE2ODg4NDIyMDUuNDkuMC4w&_ga=2.79874967.1247302559.1688842194-1332756129.1688406021) and [Faust](https://faust.readthedocs.io/en/latest/playbooks/quickstart.html) for streaming events from a FastAPI application.
<br></br>
![Alt text](assets/inarious.png?raw=true "Diagram")
<br></br>
This Project uses docker and docker compose to create a development environment.
Run the docker compose file with:
```commandline
docker compose -f ./docker/docker-compose.yml up -d
```
The idea for this project was to keep the use case simple and focus on how these technologies can work together 
to create a real-time data streaming application.
<br></br>
We are creating a `Users` collection in Arangodb to store user information.
The REST API (a.k.a Inarious) only has a GET and POST REST endpoint for the Users resource.
Anytime a client uses an endpoint an activity event message is created, serialized with protobuf 
and send to the `Users` Kafka topic.
Then the Faust worker service will be consuming the `Users` topic 
and deserializing the incoming messages using protobuf.
<br></br>
Once the Faust worker has received the message it can proceed to perform a task or event based on that message.
For example in this case it will be receiving the below structured data:
```commandline
message BackendApiActivity {
    string client_host = 1;
    string client_port = 2;
    string endpoint = 3;
    string http_method = 4;
}
```
This data could then be aggregated to track the users api usage and populate a dashboard graph.
These graphs could then be used to see in real time what resources the user is using the most.
<br></br>
This was a fun mini-project to help me learn more about Kafka, pub-sub systems and protobuf.
I hope this can be helpful to someone else as well, and I have linked to some resources I needed to use below
to build this application.


# Development Notes
## Protobuf
Need to install the protoc compiler first.
I am using an Ubuntu 20.04 OS, so you may need to adjust the below command accordingly, 
see [Protobuf Releases](https://github.com/protocolbuffers/protobuf/releases)
to find the release compatible with your OS and replace the `PROTOC_ZIP` and `PROTOC_VERSION` variables in the below
command: 
```commandline
PROTOC_ZIP=protoc-23.4-linux-x86_64.zip
PROTOC_VERSION=v23.4
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/$PROTOC_VERSION/$PROTOC_ZIP
sudo unzip -o $PROTOC_ZIP -d /usr/local bin/protoc
sudo unzip -o $PROTOC_ZIP -d /usr/local 'include/*'
rm -f $PROTOC_ZIP
```
To generate usable integration code, we use the proto compiler which compiles a given
`.proto` file into language-specific integration classes. 
For Python we can use the below command:
```commandline
protoc -I=. --python_out=. ./example.proto
```

# Where to go from here
I will continue to update this repo and use it to expand the current simple use case with:
* CI
* dashboard interface for the real-time data stream.
* kafka schema registry.
* more friendly development setup environment (i.e. mounting the fast api project folder).
* expand more into Arangodb's multi-model system and build a basic graph database.

# Resources
### FastAPI
* [Medium Project Structure](https://stackoverflow.com/questions/64943693/what-are-the-best-practices-for-structuring-a-fastapi-project)
* [Large Project Structure](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
### Protobuf
* [protoc Linux Installation](http://google.github.io/proto-lens/installing-protoc.html)
* [How to use Protobuf in Python](https://www.freecodecamp.org/news/googles-protocol-buffers-in-python/)
### Faust
* [Faust Quick Start](https://faust.readthedocs.io/en/latest/playbooks/quickstart.html)
* [Faust Protobuf Serialization Troubleshooting](https://stackoverflow.com/questions/64686686/using-python-compiled-protobuf-pb2-as-key-and-value-serializer)
