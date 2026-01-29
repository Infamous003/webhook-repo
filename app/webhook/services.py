from datetime import datetime, timezone
from .enums import Action

def build_push_event(payload: dict) -> dict:
    pusher = payload.get("pusher", {})
    head_commit = payload.get("head_commit", {})

    # example: refs/heads/main where branch name is main
    ref = payload.get("ref", "")
    to_branch = ref.split("/")[-1]
    
    raw_timestamp = head_commit.get("timestamp")
    utc_timestamp = normalize_timestamp(raw_timestamp)

    return {
        "request_id": head_commit.get("id"),
        "author": pusher.get("name"),
        "action": Action.PUSH.value,
        "from_branch": None,
        "to_branch": to_branch,
        "timestamp": utc_timestamp,
    }

def normalize_timestamp(raw_timestamp: str) -> str:
    return (
        datetime.fromisoformat(raw_timestamp)
        .astimezone(timezone.utc)
        .isoformat()
    )