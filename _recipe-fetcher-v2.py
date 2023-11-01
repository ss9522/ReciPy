# import os  # Redundant
import requests
# import json  # Redundantd659f88993504008804de96dea7416c4
# import webbrowser  # Redundant
from html.parser import HTMLParser

# <<< Start of class and function definitions >>>
class MyHTMLParser(HTMLParser):  # Subclass inherited from the imported HTMLParser
    def __init__(self):
        super().__init__()  # Make sure OG HTMLParser init gets executed.
        self.instructions = []  # Empty list to store cleaned instructions.
        self.recording = False  # Not recording anything yet during init.

    def handle_starttag(self, tag, attrs):  # Attributes not yet in use but there just in case.
        if tag == 'li':  # Condition to check for tags starting with <li>.
            self.recording = True  # Set recording flag to begin capturing data inside tag.
            self.data = ''  # Create empty string for adding content from tag.

    def handle_endtag(self, tag):
        if tag == 'li' and self.recording:  # Condition to check for tags ending </li> and if the parser is already capturing contents inside the <li>example</li>.
            self.recording = False  # Stop recording at end of tag (</li>).
            self.instructions.append(self.data.strip()) # Strip whitespace before/after content of each tag, then append to instructions list.

    def handle_data(self, data):
        if self.recording:  # Should only work when recording flag is enabled.
            self.data += data  # Aggregate content inside <li></li>.

def clean_html_instructions(html_content):

    def add_period_to_instruction(instruction):  # Utility function to add period at the end of instruction if it doesn't already have one.
        instruction = instruction.strip()  # Strips the instruction of any whitespace before/after content.
        if not instruction.endswith('.'):  # If the instruction does not already end with a full-stop:
            instruction += '.'  # Add a full-stop
        return instruction
    
    if "<li>" in html_content:  # If there are <li> tags in the content
        parser = MyHTMLParser()  # Create object from HTMLParser subclass
        parser.feed(html_content)  # Feed in HTML content
        # Ensure each instruction has a period at the end
        cleaned_instructions_list = [add_period_to_instruction(step) for step in parser.instructions]
        cleaned_instructions = '\n'.join(f"{index}. {step}" for index, step in enumerate(cleaned_instructions_list, 1))
    
    else:  # If there are no <li> tags, split by full-stops.
        # Split by full-stops and ensure each instruction has a full-stop at the end.
        instructions_list = [add_period_to_instruction(instr) for instr in html_content.split('.') if instr.strip()]
        cleaned_instructions = '\n'.join(f"{index}. {step}" for index, step in enumerate(instructions_list, 1))
    
    return cleaned_instructions  # Returns enumerated instructions as the function output.


def get_yes_no_input(prompt):  # Prompt the user for a yes or no input. Returns True for 'y' and False for 'n'.
    
    while True:  # Keeps loop running until exit condition (return) is met.
        choice = str(input(prompt)).lower()  # Parses all inputs as lowercase
        if choice[0] == 'y' or choice[0] == 'n':
            return choice[0] == 'y'  # Returns boolean True/False depending on choice being '[y]es'
        else:
            print("Invalid input. Please enter 'y' or 'n'\n>>> ")  # If input doesn't start with 'y' or 'n', keep asking the user until it does (within while True loop).

def extract_recipe_information(data):
    title = data.get('title', '')  # Extracts title from recipe info.
    ingredients = [ingredient.get('original', '') for ingredient in data.get('extendedIngredients', [])]  # Extracts extended ingredients from API response.
    html_instructions = data.get('instructions', '')  # Extracts unparsed HTML-formatted instructions, will need further cleaning prior to output.
    instructions = clean_html_instructions(html_instructions)
    return title, ingredients, instructions

def display_recipe(title, ingredients, instructions):
    print(f"Recipe: {title}\n")
    print("Ingredients:")
    for ingredient in ingredients:
        print(f"- {ingredient}")
    print("\nInstructions:")
    print(instructions)
# <<< End of class and function definitions. >>>

