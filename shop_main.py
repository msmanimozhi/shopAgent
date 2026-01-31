import time
import streamlit as st
from dotenv import load_dotenv
import os

from streamlit import image

from analyzer import analyze_products
from gpt_analysis import format_products_for_gpt, get_best_matches_from_gpt
from search import search_product, get_product_data
from userqueryhandle import extract_requirements, extract_price_from_text

load_dotenv()

apikey = os.getenv("API_KEY")
openai_api_key = os.getenv("OPEN_API_KEY")
#constants
#apikey = '5eb0586d578ed6012ffed6ed8e8377307f4a592ba976eb63f1b8b82d741eb057'
greetings = ["hi", "hello", "hey", "how are you", "good morning", "good evening", "what's up", "howdy","Greetings","Greetings!","hi!","hello!"]
exit_words = {"bye", "exit", "quit"}
#openai_api_key = "REDACTED_OPENAI_KEY"

#load the css file
def local_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        st.write(f"<style>{css}</style>", unsafe_allow_html=True)
# Call it here

# Display chat history (oldest at top, newest at bottom)
def display_chat(msglist):
    local_css("style.css")
    st.session_state.messages = msglist
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "content" in msg:
                st.write(msg["content"], unsafe_allow_html=True)
            if "image" in msg:
                st.image(msg["image"], width=200)


def run_shopping_assistant():
    #css call for style changes
    st.set_page_config(page_title="Shopping AI Assistant", layout="centered")
    local_css("style.css")
    st.title("🛍️ AI Shopping Assistant")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    user_input = st.chat_input("Enter a product to search...(Type 'exit' or 'quit' to stop)")
    print("User Input greetings test : ", user_input)

    if user_input:
        print("User Input greetings test 1 : ", user_input)
        cleaned_input = user_input.lower().strip()
        print("User Input greetings test 2: ", cleaned_input)
        if any(greet in cleaned_input for greet in greetings):
            st.session_state.messages.append({
                "role": "user",
                "content": cleaned_input
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": "👋 Hello! I'm your shopping assistant. What can I help you find today?"
            })

            display_chat(st.session_state.messages)


        elif cleaned_input in exit_words:
            st.session_state.exit_triggered = True

            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({
                "role": "assistant",
                "content": "👋 Thanks for using the shopping assistant. Goodbye!"
            })

            display_chat(st.session_state.messages)
            time.sleep(2)
            st.session_state.messages = []
            st.stop()
            st.rerun()

        else:
            print("openai_api_key : ", openai_api_key)
            print("user_input : ",user_input)
            answer = get_best_matches_from_gpt(user_input,openai_api_key)
            print("answer : ", answer)

            # product, keywords, user_display_summary = extract_requirements(user_input)
            # max_price = extract_price_from_text(user_input)
            # # Generate assistant response
            # st.session_state.messages.append({"role": "user", "content": user_input})
            # response = f"🔍 I'm **{user_display_summary}**. (Imagine product results here)"
            # st.session_state.messages.append({"role": "assistant", "content": response})
            # display_chat(st.session_state.messages)
            # #Call the api to get the product results
            # print("apikey : ",apikey)
            # print("opnekey :",openai_api_key)
            # product_id_list, result_dict = search_product(product,keywords,max_price, apikey)
            #
            # if result_dict and product_id_list:
            #     # Call the api to get the product description
            #     prod_result_dict = get_product_data(product_id_list, result_dict, apikey)
            #     print("prod_result_dict : ", prod_result_dict)
            #     # Send the product results to analyze. this will bring the best matched results based on user need
            #     formatted_products = format_products_for_gpt(prod_result_dict)
            #     print("formatted_products : ", formatted_products)
            #     answer = get_best_matches_from_gpt(user_input, formatted_products, openai_api_key)

                #st.markdown(f"best products for your needs : ",answer)
                #final_result_dict, price_flag = analyze_products(prod_result_dict, keywords, max_price)

            #final_result_dict= {}
            #     if final_result_dict:
            #         st.markdown("### 🧾 Top Results:")
            #         for result_product in final_result_dict:
            #             if 'link' in result_product:
            #
            #                 st.markdown(
            #                     f"<a href='{result_product['link']}' target='_blank'>{result_product['title']}</a>",
            #                     unsafe_allow_html=True)
            #                 message = {
            #                     "role": "assistant",
            #                     "content": f"**<a href='{result_product['link']}' target='_blank'>{result_product['title']}</a>"
            #                                f"\n\n**Price:** {result_product.get('price', 'N/A')}",
            #                     "image": result_product.get("image")
            #                 }
            #                 st.session_state.messages.append(message)
            #             else:
            #                 message = {
            #                     "role": "assistant",
            #                     "content": f"{result_product['title']}"
            #                                f"\n\n**Price:** {result_product.get('price', 'N/A')}",
            #                     "image": result_product.get("image")
            #                 }
            #                 st.session_state.messages.append(message)
            #                 st.subheader(f"{result_product['title']}")
            #             st.markdown(f"**Price:** {result_product.get('price', 'N/A')}")
            #             st.image(result_product.get("image"), width=200)
            #             st.markdown("---")
            #
            #             print(f"Title : {result_product['title']}")
            #     else:
            #         if price_flag:
            #             print("No Product found for this price")
            #             st.warning("No products found for this price")
            #         else:
            #             st.warning("No products found. Try a different query.")
            print("outside answer : ", answer)
            if answer:
                st.subheader('Best Matches:')
                for ans in answer:
                    if 'product' in ans:
                        product = ans.get('product')
                        if 'title' in product:
                            title = product.get("title","Title Not Available")
                        if 'price' in product:
                            price = product.get("price", "Price Not Available")
                        if 'link' in product:
                            link = product.get("link", "Link Not Available")
                        if 'image' in product:
                            image = product.get("image", "Image Not Available")
                    else:
                        if 'title' in ans:
                            title = ans.get("title","No Title Available")

                        if 'price' in ans:
                            price = ans.get('price',"No Price Available")

                        if 'link' in ans:
                            link = ans.get('link',"No Link Available")

                        if 'image' in ans:
                            image = ans.get("image", "Image Not Available")
                            if "example.com" in image:
                                image = "Image Not Available"

                    with st.container():
                        st.markdown(f" #### {title}")
                        st.markdown(f"{price}")
                        st.markdown(f"{link}")
                        if not image =='Image Not Available':
                            st.image(f"{image}",width=200)
                        st.markdown("---")
            else:
                print("No products found")
                st.warning("No products found. Try a different query.")

        print("st.session_state.messages:  ",st.session_state.messages)

run_shopping_assistant()
 # if answer:
            #     st.subheader('Best Matches:')
            #     print("inside answer : ", answer)
            #     for ans in answer:
            #
            #             if 'product' in ans:
            #
            #                 if 'title' in ans['product']:
            #                     st.markdown(f"### {ans['product']['title']}")
            #                 if 'price' in ans['price']:
            #                     st.markdown(f"**Price:** {ans['price']}")
            #                 if 'link' in ans['link']:
            #                     st.link_button("🔗 View Product", ans['link'])
            #                 st.markdown("---")