from enum import Enum

class Action(str, Enum):
  PUSH = "PUSH"
  PULL_REQUEST = "PULL_REQUEST"
  MERGE = "MERGE"