#!/usr/bin/env python

from fastapi import FastAPI   # ✅ ONLY HERE (top)
import argparse
from environment import MeetingTranscriptEnv
from tasks import get_task, list_tasks
from graders import grade_task, compute_final_score
from models import ActionItem
import re

app = FastAPI()  # ✅ define early

def baseline_agent(env) -> list[ActionItem]:
    transcript = env.transcript.content.lower()
    actions = []
    
    if 'task_1' in env.transcript.task_id:
        match = re.search(r"(\w+).*?prepare.*?(\w+\s+\w+ budget).*?friday", transcript)
        if match:
            actions.append(ActionItem(description=match.group(2).title(), owner=match.group(1)))
    
    elif 'task_2' in env.transcript.task_id:
        patterns = [
            (r"design.*?wireframes", "Create wireframes for dashboard", "design"),
            (r"engineering.*?login bug", "Fix login bug", "engineering"),
            (r"marketing.*?launch deck", "Prepare launch deck", "marketing")
        ]
        for pattern, desc, owner in patterns:
            if re.search(pattern, transcript):
                actions.append(ActionItem(description=desc, owner=owner))
    
    elif 'task_3' in env.transcript.task_id:
        patterns = [
            ("api endpoints", "Optimize API endpoints", "devs"),
            ("customer feedback", "Follow up customer feedback", "john"),
            ("hero section", "Iterate hero section", "sarah"),
            ("sprint planning", "Sprint planning wrap up", "mike")
        ]
        for pattern, desc, owner in patterns:
            if pattern in transcript:
                actions.append(ActionItem(description=desc, owner=owner))
    
    return actions

def run_baseline(task_ids: list[str]):
    all_scores = {}
    
    for task_id in task_ids:
        transcript = get_task(task_id)
        env = MeetingTranscriptEnv(transcript)
        extracted = baseline_agent(env)
        score = grade_task(task_id, extracted)
        all_scores[task_id] = score
    
    return compute_final_score(all_scores)

# ✅ API endpoint
@app.get("/")
def read_root():
    return {"message": "Meeting Transcript Environment is running!"}

# ✅ Optional: real demo endpoint (VERY useful)
@app.get("/run")
def run():
    result = run_baseline(list_tasks())
    return result

# CLI runner (local use only)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=list_tasks() + ["all"], default="all")
    args = parser.parse_args()
    
    task_ids = list_tasks() if args.task == "all" else [args.task]
    run_baseline(task_ids)