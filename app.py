import os

from fastapi import FastAPI
import requests

app = FastAPI()

# Apigee Gateway URL
APIGEE_GATEWAY ="https://poc.api.gevernova.com/agent-gateway"

# API Key configured in Apigee Product/App
API_KEY = "oJepoMdyIfmyxVFAGypBujEC6nEAZj3U6Yjcc4WB4Y0MwfoXwryuw"

leave_data = {
    "1001": 12,
    "1002": 4,
    "1003": 20
}


@app.get("/")
def home():
    return {
        "status": "running",
        "agent": "leave-agent"
    }


@app.get("/.well-known/agent.json")
def agent_card():
    return {
        "name": "leave-agent",
        "description": "Leave Approval Agent",
        "version": "2.0",
        "skills": [
            {
                "id": "leave_approval",
                "description": "Approve or reject leave requests"
            }
        ]
    }


@app.get("/leave-approval/{empid}/{days}")
def leave_approval(empid: str, days: int):

    try:
        response = requests.get(
            f"{APIGEE_GATEWAY}/employee-agent/{empid}",
            headers={
                "x-api-key": API_KEY
            },
            timeout=10
        )
        response.raise_for_status()
        employee = response.json()

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Could not reach employee agent: {e}"
        }

    # Employee existence is determined by the employee-agent lookup,
    # not by leave balance (an employee can legitimately have 0 days left).
    employee_found = empid in leave_data and employee.get("name") not in (None, "Unknown")
    balance = leave_data.get(empid, 0)

    if not employee_found:
        decision = "Rejected"
        reason = "Employee not found"

    elif days > balance:
        decision = "Rejected"
        reason = "Insufficient leave balance"

    elif days > 5:
        decision = "Manager Approval Required"
        reason = "Leave exceeds auto approval limit"

    else:
        decision = "Approved"
        reason = "Within policy limits"

    return {
        "employee": employee,
        "leaveBalance": balance,
        "requestedDays": days,
        "decision": decision,
        "reason": reason
    }
