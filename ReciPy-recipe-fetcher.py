import os
import requests
from random import choice
from html.parser import HTMLParser
from datetime import datetime
import webbrowser

# <<< Change working directory to prevent files being saved to user's root directory >>>
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# <<< Start of class, function, and API construction definitions >>>
class MyHTMLParser(HTMLParser):  # Subclass inherited from the imported HTMLParser
    def __init__(self):
        super().__init__()  # Make sure OG HTMLParser init gets executed.
        self.instructions = []  # Empty list to store cleaned instructions.
        self.recording = False  # Not recording anything yet during init.

    def handle_starttag(self, tag, attrs):  # Attributes not yet in use but there just in case.
        if tag == "li":  # Condition to check for tags starting with <li>.
            self.recording = True  # Set recording flag to begin capturing data inside tag.
            self.data = ""  # Create empty string for adding content from tag.

    def handle_endtag(self, tag):
        if tag == "li" and self.recording:  # Condition to check for tags ending </li> and if the parser is already capturing contents inside the <li>example</li>.
            self.recording = False  # Stop recording at end of tag (</li>).
            self.instructions.append(self.data.strip()) # Strip whitespace before/after content of each tag, then append to instructions list.

    def handle_data(self, data):
        if self.recording:  # Should only work when recording flag is enabled.
            self.data += data  # Aggregate content inside <li></li>.

def clean_html_instructions(html_content):

    def add_period(instruction):  # Inner function to add period to the instruction if not present.
        instruction = instruction.strip()  # Removing any extra spaces from start and end.
        if not instruction.endswith("."):
            instruction += "."  # Add a period if not already there.
        return instruction

    
    
    if any(tag in html_content for tag in ["<li>", "<ol>"]):  # The block inside this condition will execute if <li> or <ol> tags exist in the content.
        parser = MyHTMLParser()  # Create an instance of the parser.
        parser.feed(html_content)  # Feed the html content to the parser.
        cleaned_instructions_list = [add_period(step) for step in parser.instructions]  # Construct list of cleaned instructions after adding period.
        html_content = ". ".join(cleaned_instructions_list)  # Converting the list into a string for further processing.

    instructions_list = [add_period(instr) for instr in html_content.split(".") if instr.strip()]  # Split by periods and clean each instruction, regardless of whether <li> tags exist.
    cleaned_instructions = "\n".join(f"{index}. {step}" for index, step in enumerate(instructions_list, 1))  # Joining the instructions to create a single string.
    cleaned_instructions = cleaned_instructions.replace("<ol>", "").replace("</ol>", "").replace("<p>", "").replace("</p>", "").strip()  # Check and remove the <ol> and </ol> tags if they are present.

    return cleaned_instructions

def get_yes_no_input(prompt):  # Prompt the user for a yes or no input. Returns True for 'y' and False for 'n'.
    
    while True:  # Keeps loop running until exit condition (return) is met.
        choice = str(input(prompt + "\n[Y]es\t[N]o\n>>> ")).lower()  # Parses all inputs as lowercase
        if len(choice) > 0 and (choice[0] == "y" or choice[0] == "n"):
            return choice[0] == "y"  # Returns boolean True/False depending on choice being '[y]es'
        else:
            print("Invalid input.\n")  # If input doesn't start with 'y' or 'n', keep asking the user until it does (within while True loop).


def extract_recipe_information(data):
    title = data.get("title", "")  # Extracts title from recipe info.
    ingredients = [ingredient.get("original", "") for ingredient in data.get("extendedIngredients", [])]  # Extracts extended ingredients from API response.
    html_instructions = data.get("instructions", "")  # Extracts unparsed HTML-formatted instructions, will need further cleaning prior to output.
    instructions = clean_html_instructions(html_instructions) # Call HTML cleaner function with raw HTML instructions as argument
    return title, ingredients, instructions

def display_recipe(title, ingredients, instructions):  # Define function that displays recipes in user-friendly format, taking title, ingredients, and cleaned instructions as arguments.
    print(f"Recipe: {title}\n")  # Prints recipe title
    print("Ingredients:")           # |
    for ingredient in ingredients:  # |------> Prints list of ingredients
        print(f"- {ingredient}")    # |
    print("\nInstructions:")
    print(instructions)  # Prints instructions from clean_html_instructions output

def end_greeting():
    greeting = ["Bon appetit!", "Enjoy the meal!", "Happy cooking!", "*Chef's kiss*"]
    visit_site = get_yes_no_input("\nWould you like to visit Spoonacular to find more recipes?")
    if visit_site:
        webbrowser.open("https://www.spoonacular.com/")
    print("\n" + choice(greeting))
    
def save_to_file(filename, title, ingredients, instructions):
    fulldatetime = datetime.now().strftime("%a %d %b, %H:%M %z")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"\n{logo}\n\nRecipe Export - {fulldatetime}\n")
        if vegan:
            file.write("Dietary Preference: Vegan")
        if vegetarian:
            file.write("Dietary Preference: Vegetarian")
        if len(exclusions) > 0:
            file.write("\n\nExclusions: ")
            for exclusion in exclusions:
                exclusion_cap = exclusion.capitalize()
                file.write(f"\n- {exclusion_cap}")
        file.write(f"\n\nRecipe: {title}\n")
        file.write("\nIngredients:\n")
        for ingredient in ingredients:
            file.write(f"- {ingredient}\n")
        file.write("\nInstructions:\n")
        file.write(f"\n{instructions}\n")
        file.write("\nThanks for using ReciPy!\nData provided by Spoonacular API (www.spoonacular.com)\n")



