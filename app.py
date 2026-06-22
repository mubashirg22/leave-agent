from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "running"
    }

@app.get("/.well-known/agent.json")
def agent_card():
    return {
        "name": "leave-agent",
        "description": "Leave Management Agent",
        "version": "1.0",
        "skills": [
            {
                "id": "leave_balance",
                "description": "Check employee leave balance"
            }
        ]
    }

@app.get("/leave/{empid}")
def leave_balance(empid):
    leave_data = {
        "1001": 12,
        "1002": 8,
        "1003": 20
    }

    balance = leave_data.get(empid, 5)

    return {
        "employeeId": empid,
        "leaveBalance": balance,
        "status": "available"
    }
