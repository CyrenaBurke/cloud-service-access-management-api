# Cloud Service Access Management API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen?logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

A production-style backend API for managing cloud service subscriptions, role-based access control, usage limits, and real-time quota enforcement — built with FastAPI and MongoDB Atlas.

**🔗 Live Demo:** [https://cloud-access-api-edwj.onrender.com/docs](https://cloud-access-api-edwj.onrender.com/docs)

> The free tier may take ~30 seconds to wake up on first request.

---

## Overview

This project simulates a subscription-based cloud service platform where administrators can define service plans and permissions, and customers can subscribe, consume services, and track their usage in real time.

The API enforces usage limits automatically — when a customer approaches or exceeds their quota, the system detects it via a scheduled background job and blocks further access. All endpoints are secured and documented via Swagger/OpenAPI.

---

## Features

- **Role-Based Access Control (RBAC)** — separate admin and customer permission models with extensible roles
- **Subscription plan management** — create, update, and delete tiered service plans with configurable API permissions and usage limits
- **Real-time quota enforcement** — APScheduler runs background validation to detect and alert on quota overuse before it occurs
- **Usage tracking** — per-user service consumption is logged and retrievable via API
- **JWT Authentication** — all endpoints secured with token-based authentication
- **Interactive API docs** — full Swagger/OpenAPI UI available at `/docs`
- **MongoDB Atlas** — scalable document-based storage for multi-tenant data

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | MongoDB Atlas (via Motor async driver) |
| Authentication | JWT (python-jose) |
| Scheduling | APScheduler |
| Templating | Jinja2 |
| Deployment | Render |
| Language | Python 3.11 |

---

## API Endpoints

### Admin Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/admin/subscription_plans` | Create a new subscription plan |
| `GET` | `/api/admin/subscription_plans` | List all subscription plans |
| `PUT` | `/api/admin/subscription_plans/{id}` | Update a subscription plan |
| `DELETE` | `/api/admin/subscription_plans/{id}` | Delete a subscription plan |
| `POST` | `/api/admin/permissions` | Add a new service permission |
| `GET` | `/api/admin/permissions` | List all permissions |
| `PUT` | `/api/admin/permissions/{id}` | Update a permission |
| `DELETE` | `/api/admin/permissions/{id}` | Delete a permission |

### Customer Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/customer/subscribe` | Subscribe a user to a plan |
| `GET` | `/api/customer/usage/{user_id}` | View a user's usage statistics |
| `POST` | `/api/service/{api_name}` | Call a service (enforces quota limits) |

---

## Getting Started

### Prerequisites

- Python 3.11+
- MongoDB Atlas account (free tier works)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CyrenaBurke/cloud-service-access-management-api.git
cd cloud-service-access-management-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure MongoDB Atlas**

   - Create a free cluster at [cloud.mongodb.com](https://cloud.mongodb.com)
   - Add a database user and copy your connection string
   - Create a database named `cloud_services` with collections:
     - `subscription_plans`
     - `permissions`
     - `user_subscriptions`
     - `user_usage_stats`

4. **Set environment variables**

   Create a `.env` file in the project root:
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/
   ```

5. **Run the application**
```bash
uvicorn app:app --reload
```

6. **Open the API docs**

   Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure

```
cloud-service-access-management-api/
├── app.py              # Main FastAPI application
├── templates/
│   └── home.html       # Home page template
├── static/
│   └── styles.css      # Static styles
├── requirements.txt
└── README.md
```

---

## Screenshots

### Subscription Plans
![Get Plans](https://github.com/user-attachments/assets/dd73fd1d-a0a1-4317-bf39-f5c1377a7a00)

### Create Subscription
![Post Subscription](https://github.com/user-attachments/assets/a8f8ada7-155b-4d2b-a226-4feb8677c219)

### Permissions Management
![Get Permissions](https://github.com/user-attachments/assets/57d9be15-cb67-4120-bf5d-4039dfafea67)

### Service API Call
![Post API](https://github.com/user-attachments/assets/f1131797-54f3-4e3f-8257-ca3a92671924)

---

## Video Demonstration

A full walkthrough of the API using Swagger UI is available here:
[Watch Demo](https://adcsuf-my.sharepoint.com/:v:/r/personal/aviyasingh_csu_fullerton_edu/Documents/Attachments/fastapi-swagger-ui_wGugpOl6.mp4?csf=1&web=1&e=yMt6Pb)

---

## Author

**Cyrena Burke**
[LinkedIn](https://www.linkedin.com/in/cyrena-burke/) · [GitHub](https://github.com/CyrenaBurke)
