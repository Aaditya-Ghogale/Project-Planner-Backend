# storage.py

from tinydb import TinyDB, Query
from tinydb.operations import delete
from uuid import uuid4
from datetime import datetime

# Setup database
db = TinyDB('db/database.json')
users_table = db.table('users')
teams_table = db.table('teams')
boards_table = db.table('boards')
tasks_table = db.table('tasks')

# Timestamp helper
def now():
    return datetime.utcnow().isoformat()

# Create user
def create_user(name, email, phone):
    user_id = str(uuid4())
    user = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "phone": phone,
        "created_at": now()
    }
    users_table.insert(user)
    return user

# Create team
def create_team(name, description):
    team_id = str(uuid4())
    team = {
        "team_id": team_id,
        "name": name,
        "description": description,
        "members": [],
        "created_at": now()
    }
    teams_table.insert(team)
    return team

# Add user to team
def add_user_to_team(team_id, user_id):
    Team = Query()
    team = teams_table.get(Team.team_id == team_id)
    if not team:
        raise ValueError("Team not found")
    if user_id in team["members"]:
        raise ValueError("User already in team")
    if len(team["members"]) >= 50:
        raise ValueError("Team member limit reached")
    team["members"].append(user_id)
    teams_table.update({"members": team["members"]}, Team.team_id == team_id)

# Create board
def create_board(team_id, title):
    board_id = str(uuid4())
    board = {
        "board_id": board_id,
        "team_id": team_id,
        "title": title,
        "status": "OPEN",
        "created_at": now(),
        "closed_at": None
    }
    boards_table.insert(board)
    return board

# Create task
def create_task(board_id, title, description, assigned_to=None):
    task_id = str(uuid4())
    task = {
        "task_id": task_id,
        "board_id": board_id,
        "title": title,
        "description": description,
        "status": "TODO",
        "assigned_to": assigned_to,
        "created_at": now(),
        "updated_at": now()
    }
    tasks_table.insert(task)
    return task
