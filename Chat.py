import ollama

def chat_with_model():
    model_name = "llama3.2"  # Specify the LLM model to use
    chat_history = []  # To store the conversation

    print("Welcome to the Llama3.2 chatbot! Type your question below or type 'Bye' to exit.")

    while True:
        user_input = input("You: ")
        
        if user_input.strip().lower() == "bye":
            print("Llama3.2: See you soon!")
            chat_history.append(f"You: {user_input}\nLlama3.2: See you soon!")
            break

        try:
            # Generate a response using the model
            response = ollama.generate(model=model_name, prompt=user_input)
            model_response = response['response']
            print(f"Llama3.2: {model_response}")

            # Save the interaction to the chat history
            chat_history.append(f"You: {user_input}\nLlama3.2: {model_response}")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Save the chat history to a file
    try:
        with open("chat_history.txt", "w", encoding="utf-8") as file:
            file.write("\n\n".join(chat_history))
        print("Chat history saved to 'chat_history.txt'")
    except Exception as e:
        print(f"An error occurred while saving the chat history: {e}")

if __name__ == "__main__":
    chat_with_model()
