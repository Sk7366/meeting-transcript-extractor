from models import Transcript, ActionItem
from datetime import date
from typing import Dict, List

TASKS: Dict[str, Transcript] = {}

# Task 1: Easy - 1 explicit action
TASKS["task_1"] = Transcript(
    content="""
Alice: Great meeting. Bob, please prepare the Q1 budget by Friday.
Bob: Got it, budget by Friday March 15th.
Charlie: Perfect.
""",
    ground_truth=[
        ActionItem(
            description="Prepare Q1 budget",
            owner="Bob",
            deadline=date(2026, 3, 15)
        )
    ],
    task_id="task_1",
    metadata={"difficulty": "easy", "lines": 10, "items": 1}
)

# Task 2: Medium - 3 items, implied owners
TASKS["task_2"] = Transcript(
    content="""""
Team meeting notes:

Design should create wireframes for new dashboard by EOW.
Engineering needs to fix the login bug ASAP.
Marketing team - prepare launch deck for next week.

Sarah: Questions?
Everyone: No.
""",
    ground_truth=[
        ActionItem(description="Create wireframes for dashboard", owner="design", deadline=date(2026, 3, 14)),
        ActionItem(description="Fix login bug", owner="engineering", deadline=date(2026, 3, 10)),
        ActionItem(description="Prepare launch deck", owner="marketing", deadline=date(2026, 3, 17))
    ],
    task_id="task_2",
    metadata={"difficulty": "medium", "lines": 25, "items": 3}
)

# Task 3: Hard - 4 ambiguous items
TASKS["task_3"] = Transcript(
    content="""
Casual chat first...

Mike: Hey team, sprint planning.
Discussing priorities...

 buried action: Devs should optimize the API endpoints before next release.

Later: John mentioned following up on customer feedback from last week.

Design team (Sarah?) needs to iterate on that hero section.

No explicit deadline but end of sprint is Friday.

Wrap up?
""",
    ground_truth=[
        ActionItem(description="Optimize API endpoints", owner="devs", deadline=date(2026, 3, 14)),
        ActionItem(description="Follow up customer feedback", owner="John", deadline=date(2026, 3, 14)),
        ActionItem(description="Iterate hero section", owner="Sarah", deadline=date(2026, 3, 14)),
        ActionItem(description="Sprint planning wrap up", owner="Mike", deadline=date(2026, 3, 14))
    ],
    task_id="task_3",
    metadata={"difficulty": "hard", "lines": 40, "items": 4}
)

def get_task(task_id: str) -> Transcript:
    """Get task by ID."""
    if task_id not in TASKS:
        raise ValueError(f"Task {task_id} not found. Available: {list(TASKS.keys())}")
    return TASKS[task_id]

def list_tasks() -> List[str]:
    """List all task IDs."""
    return list(TASKS.keys())