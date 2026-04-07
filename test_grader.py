from graders import compute_reward

pred = [
    {
        "description": "Finalize the marketing report",
        "owner": "Alice",
        "deadline": "Friday",
    }
]

truth = [
    {
        "description": "Finalize the marketing report",
        "owner": "Alice",
        "deadline": "Friday",
    }
]

print(compute_reward(pred, truth))