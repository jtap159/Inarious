# A FastAPI, Kafka, and Faust mini-project
A basic use case for how to leverage [Kafka](https://developer.confluent.io/quickstart/kafka-on-confluent-cloud/?_gl=1*54cy62*_ga*MTMzMjc1NjEyOS4xNjg4NDA2MDIx*_ga_D2D3EGKSGD*MTY4ODg0MjE5NC4xMC4xLjE2ODg4NDIyMDUuNDkuMC4w&_ga=2.79874967.1247302559.1688842194-1332756129.1688406021) and [Faust](https://faust.readthedocs.io/en/latest/playbooks/quickstart.html) for streaming events from a FastAPI application.

# Protobuf
Need to install the protoc compiler first: 
```commandline
PROTOC_ZIP=protoc-23.4-linux-x86_64.zip
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v23.4/$PROTOC_ZIP
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


# Resources
* [protoc Linux Installation](http://google.github.io/proto-lens/installing-protoc.html)
