import google.generativeai as genai

genai.configure(api_key="AIzaSyCC-B1PFwUKg6c4ryvQh_QhjCex3bYxSsA")

models = genai.list_models()
for model in models:
    print(model.name)
