
from serpapi import GoogleSearch

def search_product(user_input, keywords, max_price,apikey, top_k=3):
    new_user_input = user_input + " ".join(keywords) if keywords else user_input
    new_user_input = new_user_input + " for price around" +" ".join(max_price) if max_price !="" else new_user_input

    params = {
        "engine": "google_shopping",
        "q": new_user_input,
        "hl": "en",
        "gl": "us",
        "api_key": apikey
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    product_id_list = []
    result_dict = {}

    shopping_results = results.get("shopping_results", [])
    print(f"🔍 Search result count: {len(shopping_results)}")

    for product in shopping_results[:top_k]:
        prod_id = product.get("product_id")
        link = product.get("product_link")
        price = product.get("price")

        if prod_id:
            result_dict[prod_id] = {"link": link, "price": price}
            product_id_list.append(prod_id)
            print(f"✅ Found product: {prod_id} - {link} - {price}")

    return product_id_list, result_dict


def get_product_data(product_id_list, result_dict, apikey):
    prod_result_dict = {}

    for prod_id in product_id_list:
        product_params = {
            "engine": "google_product",
            "product_id": prod_id,
            "api_key": apikey
        }
        product_search = GoogleSearch(product_params)
        product_data = product_search.get_dict()
        products_info = product_data.get("product_results", {})

        print(f"📦 Detailed info for {prod_id}: {products_info}")

        title = products_info.get("title", "Unknown Title")
        description = products_info.get("description", "No description available.")
        image = next((m["link"] for m in products_info.get("media", []) if m.get("type") == "image"),
                     "Image Not Available")

        base_info = result_dict.get(prod_id, {})
        link = base_info.get("link", "#")
        price = base_info.get("price", "N/A")

        prod_result_dict[prod_id] = {
            "title": title,
            "price": price,
            "link": link,
            "description": description,
            "image": image
        }

    print(f"✅ Total enriched products: {len(prod_result_dict)}")
    return prod_result_dict

