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

def build_pull_request_event(payload: dict) -> dict:
    action = payload["action"]
    pr = payload["pull_request"]

    if not pr:
        return None
    
    # When PR is OPENED
    if action == "opened":
        return {
            "request_id": str(pr.get("id")),
            "author": pr.get("user", {}).get("login"),
            "action": Action.PULL_REQUEST.value,
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": normalize_timestamp(pr.get("created_at")),
        }
    
    # When PR is MERGED
    if action == "closed" and pr.get("merged") is True:
        return {
            "request_id": str(pr.get("id")),
            "author": pr.get("merged_by", {}).get("login"),
            "action": Action.MERGE.value,
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": normalize_timestamp(pr.get("merged_at")),
        }
    return None

def normalize_timestamp(raw_timestamp: str) -> str:
    """
    Convert/Normalize Github timestamps into UTC strings
    """
    if not raw_timestamp:
        return None
    
    if raw_timestamp.endswith("Z"):
        raw_timestamp = raw_timestamp.replace("Z", "+00:00")
    
    dt = datetime.fromisoformat(raw_timestamp)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.astimezone(timezone.utc).isoformat()