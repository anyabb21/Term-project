from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "9cfb185dc55340b5b0e980bc2d2b97ba"
BASE_URL = "https://api.spoonacular.com/mealplanner/generate"

def get_meal_plans(dietary_preference, target_calories=2000, time_frame="day"):
    params = {
        "apiKey": API_KEY,
        "timeFrame": time_frame,
        "targetCalories": target_calories,
        "diet": dietary_preference
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        meals = [meal['title'] for meal in data['meals']]
        nutrients = data['nutrients']
        return meals, nutrients
    else:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        preference = request.form['preference'].lower()
        target_calories = int(request.form['target_calories'])
        meal_plan, nutrients = get_meal_plans(preference, target_calories)

        if meal_plan:
            return render_template('result.html', preference=preference, meal_plan=meal_plan, nutrients=nutrients)
        else:
            return render_template('error.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

    