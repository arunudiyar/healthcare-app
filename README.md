# Healthcare IoT Real-Time Ingestion Platform (AWS Serverless)

## Architecture Goals

This architecture was designed with production-oriented healthcare telemetry objectives:

* high-throughput ingestion from large-scale medical device fleets
* burst-resilient buffering using streaming architecture
* time-series optimized storage for device-based queries
* serverless auto-scaling without infrastructure management overhead
* compliance-ready security posture aligned with HIPAA / GDPR patterns
* cost-aware telemetry retention lifecycle using hot / warm / cold storage tiers

---

# Project Overview

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

## Amazon API Gateway

Used as the secure ingestion entry point and retrieval API exposure layer.

Provides:

* HTTPS endpoint exposure
* throttling protection
* scalable ingestion layer

## Amazon Kinesis Data Streams

Acts as a buffering layer between ingestion and processing.

Provides:

* burst traffic absorption
* stream replay capability
* horizontal shard scaling
* near real-time processing

## AWS Lambda

Processes telemetry events and serves realtime and historical API requests.

Provides:

* event-driven execution
* automatic scaling
* batch processing support
* cost-efficient compute

## Amazon DynamoDB

Stores telemetry data using a time-series schema optimized for device-based access patterns.

Provides:

* millisecond latency reads
* infinite horizontal scaling
* serverless storage
* multi-AZ high availability

## Amazon CloudWatch

Used for monitoring, logging, and observability.

Provides:

* ingestion pipeline visibility
* latency tracking
* failure monitoring
* alarm triggering capability

## AWS CloudFormation

Used to provision infrastructure in a repeatable and version-controlled manner.

## AWS IAM

Provides secure least-privilege service-to-service access.

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

Supports:

* fast retrieval of latest readings
* efficient timeline queries
* predictable scaling performance

---

# APIs Implemented

## POST /ingest-health-data

Accepts telemetry data from simulator devices and forwards it into the ingestion pipeline.

## GET /realtime-data

Returns the most recent telemetry reading for a device.

Example:

```
GET /realtime-data?device_id=device001
```

## GET /historical-data

Returns historical telemetry records.

Example:

```
GET /historical-data?device_id=device001
```

---

# Setup Steps (AWS Console Deployment)

## Step 1 — Deploy Infrastructure

1. Open AWS Console
2. Navigate to CloudFormation
3. Click **Create Stack**
4. Upload:

```
cloudformation/healthcare-stack.yaml
```

5. Enter stack name:

```
healthcare-stack
```

6. Enable:

```
CAPABILITY_NAMED_IAM
```

7. Create stack

This provisions:

* DynamoDB table
* Kinesis stream
* S3 archive bucket
* Lambda integrations
* API Gateway routing support

---

## Step 2 — Verify Resources

Verify following services are created:

| Service     | Resource       |
| ----------- | -------------- |
| DynamoDB    | health_data    |
| Kinesis     | health-stream  |
| S3          | archive bucket |
| API Gateway | health-api     |

---

## Step 3 — Configure API Routes (If Not Auto-Created)

Navigate to:

```
API Gateway → health-api
```

Create routes:

```
POST /ingest-health-data
GET /realtime-data
GET /historical-data
```

Attach integrations:

| Route                   | Lambda                |
| ----------------------- | --------------------- |
| POST ingest-health-data | ingest-health-data    |
| GET realtime-data       | realtime-health-api   |
| GET historical-data     | historical-health-api |

Deploy stage:

```
prod
```

---

## Step 4 — Run Device Simulator

```
python simulator/simulator.py
```

Generates telemetry every 2 seconds.

---

## Step 5 — Test APIs

Realtime:

```
GET /realtime-data?device_id=device001
```

Historical:

```
GET /historical-data?device_id=device001
```

---

## Step 6 — Load Testing

```
k6 run --vus 100 --duration 30s load-test/loadtest.js
```

Result:

```
14,000+ requests processed successfully with zero failures
```

---

# Storage Strategy (Hot / Warm / Cold Tiering)

Hot:

Recent telemetry stored in DynamoDB

Warm:

Exported to S3 Standard

Cold:

Archived using S3 Glacier lifecycle rules

Supports analytics scalability and compliance retention.

---

# Scalability Model

Architecture supports:

* 100,000 registered devices
* ~15% concurrently active devices
* 7,500 events/sec baseline
* 5× burst traffic handling capability

Scaling handled by:

* Kinesis shard scaling
* Lambda concurrency scaling
* DynamoDB on-demand mode
* API Gateway managed scaling

All services operate multi-AZ by default.

---

# Security Architecture

Security best practices implemented:

* HTTPS ingestion endpoints
* TLS encryption in transit
* encryption at rest (DynamoDB, Kinesis)
* IAM least-privilege roles
* CloudTrail audit logging readiness

JWT authorization or Cognito can be added for production.

---

# Compliance Readiness (HIPAA / GDPR)

Architecture supports compliance-oriented deployment through:

* encryption at rest
* encryption in transit
* IAM role-based access control
* CloudTrail audit logging
* serverless infrastructure isolation

---

# Monitoring and Observability

Monitoring implemented using CloudWatch.

Tracks:

* Lambda execution logs
* API latency metrics
* DynamoDB capacity usage
* Kinesis stream activity

CloudWatch alarms detect failures and latency spikes.

---

# Estimated Cost Model (Mumbai Region)

Assumptions:

* 100,000 registered devices
* ~15% concurrently active
* telemetry every 2 seconds
* 7,500 events/sec baseline
* 5× burst support

Estimated monthly cost:

| Service     | Monthly Cost |
| ----------- | ------------ |
| API Gateway | ~$19,000     |
| Kinesis     | ~$2,500      |
| Lambda      | ~$1,000      |
| DynamoDB    | ~$5,000      |
| CloudWatch  | ~$500        |

Total:

```
~$28,000/month (~₹23 lakh/month)
```

Calculated using realistic concurrency modeling.

---

# Design Decisions

API Gateway selected instead of IoT Core for simulator-based ingestion simplicity.

Kinesis introduced for burst buffering and decoupling pipeline stages.

Lambda used for event-driven compute scaling.

DynamoDB selected for time-series access performance.

CloudFormation used for infrastructure reproducibility.

---

# Trade-offs

IoT Core recommended for production-scale authentication.

Single-region deployment used for simplicity.

Amazon Timestream considered but DynamoDB selected for API flexibility.

Caching not required due to DynamoDB low-latency reads.

---

# Cost Optimization Strategy

Optimizations include:

* serverless compute model
* DynamoDB hot-storage retention
* shard-based Kinesis scaling
* S3 Glacier lifecycle archival

IoT Core can further reduce ingestion cost at very large scale.

---

# Future Improvements

Planned enhancements:

* AWS IoT Core device authentication
* JWT authorization
* multi-region disaster recovery deployment
* CI/CD automation using GitHub Actions
* Grafana dashboards
* DynamoDB Global Tables for geo-replication
