import os

from dotenv import load_dotenv


load_dotenv()

Spoonacular_API_Key = os.getenv("Spoonacular_API_Key") 



from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

API_KEY = Spoonacular_API_Key
BASE_URL = "https://api.spoonacular.com/mealplanner/generate"
RECIPE_URL = "https://api.spoonacular.com/recipes/{id}/information"

def get_meal_plans(dietary_preference, target_calories=2000, time_frame="day"):
    params = {
        "apiKey": API_KEY,
        "timeFrame": time_frame,
        "targetCalories": target_calories,
        "diet": dietary_preference
    }
    response = requests.get(BASE_URL, params=params)
    print (response)

    if response.status_code == 200:
        data = response.json()
        meals = []
        for meal in data['meals']:
            meal_info = get_recipe_info(meal['id'])
            meals.append(meal_info)
        nutrients = data['nutrients']
        return meals, nutrients
    else:
        return None, None



def get_recipe_info(recipe_id):
    params = {"apiKey": API_KEY}
    response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
    if response.status_code == 200:
        data = response.json()
        
        def clean_instruction(instruction):
            import re
            # Remove HTML tags and extra whitespace
            cleaned = re.sub(r'<[^>]+>', '', instruction).strip()
            return cleaned

        # Join instructions into a single paragraph
        instructions = ' '.join(
            clean_instruction(step) 
            for step in data['instructions'].split('\n') 
            if clean_instruction(step).strip()
        )

        return {
            'title': data['title'],
            'instructions': instructions,
            'ingredients': [ingredient['original'] for ingredient in data['extendedIngredients']]
        }
    return None

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/meal_plan', methods=['GET', 'POST'])
def meal_plan():
    if request.method == 'POST':
        preference = request.form['preference'].lower()
        target_calories = int(request.form['target_calories'])
        meal_plan, nutrients = get_meal_plans(preference, target_calories)
        print (meal_plan)

        if meal_plan:
            return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
        else:
            return render_template('error.html')
    return render_template('index.html')

@app.route('/random_meal')
def random_meal():
    meal_plan, _ = get_meal_plans("", target_calories=random.randint(1500, 2500))
    if meal_plan:
        return jsonify(random.choice(meal_plan))
    return jsonify({"error": "Unable to fetch random meal"}), 400

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         preference = request.form['preference'].lower()
#         target_calories = int(request.form['target_calories'])
#         meal_plan, nutrients = get_meal_plans(preference, target_calories)

#         if meal_plan:
#             return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
#         else:
#             return render_template('error.html')
#     return render_template('index.html')

# @app.route('/')
# def welcome():
#     return render_template('welcome.html')

# @app.route('/meal_plan', methods=['GET', 'POST'])
# def meal_plan():
#     if request.method == 'POST':
#         preference = request.form['preference'].lower()
#         target_calories = int(request.form['target_calories'])
#         meal_plan, nutrients = get_meal_plans(preference, target_calories)

#         if meal_plan:
#             return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
#         else:
#             return render_template('error.html')
#     return render_template('index.html')

# @app.route('/random_meal')
# def random_meal():
#     meal_plan, _ = get_meal_plans("", target_calories=random.randint(1500, 2500))
#     if meal_plan:
#         return jsonify(random.choice(meal_plan))
#     return jsonify({"error": "Unable to fetch random meal"}), 400

# @app.route('/')
# def welcome():
#     return render_template('welcome.html')

# @app.route('/meal_plan', methods=['GET', 'POST'])
# def meal_plan():
#     if request.method == 'POST':
#         preference = request.form['preference'].lower()
#         target_calories = int(request.form['target_calories'])
#         meal_plan, nutrients = get_meal_plans(preference, target_calories)

#         if meal_plan:
#             return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
#         else:
#             return render_template('error.html')
#     return render_template('index.html')



# @app.route('/random_meal')
# def random_meal():
#     meal_plan, _ = get_meal_plans("", target_calories=random.randint(1500, 2500))
#     if meal_plan:
#         return jsonify(random.choice(meal_plan))
#     return jsonify({"error": "Unable to fetch random meal"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)









# from flask import Flask, render_template, request, jsonify
# import requests
# import random

# app = Flask(__name__)

# API_KEY = "9cfb185dc55340b5b0e980bc2d2b97ba"
# BASE_URL = "https://api.spoonacular.com/mealplanner/generate"
# RECIPE_URL = "https://api.spoonacular.com/recipes/{id}/information"

# def get_meal_plans(dietary_preference, target_calories=2000, time_frame="day"):
#     params = {
#         "apiKey": API_KEY,
#         "timeFrame": time_frame,
#         "targetCalories": target_calories,
#         "diet": dietary_preference
#     }
#     response = requests.get(BASE_URL, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         meals = []
#         for meal in data['meals']:
#             meal_info = get_recipe_info(meal['id'])
#             meals.append(meal_info)
#         nutrients = data['nutrients']
#         return meals, nutrients
#     else:
#         return None, None

