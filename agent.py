import google.generativeai as genai
import os
from dotenv import load_dotenv


def get_api_key():
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return api_key

def code_mapper_agent(inputs):
    api_key=get_api_key()

    genai.configure(api_key=api_key)
    prompt=prompt = ("""
    You are an expert code analyst specializing in creating comprehensive code maps. Analyze the provided code and create a detailed map that includes:

    1. High-Level Overview:
       - Main purpose and functionality
       - Architecture patterns used
       - Key components and their relationships

    2. Detailed Structure:
       - Function/method hierarchy and relationships
       - Class inheritance and composition
       - Module dependencies
       - Data flow patterns

    3. Code Quality Analysis:
       - Potential bottlenecks
       - Code complexity assessment
       - Reusability opportunities
       - Design pattern implementations

    4. Documentation Status:
       - Coverage of comments and documentation
       - API documentation completeness
       - Missing documentation areas

    Format your response as a structured markdown document with sections and subsections.
    Use diagrams notation (like mermaid) when appropriate to visualize relationships.
    
    Analyze the following code:
    {code}
    """).format(**inputs)
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')
    response = model.generate_content(prompt)
    return response.text


def get_project_description_agent():
    with open('project_desc.txt','w') as desc:
     directory=os.listdir()
     if "README.md" in directory:
        with open("README.md", "r") as file:
            readme_content = file.read()
        return readme_content
     for i in directory:
        if os.path.isdir(i):
            curr_dir=os.chdir(i)
            for i in curr_dir:
                if os.path.isdir(i):
                    curr_dir=os.chdir(i)
                    for i in curr_dir:
                        if os.path.isdir(i):
                            curr_dir=os.chdir(i)
                            for i in curr_dir:
                                if os.path.isdir(i):
                                    curr_dir=os.chdir(i)
                                    for i in curr_dir:
                                        if os.path.isdir(i):
                                            curr_dir=os.chdir(i)
                                            for i in curr_dir:
                                                if os.path.isdir(i):
                                                    curr_dir=os.chdir(i)
                                                    for i in curr_dir:
                                                        if os.path.isdir(i):
                                                            curr_dir=os.chdir(i)
                                                            for i in curr_dir:
                                                                code_map=code_mapper_agent(i)
                                                                desc.write(code_map)
    
def create_readme_agent():
 api_key=get_api_key()

def create_refactor_agent():
    api_key=get_api_key()
    genai.configure(api_key=api_key)

    def generate_refactored_code(inputs):
        prompt = (
            "You are an expert software developer in {language}. Review and refactor the following code. "
            "Your goals are to:\n"
            "1. Fix any likely errors or bugs in the code.\n"
            "2. Correct all wrong syntax and formatting issues.\n"
            "3. Implement the requests in the comments.\n"
            "3. Make the code more efficient and optimize performance where possible.\n"
            "4. Improve the code's readability and adhere to industry best practices.\n\n"
            "{code}\n\n"
            "Provide the refactored code without explanations of the changes you made. "
            "Turn your explanation into a comment in the code.\n\n"
            "Return the response in the following format:\n"
            "The refactored code alone\n\n"
            "Examples:\n"
            "1. Input Code:\n"
            "def add(a, b):\n"
            "    return a + b\n\n"
            "Refactored Code:\n"
            "def add(a, b):\n"
            "    # Adds two numbers and returns the result\n"
            "    return a + b\n\n"
            "2. Input Code:\n"
            "def divide(a, b):\n"
            "    return a / b\n\n"
            "Refactored Code:\n"
            "def divide(a, b):\n"
            "    # Divides a by b, raises ValueError if b is zero\n"
            "    if b == 0:\n"
            "        raise ValueError('Cannot divide by zero')\n"
            "    return a / b\n\n"
            "3. Input Code:\n"
            "for i in range(10):\n"
            "    print(i)\n\n"
            "Refactored Code:\n"
            "# Prints numbers from 0 to 9\n"
            "for i in range(10):\n"
            "    print(i)\n\n"
            "Now refactor the following code:\n"
            "{code}\n\n"
            "Return only the refactored code with comments explaining the changes."
        ).format(**inputs)

        model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-1219')  
        response = model.generate_content(prompt)
        return response.text

    return generate_refactored_code

def main():
    code_to_refactor = input("Enter the code to refactor:\n")
    language = input("Enter the language of the code to refactor:\n")

    refactor_agent = create_refactor_agent()

    try:
        refactored_code = refactor_agent({"code": code_to_refactor, "language": language})
        print("\nRefactored Code:\n")
        print(refactored_code)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()