# <<< End of class, function, and API construction definitions. >>>

# <<< Program Introduction >>>
logo = """
 #######                      ##   #######           
  ##   ##                           ##   ##          
  ##   ##   #####    #####  ####    ##   ##  ##  ##  
  ######   ##   ##  ##        ##    ######   ##  ##  
  ## ##    #######  ##        ##    ##       ##  ##  
  ##  ##   ##       ##        ##    ##        #####  
  ##   ##   #####    #####  ######  ##           ##  
                                              ####  
"""
print(logo+"\n") # Prints ASCII logo above
print("Welcome to ReciPy, a simple Python program for providing recipes.\n*Recipe data provided by Spoonacular (www.spoonacular.com)\n") # Brief description of program. Backlink as requested by Spoonacular for using free tier to access their API.
# <<< End of program introduction >>>

# <<< Start of User Preferences >>>
vegan = get_yes_no_input("Are you vegan?")
vegetarian = False
dairy_ok = False
eggs_ok = False
if not vegan:
    vegetarian = get_yes_no_input("\nAre you vegetarian?")
    dairy_ok = get_yes_no_input("\nIs dairy ok?")
    eggs_ok = get_yes_no_input("\nAnd what about eggs?")

print("\nList your intolerances separated by space (e.g. \"g w m s\") and hit Enter.\n")

if vegan or vegetarian:  # Provide a list of intolerances that exclude meat options.
    print("Options: \n\nGr[a]in    \tSul[f]ite  \t[G]luten \n\nSesa[m]e   \t[P]eanut   \t[S]oy   \n\n[T]ree Nut \t[W]heat")
else:  # Provide a list of intolerances inclusive of meat options
    print("Options: \n\nGr[a]in    \tS[e]afood  \tSul[f]ite\n\n[G]luten   \tS[h]ellfish\tSesa[m]e\n\n[P]eanut   \t[S]oy      \t[T]ree Nut \n\n[W]heat")

intolerances_input = str(input("\nOr else, just hit Enter if you have no intolerances.\n>>> ")).lower()  # Requires user input

intolerances_map = {"a": "grain", 
                    "e": "seafood", 
                    "f": "sulfite", 
                    "g": "gluten", 
                    "h": "shellfish", 
                    "m": "sesame", 
                    "p": "peanut", 
                    "s": "soy", 
                    "t": "tree-nut", 
                    "w": "wheat",       
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

exclusions_param = ",".join(exclusions)  # Set up the exclusion parameter for the API call
# <<< End of User Preferences >>>

# print(exclusions_param)  # Uncomment for debug output

# <<< Construct API call using parameters from above user preferences >>
API_KEY = str(input("\nEnter your Spoonacular API key below.\n(Visit www.spoonacular.com/food-api to obtain a key.)\n>>> "))  # requests users to input their own Spoonacular API key
BASE_URL = "https://api.spoonacular.com/recipes/random" # base URL lifted from Spoonacular API guide
DETAILED_RECIPE_URL = "https://api.spoonacular.com/recipes/{id}/information"  # Recipe endpoint from Spoonacular API guide

parameters = {  # Parameters for the Spoonacular API call
    "number": 1,  # for simplicity, 1 meal
    "tags": f"",  # Empty string, to be populated from vegetarian/vegan requirement
    "intolerances": exclusions_param  # Fed from prior user inputs
}

if vegan:
    parameters["tags"] += "vegan"  # Add vegan to tag parameter
elif vegetarian:
    parameters["tags"] += "vegetarian"  # Add vegetarian to tag parameter

headers = {  # Headers for the API call
    "Content-Type": "application/json",  # Default content type per Spoonacular API documentation
    "x-api-key": API_KEY  # Fed into API call as a header
}
# <<< End of API call construction >>>

response = requests.get(BASE_URL, headers=headers, params=parameters)  # API request

if response.status_code != 200:  # Code 200 indicates success. Anything else, we'll want to know.
    print(f"Error fetching random recipe: Code - {response.status_code}")  # Verbose
    exit()

recipe_id = response.json()["recipes"][0]["id"]

response = requests.get(DETAILED_RECIPE_URL.format(id=recipe_id), params={"apiKey": API_KEY})

if response.status_code != 200:  # Code 200 indicates success. Anything else, we'll want to know.
    print(f"Error fetching detailed recipe: Code - {response.status_code}")
    exit()

recipe_info = response.json()
# Uncomment to debug
# print("--------------------\nDebug Output: Raw Instructions:", recipe_info.get("instructions"),"\n--------------------")

print("\n")
title, ingredients, instructions = extract_recipe_information(recipe_info)

print("\n")
display_recipe(title, ingredients, instructions)

print("\n")
if get_yes_no_input("Would you like to save this recipe as a text file?"):
    current_datetime = datetime.now().strftime("%d-%m-%y-%H%M%z")
    filename = f"ReciPy - {title} - {current_datetime}.txt"
    save_to_file(filename, title, ingredients, instructions)
    print(f"\nRecipe saved to {filename}.\n")

end_greeting()
input("\nPress [Enter] to exit...\n>>> ")