# def get_recipe_info(recipe_id):
#     params = {"apiKey": API_KEY}
#     response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
#     if response.status_code == 200:
#         data = response.json()
        
#         def clean_instruction(instruction):
#             import re
#             cleaned = re.sub(r'<[^>]+>', '', instruction).strip()
#             return cleaned

#         instructions = ' '.join(
#             clean_instruction(step) 
#             for step in data['instructions'].split('\n') 
#             if clean_instruction(step).strip()
#         )

#         return {
#             'title': data['title'],
#             'instructions': instructions,
#             'ingredients': [ingredient['original'] for ingredient in data['extendedIngredients']]
#         }
#     return None

# @app.route('/')
# def welcome():
#     return render_template('welcome.html')

# @app.route('/meal_plan', methods=['GET', 'POST'])
# def meal_plan():
#     if request.method == 'POST':
#         preference = request.form['preference'].lower()
#         target_calories = int(request.form['target_calories'])
#         meal_plan, nutrients = get_meal_plans(preference, target_calories)

#         if meal_plan:
#             return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
#         else:
#             return render_template('error.html')
#     return render_template('index.html')

# @app.route('/random_meal')
# def random_meal():
#     meal_plan, _ = get_meal_plans("", target_calories=random.randint(1500, 2500))
#     if meal_plan:
#         return jsonify(random.choice(meal_plan))
#     return jsonify({"error": "Unable to fetch random meal"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask, render_template, request
# import requests

# app = Flask(__name__)

# API_KEY = "9cfb185dc55340b5b0e980bc2d2b97ba"
# BASE_URL = "https://api.spoonacular.com/mealplanner/generate"

# def get_meal_plans(dietary_preference, target_calories=2000, time_frame="day"):
#     params = {
#         "apiKey": API_KEY,
#         "timeFrame": time_frame,
#         "targetCalories": target_calories,
#         "diet": dietary_preference
#     }
#     response = requests.get(BASE_URL, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         meals = [meal['title'] for meal in data['meals']]
#         nutrients = data['nutrients']
#         return meals, nutrients
#     else:
#         return None, None

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         preference = request.form['preference'].lower()
#         target_calories = int(request.form['target_calories'])
#         meal_plan, nutrients = get_meal_plans(preference, target_calories)

#         if meal_plan:
#             return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
#         else:
#             return render_template('error.html')
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# def get_recipe_info(recipe_id):
#     params = {"apiKey": API_KEY}
#     response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             'title': data['title'],
#             'instructions': data['instructions'].split('\n'),  # Split instructions into a list
#             'ingredients': [ingredient['original'] for ingredient in data['extendedIngredients']]
#         }
#     return None
# def get_recipe_info(recipe_id):
#     params = {"apiKey": API_KEY}
#     response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
#     if response.status_code == 200:
#         data = response.json()
        
#         # Clean instructions
#         def clean_instruction(instruction):
#             # Remove HTML tags
#             import re
#             cleaned = re.sub(r'<[^>]+>', '', instruction)
#             # Remove numbers at the start
#             cleaned = re.sub(r'^\d+\.\s*', '', cleaned.strip())
#             return cleaned

#         instructions = [
#             clean_instruction(step) 
#             for step in data['instructions'].split('\n') 
#             if clean_instruction(step)
#         ]

#         return {
#             'title': data['title'],
#             'instructions': instructions,
#             'ingredients': [ingredient['original'] for ingredient in data['extendedIngredients']]
#         }
#     return None

# def get_recipe_info(recipe_id):
#     params = {"apiKey": API_KEY}
#     response = requests.get(RECIPE_URL.format(id=recipe_id), params=params)
#     if response.status_code == 200:
#         data = response.json()
        
#         def clean_instruction(instruction, index):
#             import re
#             # Remove HTML tags, leading numbers, and extra whitespace
#             cleaned = re.sub(r'<[^>]+>', '', instruction).strip()
#             cleaned = re.sub(r'^\d+\.?\s*', '', cleaned)
#             # Prepend index if not already numbered
#             return f"{index}. {cleaned}"

#         instructions = [
#             clean_instruction(step, index+1) 
#             for index, step in enumerate(data['instructions'].split('\n')) 
#             if clean_instruction(step, index+1).strip()
#         ]

#         return {
#             'title': data['title'],
#             'instructions': instructions,
#             'ingredients': [ingredient['original'] for ingredient in data['extendedIngredients']]
#         }
#     return None


# @app.route('/random_meal')
# def random_meal():
#     meal_plan, _ = get_meal_plans("", target_calories=random.randint(1500, 2500))
#     if meal_plan:
#         return jsonify(random.choice(meal_plan))
#     return jsonify({"error": "Unable to fetch random meal"}), 400
