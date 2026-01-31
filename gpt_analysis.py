import ast

import openai
import time

from openai import RateLimitError, OpenAI


def format_products_for_gpt(prod_result_dict):
    product_texts = []
    for idx, (prod_id, details) in enumerate(prod_result_dict.items(), 1):
        title = details.get("title", "No Title")
        description = details.get("description", "No Description")
        price = details.get("price", "Unknown Price")
        link = details.get("link", "#")

        product_text = f"""
        Product {idx}:
        Title: {title}
        Description: {description}
        Price: {price}
        Link: {link}
        """
        product_texts.append(product_text.strip())

    return "\n\n".join(product_texts)

def get_best_matches_from_gpt(user_query, openai_api_key, num_results=3):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"""
    You are an expert shopping assistant.
    The user is looking for: "{user_query}".
    Please give the best product from google amazon walmart 
    results in title,price,image, link a python dict format.
    Don't get example.com link or image
    """
    retries = 5
    delay = 1  # Initial delay of 1 second
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Reply only in Python dict format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.2,
                n=num_results,
            )
            print("Response from openai : ",response)

            response_lst = []
            if response:
                if response.choices:
                    for idx, choice in enumerate(response.choices):
                        #response_text = choice.message.content.strip()
                        try:
                            response_text=  ast.literal_eval(choice.message.content.strip())
                        except (ValueError, SyntaxError) as e:
                            continue
                            print("Error processing the dict from response ", e)

                        print(f"Response from response_text {idx} : ", response_text)

                        response_lst.append(response_text)
                else:
                    print("No response found with choices")
                    return None
            else:
                print("No response found")
                return None

            print("Response list: ", response_lst)
            return response_lst
            #return answer
        except RateLimitError as e:
            print(f"Rate limit error encountered: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 1  # Exponential backoff
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return None

    # Extracting the response content from the new API structure
      # Use 'text' instead of 'message' in the new API
