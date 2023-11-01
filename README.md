# ReciPy
A simple Python program that uses the Spoonacular API to fetch a random recipe based on user preferences.

## Introduction
This README serves as something of a technical blog post - I hope you enjoy reading through this, just as much as I enjoyed writing it (and the code!).

I evidently didn't put much thought into the name of this program, which is merely a combination of **Reci**pes and **Py**thon. *(If anyone owns a copyright, I'm sorry.)*

I designed ReciPy to be a simple terminal-based program that:
1. Takes user inputs on *dietary preferences & restrictions* (parameters); 
2. Pulls a random recipe from online based on those parameters using [Spoonacular's API](https://www.spoonacular.com/food-api); and
3. Delivers the recipe (ingredients & instructions) in a concise format in the terminal itself.

If this program were to solve a problem, I'd wager that *decision fatigue* from looking at countless recipes would be greatly reduced. 

### My Journey with Python
I've always had an interest in technology but never really "programmed" ... until now.

The extent of my technical ability lay on the heels of bash scripting and command-line operations from my youthful Linux distro-hopping.

I decided to explore programming more seriously and Python seemed like a great language to learn with, due to its "syntactic sugar" (how closely it resembles English) and overall simplicity.

The initial stages of my Python journey were a breeze when covering the basics such as lists, loops, conditions, and functions. 

However, I began hitting proverbial walls as I tackled more advanced concepts, such as the nuances of object-oriented programming.

Working on this project and practically applying these concepts has left me more grounded and with that, I look forward to continuing my learning journey.

Additionally, this project has exposed me to other crucial programming concepts such as Git (for version control), and the use of external APIs to use in my own program.

### The Genesis of "ReciPy"
I love to cook almost as much as I love to eat. I therefore wanted my first program to be food-related, hence *ReciPy*.

I came up with ReciPy mainly to impress my fiancée by finding random new recipes without taking forever to find the "perfect recipe".

My initial plan was to store pre-set recipes in my Python program. Aggregating and storing these static recipes might take forever in itself and for the user, where's the fun in that?

As a means to get access to thousands of recipes from online (and also to challenge myself), I decided to learn about, and make use of **APIs**, to bring these recipes with my program.

### APIs: A Brief Overview

**Application Programming Interfaces** (APIs) are essentially a set of protocols that allow different software systems to interact and integrate, allowing them to work together. 

To serve as a non-technical analogy, APIs are akin to waiters in a restaurant. They: 
1. Take meal requests from patrons;
2. Standardise those requests in a way that chefs can understand; and
3. Return to patrons with the dishes they requested.

**_APIs are everywhere we look -_**
* When you check the weather using an app on your phone, it's probably using a Yahoo! or AccuWeather API to do so. 

* When businesses display an interactive map with a red pin on their website's "Find Us" page, they're likely using a Google API.

* When a website allows you to sign in with your Microsoft / Office 365 account, they're likely leveraging Microsoft authentication APIs.

In short, APIs are essential to the functionality of most software we use in our day-to-day.

### Diving into Spoonacular

#### Introduction
When developing an app for food, diet, and cooking, the importance of having access to a vast recipe database cannot be understated.

I also had to balance this with the need for a service which would allow me to access their API for free. I also required a reasonable quota limit, since testing and debugging can rack up these calls significantly.

After researching several APIs such as Edamam and the Free Meal API, I felt that **Spoonacular** would be the best option. 

Spoonacular offers several benefits for my use-case, such as:

* A free tier which offers a quota of 150 requests per day;

* Access to over 300,000 recipes;

* Granular information on each recipe; and finally,

* The ability to specify dietary preferences, requirements, restrictions, and intolerances.

### Challenges Faced

#### Constructing the API request
Before I could begin calling the Spoonacular API, I had to learn how to use Python to generate such requests.

Enter, the `requests` module. `requests` simplifies the process of making HTTP requests to an API by eliminating the need to manually add query strings to the URL. 

When querying the spoonacular API as an example, this is how I'd structure a request using `requests`:

```
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # replace with your key
BASE_URL = "https://api.spoonacular.com/recipes/random"


parameters = {
    "number": 1,
    "tags": "vegetarian"
}

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

response = requests.get(BASE_URL, headers=headers, params=parameters)

```

The `requests` module makes light work of concatenating strings to construct the URL for the request, which might look something like this when done manually:

`https://api.spoonacular.com/recipes/random?number=1&tags=vegetarian&intolerances={YOUR_EXCLUSIONS_HERE}
`

#### Parsing the API output
Obtaining an output from the API wasn't really where the challenge was, however. 

The real challenge came when I received my first output, which looked something like the below, which corresponds to a _Mozzarella Sticks_ recipe.

```
sample_data =
{"recipes":[{"vegetarian":true,"vegan":false,"glutenFree":false,"dairyFree":false,"veryHealthy":false,"cheap":false,"veryPopular":false,"sustainable":false,"lowFodmap":false,"weightWatcherSmartPoints":60,"gaps":"no","preparationMinutes":-1,"cookingMinutes":-1,"aggregateLikes":11,"healthScore":35,"creditsText":"Foodista.com – The Cooking Encyclopedia Everyone Can Edit","license":"CC BY 3.0","sourceName":"Foodista","pricePerServing":1035.09,"extendedIngredients":[{"id":1001,"aisle":"Milk, Eggs, Other Dairy","image":"butter-sliced.jpg","consistency":"SOLID","name":"butter","nameClean":"butter","original":"1 tablespoon Butter or marg., melted","originalName":"Butter or marg., melted","amount":1.0,"unit":"tablespoon","meta":["melted"],"measures":{"us":{"amount":1.0,"unitShort":"Tbsp","unitLong":"Tbsp"},"metric":{"amount":1.0,"unitShort":"Tbsp","unitLong":"Tbsp"}}},{"id":18079,"aisle":"Pasta and Rice","image":"breadcrumbs.jpg","consistency":"SOLID","name":"bread crumbs","nameClean":"breadcrumbs","original":"1 cup Dry bread crumbs","originalName":"Dry bread crumbs","amount":1.0,"unit":"cup","meta":["dry"],"measures":{"us":{"amount":1.0,"unitShort":"cup","unitLong":"cup"},"metric":{"amount":108.0,"unitShort":"ml","unitLong":"milliliters"}}},{"id":1123,"aisle":"Milk, Eggs, Other Dairy","image":"egg.png","consistency":"SOLID","name":"eggs","nameClean":"egg","original":"2 eggs","originalName":"eggs","amount":2.0,"unit":"","meta":[],"measures":{"us":{"amount":2.0,"unitShort":"","unitLong":""},"metric":{"amount":2.0,"unitShort":"","unitLong":""}}},{"id":20081,"aisle":"Baking","image":"flour.png","consistency":"SOLID","name":"flour","nameClean":"wheat flour","original":"3 tablespoons All-purpose flour","originalName":"All-purpose flour","amount":3.0,"unit":"tablespoons","meta":["all-purpose"],"measures":{"us":{"amount":3.0,"unitShort":"Tbsps","unitLong":"Tbsps"},"metric":{"amount":3.0,"unitShort":"Tbsps","unitLong":"Tbsps"}}},{"id":1022020,"aisle":"Spices and Seasonings","image":"garlic-powder.png","consistency":"SOLID","name":"garlic powder","nameClean":"garlic powder","original":"1/2 teaspoon Garlic powder","originalName":"Garlic powder","amount":0.5,"unit":"teaspoon","meta":[],"measures":{"us":{"amount":0.5,"unitShort":"tsps","unitLong":"teaspoons"},"metric":{"amount":0.5,"unitShort":"tsps","unitLong":"teaspoons"}}},{"id":1022027,"aisle":"Spices and Seasonings","image":"dried-herbs.png","consistency":"SOLID","name":"seasoning","nameClean":"italian seasoning","original":"2 1/2 teaspoons Italian seasoning","originalName":"Italian seasoning","amount":2.5,"unit":"teaspoons","meta":["italian"],"measures":{"us":{"amount":2.5,"unitShort":"tsps","unitLong":"teaspoons"},"metric":{"amount":2.5,"unitShort":"tsps","unitLong":"teaspoons"}}},{"id":1002030,"aisle":"Spices and Seasonings","image":"pepper.jpg","consistency":"SOLID","name":"pepper","nameClean":"black pepper","original":"1/8 teaspoon Pepper","originalName":"Pepper","amount":0.125,"unit":"teaspoon","meta":[],"measures":{"us":{"amount":0.125,"unitShort":"tsps","unitLong":"teaspoons"},"metric":{"amount":0.125,"unitShort":"tsps","unitLong":"teaspoons"}}},{"id":10011549,"aisle":"Pasta and Rice","image":"tomato-sauce-or-pasta-sauce.jpg","consistency":"SOLID","name":"spaghetti sauce","nameClean":"pasta sauce","original":"1 cup Marinara or spaghetti sauce, heated","originalName":"Marinara or spaghetti sauce, heated","amount":1.0,"unit":"cup","meta":[],"measures":{"us":{"amount":1.0,"unitShort":"cup","unitLong":"cup"},"metric":{"amount":245.0,"unitShort":"ml","unitLong":"milliliters"}}},{"id":98970,"aisle":"Cheese","image":"string-cheese.png","consistency":"SOLID","name":"string cheese","nameClean":"string cheese","original":"12 string cheese","originalName":"string cheese","amount":12.0,"unit":"","meta":[],"measures":{"us":{"amount":12.0,"unitShort":"","unitLong":""},"metric":{"amount":12.0,"unitShort":"","unitLong":""}}},{"id":14412,"aisle":"Beverages","image":"water.png","consistency":"LIQUID","name":"water","nameClean":"water","original":"1 tablespoon Water","originalName":"Water","amount":1.0,"unit":"tablespoon","meta":[],"measures":{"us":{"amount":1.0,"unitShort":"Tbsp","unitLong":"Tbsp"},"metric":{"amount":1.0,"unitShort":"Tbsp","unitLong":"Tbsp"}}}],"id":652513,"title":"Mozzarella Sticks","readyInMinutes":45,"servings":1,"sourceUrl":"http://www.foodista.com/recipe/LVT5MJLZ/mozzarella-sticks","image":"https://spoonacular.com/recipeImages/652513-556x370.jpg","imageType":"jpg","summary":"Mozzarella Sticks is a <b>lacto ovo vegetarian</b> hor d'oeuvre. One serving contains <b>1773 calories</b>, <b>104g of protein</b>, and <b>99g of fat</b>. For <b>$10.35 per serving</b>, this recipe <b>covers 45%</b> of your daily requirements of vitamins and minerals. This recipe serves 1. A mixture of string cheese, bread crumbs, pepper, and a handful of other ingredients are all it takes to make this recipe so yummy. From preparation to the plate, this recipe takes around <b>45 minutes</b>. 11 person were glad they tried this recipe. It is brought to you by Foodista. Overall, this recipe earns an <b>outstanding spoonacular score of 83%</b>. <a href=\"https://spoonacular.com/recipes/mozzarella-sticks-1520603\">Mozzarella Sticks</a>, <a href=\"https://spoonacular.com/recipes/mozzarella-sticks-1772345\">Mozzarella Sticks</a>, and <a href=\"https://spoonacular.com/recipes/mozzarella-sticks-675804\">Mozzarella Sticks</a> are very similar to this recipe.","cuisines":[],"dishTypes":["fingerfood","antipasti","starter","snack","appetizer","antipasto","hor d'oeuvre"],"diets":["lacto ovo vegetarian"],"occasions":[],"instructions":"<ol><li>Taste of Home. It won a prize in their cheese contest. Mary Merchant of</li><li>In a small bowl, beat eggs and water. In a plastic bag, combine bread crumbs, Italian seasoning, garlic powder and pepper. Coat cheese sticks in flour, then dip in egg mixture and bread crumb mixture. Repeat egg and bread crumb coatings. Cover and chill for at least 4 hours or overnight.</li><li>Place on an ungreased baking sheet; drizzle with butter. Bake, uncovered, at 400 for 6 to 8 minutes or until heated through. Allow to stand for 3 to 5 minutes before serving. Use marinara or spaghetti sauce for dipping.</li><li>Yield: 4 to 6 servings.</li><li>Note: Regular mozzarella cheese, cut into 4 inch by 1/2 inch sticks can be substituted for the string cheese.</li></ol>","analyzedInstructions":[{"name":"","steps":[{"number":1,"step":"Taste of Home. It won a prize in their cheese contest. Mary Merchant ofIn a small bowl, beat eggs and water. In a plastic bag, combine bread crumbs, Italian seasoning, garlic powder and pepper. Coat cheese sticks in flour, then dip in egg mixture and bread crumb mixture. Repeat egg and bread crumb coatings. Cover and chill for at least 4 hours or overnight.","ingredients":[{"id":1022027,"name":"italian seasoning","localizedName":"italian seasoning","image":"dried-herbs.png"},{"id":98970,"name":"string cheese","localizedName":"string cheese","image":"string-cheese.png"},{"id":1022020,"name":"garlic powder","localizedName":"garlic powder","image":"garlic-powder.png"},{"id":18079,"name":"breadcrumbs","localizedName":"breadcrumbs","image":"breadcrumbs.jpg"},{"id":1041009,"name":"cheese","localizedName":"cheese","image":"cheddar-cheese.png"},{"id":1002030,"name":"pepper","localizedName":"pepper","image":"pepper.jpg"},{"id":18064,"name":"bread","localizedName":"bread","image":"white-bread.jpg"},{"id":20081,"name":"all purpose flour","localizedName":"all purpose flour","image":"flour.png"},{"id":14412,"name":"water","localizedName":"water","image":"water.png"},{"id":1123,"name":"egg","localizedName":"egg","image":"egg.png"},{"id":0,"name":"dip","localizedName":"dip","image":""}],"equipment":[{"id":221671,"name":"ziploc bags","localizedName":"ziploc bags","image":"plastic-bag.jpg"},{"id":404783,"name":"bowl","localizedName":"bowl","image":"bowl.jpg"}],"length":{"number":240,"unit":"minutes"}},{"number":2,"step":"Place on an ungreased baking sheet; drizzle with butter.","ingredients":[{"id":1001,"name":"butter","localizedName":"butter","image":"butter-sliced.jpg"}],"equipment":[{"id":404727,"name":"baking sheet","localizedName":"baking sheet","image":"baking-sheet.jpg"}]},{"number":3,"step":"Bake, uncovered, at 400 for 6 to 8 minutes or until heated through. Allow to stand for 3 to 5 minutes before serving. Use marinara or spaghetti sauce for dipping.","ingredients":[{"id":10011549,"name":"pasta sauce","localizedName":"pasta sauce","image":"tomato-sauce-or-pasta-sauce.jpg"}],"equipment":[{"id":404784,"name":"oven","localizedName":"oven","image":"oven.jpg"}],"length":{"number":9,"unit":"minutes"}}]}],"originalId":null,"spoonacularSourceUrl":"https://spoonacular.com/mozzarella-sticks-652513"}]}
```

Clearly, there's a ton of information about this recipe - nearly 11,000 characters to be more specific. There was a lot more information than I was bargaining for, including various IDs for ingredients, hyperlinks to similar recipes, references to images
(in this case, something like ![Mozzarella Sticks Picture](https://spoonacular.com/recipeImages/652513-556x370.jpg)), and short and long versions of units (e.g. ml or millilitres).

I initially wanted to turn this data dump into a Python dictionary so I could try and access its values using dictionary `keys` (e.g. `data['ingredients'][1]` to access the first ingredient.

After hitting a wall trying to directly interpret the output as a Python dictionary, my next step was to try and convert the output to a Python dictionary using `json.loads()`.

This was the output I got when attempting to convert the JSON to a dictionary:

```
Traceback (most recent call last):
  File "c:\Users\ssrir\Codecademy Projects\Portfolio\Mealplanner\test2.py", line 10, in <module>
    sample_load = json.loads(sample_data_string)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ssrir\AppData\Local\Programs\Python\Python311\Lib\json\__init__.py", line 346, in loads  
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ssrir\AppData\Local\Programs\Python\Python311\Lib\json\decoder.py", line 337, in decode  
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\ssrir\AppData\Local\Programs\Python\Python311\Lib\json\decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 2 column 5166 (char 5166)
```

After multiple decode errors of various sorts, I decided to take a step back and see if I could modify my API request or create a new request as such that I can directly request the specific information I needed.

I therefore modified my code to make **two** separate requests - one for a _random recipe ID_, and another for _detailed recipe information_:
```
API_KEY = str(input("\nEnter your Spoonacular API key below.\n(Visit www.spoonacular.com/food-api to obtain a key.)\n>>> "))
BASE_URL = "https://api.spoonacular.com/recipes/random"
DETAILED_RECIPE_URL = "https://api.spoonacular.com/recipes/{id}/information"

parameters = {
    "number": 1,
    "tags": f"",
    "intolerances": exclusions_param  
}

if vegan:
    parameters["tags"] += "vegan"
elif vegetarian:
    parameters["tags"] += "vegetarian"

headers = {
    "Content-Type": "application/json",  # Default content type per Spoonacular API documentation
    "x-api-key": API_KEY  # Fed into API call as a header
}

response = requests.get(BASE_URL, headers=headers, params=parameters)

if response.status_code != 200:
    print(f"Error fetching random recipe: Code - {response.status_code}")  # Verbose
    exit()

recipe_id = response.json()['recipes'][0]['id']

response = requests.get(DETAILED_RECIPE_URL.format(id=recipe_id), params={"apiKey": API_KEY})

if response.status_code != 200:
    print(f"Error fetching detailed recipe: Code - {response.status_code}")
    exit()
```

This revised method would now expend 2 API credits as opposed to just one, but it also meant a much cleaner output which would be easier to parse.


#### Cleaning HTML tags
My next challenge lay with the instructions - some outputs had html tags to indicate new lines, such as:

```
<li>example</li><li>example2</li>
```

Since some API outputs contained these tags and some didn't, I needed to build logic to handle this separately. 

This was when I revisited object-oriented programming to create a subclass of the `HTMLParser` class from the `html.parser` module.

```
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.instructions = []
        self.recording = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li':  # Condition to check for tags starting with <li>.
            self.recording = True
            self.data = ''

    def handle_endtag(self, tag):
        if tag == 'li' and self.recording:
            self.recording = False
            self.instructions.append(self.data.strip())

    def handle_data(self, data):
        if self.recording:
            self.data += data
```

I then created a function that creates an object out of the `MyHTMLParser` class, and uses methods inherited from `HTMLParser` to clean instructions with HTML tags, and/or enumerate the instructions on new lines based on when each sentence ends.

```
def clean_html_instructions(html_content):

    def add_period(instruction):
        instruction = instruction.strip()
        if not instruction.endswith('.'):
            instruction += '.'
        return instruction
    
    if "<li>" in html_content:
        parser = MyHTMLParser()
        parser.feed(html_content)
        cleaned_instructions_list = [add_period(step) for step in parser.instructions]
        cleaned_instructions = '\n'.join(f"{index}. {step}" for index, step in enumerate(cleaned_instructions_list, 1))
    
    else:
        instructions_list = [add_period(instr) for instr in html_content.split('.') if instr.strip()]
        cleaned_instructions = '\n'.join(f"{index}. {step}" for index, step in enumerate(instructions_list, 1))
    
    return cleaned_instructions

```

### Version Control with Git
Git offers several benefits, especially for developers working in large teams. From my basic understanding, Git:
* Tracks changes for **easy understanding** and **potential rollbacks** if needed

* Allows for **branching** (creation of parallel codebases in the same repository), **forking** (creating a parallel repository for isolated development), and **merging** (integration of code back into the main codebase).

* Fosters **accountability** by assigning 'blame' to contributors as such that one can see _who_ did _what_.

Although I'd learned about git on a very cursory level through the use of [Codecademy](https://www.codecademy.com), I found the learning curve much steeper when committing my program to a Git repository.

#### The .gitignore file
When I first initialised an empty git repository in the directory where my Python file and virtul environment were located, I found that .gitignore was preventing all my files from being committed.

Upon closer inspection of the .gitignore file, I found that there was a single asterisk in the file:
```
* 
```
This essentially meant my git was going to ignore _all_ files in the directory.

I decided to leave the file empty and commit everything in the directory. From creating a virtual environment, this meant that those would also be committed to the git repository (all 800+ files).

As I continue to learn about Git, I will focus my efforts on ensuring that the .gitignore file is configured correctly going forward.

#### Pushing my local git repository to Github
To push my local commits to my remote Github repository, I needed to install `git bash` and the `github.cli` given that my machine runs Windows.

I then used `gh auth login` to connect my local computer to my Github account, so I could begin pushing my local commits to my newly minted Github repository.

I found that the master repository had all the relevant files, but the main repository was still empty. 

I therefore did a merge from master to main with the `--allow-unrelated-histories` tag and now, my main repository has all the needed files.

### Key Takeaways from ReciPy
#### Learning Curve
Building ReciPy was a huge learning curve for me. 

I'd learned about all the individual components of Python programming, and had to marry everything together in this program to make it work. It was both exciting, and challenging.

Through this journey, I also learned how to:

* Handle user inputs and use conditional statements to include/exclude further inputs;

* Inherit classes and modify these new subclasses to fulfil specific and complicated objectives (such as parsing HTML code to clean outputs for further presentation to users); and

* Read through API documentation to make best use of the API's parameters (rather than try to parse through giant output strings in my own program).

#### Personal Growth

There were countless instances of getting headaches while debugging, and being on the verge of giving up (especially when tackling the API output problem in the initial stage).

One thing that really helped me in the debugging process was adding print statements in various steps to see what the output might be, to identify the source of bugs.

I learned how to persevere through problems and find new ways of solving them, rather than trying to make one specific solution work.

The satisfaction of getting this program to work, more than compensated for the struggles I bore while putting ReciPy together.

### What's Next?

#### Improving the program
* I want to find a way of integrating _macro-nutrient information_ into these recipes, so users have a clearer idea of carbohydrate, fat, and protein intake.
    * For the moment, I'm still trying to figure out how to obtain this information from Spoonacular's API output - but some recipes have this information, while others don't.

* It would be helpful for users to save these recipes for future reference, since in this program's existing form, recipes are nuked once the program is closed.
    * A small workaround would be to highlight the terminal output and save it to a text file.
    * A potential long-term solution would be to integrate `with open()` and `sys.stdout` to save all printed outputs to a text file.

#### Learning new technologies
As I master programming through Python, I look forward to transferring these skills to C++ and Java. 

These languages are less syntactically friendly in comparison to Python, but I'm hoping that my basic understanding of fundamental concepts will make this transition more seamless.

### Conclusion
Overall, this project has had the biggest impact on my learning - while it's easy to follow Codecademy's step-by-step guidance, it's a much taller order when you're essentially on your own.

That said, I'd love to give a shout-out to:
* **Codecademy**, for adding much-needed structure to my learning journey;
* **ChatGPT-4**, for aiding my debugging and saving me countless hours in the process; and of course,
* **Wifey**, for the countless hugs she gave me whilst I was debugging and optimising the program.

### Appendix
#### Resources Used:
##### Software Packages
* [**PyCharm IDE - Community Edition**](https://www.jetbrains.com/pycharm/), my main IDE for writing ReciPy.
    * Helped me create a virtual environment for my Python code

* [**Visual Studio Code**](https://code.visualstudio.com/), my main IDE for writing ReciPy.
    * Several plugins and extensions, including Python and Git
    * Highly customisable and resource-efficient compared to most IDEs

* [**Python 3.11 (Windows Store)**](https://apps.microsoft.com/detail/python-3-11/9NRWMJP3717K?hl=en-US)
    * Required for Visual Studio Code's Python extension to work.

* [**GitHub Desktop** (optional)](https://desktop.github.com/)
    * Brings the GitHub experience to a standalone program, but can be fulfilled through the browser.

* [**GitHub CLI**](https://cli.github.com/) 
    * Required for integration with GitHub to push local repositories to the web. 

* [**Git Bash** (only for Windows)](https://gitforwindows.org/)
    * Required to perform Git operations locally on Windows machines, though _VS Code could replace this functionality entirely_.
