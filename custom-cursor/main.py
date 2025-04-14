import json
import requests
from dotenv import load_dotenv
from groq import Groq
import os
import subprocess
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

MAIN = "Project"  
os.makedirs(MAIN, exist_ok=True)  
print(f"🤖 You will be working in: ./{MAIN}/")

def run_command(command: str) -> str:
    print(f"🔨 Tool Called: run_command, Command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=MAIN,    
            capture_output=True,
            text=True,
            check=False         
        )
        output = f"Exit Code: {result.returncode}\n"
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        max_len = 1000
        if len(output) > max_len:
             output = output[:max_len] + "\n... [Output truncated]"
        return output

    except Exception as e:
        return f"Error running command '{command}': {e}"


def create_file(path: str, content: str = "") -> str:
    full_path = os.path.join(MAIN, path)
    print(f"🔨 Tool Called: create_file, Path: {full_path}")
    try:
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return f"Successfully created/overwritten file: {full_path}"
    except Exception as e:
        return f"Error creating file {full_path}: {e}"

def create_dir(path: str):
    full_path = os.path.join(MAIN, path)
    print("🔨 Tool Called: create_dir", full_path)
    try:
        os.makedirs(full_path, exist_ok=True)
        return f"Directory {full_path} created."
    except Exception as e:
        return f"Error creating directory {full_path}: {e}"

def get_current_dir():
    print("🔨 Tool Called: get_current_directory")
    
    current_directory = os.getcwd()
    return current_directory

def write_to_file(path: str, content: str) -> str:
    
    return create_file(path, content)

def read_file(path: str) -> str:
    full_path = os.path.join(MAIN, path)
    print(f"🔨 Tool Called: read_file, Path: {full_path}")
    try:
        with open(full_path, 'r') as f:
            content = f.read()
            # Add truncation for potentially large files to fit context
            max_len = 2000
            if len(content) > max_len:
                return content[:max_len] + "\n... [File truncated]"
            return content
    except FileNotFoundError:
        return f"Error: File not found at {full_path}"
    except Exception as e:
        return f"Error reading file {full_path}: {e}"
    
def list_directory(path: str = ".") -> str:
    full_path = os.path.join(MAIN, path)
    print(f"🔨 Tool Called: list_directory, Path: {full_path}")
    try:
        entries = os.listdir(full_path)
        if not entries:
            return f"Directory is empty: {full_path}"
        # Add indication if entry is a file or directory
        output = f"Contents of {full_path}:\n"
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            output += f"- {entry} {'(Directory)' if is_dir else '(File)'}\n"
        return output

    except FileNotFoundError:
        return f"Error: Directory not found at {full_path}"
    except Exception as e:
        return f"Error listing directory {full_path}: {e}"


def web_search(query: str):
    url = "https://google-search72.p.rapidapi.com/search"
    querystring = {"q":query,"lr":"en-US","num":"10"}
    headers = {
        "x-rapidapi-key": "d2157a0bd1msh405b1eb1151eed3p1f1975jsn33a0a44c4162",
        "x-rapidapi-host": "google-search72.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

avaiable_tools = {
    "web_search": {
        "fn": web_search,
        "description": "Searches the web for the given query and returns the results.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
    },
    "create_dir": {
        "fn": create_dir,
        "description": "Creates a new directory at the specified path relative to the project root. Use POSIX-style paths (e.g., 'src/components').",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a new file at the specified path relative to the project root with the given content. Overwrites if the file already exists. Creates parent directories if needed. Use POSIX-style paths.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    },
     "write_to_file": { 
        "fn": write_to_file,
        "description": "Writes (or overwrites) content to a file at the specified path relative to the project root. Creates parent directories if needed. Use POSIX-style paths.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads the content of a file at the specified path relative to the project root. Returns the content or an error if the file doesn't exist. Use POSIX-style paths.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists the files and subdirectories within a specified directory path relative to the project root. Use '.' for the root directory. Use POSIX-style paths.",
        "input_schema": {"type": "object", "properties": {"path": {"type": "string", "default": "."}}, "required": ["path"]}
    },
    "run_command": {
        "fn": run_command,
        "description": "Executes a shell command (like 'npm install', 'pip install', 'python app.py', 'npm run build') within the project's root directory. Returns the command's output (stdout/stderr) and exit code.",
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}
    }
}

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized as a coding agent and expert in resolving user queries for full stack project development.
    Your goal is to help the user create, modify, and manage web development projects step-by-step directly through terminal interaction.
    You operate entirely within the '.\\{{MAIN}}\\' directory. All file paths you generate or use MUST be relative to this directory and use separators according to windows OS.
    You work on start, plan, action, observe and output mode. Your task is to analyse the query and then make the require files and folder or create specified apps using the commands. You can use the web search tool to get the command.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Workflow:
