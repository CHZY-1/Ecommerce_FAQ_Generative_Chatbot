import spacy
from thefuzz import fuzz

# Extracts keywords from user message after removing stop words
def extract_keywords(user_message):

    nlp = spacy.load("en_core_web_sm")

    # tokenize message
    doc = nlp(user_message)

    # extract lower case keywords from user msg
    keywords = [token.text.lower() for token in doc if not token.is_stop]
    return keywords

# Finds the best keyword match for a user input in a list of keywords using fuzzy string matching
# https://github.com/seatgeek/thefuzz
def find_best_match(user_input, keyword_list):
    best_score = 0
    best_match = None

    for keyword in keyword_list:
        # Calculate the similarity score (Levenshtein Distance) between the user input and the keyword
        similarity_score = fuzz.ratio(user_input, keyword)

        # Update the best match if the current keyword has a higher score
        if similarity_score > best_score:
            best_score = similarity_score
            best_match = keyword

    return best_match

# Determine the user intent by analyzing keywords
def determine_intent(user_message):

    user_keywords = extract_keywords(user_message)

    customer_service_keywords = ["customer service", "support", "help", "issue", "assistant" ,"problem", "account" "payment method", "order", "return policy", "price matching policy" , "price adjustment policy",
                                 "shipping", "package", "product", "item", "reviews", "customer support", "warpping service", "payment", "loyalty program", "bulk or wholesale discount", "return", 
                                 "cancel", "refund", "promo code", "stock", "email", "discount", "sale", "installation", "receipt", "delivery", "purchase", "invoice", "return a product", "packaging", 
                                 "replacement", "sold out", "available", "clearance", "pre-order", "pendrive", "flash drive", "usb", "usb-c", "specification", "password", "order", "pen drive", "gift warpping"]

    for keyword in user_keywords:
        for cs_keyword in customer_service_keywords:
            # if similarity score > 80
            if fuzz.ratio(keyword, cs_keyword) > 80:
                return "customer_service"

    return "general"


if __name__ == "__main__":
    user_message = "How can I track my order?"
    user_message1 = "Hello, how are you"
    user_message2 = "i want to preorder"
    intent = determine_intent(user_message2)
    print(f"Intent: {intent}")
