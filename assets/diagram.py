# diagram.py
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, EC2
from diagrams.aws.database import RDS
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Zookeeper

with Diagram("Inarious", show=False, direction="TB"):
    rest_api = ECS("REST API")
    database = RDS("Arangodb")
    worker = EC2("Faust Worker")
    with Cluster("Kafka Cluster"):
        zookeeper = Zookeeper("Zookeeper")
        kafka = Kafka("Kafka Broker")
        zookeeper >> kafka

    rest_api >> [kafka,
                 database]
    kafka >> worker
