import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class RecipeSuggestor:
    def __init__(self):
        load_dotenv()
        
        # Initialize API keys from environment variables
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        # Initialize LangChain components
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.google_api_key
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            google_api_key=self.google_api_key,
            convert_system_message_to_human=True
        )

    def suggest_recipe(self, ingredients):
        """
        Suggest a recipe based on available ingredients
        """
        prompt_template = """
        Given these ingredients: {ingredients}
        Suggest a recipe that can be made. Include:
        1. Recipe name
        2. Ingredients list with measurements
        3. Step by step instructions
        4. Approximate cooking time
        """
        
        prompt = PromptTemplate(
            input_variables=["ingredients"],
            template=prompt_template
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = chain.invoke({"ingredients": ingredients})
            return response['text']
        except Exception as e:
            return f"Error generating recipe suggestion: {str(e)}"