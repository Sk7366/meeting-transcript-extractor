from environment import MeetingEnv

env = MeetingEnv("easy")

obs = env.reset()
print(obs)

# Step 1: extract
print(env.step("extract_action", {"description": "Finalize the marketing report"}))

# Step 2: assign owner
print(env.step("assign_owner", {"owner": "Alice"}))

# Step 3: deadline
print(env.step("set_deadline", {"deadline": "Friday"}))

# Step 4: complete
print(env.step("mark_complete"))