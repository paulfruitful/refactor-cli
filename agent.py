from google import genai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def create_refactor_agent():
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

    prompt = PromptTemplate(
        input_variables=["code", "language"],
        template=(
            "You are an expert software developer in {language}. Review and refactor the following code. "
            "Your goals are to:\n"
            "1. Fix any likely errors or bugs in the code.\n"
            "2. Make the code more efficient and optimize performance where possible.\n"
            "3. Improve the code's readability and adhere to industry best practices.\n\n"
            "{code}\n\n"
            "Provide only the refactored code without any additional explanations, comments, or English text. "
            "Return only the updated code."
        ),
    )

    def generate_refactored_code(inputs):
        response = client.models.generate_content(
            model='gemini-2.0-flash-thinking-exp',
            contents=prompt.format(**inputs)
        )
        return response.result

    chain = LLMChain(llm=generate_refactored_code, prompt=prompt)
    return chain

def main():
    code_to_refactor = input("Enter the code to refactor:\n")
    language = input("Enter the language of the code to refactor:\n")
    refactor_agent = create_refactor_agent()
    refactored_code = refactor_agent.run({"code": code_to_refactor, "language": language})
    print("\nRefactored Code:\n")
    print(refactored_code)

if __name__ == "__main__":
    main()
