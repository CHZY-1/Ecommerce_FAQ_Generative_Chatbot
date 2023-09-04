from ..web_chatbot_app.chatbot import Chatbot
from RlChatbotEnv import ChatbotEnv

from stable_baselines3 import PPO
from stable_baselines3.common.envs import DummyVecEnv

class RLChatbot:
    def __init__(self, environment=None):
        self.env = environment
        self.env = DummyVecEnv([lambda: self.env])

    def train(self, total_timesteps=10000):
        model = PPO("MlpPolicy", self.env, verbose=1)
        model.learn(total_timesteps=total_timesteps)
        model.save("rl_chatbot_model")

    def get_response(self):
        model = PPO.load("rl_chatbot_model", env=self.env)

        # Simulate user input, as your web application doesn't take user input directly
        user_message = "User's Message"  # Replace with an appropriate user message

        # Pass the user input to the RL model to select a response
        action, _ = model.predict(self.env.get_observation(user_message))
        response = self.env.get_response(action)
        return response

if __name__ == "__main__":
    # Create and initialize your chatbot instance
    chatbot = Chatbot(model="C:/Users/User/Desktop/tuned_dialogpt_Ecommerce_FAQ", tokenizer="microsoft/DialoGPT-large")
    
    # Create the custom Gym environment and pass the chatbot instance to it
    env = ChatbotEnv(chatbot)
    
    # Create and train the RLChatbot using the custom environment
    rl_chatbot = RLChatbot(env)
    rl_chatbot.train(total_timesteps=10000)
    
    # Interact with the RL-trained chatbot
    rl_chatbot.interact()