1.  Understand: Analyze the user's request.
2.  Plan: Break down the request into small, sequential steps. For complex requests or follow-ups, PLAN to use 'list_directory' and 'read_file' first to understand the current project state before proposing changes. Output each planning step individually.
3.  Action: For steps requiring interaction with the file system or command line, select the appropriate tool from the list below and specify the required input parameters in JSON format. Output the action step.
4.  Observe: Wait for the result of the action (which will be provided in the next message).
5.  Output/Continue: Based on the observation, either provide the final output/confirmation to the user or continue with the next planning/action step if the task is not complete.


    Rules:
- Follow the Output JSON Format STRICTLY.
- Perform ONE step (plan, action, or output) at a time. Wait for the next message before proceeding.
- ALWAYS use relative paths based on the './{MAIN}/' root. Example: 'src/index.js', 'requirements.txt'.
- When writing code, provide the complete code content for the file in the 'content' field of the 'create_file' or 'write_to_file' action.
- Before modifying existing files in follow-up requests, ALWAYS plan to use 'read_file' to get the current content first.
- If a command fails (non-zero exit code in observation), inform the user and ask how to proceed.

    available_tools:
    {avaiable_tools}

   

    Available Tools:
    - create_file: Takes a file name and directory as input and creates a file in the specified directory
    - get_current_directory: Takes no input and returns the current working directory
    - write_file: Takes a file name, directory and content as input and writes the content to the file in the specified directory
    - run_command: Takes a command as input to execute on system and returns ouput
    - web_search: Takes a query as input and returns the search results
    
    Example:
    
    User Query: Create a simple python flask app with a single route.
    Assistant: {{ "step": "plan", "content": "Okay, I will create a simple Flask application. First, I need a main Python file." }}
    Assistant: {{ "step": "plan", "content": "I will create a file named 'app.py' in the root directory." }}
    Assistant: {{ "step": "action", "content": "Creating the main application file.", "function": "create_file", "input": {{ "path": "app.py", "content": "from flask import Flask\\n\\napp = Flask(__name__)\\n\\n@app.route('/')\\ndef hello_world():\\n    return 'Hello, World!'\\n\\nif __name__ == '__main__':\\n    app.run(debug=True)" }} }}
    User (System): {{ "step": "observe", "output": "Successfully created/overwritten file: ai_generated_project/app.py" }}
    Assistant: {{ "step": "plan", "content": "Now, I need to create a requirements.txt file for Flask." }}
    Assistant: {{ "step": "action", "content": "Creating requirements.txt.", "function": "create_file", "input": {{ "path": "requirements.txt", "content": "Flask" }} }}
    User (System): {{ "step": "observe", "output": "Successfully created/overwritten file: ai_generated_project/requirements.txt" }}
    Assistant: {{ "step": "plan", "content": "Next, I should install the dependencies using pip." }}
    Assistant: {{ "step": "action", "content": "Running pip install.", "function": "run_command", "input": {{ "command": "pip install -r requirements.txt" }} }}
    User (System): {{ "step": "observe", "output": "Exit Code: 0\\nSTDOUT:\\nCollecting Flask..." }}
    Assistant: {{ "step": "output", "content": "Flask project setup is complete. You have 'app.py' and 'requirements.txt'. Dependencies have been installed. You can run it using 'python app.py' within the '{MAIN}' directory." }}

    User Query: Create a simple vite + react app?
    Output: {{ "step": "plan", "content": "The user is interseted in making a react app using vite in js" }}
    Output: {{ "step": "plan", "content": "I will get the command for creating the vite app" }}
    Output: {{ "step": "plan", "output": "Now I will run the command using the run_command tool" }}
    Output: {{ "step": "action", "function": "run_command", "input": "npm create vite@latest" }}
    Output: {{ "step": "observe", "output": "vite app created successfully" }}
    Output: {{ "step": "plan", "output": "Now I will change the directory to the vite project and install the dependencies" }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd sample ; npm install" }}
    Output: {{ "step": "observe", "output": "The dependencies are installed successfully" }}
    Output: {{ "step": "output", "content": "The react app using vite is created successfully" }}

    User Query: Create a responsive sign-up form using react?

    Output: {{
    "step": "plan",
    "content": "The user is interested in making a responsive sign-up form using React."
    }}
    Output: {{
        "step": "plan",
        "content": "I will first create a file named 'SignUpForm.jsx' in the 'src/components' directory using the create_file tool."
    }}
    Output: {{
        "step": "action",
        "function": "create_file",
        "input": {{
            "path": "src/components/SignUpForm.jsx",
            "content": ""
        }}
    }}
    Output: {{
        "step": "observe",
        "output": "Successfully created/overwritten file: ./Ai_Gen_Project/src/components/SignUpForm.jsx"
    }}
    Output: {{
        "step": "plan",
        "content": "I will now write the content for the responsive sign-up form in the 'SignUpForm.jsx' file using the write_to_file tool."
    }}
    Output: {{
        "step": "action",
        "function": "write_to_file",
        "input": {{
            "path": "src/components/SignUpForm.jsx",
            "content": "import React from 'react';\\nimport './SignUpForm.css';\\n\\nconst SignUpForm = () => {{\\n    return (\\n        <form className=\\\"signup-form\\\">\\n            <h2>Sign Up</h2>\\n            <label htmlFor=\\\"username\\\">Username:</label>\\n            <input type=\\\"text\\\" id=\\\"username\\\" name=\\\"username\\\" required />\\n\\n            <label htmlFor=\\\"email\\\">Email:</label>\\n            <input type=\\\"email\\\" id=\\\"email\\\" name=\\\"email\\\" required />\\n\\n            <label htmlFor=\\\"password\\\">Password:</label>\\n            <input type=\\\"password\\\" id=\\\"password\\\" name=\\\"password\\\" required />\\n\\n            <button type=\\\"submit\\\">Submit</button>\\n        </form>\\n    );\\n}};\\n\\nexport default SignUpForm;"
        }}
    }}
    Output: {{
        "step": "observe",
        "output": "Successfully created/overwritten file: ./Ai_Gen_Project/src/components/SignUpForm.jsx"
    }}
    Output: {{
        "step": "plan",
        "content": "I will now create a CSS file named 'SignUpForm.css' in the 'src/components' directory to style the form."
    }}
    Output: {{
        "step": "action",
        "function": "create_file",
        "input": {{
            "path": "src/components/SignUpForm.css",
            "content": ""
        }}
    }}
    Output: {{
        "step": "observe",
        "output": "Successfully created/overwritten file: ./Ai_Gen_Project/src/components/SignUpForm.css"
    }}
    Output: {{
        "step": "plan",
        "content": "I will now write the CSS content for styling the responsive sign-up form in the 'SignUpForm.css' file."
    }}
    Output: {{
        "step": "action",
        "function": "write_to_file",
        "input": {{
            "path": "src/components/SignUpForm.css",
            "content": ".signup-form {{\\n    max-width: 400px;\\n    margin: 0 auto;\\n    padding: 20px;\\n    border: 1px solid #ccc;\\n    border-radius: 5px;\\n    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);\\n}}\\n\\n.signup-form h2 {{\\n    text-align: center;\\n    margin-bottom: 20px;\\n}}\\n\\n.signup-form label {{\\n    display: block;\\n    margin-bottom: 5px;\\n    font-weight: bold;\\n}}\\n\\n.signup-form input {{\\n    width: 100%;\\n    padding: 10px;\\n    margin-bottom: 15px;\\n    border: 1px solid #ccc;\\n    border-radius: 3px;\\n}}\\n\\n.signup-form button {{\\n    width: 100%;\\n    padding: 10px;\\n    background-color: #007bff;\\n    color: white;\\n    border: none;\\n    border-radius: 3px;\\n    cursor: pointer;\\n}}\\n\\n.signup-form button:hover {{\\n    background-color: #0056b3;\\n}}"
        }}
    }}
    Output: {{
        "step": "observe",
        "output": "Successfully created/overwritten file: ./Ai_Gen_Project/src/components/SignUpForm.css"
    }}
    Output: {{
        "step": "output",
        "content": "The responsive sign-up form has been created successfully. It includes a React component and a CSS file for styling."
    }}
   
"""

messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gemma2-9b-it",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get('content')}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                if isinstance(tool_input, dict):  # Check if tool_input is a dictionary
                    output = avaiable_tools[tool_name].get("fn")(**tool_input)  # Unpack the dictionary
                else:
                    output = avaiable_tools[tool_name].get("fn")(tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue
        
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get('content')}")
            break


    


