from fastapi import FastAPI
import requests

app = FastAPI()

EMPLOYEE_AGENT_CARD = "https://employee-agent-fis1.onrender.com/.well-known/agent.json"
EMPLOYEE_API = "https://employee-agent-fis1.onrender.com/employee"

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
        "version": "1.0",
        "skills": [
            {
                "id": "leave_approval",
                "description": "Approve or reject leave requests"
            }
        ]
    }

@app.get("/leave-approval/{empid}/{days}")
def leave_approval(empid: str, days: int):

    # Agent Discovery
    card = requests.get(EMPLOYEE_AGENT_CARD).json()

    # Agent Invocation
    employee = requests.get(
        f"{EMPLOYEE_API}/{empid}"
    ).json()

    balance = leave_data.get(empid, 0)

    if balance == 0:
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
        "agentDiscovered": card["name"],
        "employee": employee,
        "leaveBalance": balance,
        "requestedDays": days,
        "decision": decision,
        "reason": reason
    }
