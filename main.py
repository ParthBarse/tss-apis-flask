import pandas as pd
df = pd.read_excel('products.xlsx')
json_data = df.to_json(orient='records')
with open('output.json', 'w') as f:
    f.write(json_data)