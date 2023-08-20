# %%
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# %%
def load_tokenizer_and_model(model="microsoft/DialoGPT-medium"):
  """
    Load tokenizer and model instance for some specific DialoGPT model.
  """
  # Initialize tokenizer and model
  print("Loading model...")

  if model == "microsoft/DialoGPT-medium":
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(model)
  
  # Return tokenizer and model
  return tokenizer, model


# %% [markdown]
# HuggingFace AutoModelForCasualLM "decoder-only architecture" warning issue
# 
# https://stackoverflow.com/questions/74748116/huggingface-automodelforcasuallm-decoder-only-architecture-warning-even-after

# %%
def generate_response(tokenizer, model, chat_round, chat_history_ids):
  """
    Generate a response to user input.
  """

  user_question = input(">> User:")

  # Encode user input and End-of-String (EOS) token
  new_input_ids = tokenizer.encode(user_question + tokenizer.eos_token, return_tensors='pt')

  # Append tokens to chat history
  bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids
  
  chat_history_ids = model.generate(
    bot_input_ids, 
    max_length=1250,
    pad_token_id=tokenizer.eos_token_id)
  
  # Print response
  print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
  
  # Return the chat history ids
  return chat_history_ids

# %%
def chat_for_n_rounds(n=5, model='default'):
  """
  Chat with chatbot for n rounds (n = 5 by default)
  """

  # Initialize tokenizer and model
  if model == 'default':
    tokenizer, model = load_tokenizer_and_model()
  else:
    tokenizer, model = load_tokenizer_and_model(model)
  
  # Initialize history variable
  chat_history_ids = None
  
  # Chat for n rounds
  for chat_round in range(n):
    chat_history_ids = generate_response(tokenizer, model, chat_round, chat_history_ids)

# %%
chat_for_n_rounds(n=2)


