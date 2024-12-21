from langchain.llms import Ollama


def fine_tune(data_path):
    llm = Ollama(model="llama-3.2")
    fine_tuned_model = llm.fine_tune(input_data=data_path)
    return fine_tuned_model


if __name__ == "__main__":
    model = fine_tune("path/to/training/data.json")
    print("Fine-tuned model created:", model)
