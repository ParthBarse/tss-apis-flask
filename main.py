# import pandas as pd
# df = pd.read_excel('exported_products.xlsx')
# json_data = df.to_json(orient='records')
# with open('output.json', 'w') as f:
#     f.write(json_data)

import json


original_data = {
    "pid": "ca5751d2-59ea-414a-b0c2-71ef7e2b3ae6",
    "product_name": "Tops",
    "desc": "Explore our extensive collection of stylish tops, from casual tees to elegant blouses, perfect for any event or mood. Find your perfect fit and elevate your wardrobe with our versatile selection. Shop now for the latest trends!",
    "fit": "<ol><li>Slim fit<\/li><li>Regular fit<\/li><li>Loose fit<\/li><li>Relaxed fit<\/li><li>Oversized fit<\/li><li>Cropped fit<\/li><li>Fitted<\/li><li>Tailored fit<\/li><li>Boxy fit<\/li><li>Peplum fit<\/li><li>Wrap fit<\/li><\/ol><p><br><\/p>",
    "discount": 20,
    "discount_date_start": "2024-02-01",
    "discount_date_end": "2024-02-10",
    "discount_type": "percent",
    "category": "Gifts",
    "sub_category": "bferg",
    "quantity_pi": 45,
    "reward_points": 5,
    "sku": "Discover the Latest Trends in Tops for Every Occasion | Shop Now!",
    "tags": "#tops",
    "unit": 12,
    "unit_price": 180,
    "variantEnabled": True,
    "colors_0_name": "black",
    "colors_0_value": "#000000",
    "variants_0_variantId": 1.0,
    "variants_0_color": "#000000",
    "variants_0_size": "28-30",
    "variants_0_ThumbImg": "['http:\/\/64.227.186.165\/tss_files\/All_Files\/fac15bc5-2904-4d7d-b462-e8044e2696fa.jpg']",
    "variants_0_GalleryImg": "['http:\/\/64.227.186.165\/tss_files\/All_Files\/daf6177c-b9db-4bc9-9e07-27b83d238d19.jpg', 'http:\/\/64.227.186.165\/tss_files\/All_Files\/e2d0e013-61ae-4112-bd5f-5aefbd54d3cd.jpg']",
    "variants_0_price": 0.0,
    "variants_0_quantity": 0.0,
    "variants_0_isEnabled": 1.0,
    "size_0_name": "L",
    "size_0_value": "28-30",
    "fabric": "<ol><li>Cotton<\/li><li>Polyester<\/li><li>Silk<\/li><li>Linen<\/li><li>Rayon<\/li><li>Nylon<\/li><li>Spandex<\/li><li>Wool<\/li><li>Velvet<\/li><li>Chiffon<\/li><li>Denim<\/li><\/ol><p><br><\/p>",
    "about": "<p><span style=\"color: rgb(55, 65, 81);\">Embellishments and decorations, such as embroidery, sequins, and lace trim, add flair and personality to tops, while closures like buttons, zippers, and tie-fronts provide functionality and style. Details like pockets, pleats, and draping further enhance the visual interest and sophistication of tops. Fabric texture also plays a crucial role, whether it's a ribbed knit for added dimension or a sheer chiffon for an ethereal touch. Overall, the intricate details of tops ensure that there's a perfect option for every individual style and occasion.<\/span><\/p>",
    "refund": None,
    "rating": 4,
    "draft": False,
    "product_detail": "<p><span style=\"color: rgb(55, 65, 81);\">Tops come in a myriad of styles, each distinguished by its unique details that contribute to its overall design and appeal. From neckline to hemline, these details offer a plethora of options to suit different preferences and occasions. Whether you prefer a classic crew neck or a trendy off-the-shoulder style, tops cater to various tastes with their diverse neckline options. Sleeve length adds another dimension, ranging from the breeziness of sleeveless designs to the coziness of long sleeves or the chicness of three-quarter sleeves.<\/span><\/p>",
    "SEOArea_metaTitle": "Discover the Latest Trends in Tops for Every Occasion | Shop Now!",
    "SEOArea_metaDescription": "Explore our extensive collection of stylish tops, from casual tees to elegant blouses, perfect for any event or mood. Find your perfect fit and elevate your wardrobe with our versatile selection. Shop now for the latest trends!",
    "SEOArea_metaKeywords": "Sweaters\nTunics\nHoodies\nLong-sleeve tops\nShort-sleeve tops",
    "SEOArea_images1": "http:\/\/64.227.186.165\/tss_files\/All_Files\/e4cd86c0-ef74-4082-97b7-b99167bd0349.jpg"
}

# Convert the original data into the desired format
converted_data = {}

# Copy non-nested fields directly
converted_data["pid"] = original_data["pid"]
converted_data["product_name"] = original_data["product_name"]
converted_data["desc"] = original_data["desc"]
converted_data["fit"] = original_data["fit"]
converted_data["discount"] = str(original_data["discount"])
converted_data["discount_date"] = {
    "start": original_data["discount_date_start"],
    "end": original_data["discount_date_end"]
}
converted_data["discount_type"] = original_data["discount_type"]
converted_data["category"] = original_data["category"]
converted_data["sub_category"] = original_data["sub_category"]
converted_data["quantity_pi"] = original_data["quantity_pi"]
converted_data["reward_points"] = str(original_data["reward_points"])
converted_data["sku"] = original_data["sku"]
converted_data["tags"] = original_data["tags"]
converted_data["unit"] = str(original_data["unit"])
converted_data["unit_price"] = original_data["unit_price"]
converted_data["variantEnabled"] = original_data["variantEnabled"]
converted_data["refund"] = original_data["refund"]
converted_data["rating"] = str(original_data["rating"])
converted_data["draft"] = str(original_data["draft"])
converted_data["product_detail"] = original_data["product_detail"]

# Process nested fields
converted_data["colors"] = [{
    "name": original_data["colors_0_name"],
    "value": original_data["colors_0_value"]
}]

converted_data["variants"] = [{
    "variantId": int(original_data["variants_0_variantId"]),
    "color": original_data["variants_0_color"],
    "size": original_data["variants_0_size"],
    "ThumbImg": json.loads(original_data["variants_0_ThumbImg"]),
    "GalleryImg": json.loads(original_data["variants_0_GalleryImg"]),
    "price": original_data["variants_0_price"],
    "quantity": original_data["variants_0_quantity"],
    "isEnabled": bool(original_data["variants_0_isEnabled"])
}]

converted_data["size"] = [{
    "name": original_data["size_0_name"],
    "value": original_data["size_0_value"]
}]

converted_data["fabric"] = original_data["fabric"]
converted_data["about"] = original_data["about"]

converted_data["SEOArea"] = {
    "metaTitle": original_data["SEOArea_metaTitle"],
    "metaDescription": original_data["SEOArea_metaDescription"],
    "metaKeywords": original_data["SEOArea_metaKeywords"],
    "images1": original_data["SEOArea_images1"]
}

# Display the converted data
print(json.dumps(converted_data, indent=2))
