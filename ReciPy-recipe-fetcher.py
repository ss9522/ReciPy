import os
import requests
from random import choice
from html.parser import HTMLParser
from datetime import datetime
from time import sleep as slp
import webbrowser

def recipy():

    # <<< Change working directory to prevent files being saved to user's root directory >>>
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Superseded by `os` operations in save_to_file function definition.

    # <<< Start of class, function, and API construction definitions >>>
    def start_sequence():
        global logo
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
        slp(1)
        print("ReciPy - a simple Python program for providing recipes.\n")
        slp(2)
        disclaimer_text = """*DISCLAIMER*
- This program is a pet-project with no commercial intent.
- Recipe data provided by Spoonacular (www.spoonacular.com).
- Spoonacular recipes are aggregated from various individuals and websites.
- Formatting differences between recipes can (and do) affect ReciPy's outputs.
- Some recipes are incorrectly categorised or contain inaccurate information.
- Some recipe instructions consist of hyperlinks to other websites.

Press Ctrl+C to exit at any time."""
        for line in disclaimer_text.split("\n"):
                print(line)
                slp(0.1)

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
                self.instructions.append(self.data.strip())  # Strip whitespace before/after content of each tag, then append to instructions list.

        def handle_data(self, data):
            if self.recording:  # Should only work when recording flag is enabled.
                self.data += data  # Aggregate content inside <li></li>.

    def clean_html_instructions(html_content):

        def add_period(instruction):  # Inner function to add period to the instruction if not present.
            instruction = instruction.strip()  # Removing any extra spaces from start and end.
            endings = [".", "!", ".)", "!)", "...", ".."]
            if not any(instruction.endswith(ending) for ending in endings):
                instruction += "."  # Add a period if not already there.
            return instruction

        if any(tag in html_content for tag in ["<li>", "<ol>"]):  # The block inside this condition will execute if <li> or <ol> tags exist in the content.
            parser = MyHTMLParser()  # Create an instance of the parser.
            parser.feed(html_content)  # Feed the html content to the parser.
            cleaned_instructions_list = [add_period(step) for step in parser.instructions]  # Construct list of cleaned instructions after adding period.
            cleaned_instructions = "\n".join(f"{index}. {step}" for index, step in enumerate(cleaned_instructions_list, 1))  # Formatting the instructions.
        else:
            instructions_list = [add_period(instr) for instr in html_content.split(".") if instr.strip()]  # Split by periods and clean each instruction.
            cleaned_instructions = "\n".join(f"{index}. {step}" for index, step in enumerate(instructions_list, 1))  # Joining the instructions to create a single string.

        cleaned_instructions = cleaned_instructions.replace("<ol>", "").replace("</ol>", "").replace("<p>", "").replace("</p>", "").strip()  # Check and remove the <ol> and </ol> tags if they are present.

        return cleaned_instructions


    def get_yes_no_input(prompt):  # Prompt the user for a yes or no input. Returns True for "y" and False for "n".
        
        while True:  # Keeps loop running until exit condition (return) is met.
            choice = str(input(prompt + "\n[Y]es\t[N]o\n>>> ")).lower()  # Parses all inputs as lowercase
            if len(choice) > 0 and (choice[0] == "y" or choice[0] == "n"):
                return choice[0] == "y"  # Returns boolean True/False depending on choice being "[y]es"
            else:
                print("Invalid input.\n")  # If input doesn't start with "y" or "n", keep asking the user until it does (within while True loop).

    def find_recipe():  # Encapsulated program flow into function to make way for continuous loop
        print("\nFetching recipe...\n")
        slp(1)
        response = requests.get(BASE_URL, headers=headers, params=parameters)  # API request

        if response.status_code != 200:  # Code 200 indicates success. Anything else, we'll want to know.
            print(f"\nError fetching random recipe: Code - {response.status_code}\n")  # Verbose
            if response.status_code == 401:
                slp(1)
                global API_KEY
                API_KEY = input("Not Authorised. Could you check your API key and re-enter it below?\n>>> ")
                headers["x-api-key"] = API_KEY
                print("\nRetrying", end="")
                for i in range(3, 0, -1):
                    print(".", end="", flush=True)
                    slp(1)
                print("\n\n")
                response = requests.get(BASE_URL, headers=headers, params=parameters)

        recipe_id = response.json()["recipes"][0]["id"]

        response = requests.get(DETAILED_RECIPE_URL.format(id=recipe_id), params={"apiKey": API_KEY})

        if response.status_code != 200:  # Code 200 indicates success. Anything else, we'll want to know.
            print(f"\n\nError fetching detailed recipe: Code - {response.status_codye}")

        recipe_info = response.json()
        # Uncomment to debug
        # print("--------------------\nDebug Output: Raw Instructions:", recipe_info.get("instructions"),"\n--------------------")

        title, ingredients, instructions = extract_recipe_information(recipe_info)

        print("\n")
        display_recipe(title, ingredients, instructions)

        if get_yes_no_input("\nWould you like to save this recipe as a text file?"):
            current_datetime = datetime.now().strftime("%d-%m-%y-%H%M%z")
            print("\nMaking sure filename is valid", end="")
            for i in range(3, 0, -1):
                print(".", end="", flush=True)
                slp(1)
            fs_friendly_title = make_fs_friendly(title)
            filename = f"{fs_friendly_title}-{current_datetime}.md"
            save_to_file(filename, title, ingredients, instructions)
            print(f"\n\nRecipe saved to {filename}. Please see \"ReciPy\" folder.")
        slp(1)
        greeting = ["Bon appetit!", "Enjoy the meal!", "Happy cooking!", "*Chef's kiss*"]
        print("\n" + choice(greeting))

    def extract_recipe_information(data):
        print("Extracting recipe information", end="")
        for i in range(3, 0, -1):
            print(".", end="", flush=True)
            slp(1)
        title = data.get("title", "")  # Extracts title from recipe info.
        ingredients = [ingredient.get("original", "") for ingredient in data.get("extendedIngredients", [])]  # Extracts extended ingredients from API response.
        html_instructions = data.get("instructions", "")  # Extracts unparsed HTML-formatted instructions, will need further cleaning prior to output.
        instructions = clean_html_instructions(html_instructions) # Call HTML cleaner function with raw HTML instructions as argument
        return title, ingredients, instructions

    def display_recipe(title, ingredients, instructions):  # Define function that displays recipes in user-friendly format, taking title, ingredients, and cleaned instructions as arguments.
        print(f"Recipe: {title}\n")  # Prints recipe title
        slp(1)
        print("Ingredients:")
        slp(0.5)                        # |
        for ingredient in ingredients:  # |------> Prints list of ingredients
            print(f"- {ingredient}")    # |
            slp(0.2)
        print("\nInstructions:")
        slp(0.5)
        for instruction in instructions.split("\n"):
            print(instruction)
            slp(0.2)  
        slp(1.8)
          
    def make_fs_friendly(title):
        unwanted_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*", " "]
        for char in unwanted_chars:
            title = title.replace(char, "-")
        return title

    def save_to_file(filename, title, ingredients, instructions):
        directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ReciPy")
        if not os.path.exists(directory_path):
            os.makedirs(directory_path) 
        
        full_file_path = os.path.join(directory_path, filename)
        fulldatetime = datetime.now().strftime("%a %d %b, %H:%M %z")
        
        with open(full_file_path, "w", encoding="utf-8") as file:
            print("\n\nGenerating file", end="")
            for i in range(3, 0, -1):
                print(".", end="", flush=True)
                slp(1)
            file.write(f"\n```\n{logo}\n```\n\n# ReciPy Recipe Export\n\nGenerated on {fulldatetime}\n")
            if vegan:
                file.write("### Dietary Preference:\nVegan")
            if vegetarian:
                file.write("### Dietary Preference:\nVegetarian")
            if len(exclusions) > 0:
                file.write("\n\n### Exclusions & Intolerances: ")
                for exclusion in exclusions:
                    exclusion_cap = exclusion.capitalize()
                    file.write(f"\n* {exclusion_cap}")
            file.write(f"\n\n## Recipe: {title}\n\n### Ingredients:\n")
            for ingredient in ingredients:
                file.write(f"* {ingredient}\n")
            file.write(f"\n### Instructions:\n{instructions}\n\nThanks for using **ReciPy**!\nData provided by [Spoonacular](www.spoonacular.com)")

    def exit_sequence():
        input("\nPress [Enter] to exit\n>>> ")
        print("\nExiting ReciPy", end="")
        for i in range(3, 0, -1):
            print(".", end="", flush=True)
            slp(1)
        print("\n\nExit Code [0]\n")
        slp(0.5)

    # <<< End of class, function, and API construction definitions. >>>

    start_sequence()

    # <<< Start of User Preferences >>>
    slp(1)
    print("\nWelcome to ReciPy.")
    slp(1)
    vegan = get_yes_no_input("\nAre you vegan?")
    vegetarian = False
    dairy_ok = False
    eggs_ok = False
    if not vegan:
        vegetarian = get_yes_no_input("\nAre you vegetarian?")
        dairy_ok = get_yes_no_input("\nIs dairy ok?")
        eggs_ok = get_yes_no_input("\nHow about eggs?")

    print("\nList your intolerances separated by space (e.g. \"g w m s\") and hit [Enter].\n")
    slp(1)
    if vegan or vegetarian:  # Provide a list of intolerances that exclude meat options.
        print("Options: \n\nGr[a]in    \tSul[f]ite  \t[G]luten \n\nSesa[m]e   \t[P]eanut   \t[S]oy   \n\n[T]ree Nut \t[W]heat")
    else:  # Provide a list of intolerances inclusive of meat options
        print("Options: \n\nGr[a]in    \tS[e]afood  \tSul[f]ite\n\n[G]luten   \tS[h]ellfish\tSesa[m]e\n\n[P]eanut   \t[S]oy      \t[T]ree Nut \n\n[W]heat")
    slp(2)
    intolerances_input = str(input("\nOr else, just hit [Enter] if you have no intolerances.\n>>> ")).lower()  # Requires user input

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
        exclusions.append("dairy")  # Append "dairy" to exclusions list if answered "n" to dairy in beginning
    if not eggs_ok:
        exclusions.append("egg")  # Append "eggs" to exclusions list if answered "n" to eggs in beginning

    exclusions_param = ",".join(exclusions)  # Set up the exclusion parameter for the API call
    # <<< End of User Preferences >>>

    # print(exclusions_param)  # Uncomment for debug output

    # <<< Construct API call using parameters from above user preferences >>
    slp(1)
    global API_KEY
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

    while True:
        find_recipe()
        slp(1)
        if not get_yes_no_input("\nWould you like to fetch another recipe?"):
            slp(0.5)
            if get_yes_no_input("\nWould you like to visit Spoonacular?"):
                webbrowser.open("https://www.spoonacular.com/")
            slp(0.5)
            break

    exit_sequence()

if __name__ == "__main__":
    try:
        recipy()
    except KeyboardInterrupt:
        print("\n\nProgram aborted by user.")
        slp(0.5)
        print("\nCleaning up", end="")
        for i in range(3, 0, -1):
            print(".", end="", flush=True)
            slp(1)
        print("\n\nExit Code [2]\n")
        slp(0.5)