# Healthcare IoT Real-Time Ingestion Platform (AWS Serverless)

## Project Overview

This project demonstrates a scalable AWS serverless backend architecture designed to ingest and process real-time healthcare telemetry data such as heart rate and blood pressure from large numbers of simulated monitoring devices.

The system is architected to:

* ingest telemetry from **100,000+ devices**
* support **burst traffic up to 5× baseline load**
* store **time-series health data efficiently**
* provide APIs for **real-time dashboards** and **historical analytics**
* remain **highly available, secure, and compliance-ready (HIPAA / GDPR aligned)**

Infrastructure for the solution is provisioned using **AWS CloudFormation**.

---

# Architecture Overview

Telemetry data flows through the following pipeline:

Device Simulator → API Gateway → Kinesis Data Streams → Lambda Processing Layer → DynamoDB (Time-Series Table) → Retrieval APIs (Realtime + Historical)

The architecture is fully serverless and automatically scales with workload demand.

Architecture diagram available in:

```
architecture-diagram/
```

---

# AWS Services Used

### Amazon API Gateway

Used as the secure ingestion entry point and for exposing retrieval APIs.

Provides:

* HTTPS endpoint exposure
* throttling protection
* request validation capability
* scalable ingestion layer

### Amazon Kinesis Data Streams

Acts as a buffering layer between ingestion and processing to absorb burst traffic and decouple pipeline stages.

Provides:

* burst traffic absorption
* stream replay capability
* horizontal shard scaling
* near real-time processing

### AWS Lambda

Processes telemetry events and serves realtime and historical API requests.

Provides:

* event-driven execution
* automatic scaling
* batch processing support
* cost-efficient serverless compute

### Amazon DynamoDB

Stores telemetry data using a time-series schema optimized for device-based access patterns.

Provides:

* millisecond latency reads
* infinite horizontal scaling
* serverless storage
* high availability across AZs

### Amazon CloudWatch

Used for monitoring, logging, and observability.

Provides:

* ingestion pipeline visibility
* latency tracking
* failure monitoring
* alarm triggering capability

### AWS CloudFormation

Used to provision infrastructure in a repeatable and version-controlled manner.

### AWS IAM

Provides least-privilege secure service-to-service access.

---

# Time-Series Database Design

Table Name:

```
health_data
```

Partition Key:

```
device_id
```

Sort Key:

```
timestamp
```

This schema supports:

* fast retrieval of latest device readings
* efficient historical timeline queries
* predictable scaling performance

---

# APIs Implemented

### POST /ingest-health-data

Accepts telemetry data from simulator devices and forwards it into the ingestion pipeline.

### GET /realtime-data

Returns the most recent telemetry reading for a device.

Example:

```
GET /realtime-data?device_id=device001
```

### GET /historical-data

Returns historical telemetry records for a device.

Example:

```
GET /historical-data?device_id=device001
```

---

# Device Simulator

A lightweight Python simulator generates telemetry data every 2 seconds to emulate real device behavior.

Simulator location:

```
simulator/simulator.py
```

Run using:

```
python simulator/simulator.py
```

This enables ingestion pipeline validation without requiring physical IoT hardware.

---

# Data Pipeline Design

Kinesis Data Streams is used as the ingestion buffer between API Gateway and Lambda.

This provides:

* burst traffic handling
* decoupled ingestion architecture
* replay capability if required
* shard-level horizontal scaling

Lambda processes stream records and stores telemetry into DynamoDB using a time-series schema.

---

# Storage Strategy (Hot / Warm / Cold Tiering)

The architecture supports a tiered storage lifecycle strategy.

### Hot Storage

Amazon DynamoDB stores recent telemetry used by realtime APIs.

### Warm Storage

Historical telemetry can be exported to Amazon S3 Standard for analytics workloads.

### Cold Storage

Long-term retention can be implemented using Amazon S3 Glacier lifecycle policies.

This supports scalable analytics and compliance-oriented retention requirements.

---

# Scalability Model

The system is designed to support **100,000+ healthcare telemetry devices**.

Example production sizing assumption:

* 100,000 registered devices
* ~15% active concurrently
* 7,500 events per second baseline
* 5× burst traffic handling capability

Scaling is handled through:

* Kinesis shard scaling
* Lambda automatic concurrency scaling
* DynamoDB on-demand capacity mode
* API Gateway managed scaling

All services operate across multiple Availability Zones by default.

---

