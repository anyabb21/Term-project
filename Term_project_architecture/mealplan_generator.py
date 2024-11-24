




import requests
import random

API_KEY = "9cfb185dc55340b5b0e980bc2d2b97ba"
BASE_URL = "https://api.spoonacular.com/mealplanner/generate?timeFrame=day"

def get_meal_plans(dietary_preference, target_calories= 2000, time_frame = "day"):
    params = {
        "apiKey": API_KEY,
        "timeFrame": time_frame,
        "targetCalories": target_calories,
        "diet":dietary_preference


    }
    responses = requests.get(BASE_URL, params=params)

    if responses.status_code == 200:
        data = responses.json()
        meals = [meal['title'] for meal in data['meals']]
        nutrients = data ['nutrients']
        return meals, nutrients
    else:
        print(f"An error occured: {responses.status_code} - {responses.text}")
        return None, None
    
def main():
    print("Welcome to your meal plan! Let's help you eat healthier!")
    preference = input ("Enter your dietary preference:").lower() 
    target_calories = int(input("Enter your daily calorie target:"))
    meal_plan, nutrients = get_meal_plans(preference, target_calories)

    if meal_plan:
        print(f"\nHere's your {preference} meal plan for the day:")
        meal_types = ["Breakfast", "Lunch", "Dinner"]
        for meal_type, meal in zip(meal_types, meal_plan):
            print(f"{meal_type}: {meal}")

        print("\nNutritional Information:")
        print(f"Calories: {nutrients['calories']: .2f}")
        print(f"Carbohydrates: {nutrients['carbohydrates']:.2f}g")
        print(f"Fat: {nutrients['fat']:.2f}g")
        print(f"Protein:{nutrients['protein']:.2f}g")
    else:
        print("sorry, we could not fetch a meal plan")

if __name__ == "__main__":
        main()

