import ollama
import requests
from bs4 import BeautifulSoup

def summarize_article(model_name, url):
    try:
        # Fetch and parse the article content
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from the article
        paragraphs = soup.find_all("p")
        article_text = " ".join([p.get_text() for p in paragraphs])

        if not article_text.strip():
            return "The article appears to have no readable content."

        # Ask the model to summarize the article
        summary_prompt = f"Summarize the following article:\n\n{article_text}"
        summary_response = ollama.generate(model=model_name, prompt=summary_prompt)
        return summary_response['text']

    except Exception as e:
        return f"An error occurred while processing the article: {e}"

def chat_with_model():
    model_name = "llava"  # Specify the LLM model to use
    chat_history = []  # To store the conversation

    print("Welcome to the Llava chatbot! Type your question below, type 'Bye' to exit, or provide an article URL to summarize.")

    while True:
        user_input = input("You: ")
        
        if user_input.strip().lower() == "bye":
            print("Llava: See you soon!")
            chat_history.append(f"You: {user_input}\nLlava: See you soon!")
            break

        if user_input.startswith("http://") or user_input.startswith("https://"):
            print("Llava: Fetching and summarizing the article. Please wait...")
            summary = summarize_article(model_name, user_input)
            print(f"Llava: {summary}")
            chat_history.append(f"You: {user_input}\nLlava: {summary}")
        else:
            try:
                # Generate a response using the model
                response = ollama.generate(model=model_name, prompt=user_input)
                model_response = response['response']
                print(f"Llava: {model_response}")

                # Save the interaction to the chat history
                chat_history.append(f"You: {user_input}\nLlava: {model_response}")
            except Exception as e:
                print(f"An error occurred: {e}")

    # Save the chat history to a file
    try:
        with open("chat_history_llava.txt", "w", encoding="utf-8") as file:
            file.write("\n\n".join(chat_history))
        print("Chat history saved to 'chat_history_llava.txt'")
    except Exception as e:
        print(f"An error occurred while saving the chat history: {e}")

if __name__ == "__main__":
    chat_with_model()
