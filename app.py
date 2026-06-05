from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio
import os

app = FastAPI()

# MongoDB Configuration
MONGO_URI = "mongodb+srv://cyrenaburke:Msmaraija15@cluster0.sgudd.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client.cloud_services

# Static and Templates Configuration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Models

class SubscriptionPlan(BaseModel):
    name: str
    description: str
    api_permissions: List[str]
    usage_limits: Dict[str, int]

class Permission(BaseModel):
    name: str
    api_endpoint: str
    description: str

class UserSubscription(BaseModel):
    user_id: str
    plan_id: str

class UsageUpdate(BaseModel):
    user_id: str
    api: str

# Helper Functions
async def check_access(user_id: str, api: str) -> bool:
    subscription = await db.user_subscriptions.find_one({"user_id": user_id})
    if not subscription:
        return False

    plan = await db.subscription_plans.find_one({"_id": subscription["plan_id"]})
    if not plan or api not in plan["api_permissions"]:
        return False

    usage = await db.user_usage_stats.find_one({"user_id": user_id})
    if usage and usage["usage"].get(api, 0) >= plan["usage_limits"].get(api, float("inf")):
        return False

    return True

async def update_usage(user_id: str, api: str):
    usage = await db.user_usage_stats.find_one({"user_id": user_id})
    if not usage:
        usage = {"user_id": user_id, "usage": {}, "restricted": False}

    usage["usage"][api] = usage["usage"].get(api, 0) + 1
    await db.user_usage_stats.update_one({"user_id": user_id}, {"$set": usage}, upsert=True)

# Routes

@app.get("/")
async def home(request: Request):
    plans = await db.subscription_plans.find().to_list(100)
    return templates.TemplateResponse("home.html", {"request": request, "plans": plans})

@app.post("/api/admin/subscription_plans", status_code=201)
async def create_subscription_plan(plan: SubscriptionPlan):
    result = await db.subscription_plans.insert_one(plan.dict())
    return {"message": "Subscription plan created", "plan_id": str(result.inserted_id)}

@app.put("/api/admin/subscription_plans/{plan_id}")
async def modify_subscription_plan(plan_id: str, plan: SubscriptionPlan):
    result = await db.subscription_plans.update_one({"_id": plan_id}, {"$set": plan.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Subscription plan updated"}

@app.delete("/api/admin/subscription_plans/{plan_id}")
async def delete_subscription_plan(plan_id: str):
    if not ObjectId.is_valid(plan_id):
        raise HTTPException(status_code=400, detail="Invalid plan_id format")
    result = await db.subscription_plans.delete_one({"_id": ObjectId(plan_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Subscription plan deleted"}

@app.get("/api/admin/subscription_plans")
async def list_subscription_plans():
    plans = await db.subscription_plans.find().to_list(100)
    # Convert ObjectId to string
    for plan in plans:
        plan["_id"] = str(plan["_id"])
    return plans

@app.post("/api/admin/permissions", status_code=201)
async def add_permission(permission: Permission):
    result = await db.permissions.insert_one(permission.dict())
    return {"message": "Permission added", "permission_id": str(result.inserted_id)}

@app.put("/api/admin/permissions/{permission_id}")
async def modify_permission(permission_id: str, permission: Permission):
    result = await db.permissions.update_one({"_id": permission_id}, {"$set": permission.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission updated"}

@app.delete("/api/admin/permissions/{permission_id}")
async def delete_permission(permission_id: str):
    if not ObjectId.is_valid(permission_id):
        raise HTTPException(status_code=400, detail="Invalid permission_id format")

    result = await db.permissions.delete_one({"_id": ObjectId(permission_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found")

    return {"message": "Permission deleted"}

@app.get("/api/admin/permissions")
async def list_permissions():
    permissions = await db.permissions.find().to_list(100)
    # Convert ObjectId to string
    for permission in permissions:
        permission["_id"] = str(permission["_id"])
    return permissions

@app.post("/api/customer/subscribe", status_code=201)
async def subscribe_to_plan(subscription: UserSubscription):
    if not ObjectId.is_valid(subscription.plan_id):
        raise HTTPException(status_code=400, detail="Invalid plan_id format")

    plan = await db.subscription_plans.find_one({"_id": ObjectId(subscription.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    await db.user_subscriptions.insert_one(subscription.dict())
    await db.user_usage_stats.insert_one({"user_id": subscription.user_id, "usage": {}, "restricted": False})
    return {"message": "Subscribed successfully"}


@app.get("/api/customer/subscription/{user_id}")
async def view_subscription_details(user_id: str):
    subscription = await db.user_subscriptions.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")
    subscription["_id"] = str(subscription["_id"])  # Convert ObjectId to string
    return subscription

@app.get("/api/customer/usage/{user_id}")
async def view_usage_statistics(user_id: str):
    usage = await db.user_usage_stats.find_one({"user_id": user_id})
    if not usage:
        raise HTTPException(status_code=404, detail="No usage data found")

    # Convert ObjectId to string
    if "_id" in usage:
        usage["_id"] = str(usage["_id"])

    return usage

@app.post("/api/service/{api_name}")
async def call_service(api_name: str, update: UsageUpdate):
    if not await check_access(update.user_id, api_name):
        raise HTTPException(status_code=403, detail="Access denied")
    await update_usage(update.user_id, api_name)
    return {"message": f"Accessed {api_name}"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred", "details": str(exc)},
    )
