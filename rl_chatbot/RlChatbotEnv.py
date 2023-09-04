from ..web_chatbot_app.chatbot import Chatbot

import gym
import numpy as np
import json

class RLChatbotEnv(gym.Env):
    def __init__(self, chatbot, conversation_data_path):
        super(RLChatbotEnv, self).__init__()
        self.chatbot = chatbot
        self.conversation_data_path = conversation_data_path
        self.current_step = 0
        self.max_steps = 100  # Set the maximum number of conversation steps

        self.conversation_data = self.load_conversation_data()
        self.num_episodes = len(self.conversation_data)
        self.current_episode = 0

        self.action_space = gym.spaces.Discrete(1)  # Single action space (response selection)

    def step(self, action):
        if self.current_step >= len(self.conversation_data[self.current_episode]["user_messages"]):
            done = True
            return "", 0, done, {}

        user_message = self.conversation_data[self.current_episode]["user_messages"][self.current_step]
        expected_response = self.conversation_data[self.current_episode]["expected_responses"][self.current_step]

        # Generate the chatbot's response
        chatbot_response = self.chatbot.generate_response(user_message)

        # Calculate reward based on user feedback
        feedback = self.conversation_data[self.current_episode]["feedback"][self.current_step]
        reward = self.calculate_reward(chatbot_response, expected_response, feedback)

        self.current_step += 1
        done = self.current_step >= len(self.conversation_data[self.current_episode]["user_messages"])

        return chatbot_response, reward, done, {}

    def reset(self):
        if self.current_episode < self.num_episodes:
            self.current_step = 0
            self.current_episode += 1
            return self.conversation_data[self.current_episode - 1]["user_messages"][0]
        else:
            return None

    def load_conversation_data(self):
        with open(self.conversation_data_path, "r") as file:
            conversation_data = json.load(file)
        return conversation_data

    def calculate_reward(self, user_feedback):
        if user_feedback == 1:
            return 1.0  # Positive feedback, reward +1
        elif user_feedback == -1:
            return -1.0  # Negative feedback, reward -1
        elif user_feedback is None:
            return 0.0  # No feedback provided, no reward
        else:
            return 0.0  # Unknown or undefined feedback, no reward