readme_content = """
# Serverless Job Scheduler ⏰☁️

A fully serverless backend system to schedule and execute jobs at specific times. Built with AWS Lambda, DynamoDB, API Gateway, and Terraform — ideal for showcasing cloud and backend engineering skills.

---

## 📌 Features

- 🔁 Schedule jobs via REST API  
- 🕐 Executes jobs at defined times  
- 🗃️ Stores jobs in DynamoDB  
- 🧱 Infrastructure-as-Code with Terraform  
- 🧩 Fully serverless and cost-efficient  

---

## 🧱 Architecture

Client/API → API Gateway → createJob Lambda  
               ↘ DynamoDB (Job Table)  
Periodic Trigger → executeJob Lambda → Execute jobs

---

## 📂 Folder Structure

serverless-job-scheduler/  
├── lambdas/  
│  ├── createJob/  
│  │  ├── src/index.py  
│  │  └── createJob.zip  
│  └── executeJob/  
│    ├── src/index.py  
│    └── executeJob.zip  
├── infrastructure/  
│  └── main.tf  
├── requirements.txt  
└── README.md  

---

## 🚀 Getting Started

1. **Clone the Repo**  
   git clone https://github.com/yourusername/serverless-job-scheduler.git  
   cd serverless-job-scheduler  

2. **Configure AWS CLI**  
   aws configure  
   (You'll need AWS Access Key, Secret Key, and a default region like `us-east-1`.)  

3. **Build Lambda ZIPs**  
   cd lambdas/createJob  
   pip install -r ../../requirements.txt -t build/  
   cp src/index.py build/  
   cd build && zip -r ../createJob.zip .  

   cd ../../executeJob  
   pip install -r ../../requirements.txt -t build/  
   cp src/index.py build/  
   cd build && zip -r ../executeJob.zip .  

4. **Deploy with Terraform**  
   cd infrastructure  
   terraform init  
   terraform apply  

---

## 🔍 Sample API Request

POST /create-job  

{  
 "job_id": "email-123",  
 "run_at": "2025-06-10T14:00:00Z",  
 "action": "send_email",  
 "payload": {  
  "to": "user@example.com",  
  "subject": "Reminder",  
  "message": "Time to check the app!"  
 }  
}  

---

## ✅ Free Tier Usage

This project stays within AWS Free Tier limits:  
- Lambda: 1M requests/month  
- DynamoDB: 25GB + 200M reads/writes  
- API Gateway: 1M calls/month  

---
