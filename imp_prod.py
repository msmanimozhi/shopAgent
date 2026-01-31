import re
from rapidfuzz import process,fuzz
from word2number import w2n
import pandas as pd
data = pd.read_csv("productslist.csv")
prod_data_list = data.Product_name.tolist()
keyword_data = pd.read_csv("key_words_list.csv")
keyword_data_list = keyword_data.keywords.tolist()
print("keywords from csv : ", keyword_data_list)
user_input = "'vascum cleaner100$ quiet pet hair "
def fuzzy_match(word, options, threshold=70):
    return [opt for opt in options if fuzz.ratio(word, opt) >= threshold]

def get_most_likely_product(user_input, product_list):
    scores = []
    for product in product_list:
        score = fuzz.partial_ratio(product, user_input)
        scores.append((product, score))
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0]


clean_query = re.sub(r"[^\w\s]", "", user_input.lower())
user_input_clean = re.sub(r"[^\w\s$]", "", user_input.lower())  # remove punctuation

# Step 2: Fuzzy match words to known product names
top_product, score = get_most_likely_product(user_input_clean, prod_data_list)

if score >= 60:
    print("🛍️ Product:", top_product)
else:
    print("❓ No clear match found")

print("clean query : ", clean_query)
match, score, _ = process.extractOne(user_input, prod_data_list)
if score > 70:
    print(f"Matched: {match}")
else:
    print("No confident match.")

price_pattern = re.search(
        r'\b(under|below|less than)\b\s*\$?\s*(\d+|[a-zA-Z\-]+)',
        user_input.lower()
    )
print("price_pattern : ",price_pattern)

if price_pattern:
    #price_str = price_pattern.group(2).strip()
    price_str = price_pattern.group(0)
    price_str = price_str.replace("$", "").strip()
    print("price_pattern : ", price_str)
    price_num = 0
    try:
        # Try converting using word2number
        price_num = w2n.word_to_num(price_str)
        print ("price_num from words : ", price_num)
    except:
        # If that fails, try to extract digits directly
        digit_match = re.search(r'\d+', price_str)
        print("price_num from words %^%^: ", digit_match.group(0))
        price_num=digit_match.group(0)

print("price_num after from words %^%^: ", price_num)
words = clean_query.split()
print("clean query words : ", words)
matched_features = []
for word in words:
    matched_features += fuzzy_match(word, keyword_data_list)

if matched_features:
    print("Keywords found :", matched_features)
else:
    print("Keywords not found")
summary = f"Searching for a {match}"
if matched_features:
    summary += f" with features: {', '.join(set(matched_features))}"
if price_num:
    summary += f" under ${price_num}"
summary += "."

print(summary)