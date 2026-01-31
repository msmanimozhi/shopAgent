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

def get_best_matches_from_gpt12(user_query, formatted_products, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"""
You are an expert shopping assistant.
The user is looking for: "{user_query}".
Here are some product options:\n\n{formatted_products}
Please give the best product search results with title link and price.
"""
    retries = 5
    delay = 1  # Initial delay of 1 second
    for attempt in range(retries):
        try:
    # Using the new completions.create() method
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # You can use gpt-4 or other models as per your requirement
                prompt=prompt,  # The prompt that GPT will process
                max_tokens=100,  # Adjust max_tokens as needed
                temperature=0.2  # Adjust temperature for response creativity
            )
            answer = response['choices'][0]['text'].strip()
            return answer
        except RateLimitError as e:
            print(f"Rate limit error encountered: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 1 # Exponential backoff
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return None

def get_best_matches_from_gpt(user_query, openai_api_key, num_results=3):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"""
    You are an expert shopping assistant.
    The user is looking for: "{user_query}".
    Please give the best product search results with title link and price.
    """
    retries = 5
    delay = 1  # Initial delay of 1 second
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.2,
                n=num_results,
            )
            print("Response from openai : ",response)
            #answer = response.choices[0].message.content.strip()
            #answer = response['choices'][0]['text'].strip()
            results = []
            for choice in response.choices:
                results.append(choice.message.content.strip())

            return results
            #return answer
        except RateLimitError as e:
            print(f"Rate limit error encountered: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 1  # Exponential backoff
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return None

    def get_best_matches_from_gpt_456_9(user_query, formatted_products, openai_api_key):
        # openai.api_key = openai_api_key
        client = OpenAI(api_key=openai_api_key)
        #     prompt = f"""
        # You are an expert shopping assistant.
        # The user is looking for: "{user_query}".
        # Please give the best product search results with title link and price.
        # """
        if formatted_products:
            prompt = f"""
            You are an expert shopping assistant.
            The user is looking for: "{user_query}".
            Here are some product options:\n\n{formatted_products}
            Please give the best product search results with title link and price.
            """
        else:
            prompt = f"""
            You are an expert shopping assistant.
            The user is looking for: "{user_query}".
            Please give the best product search results with title link and price.
            """

        retries = 5
        delay = 1  # Initial delay of 1 second
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.2,
                )
                print("Response from openai : ", response)
                answer = response.choices[0].message.content.strip()
                # answer = response['choices'][0]['text'].strip()
                return answer
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