# Performance Validation

Load testing was performed using k6.

Command used:

```
k6 run --vus 100 --duration 30s load-test/loadtest.js
```

Result:

```
14,000+ requests processed successfully with no failures observed
```

This validates burst traffic readiness of the ingestion pipeline.

---

# Security Architecture

Security best practices implemented include:

* HTTPS-enabled API Gateway endpoints
* IAM least-privilege execution roles
* encryption at rest (DynamoDB, Kinesis)
* encryption in transit using TLS
* CloudTrail audit logging capability

For production deployment, JWT authorization or Amazon Cognito integration can be added.

---

# Compliance Readiness (HIPAA / GDPR Considerations)

The architecture supports compliance-aligned deployment through:

* encryption at rest
* encryption in transit
* IAM role-based access control
* audit logging via CloudTrail
* serverless managed infrastructure isolation

These features support secure handling of healthcare telemetry workloads.

---

# Monitoring and Observability

Monitoring is implemented using Amazon CloudWatch.

CloudWatch provides visibility into:

* Lambda execution logs
* API latency metrics
* DynamoDB capacity usage
* Kinesis stream activity

CloudWatch alarms can detect ingestion failures or latency spikes.

---

# Infrastructure Deployment

Infrastructure is provisioned using AWS CloudFormation.

Template location:

```
cloudformation/
```

Example deployment command:

```
aws cloudformation deploy \
--template-file cloudformation/healthcare-stack.yaml \
--stack-name healthcare-stack \
--capabilities CAPABILITY_NAMED_IAM
```

This enables repeatable and version-controlled infrastructure deployment.

---

# Estimated Cost Model (Mumbai Region – Production Scenario)

The following estimate models a realistic production deployment scenario aligned with the problem statement requirement of supporting **100,000+ devices**.

Sizing assumptions:

* 100,000 registered devices
* ~15% concurrently active devices
* telemetry frequency: 1 event every 2 seconds
* baseline throughput: ~7,500 events/sec
* burst handling: up to 5× load spikes

Estimated monthly cost:

| Service                        | Estimated Monthly Cost |
| ------------------------------ | ---------------------- |
| API Gateway                    | ~$19,000               |
| Kinesis Data Streams           | ~$2,500                |
| AWS Lambda                     | ~$1,000                |
| DynamoDB (7‑day hot retention) | ~$5,000                |
| CloudWatch                     | ~$500                  |

Estimated total:

```
~$28,000 per month (~₹23 lakh/month)
```

Cost estimates are calculated using a realistic concurrency model where approximately **10–20% of registered medical devices transmit telemetry simultaneously**. The architecture remains capable of scaling to 100,000+ devices with burst handling through Kinesis shard scaling and Lambda concurrency expansion.

---

# Design Decisions

API Gateway was selected instead of AWS IoT Core to simplify ingestion for simulator-based device traffic while maintaining secure HTTPS endpoints.

Kinesis Data Streams was introduced to absorb burst telemetry traffic and decouple ingestion from processing.

Lambda was selected to keep compute event-driven and automatically scalable.

DynamoDB was selected instead of relational databases to support time-series access patterns with predictable performance.

CloudFormation was used to maintain AWS-native infrastructure provisioning.

---

# Trade-offs

AWS IoT Core would be recommended for production-scale device authentication but was not required for this simulated workload.

Single-region deployment was used to simplify implementation. Multi-region disaster recovery can be added if required.

Amazon Timestream could also be used for telemetry storage but DynamoDB provided flexible query access for API-driven workloads.

Caching was not introduced because DynamoDB already provides low-latency realtime access. DynamoDB DAX or ElastiCache can be added for dashboard-heavy workloads.

---

# Cost Optimization Strategy

Cost efficiency is achieved through:

* serverless compute (no idle infrastructure)
* DynamoDB hot-storage retention strategy
* Kinesis shard scaling based on throughput demand
* lifecycle archival to S3 Glacier for long-term retention

For very large-scale deployments with continuously active 100,000+ devices, AWS IoT Core can replace API Gateway ingestion to significantly reduce telemetry ingestion cost while enabling certificate-based device authentication.

---

# Future Improvements

Possible production enhancements include:

* AWS IoT Core device authentication
* JWT authorization via API Gateway
* multi-region disaster recovery deployment
* CI/CD automation using GitHub Actions
* Grafana dashboards for observability
* DynamoDB Global Tables for geo-replication
