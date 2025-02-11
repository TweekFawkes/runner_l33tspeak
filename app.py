import argparse

import os
# from dotenv import load_dotenv
import anthropic
# import time

### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ###

def setup_argparse():
    parser = argparse.ArgumentParser(description='L33tSpeak Translator')
    parser.add_argument('--user_input', type=str, help='User Input')
    return parser.parse_args()

### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ### ~~~ ###

def main():
    # Load environment variables
    # load_dotenv()
    
    args = setup_argparse()

    if not args.user_input:
        print("Error: --user_input is required")
        return
    
    print(f"Generating L33tSpeak for {args.user_input}")
    sText = args.user_input
    
    try:
        # Get the API key from environment variables
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=api_key)

        sUserRole = "user"
        
        # Add error handling for file operations
        try:
            with open('sSystemPrompt001.md', 'r') as file:
                sSystemPrompt = file.read()
            
            with open('sUserPrompt001.md', 'r') as file:
                sUserPrompt = file.read()
        except FileNotFoundError as e:
            print(f"Error: Required prompt files not found: {str(e)}")
            return
        
        # Send the message to Claude
        sUserPromptWithInput = sUserPrompt + " " + sText
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.7,
            system=sSystemPrompt,
            messages=[
                {"role": sUserRole, "content": sUserPromptWithInput}
            ]
        )
        
        # Extract and return the response
        print("L33tSpeak: " + message.content[0].text)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
