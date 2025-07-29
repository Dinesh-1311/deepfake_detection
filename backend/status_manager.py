# status_manager.py
from typing import Dict

status_dict: Dict[str, Dict] = {}

def set_status(task_id: str, status: str, progress: int):
    status_dict[task_id] = {
        "status": status,
        "progress": progress
    }

def update_result(task_id: str, result: Dict):
    status_dict[task_id].update({
        "status": "Completed",
        "progress": 100,
        "result": result
    })

def get_status(task_id: str):
    return status_dict.get(task_id, {"status": "Unknown", "progress": 0})
