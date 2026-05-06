# Cloud Service Access Management API

## Overview

Cloud Service Access Management API is a backend system that simulates subscription-based access control for cloud services. It allows administrators to create subscription plans, assign permissions, manage users, and enforce real-time usage limits based on each customer’s plan.

The project demonstrates backend API design, role-based access control, quota enforcement, scheduled validation, and MongoDB-backed data storage.

1. Install Required Packages
Install the necessary Python packages:
```bash
pip install fastapi uvicorn motor jinja2
```

2. Configure MongoDB Atlas
1. Log in to your MongoDB Atlas account.
2. Create a database cluster if not already available.
3. Add a database user with read/write access.
4. Update the connection string in the `app.py` file:
   ```python
   MONGO_URI = "mongodb+srv://<db_username>:<db_password>@cluster0.sgudd.mongodb.net/"
   ```
5. Ensure the database name is `cloud_services` and collections (`subscription_plans`, `permissions`, `user_subscriptions`, `user_usage_stats`) exist.

### 3. Directory Structure
Ensure your project directory has the following structure:
```
.
├── app.py                  # Main application file
├── templates/              # Directory for HTML templates
│   └── home.html           # Home page template
├── static/                 # Directory for static files (e.g., CSS, JS)
```

4. Add `home.html`
Create a `templates/home.html` file with the following content:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Services</title>
</head>
<body>
    <h1>Subscription Plans</h1>
    <ul>
        {% for plan in plans %}
            <li>{{ plan['name'] }}: {{ plan['description'] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```

**Running the Application**
1. Start the application using `uvicorn`:
   ```bash
   uvicorn app:app --reload
   ```

2. Open your browser and navigate to:
   - Home page: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Swagger UI (API documentation): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**API Usage**

Admin Endpoints
Create Subscription Plan
- **Endpoint**: `/api/admin/subscription_plans`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "name": "Basic Plan",
      "description": "Access to basic services",
      "api_permissions": ["service1", "service2"],
      "usage_limits": {"service1": 100, "service2": 50}
  }
  ```

List Subscription Plans
- **Endpoint**: `/api/admin/subscription_plans`
- **Method**: GET

Add Permission
- **Endpoint**: `/api/admin/permissions`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "name": "Service 1 Access",
      "api_endpoint": "service1",
      "description": "Access to Service 1"
  }
  ```

Customer Endpoints
Subscribe to Plan
- **Endpoint**: `/api/customer/subscribe`
- **Method**: POST
- **Request Body**:
  ```json
  {
      "user_id": "user123",
      "plan_id": "<PLAN_ID>"
  }
  ```

View Usage Statistics
- **Endpoint**: `/api/customer/usage/{user_id}`
- **Method**: GET

Call a Service
- **Endpoint**: `/api/service/{api_name}`

- **Method**: POST
- **Request Body**:
  ```json
  {
      "user_id": "user123",![getuser](https://github.com/user-attachments/assets/6f434b43-eced-456f-946c-a045647a7baf)

      "api": "service1"
  }
  ```

**Testing the Application**
1. Use Swagger UI ([http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)) to interact with the API endpoints.
2. Monitor the MongoDB Atlas database to ensure data is being saved correctly.

**Error Handling**
- **404 Not Found**: Returned when a requested resource does not exist.
- **403 Forbidden**: Returned when a user attempts to access a restricted resource.
- **500 Internal 
Server Error**: Returned for unexpected issues.

VIDEO DEMONSTRATION:
https://adcsuf-my.sharepoint.com/:v:/r/personal/aviyasingh_csu_fullerton_edu/Documents/Attachments/fastapi-swagger-ui_wGugpOl6.mp4?csf=1&web=1&e=yMt6Pb&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D


![postsub](https://github.com/user-attachments/assets/a8f8ada7-155b-4d2b-a226-4feb8677c219)
![deleteperm](https://github.com/user-attachments/assets/a7bbc27d-3469-487b-9311-04dfed61d376)
![putperm](https://github.com/user-attachments/assets/0e8e30fb-2384-4924-b8c4-015b35968bad)
![getsub](https://github.com/user-attachments/assets/37df5ff8-4989-40d7-a802-72015636b0eb)
![postapi](https://github.com/user-attachments/assets/f1131797-54f3-4e3f-8257-ca3a92671924)
![postperm](https://github.com/user-attachments/assets/b5bd0d83-a68e-4f06-97ce-bc3206d80bf3)
![getperm](https://github.com/user-attachments/assets/57d9be15-cb67-4120-bf5d-4039dfafea67)
![deleteplans](https://github.com/user-attachments/assets/6f702662-9e99-4736-8fbc-f2a0c9b3e046)
![putplans](https://github.com/user-attachments/assets/bf4ccda2-08d4-4552-a0bb-bc72dab4489b)
![postplans](https://github.com/user-attachments/assets/0ee2bae7-822b-44a2-9468-869ca5a6c012)
![gettplans](https://github.com/user-attachments/assets/dd73fd1d-a0a1-4317-bf39-f5c1377a7a00)
![gethome](https://github.com/user-attachments/assets/ce80f5bd-5672-4303-98e7-d722b4ce68a5)
