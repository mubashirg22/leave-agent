from fastapi import FastAPI
import requests

app = FastAPI()

EMPLOYEE_AGENT_CARD = \
"https://employee-agent-fis1.onrender.com/.well-known/agent.json"

EMPLOYEE_API = \
"https://employee-agent-fis1.onrender.com/employee"

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
        "description": "Leave Management Agent",
        "version": "1.0",
        "skills": [
            {
                "id": "leave_approval",
                "description": "Checks employee leave eligibility"
            }
        ]
    }

@app.get("/leave/{empid}")
def leave_check(empid: str):

    # Step 1: Discover Employee Agent
    employee_card = requests.get(
        EMPLOYEE_AGENT_CARD
    ).json()

    # Step 2: Invoke Employee Agent
    employee = requests.get(
        f"{EMPLOYEE_API}/{empid}"
    ).json()

    leave_data = {
        "1001": 12,
        "1002": 8,
        "1003": 20
    }

    balance = leave_data.get(empid, 5)

    decision = (
        "Approved"
        if balance >= 10
        else "Rejected"
    )

    return {
        "agentDiscovery": employee_card["name"],
        "employee": employee,
        "leaveBalance": balance,
        "decision": decision
    }
