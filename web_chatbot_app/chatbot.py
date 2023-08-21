import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class Chatbot:
    def __init__(self, model="microsoft/DialoGPT-large"):
        self.tokenizer, self.model = self.load_tokenizer_and_model(model)
        self.chat_history_ids = None
        self.reset_history = 0

    def load_tokenizer_and_model(self, model):
        print("Loading model...")

        if model == "microsoft/DialoGPT-large":
            tokenizer = AutoTokenizer.from_pretrained(model)
            model = AutoModelForCausalLM.from_pretrained("D:/GitProjects/tuned_dialogpt")

        print("Model loaded")

        return tokenizer, model

    def generate_response(self, user_question):
        new_input_ids = self.tokenizer.encode(user_question + self.tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1) if self.chat_history_ids is not None else new_input_ids

        chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=1250,  # response length
            temperature=0.8,  # Adjust temperature for randomness
            top_k=50,  # top k for diversity
            top_p=0.9,  # nucleus sampling
            pad_token_id=self.tokenizer.eos_token_id)

        response = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # Check if the generated response is empty or has length 0
        # reset chat history when model stop generates due to repetitive or nonsensical content
        if not response.strip():
            print("Generated response is empty. Resetting conversation history.")
            self.chat_history_ids = None
            self.reset_history + 1
            print("Reset Count:", len(self.reset_history))
            return self.generate_response(user_question)  # Regenerate response
        
        print("Generated response length:", len(response))
        self.chat_history_ids = chat_history_ids

        return response

    def chat_for_n_rounds(self, n=5):
        for chat_round in range(n):
            user_input = input(">> User:")
            response = self.generate_response(user_input)
            print("DialoGPT:", response)

    def chat(self):
        while True:
            user_input = input(">> User:")
            if user_input.lower() in ['exit', 'quit']:
                print("Chatbot: Goodbye!")
                break

            response = self.generate_response(user_input)
            print("DialoGPT:", response)

if __name__ == "__main__":
    chatbot = Chatbot()