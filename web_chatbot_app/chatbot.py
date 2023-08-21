import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class Chatbot:
    def __init__(self, model=None, tokenizer=None):
        if model is None and tokenizer is None:
            model_name = "microsoft/DialoGPT-large"
            self.tokenizer, self.model = self.load_tokenizer_and_model(model_name)
        else:
            print(f"Loading model : {model} ...")
            self.tokenizer = self.load_tokenizer(tokenizer)
            self.model = self.load_model(model)
            print("Model loaded")

        self.tokenizer.padding_side = 'left'

        self.chat_history_ids = None
        self.reset_history = 0

    def load_tokenizer_and_model(self, model_name):
        print(f"Loading model : {model_name} ...")

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        print("Model loaded")

        return tokenizer, model

    def load_tokenizer(self, tokenizer):
        return AutoTokenizer.from_pretrained(tokenizer)

    def load_model(self, model):
        return AutoModelForCausalLM.from_pretrained(model)

    def generate_response(self, user_question):

        if user_question.lower() in ['start over', 'reset']:
            self.reset_chat_history()
            return "Conversation reset"


        # Warning: A decoder-only architecture is being used, but right-padding was detected! 
        # For correct generation results, please set `padding_side='left'` when initializing the tokenizer.

        # change padding to left causes bot to genearte wierd respond, use right padding instead
        new_input_ids = self.tokenizer.encode(user_question + self.tokenizer.eos_token, return_tensors='pt')
        bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1) if self.chat_history_ids is not None else new_input_ids

        chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=500,
            min_length=10,
            temperature=0.7, # controls the randomness of the generated responses, Lower value for more deterministic responses 
            # 1.0 make the responses more diverse and creative, lower values like 0.2 make the responses more focused and deterministic.
            top_k=50,  # controls the number of highest probability words to consider in each step of response generation. 
            top_p=0.95, # nuclear sampling, Higher value for more focused responses
            no_repeat_ngram_size=3, # prevents the model from generating repetitive sequences of n-grams in the output.
            pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        if not response.strip() or self.is_repetitive_response(response):
            print("Generated response is empty or repetitive. Resetting conversation history.")
            self.reset_chat_history()
            return self.generate_response(user_question)

        print("Generated response length:", len(response))
        self.chat_history_ids = chat_history_ids

        return response

    # use parameters no_repeat_ngram_size in generate respond to handle repetitive respond.
    def is_repetitive_response(self, response, threshold=3):
        if self.chat_history_ids is not None:
            prev_response = self.tokenizer.decode(self.chat_history_ids[:, -1], skip_special_tokens=True)
            if response == prev_response:
                self.reset_history += 1
                print("Repetitive response. Reset Count:", self.reset_history)
                return self.reset_history >= threshold

        self.reset_history = 0
        return False

    def reset_chat_history(self):
        self.chat_history_ids = None

    def interactive_chat(self):
        print("Chatbot: Hi there! How can I assist you?")

        while True:
            user_input = input(">> User:")

            if user_input.lower() in ['exit', 'quit']:
                print("Chatbot: Goodbye!")
                break

            response = self.generate_response(user_input)
            print("DialoGPT:", response)

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.interactive_chat()
