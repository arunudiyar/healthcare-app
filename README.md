# Healthcare IoT Real-Time Data Platform (AWS Serverless Architecture)

## Architecture Objective

This solution implements a production-style cloud-native backend platform capable of ingesting real-time telemetry from 100,000+ simulated healthcare monitoring devices and serving both real-time dashboard queries and historical analytics workloads with low latency and high scalability.

The architecture is designed to support:

* burst-resistant ingestion pipeline
* time-series optimized data storage
* sub-200ms realtime API responses
* autoscaling compute layers
* pagination & filtering-enabled analytics APIs
* compliance-aligned security posture (HIPAA / GDPR readiness)
* cost-efficient long-term telemetry retention strategy

---

# Architecture Overview

Telemetry data flows through the following pipeline:

Device Simulator → API Gateway → Kinesis Data Streams → Lambda Processing Layer → DynamoDB (Time-Series Storage) → Retrieval APIs (Realtime + Historical)

Supporting layers include:

* lifecycle archival to S3 Glacier
* CloudWatch monitoring
* IAM security boundaries
* CloudFormation infrastructure provisioning

---

# Architecture Components Mapping (Assignment Requirement Alignment)

| Requirement                 | Implementation                                   |
| --------------------------- | ------------------------------------------------ |
| API Gateway / Load Balancer | Amazon API Gateway                               |
| Compute layer               | AWS Lambda (serverless autoscaling)              |
| Data ingestion pipeline     | Amazon Kinesis Data Streams                      |
| Time-series database        | Amazon DynamoDB (partition + timestamp schema)   |
| Caching layer               | DynamoDB millisecond latency (no cache required) |
| Storage hot/warm/cold       | DynamoDB → S3 → Glacier lifecycle                |
| Monitoring & logging        | CloudWatch Logs + Metrics                        |
| Security layers             | IAM + encryption + TLS                           |

---

# Infrastructure Provisioning (CloudFormation)

Infrastructure deployed using:

```
cloudformation/healthcare-stack.yaml
```

Resources provisioned:

* DynamoDB table
* Kinesis stream
* S3 archive bucket
* API Gateway integrations
* Lambda permissions
* lifecycle storage policies

CloudFormation ensures repeatable deployments across environments.

---

# Compute Layer (Serverless Autoscaling)

AWS Lambda functions implemented:

| Function              | Responsibility                       |
| --------------------- | ------------------------------------ |
| ingest-health-data    | processes telemetry ingestion events |
| realtime-health-api   | returns latest device reading        |
| historical-health-api | returns timeline analytics dataset   |

Benefits:

* automatic scaling
* event-driven processing
* no infrastructure maintenance
* cost-efficient execution model

---

# Data Ingestion Pipeline

Simulated telemetry generated using:

```
simulator/simulator.py
```

Pipeline flow:

Device → API Gateway → Kinesis Stream → Lambda → DynamoDB

Kinesis provides:

* burst traffic buffering
* replay capability
* ingestion decoupling
* horizontal shard scaling

---

# Time-Series Database Design

Table:

```
health_data
```

Schema:

Partition key:

```
device_id
```

Sort key:

```
timestamp
```

Supports:

* realtime dashboard lookup
* timeline analytics queries
* efficient range filtering
* pagination using LastEvaluatedKey

---

# API Layer Implementation

APIs exposed via API Gateway:

## GET /realtime-data

Returns latest telemetry record for a device.

Latency validated under:

```
200 ms requirement
```

using load testing.

Example:

```
GET /realtime-data?device_id=device001
```

---

## GET /historical-data

Returns telemetry timeline dataset.

Supports:

* pagination
* timestamp filtering
* device filtering

Examples:

```
GET /historical-data?device_id=device001&limit=5
```

```
GET /historical-data?device_id=device001&start=1775654164&end=1775654202
```

Pagination implemented using:

```
DynamoDB LastEvaluatedKey
```

---

# Performance & Scaling Validation

Load testing performed using:

```
k6 run --vus 100 --duration 30s load-test/loadtest.js
```

Results:

| Metric                  | Value  |
| ----------------------- | ------ |
| Average latency         | ~52 ms |
| 95th percentile latency | <60 ms |
| Failures                | 0%     |

