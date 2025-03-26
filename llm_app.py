import google.generativeai as genai

API_KEY = "AIzaSyB9DXELrAgFvXSC7o-pqG2VvEP_JxKvIbo"  
genai.configure(api_key=API_KEY)

def generate_response(prompt_template, user_input, model_name="gemini-1.5-pro-latest"):
    """
    Generate a response using the Gemini Pro API.
    :param prompt_template: Template for the prompt.
    :param user_input: User's input to insert into the template.
    :param model_name: The model to use (default is gemini-2).
    :return: Generated response from the model.
    """
    
    prompt = prompt_template.format(user_input=user_input)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    return response.text if response and hasattr(response, "text") else "No response generated."

prompt_template = """
You are a helpful assistant. Answer the following question clearly:
"{user_input}"
"""

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    reply = generate_response(prompt_template, user_query)
    print("\nAssistant's Response:")
    print(reply)
