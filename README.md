# Understanding How to Deploy Kafka Clusters and Kafka-UI in Docker

## Architecture

<img src="images/Kafka Docker.png" width="500">

## Docker Network

### Create a network `kafka-network` first so all containers will connect to each other

### `docker network create kafka-network`

```yaml
networks:
  kafka-network:
    external: true
```

## Kafka Clusters

### 2 Kafka Clusters `kafka-0` and `kafka-1` are created using Bitnami Kafka image

### `kafka-0` port 9094 and `kafka-1` port 9095 are exposed to the host

### Some key notes about the ENV variables

1. KAFKA_CFG_NODE_ID: Each Nodes must have different ID.
2. KAFKA_CFG_CONTROLLER_QUORUM_VOTERS: `Node ID`@`Container Name`:9093 .
3. KAFKA_KRAFT_CLUSTER_ID: All Kafka Nodes must have similar Cluster ID.
4. KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR: Set at max the number of total of Kafka Nodes.
5. KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR= Set at max the number of total of Kafka Nodes.

```yaml
kafka-0:
image: 'bitnami/kafka:latest'
hostname: kafka-0
networks:
    - kafka-network
ports:
    - '9094:9094'
environment:
    # KRaft settings
    - KAFKA_CFG_NODE_ID=0 
    - KAFKA_CFG_PROCESS_ROLES=controller,broker
    - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093,1@kafka-1:9093
    - KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv
    # Listeners
    - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094 #2
    - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-0:9092,EXTERNAL://localhost:9094 #3
    - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT #4
    - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    # Clustering
    - KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=2
    - KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=2
    - KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1
volumes:
    - ./kafka-0:/bitnami/kafka

kafka-1:
image: 'bitnami/kafka:latest'
hostname: kafka-1
networks:
    - kafka-network
ports:
    - '9095:9095'
environment:
    # KRaft settings
    - KAFKA_CFG_NODE_ID=1
    - KAFKA_CFG_PROCESS_ROLES=controller,broker
    - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-0:9093,1@kafka-1:9093
    - KAFKA_KRAFT_CLUSTER_ID=abcdefghijklmnopqrstuv
    # Listeners
    - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9095 #2
    - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-1:9092,EXTERNAL://localhost:9095 #3
    - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT #4
    - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
    # Clustering
    - KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=2
    - KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=2
    - KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1
volumes:
    - ./kafka-1:/bitnami/kafka
```

## Kafka-UI

## Connects to both Kafka Nodes at port 9092

```yaml
kafka-ui:
image: 'provectuslabs/kafka-ui:latest'
networks:
    - kafka-network
ports:
    - '8080:8080'
environment:
    - KAFKA_CLUSTERS_0_NAME=local-kafka-cluster
    - KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka-0:9092,kafka-1:9092
depends_on:
    - kafka-0
    - kafka-1
```
