import re
import time
from rapidfuzz import process, fuzz
import pandas as pd
from word2number import w2n
from serpapi import GoogleSearch
apikey = '5eb0586d578ed6012ffed6ed8e8377307f4a592ba976eb63f1b8b82d741eb057'
result_dict={}
product_id_list =[]
data = pd.read_csv("productslist.csv")
prod_data_list = data.Product_name.tolist()


def fuzzy_match(word, options, threshold=70):
    return [opt for opt in options if fuzz.ratio(word, opt) >= threshold]

def extract_price_from_text(user_input):
    user_input = user_input.lower()

    # Try to find phrases like "under 50", "less than fifty dollars", "$70"
    patterns = [
        r'(?:under|below|less than)\s+(?:\$?\s*)?([\w\-]+)',  # under 50
        r'\$([\d]+)',  # $50
        r'([\d]+)\$',  # 50$
        r'([\d]+)\s*(?:dollars?|bucks|usd|euros?|rupees?)'  # 50 dollars
    ]
    user_input = user_input.lower().strip()
    print("user_input extract price : ", user_input)

    for pattern in patterns:
        match = re.search(pattern, user_input)
        print("MAX PRICE NEW 1 : ", match)
        if match:
            price_str = match.group(1)
            print("MAX PRICE NEW 2:", match.group(0))
            print("MAX PRICE NEW 3: ",price_str)
            try:
                return str(w2n.word_to_num(price_str))
            except:
                return price_str

    return None


def extract_requirements(user_input):
    product = ""
    max_price = None
    keywords = []
    price_num = ""
    clean_query = re.sub(r"[^\w\s]", "", user_input.lower())
    # product_match = re.search(r'({prod_search_str})', user_input, re.IGNORECASE)
    # if product_match:
    #     product = product_match.group(0)
    product_match, score, _ = process.extractOne(user_input, prod_data_list)
    #price_match = re.search(r'(under|below|less than)\s*\$?(\d+)', user_input)
    #price_pattern = re.search(r'\b(under|below|less than)\b\s+(.*?)\s*\$?(\d+)(?:dollars?|rupees?|euros?)', user_input)
    #price_pattern = re.search(r'\b(under|below|less than|around)\b\s*\$?\s*(\d+)',user_input,re.IGNORECASE)
    price_pattern = re.search(
        r'\b(under|below|less than)\b\s*\$?\s*(\d+|[a-zA-Z\-]+)',
        user_input.lower()
    )
    print("extract req pricepattern: ",price_pattern)
    if price_pattern:
        #price_str = price_pattern.group(2).strip()
        price_str = price_pattern.group(0)
        price_str = price_str.replace("$", "").strip()
        print("extract req price str after stripping: " ,price_str)
        try:
            # Try converting using word2number
            price_num = w2n.word_to_num(price_str)
            print("price_num from words : ", price_num)
            max_price = price_num
        except:
            # If that fails, try to extract digits directly
            digit_match = re.search(r'\d+', price_str)
            print("price_num from words : ", digit_match.group(0))
            max_price = digit_match.group(0)

    print("clean max price in extract : ", max_price)
    keyword_data = pd.read_csv("key_words_list.csv")
    keyword_data_list = keyword_data.keywords.tolist()
    clean_words = clean_query.split()
    print("clean query words : ", clean_words)
    print("Product Match#$#$#:",product_match)
    matched_features = []
    for word in clean_words:
        matched_features += fuzzy_match(word, keyword_data_list)
    user_display_summary = f"Searching for a {product_match}"
    if matched_features:
        user_display_summary += f" with features {', '.join(set(matched_features))}"
    if max_price:
        user_display_summary += f" under ${max_price}"
    user_display_summary += "."
    print("user_display_summary in extract :",user_display_summary)
    return product_match, matched_features,user_display_summary