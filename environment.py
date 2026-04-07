import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Any, Tuple
from models import (
    EnvState, Transcript, AgentAction, ActionItem, ActionStatus,
    RewardEvent
)
import json
import re
from datetime import date, timedelta

class MeetingTranscriptEnv(gym.Env):
    """OpenEnv for meeting transcript action extraction."""
    
    def __init__(self, transcript: Transcript):
        super().__init__()
        
        self.transcript = transcript
        self.max_steps = 50
        self.action_history = []
        
        # Gym spaces
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(10000,), dtype=np.uint8
        )
        self.action_space = spaces.Discrete(4)  # 0:extract,1:owner,2:deadline,3:complete
        
        self.reset()
    
    def reset(self, seed=None, options=None) -> Tuple[EnvState, Dict[str, Any]]:
        super().reset(seed=seed)
        self.state = EnvState(transcript=self.transcript)
        self.action_history = []
        self.step_count = 0
        return self._get_obs(), {}
    
    def step(self, action_idx: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """Execute agent action and compute reward."""
        action_type_map = {
            0: "extract_action",
            1: "assign_owner", 
            2: "set_deadline",
            3: "mark_complete"
        }
        action_type = action_type_map[action_idx]
        
        # Parse value from observation (simplified for demo)
        value = self._parse_action_value(action_type)
        action = AgentAction(action_type=action_type, value=value)
        
        reward, message = self._compute_reward(action)
        self.state.total_reward += reward
        
        self.action_history.append(action)
        self.step_count += 1
        
        terminated = self._is_terminated()
        truncated = self.step_count >= self.max_steps
        
        return self._get_obs(), reward, terminated, truncated, {"message": message}
    
    def _compute_reward(self, action: AgentAction) -> Tuple[float, str]:
        """Your exact reward function."""
        if action.action_type == "extract_action":
            return self._reward_extract_action(action.value)
        elif action.action_type == "assign_owner":
            return self._reward_assign_owner(action.value)
        elif action.action_type == "set_deadline":
            return self._reward_set_deadline(action.value)
        elif action.action_type == "mark_complete":
            return self._reward_mark_complete()
        return 0.0, "Unknown action"
    
    def _reward_extract_action(self, description: str) -> Tuple[float, str]:
        ground_truth = self.transcript.ground_truth
        matches = sum(1 for gt in ground_truth if gt.description.lower() in description.lower())
        
        if matches >= 1:
            return 0.3, f"✅ Good extraction (matched {matches} GT)"
        elif len(self.state.current_actions) >= len(ground_truth) * 2:
            return -0.3, "❌ Loop: too many extractions"
        elif self._is_hallucination(description):
            return -0.2, "❌ Hallucination detected"
        return 0.1, "ℹ️ Extraction noted"
    
    def _reward_assign_owner(self, owner: str) -> Tuple[float, str]:
        if len(self.state.current_actions) == 0:
            return -0.15, "❌ No action to assign"
        if any(action.owner.lower() == owner.lower() for action in self.transcript.ground_truth):
            return 0.2, "✅ Correct owner"
        return 0.05, "ℹ️ Owner assigned"
    
    def _reward_set_deadline(self, deadline_str: str) -> Tuple[float, str]:
        if len(self.state.current_actions) == 0:
            return -0.15, "❌ No action for deadline"
        try:
            deadline = date.fromisoformat(deadline_str)
            return 0.15, "✅ Valid deadline"
        except:
            return 0.05, "ℹ️ Deadline noted"
    
    def _reward_mark_complete(self) -> Tuple[float, str]:
        incomplete = [a for a in self.state.current_actions if not a.owner or not a.deadline]
        if incomplete:
            return -0.15, f"❌ Incomplete actions: {len(incomplete)}"
        return 0.1, "✅ Action completed"
    
    def _is_hallucination(self, text: str) -> bool:
        """Simple hallucination check."""
        hallucination_patterns = ["fake", "dummy", "test", "example"]
        return any(pattern in text.lower() for pattern in hallucination_patterns)
    
    def _parse_action_value(self, action_type: str) -> str:
        """Parse action value from current transcript (demo)."""
        return f"demo_{action_type}"
    
    def _get_obs(self) -> np.ndarray:
        """Observation: transcript bytes."""
        obs_text = self.transcript.content[:10000]
        return np.frombuffer(obs_text.encode('utf-8'), dtype=np.uint8)
    
    def _is_terminated(self) -> bool:
        """Episode ends when all actions complete or timeout."""
        all_complete = all(
            action.owner and action.deadline and action.status == ActionStatus.COMPLETED
            for action in self.state.current_actions
        )
        return all_complete or len(self.state.current_actions) >= len(self.transcript.ground_truth)

    def render(self):
        print(f"State: {self.state.dict()}")