
def analyze_products(prod_result_dict, keywords, max_price):
    analysis = []
    price_flag = False
    print("prod_result_dict : ",len(prod_result_dict))
    for prod_id, product in prod_result_dict.items():

        print(f"Product data: {product}")
        title = product.get("title", "").lower()
        desc = product.get('description') or product.get('desc')
        match_score = sum(1 for k in keywords if k in title or k in desc)
        price_raw = product.get("price", "0")
        if isinstance(price_raw, str):
            price = price_raw.replace("$", "")
        else:
            price = "0"  # or str(price_raw), or however you want to handle it

        print("Cleaned Price:", type(price), "_______",price)
        price_val = 0.0
        try:
            price_val = float(price)
        except:
            print("Invalid price format")
            continue
        if max_price is not None and str(max_price).strip() != "":
        #if float(max_price) and price_val > float(max_price):
            print(f"{ max_price} : {price_val}")
            try:
                if price_val > float(max_price):
                    print(f"{max_price} : {price_val}")
                    price_flag = True
                    print(f"Price flag in analysis {price_flag}")
                    continue  # skip this product
            except ValueError:
                print("Invalid max_price value")

        print("match_score : ",match_score)

        if match_score >= 0 and price_flag == False:

            print("title ",product.get("title"))
            print("price ", product.get("price"))
            print("link",product.get("link"))
            kw= [k for k in keywords if k in title or k in desc]
            print(kw)
            print("match score : ", match_score)
            analysis.append({
                "title": product.get("title"),
                "price": product.get("price"),
                "link": product.get("link"),
                "matched_keywords": [k for k in keywords if k in title or k in desc],
                "desc":product.get("desc"),
                "score": match_score,
                "image":product.get("image")
            })

    return sorted(analysis, key=lambda x: x["score"], reverse=True),price_flag