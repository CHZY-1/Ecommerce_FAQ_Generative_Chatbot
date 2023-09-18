# https://github.com/huggingface/evaluate

import evaluate
import json

import sys
sys.path.append('web_chatbot_app')

from chatbot import Chatbot
import pandas as pd
import time

chatbot = Chatbot(model="C:/Users/User/Desktop/fine_tuned_dialogpt_FAQ_Ecommerce_1", tokenizer="microsoft/DialoGPT-large")

with open("web_chatbot_app/evaluation/test_question.json", "r") as json_file:
    test_questions = json.load(json_file)


questions = []
expected_responses = []
generated_responses = []
bleu_scores = []
meteor_scores = []
perplexity_scores = []
response_times = []


bleu_metric = evaluate.load("bleu")
meteor_metric = evaluate.load("meteor")

for item in test_questions['common_questions']:
    question = item["question"]
    expected_responses_list = item["expected_responses"]

    start_time = time.time()

    generated_response = chatbot.generate_response(question)
    print(generated_response)

    response_time = time.time() - start_time
    response_times.append(response_time)

    bleu_score = bleu_metric.compute(predictions=[generated_response], references=[expected_responses_list])
    meteor_score = meteor_metric.compute(predictions=[generated_response], references=[expected_responses_list])

    print(bleu_score)
    print(meteor_score)

    # Append data to lists
    questions.append(question)
    expected_responses.append(expected_responses_list)
    generated_responses.append(generated_response)
    bleu_scores.append(bleu_score['bleu'])
    meteor_scores.append(meteor_score['meteor'])
        


data = {
    "Question": questions,
    "Expected Response": expected_responses,
    "Generated Response": generated_responses,
    "BLEU Score": bleu_scores,
    "METEOR Score": meteor_scores,
    "Response Time": response_times
}

data["Question"].append("Average Score")
data["Expected Response"].append("-")
data["Generated Response"].append("-")
data["BLEU Score"].append(sum(bleu_scores) / len(bleu_scores))
data["METEOR Score"].append(sum(meteor_scores) / len(meteor_scores))
data["Response Time"].append(sum(response_times) / len(response_times))


df = pd.DataFrame(data)
print(df)

# df.to_csv('evaluation_Scores_tuned.csv', index=False)