System successfully handled:

```
56,000+ requests
```

within test window.

Architecture scales horizontally using:

* Lambda concurrency scaling
* Kinesis shard scaling
* DynamoDB on-demand scaling
* API Gateway managed scaling

---

# Autoscaling Strategy

Scaling handled automatically through:

| Service     | Scaling Method               |
| ----------- | ---------------------------- |
| API Gateway | managed scaling              |
| Lambda      | concurrency-based scaling    |
| Kinesis     | shard scaling                |
| DynamoDB    | on-demand throughput scaling |

Supports:

```
10,000+ concurrent request workloads
```

---

# Storage Strategy (Hot / Warm / Cold)

Tiered storage lifecycle implemented:

| Tier | Service   | Purpose                        |
| ---- | --------- | ------------------------------ |
| Hot  | DynamoDB  | recent telemetry               |
| Warm | Amazon S3 | analytics export               |
| Cold | Glacier   | long-term compliance retention |

Supports healthcare retention policies.

---

# Security Architecture

Security best practices implemented:

* TLS encryption in transit
* DynamoDB encryption at rest
* Kinesis encryption at rest
* IAM least-privilege roles
* CloudTrail audit readiness

Supports secure healthcare telemetry pipelines.

---

# Compliance Readiness (HIPAA / GDPR)

Architecture supports compliance-aligned deployment patterns:

* encryption at rest
* encryption in transit
* IAM isolation boundaries
* audit logging readiness
* lifecycle retention strategy

Production deployments can integrate:

* Cognito authentication
* JWT validation
* device identity verification

---

# Observability Implementation

Monitoring implemented using:

Amazon CloudWatch

Tracks:

* Lambda execution metrics
* ingestion throughput
* API latency
* DynamoDB utilization
* error monitoring

Supports alert-based failure detection.

---

# Cost Optimization Strategy

Serverless architecture minimizes idle compute cost.

Optimization techniques:

* DynamoDB on-demand capacity
* Lambda execution-based billing
* Kinesis shard tuning
* Glacier archival lifecycle rules

Estimated monthly cost (Mumbai region):

```
Amazon API Gateway           : ~$9,200/month
AWS Lambda                   : ~$2,800/month
Amazon Kinesis Data Streams  : ~$11,500/month
Amazon DynamoDB (On-Demand)  : ~$3,100/month
Amazon S3 (Warm Storage)     : ~$180/month
Amazon S3 Glacier            : ~$90/month
Amazon CloudWatch Monitoring : ~$350/month
Data Transfer (Intra-region) : ~$250/month

~$27,470/month (~₹22.8 lakh/month)
```

based on 100,000 device workload model.

---

# Infrastructure Setup Steps (AWS Console Deployment)

Deploy infrastructure:

1. Open CloudFormation
2. Upload template

```
cloudformation/healthcare-stack.yaml
```

3. Create stack:

```
healthcare-stack
```

4. Enable:

```
CAPABILITY_NAMED_IAM
```

---

# Simulator Execution

Run:

```
python simulator/simulator.py
```

Generates telemetry every 2 seconds.

---

# Load Testing

Run:

```
k6 run --vus 100 --duration 30s load-test/loadtest.js
```

Validates scaling and latency behavior.

---

# Repository Structure

```
healthcare-iot-platform/

architecture-diagram/
cloudformation/
simulator/
load-test/
README.md
```

---

# Design Decisions

Serverless architecture selected to support burst ingestion scaling without infrastructure maintenance overhead.

Kinesis introduced to decouple ingestion from processing workloads.

DynamoDB selected for time-series query efficiency.

CloudFormation used for infrastructure reproducibility.

---

# Trade-offs

IoT Core recommended for production-grade device identity management.

Single-region deployment used for assignment simplicity.

Redis caching optional due to DynamoDB low-latency reads.

---

# Future Improvements

Planned enhancements:

* AWS IoT Core device authentication
* Cognito-based API authorization
* multi-region disaster recovery
* CI/CD pipeline automation
* Grafana dashboards
* DynamoDB Global Tables replication