# <<< Program Introduction >>>
logo = """
######   ######     #####         ###   ##  #######   #####   
 ##  ##   ##  ##   ### ###         ##   ##   ##  ##  ##   ##  
 ##  ##   ##  ##   ##   ##         ##   ##   ##      ##       
 #####    #####    ##   ##         ##   ##   ####    ## ####  
 ##       ##  ##   ##   ##         ##   ##   ##      ##   ##  
 ##       ##  ##   ### ###          ## ##    ##  ##  ##   ##  
####     #### ###   #####            ###    #######   #####   
"""
print(logo+"\n") # Prints ASCII logo above
print("Welcome to ProVeg, a simple Python program which provides vegetarian recipes that are high in protein. *Recipe data provided by Spoonacular (www.spoonacular.com)\n") # Brief description of program. Backlink as requested by Spoonacular for using free tier to access their API.
# <<< End of program introduction >>>

# <<< Start of User Preferences >>>
dairy_ok = get_yes_no_input("Is dairy ok? ([Y]es/[N]o)\n>>> ")
eggs_ok = get_yes_no_input("\nAnd what about eggs? ([Y]es/[N]o)\n>>> ")

print("\nList your intolerances separated by space (e.g. \"g w m s\") and hit Enter.")
print("- [G]luten\n- Grain & [W]heat\n- [N]uts\n- [S]oy\n- Sesa[m]e\n- [C]orn\n")

intolerances_input = str(input("Or else, just hit Enter if you have no intolerances.\n>>> ")).lower()  # Requires user input

intolerances_map = {'g': 'gluten', 
                    'w': 'grain,wheat', 
                    'n': 'peanut,tree-nut', 
                    's': 'soy', 
                    'm': 'sesame', 
                    'c': 'corn'
                    }  # Map for shorthands

exclusions = []  # Create empty `exclusions` list
already_in_exclusions = set()  # Initialise new set to guard against duplicates

for i in intolerances_input.split():
    if i in intolerances_map and i not in already_in_exclusions:
        exclusions.append(intolerances_map[i])  # Add to exclusions
        already_in_exclusions.add(i)  # Add to set() to exclude duplicates in exclusions

if not dairy_ok:
    exclusions.append("dairy")  # Append 'dairy' to exclusions list if answered 'n' to dairy in beginning
if not eggs_ok:
    exclusions.append("eggs")  # Append 'eggs' to exclusions list if answered 'n' to eggs in beginning

# Set up the exclusion parameter for the API call
exclusions_param = ','.join(exclusions)

# print(exclusions_param)  # Debug Output


API_KEY = str(input("\nEnter your Spoonacular API key below.\n(Visit www.spoonacular.com/food-api to obtain a key.)\n>>> "))  # requests users to input their own Spoonacular API key
BASE_URL = "https://api.spoonacular.com/recipes/random" # base URL lifted from Spoonacular API guide
DETAILED_RECIPE_URL = "https://api.spoonacular.com/recipes/{id}/information"


parameters = {  # Parameters for the Spoonacular API call
    "number": 1,
    "tags": f"vegetarian,high-protein",
    "intolerances": exclusions_param  # Fed from prior user inputs
}

headers = {  # Headers for the API call
    "Content-Type": "application/json",
    "x-api-key": API_KEY  # Fed into API call as a header
}

response = requests.get(BASE_URL, headers=headers, params=parameters)

if response.status_code != 200:
    print(f"Error fetching random recipe: Code - {response.status_code}")
    exit()

recipe_id = response.json()['recipes'][0]['id']

response = requests.get(DETAILED_RECIPE_URL.format(id=recipe_id), params={"apiKey": API_KEY})

if response.status_code != 200:
    print(f"Error fetching detailed recipe: Code - {response.status_code}")
    exit()

recipe_info = response.json()
"""
print("--------------------")
print("Debug Output: Raw Instructions:", recipe_info.get("instructions"))  # Debug Output
print("--------------------")
"""

print("\n")
title, ingredients, instructions = extract_recipe_information(recipe_info)
print("\n")
display_recipe(title, ingredients, instructions)
print("\n ***Bon appetit!***")
input("\n\nPress Enter to exit...")
