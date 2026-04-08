# Healthcare IoT Real-Time Ingestion Platform (AWS Serverless)

## Project Overview

This project demonstrates a serverless AWS architecture designed to ingest and process real-time healthcare telemetry data such as heart rate and blood pressure from large numbers of simulated monitoring devices.

The system is designed to support high ingestion throughput, burst traffic scenarios, and efficient time-series data retrieval using AWS native serverless services. APIs are exposed to retrieve both real-time device readings and historical telemetry records.

Infrastructure for the solution is provisioned using AWS CloudFormation.

---

## Architecture Overview

Telemetry data flows through the following pipeline:

Device Simulator
→ API Gateway
→ Kinesis Data Streams
→ Lambda Processing Layer
→ DynamoDB (Time-Series Table)
→ Retrieval APIs (Realtime + Historical)

The architecture is fully serverless and automatically scales with workload demand.

Architecture diagram available in:

```
architecture-diagram/
```

---

## AWS Services Used

**Amazon API Gateway**
Used as the secure ingestion entry point and for exposing retrieval APIs.

**Amazon Kinesis Data Streams**
Acts as a buffering layer between ingestion and processing to absorb burst traffic and decouple pipeline stages.

**AWS Lambda**
Processes incoming telemetry events and serves realtime and historical API requests.

**Amazon DynamoDB**
Stores telemetry data using a time-series schema optimized for device-based access patterns.

**Amazon CloudWatch**
Used for logging, monitoring metrics, and operational visibility.

**AWS CloudFormation**
Used to provision infrastructure in a repeatable and version-controlled manner.

**AWS IAM**
Provides least-privilege access between services.

---

## Time-Series Database Design

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

## APIs Implemented

**POST /ingest**

Accepts telemetry data from simulator devices and forwards it into the ingestion pipeline.

**GET /realtime-data**

Returns the most recent telemetry reading for a device.

Example:

```
GET /realtime-data?device_id=device001
```

**GET /historical-data**

Returns historical telemetry records for a device.

Example:

```
GET /historical-data?device_id=device001
```

---

## Device Simulator

A lightweight Python simulator was created to generate telemetry data every 2 seconds to emulate real device behavior.

Simulator location:

```
simulator/simulator.py
```

Run using:

```
python simulator/simulator.py
```

This allows validation of the ingestion pipeline without requiring physical IoT devices.

---

## Data Pipeline Design

Kinesis Data Streams is used as the ingestion buffer between API Gateway and Lambda.

This provides:

* burst traffic handling
* decoupled ingestion architecture
* replay capability if required
* horizontal shard scaling support

Lambda processes stream records and stores telemetry into DynamoDB using a time-series schema.

---

## Storage Strategy (Hot / Warm / Cold Tiering)

The architecture supports a tiered storage strategy suitable for telemetry workloads.

**Hot Storage**

Amazon DynamoDB stores recent telemetry used by realtime APIs.

**Warm Storage**

Historical telemetry data can be exported to Amazon S3 Standard for analytics workloads.

**Cold Storage**

Long-term retention can be implemented using Amazon S3 Glacier lifecycle policies.

This approach supports scalable analytics and compliance-oriented retention requirements.

---

## Scalability Approach

The system is designed for high-volume telemetry ingestion scenarios.

Example workload assumption:

100,000 devices sending data every 2 seconds
≈ 50,000 events per second

Scaling is handled through:

* Kinesis shard scaling
* Lambda automatic concurrency scaling
* DynamoDB on-demand capacity mode
* API Gateway managed request scaling

All services operate across multiple Availability Zones by default.

---

## Performance Validation

Load testing was performed using k6.

Command used:

```
k6 run --vus 100 --duration 30s load-test/loadtest.js
```

Result:

14,000+ requests processed successfully with no failures observed.

This validates burst traffic readiness of the ingestion pipeline.

---

## Security Architecture

Security best practices implemented include:

* HTTPS-enabled API Gateway endpoints
* IAM least-privilege execution roles
* encryption at rest enabled (DynamoDB, Kinesis)
* encryption in transit using TLS
* CloudTrail audit logging supported

For production deployment, JWT authorization or AWS Cognito can be integrated with API Gateway.

---

## Compliance Readiness (HIPAA / GDPR Considerations)

The architecture supports compliance-oriented deployment through:

* encryption at rest
* encryption in transit
* IAM role-based access control
* CloudTrail audit logging capability
* serverless managed infrastructure isolation

These features support secure handling of healthcare telemetry workloads.

---

## Monitoring and Observability

Monitoring is implemented using Amazon CloudWatch.

CloudWatch provides visibility into:

* Lambda execution logs
* API latency metrics
* DynamoDB capacity usage
* Kinesis stream activity

CloudWatch alarms can be configured to detect ingestion failures or latency spikes.

---

## Infrastructure Deployment

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

## Design Decisions

API Gateway was selected instead of AWS IoT Core to simplify ingestion for simulator-based device traffic.

Kinesis Data Streams was introduced to absorb burst telemetry traffic and decouple ingestion from processing.

Lambda was selected to keep compute event-driven and automatically scalable.

DynamoDB was selected instead of a relational database to support time-series access patterns with predictable performance.

CloudFormation was used to stay within AWS native infrastructure tooling.

---

## Trade-offs

AWS IoT Core would be recommended for production-scale device authentication but was not required for this simulated workload.

Single-region deployment was used to simplify implementation. Multi-region disaster recovery can be added if required.

Amazon Timestream could also be used for telemetry storage but DynamoDB provided flexible query access for API-driven workloads.

Caching was not introduced in this implementation because DynamoDB already provides low-latency access for realtime device reads. ElastiCache or DynamoDB DAX can be added if dashboard request frequency increases significantly.

---

## Cost Optimization Strategy

Cost efficiency is achieved through:

* serverless compute (no idle infrastructure)
* DynamoDB on-demand capacity mode
* adjustable Kinesis shard configuration
* lifecycle-based archival to S3 Glacier for long-term retention

Serverless services scale based on usage, reducing baseline operational cost.

---

## Future Improvements

Possible production enhancements include:

* AWS IoT Core device authentication
* JWT authorization via API Gateway
* multi-region disaster recovery deployment
* CI/CD automation using GitHub Actions
* Grafana dashboards for advanced observability
* DynamoDB Global Tables for geo-replication
