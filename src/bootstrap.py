import pandas as pd
from pathlib import Path

def main():
    Path("data").mkdir(exist_ok=True, parents=True)

    pantry = pd.DataFrame([
        {"ingredient":"rice","unit":"g","qty_on_hand":3000,"min_par":600},
        {"ingredient":"moong dal","unit":"g","qty_on_hand":1500,"min_par":300},
        {"ingredient":"paneer","unit":"g","qty_on_hand":1200,"min_par":300},
        {"ingredient":"ragi flour","unit":"g","qty_on_hand":1000,"min_par":200},
        {"ingredient":"banana","unit":"pc","qty_on_hand":10,"min_par":4},
        {"ingredient":"spinach","unit":"g","qty_on_hand":800,"min_par":200},
        {"ingredient":"wheat flour","unit":"g","qty_on_hand":2000,"min_par":500},
        {"ingredient":"jowar flour","unit":"g","qty_on_hand":1000,"min_par":300},
        {"ingredient":"bajra flour","unit":"g","qty_on_hand":1000,"min_par":300},
    ])
    pantry.to_excel("data/pantry.xlsx", index=False)

    dishes = pd.DataFrame([
        {
          "name":"Ragi Dosa","meal_type":"breakfast",
          "tags":'["breakfast:main_starch","cuisine:south","jain"]',
          "cook_minutes":20,"difficulty":2,
          "ingredients_json":'[{"item":"ragi flour","qty":120,"unit":"g"},{"item":"water","qty":200,"unit":"ml"}]',
          "steps_json":'["Mix batter","Rest 10m","Cook on tawa 2m/side"]',
          "flavor_text":"Sizzle till the edges lift.","rarity":"rare"
        },
        {
          "name":"Sprout Salad","meal_type":"breakfast",
          "tags":'["breakfast:protein","cuisine:gujarati","kid-friendly","jain"]',
          "cook_minutes":10,"difficulty":1,
          "ingredients_json":'[{"item":"moong dal","qty":100,"unit":"g"}]',
          "steps_json":'["Boil/steam lightly","Toss with lemon, salt"]',
          "flavor_text":"Lemon wakes it up.","rarity":"common"
        },
        {
          "name":"Flax Curd","meal_type":"breakfast",
          "tags":'["breakfast:yogurt","jain"]',
          "cook_minutes":5,"difficulty":1,
          "ingredients_json":'[{"item":"yogurt","qty":200,"unit":"g"},{"item":"flaxseed","qty":10,"unit":"g"}]',
          "steps_json":'["Mix and rest 5m"]',
          "flavor_text":"Creamy and kind.","rarity":"common"
        },
        {
          "name":"Papaya Slices","meal_type":"breakfast",
          "tags":'["breakfast:fruit","jain"]',
          "cook_minutes":2,"difficulty":1,
          "ingredients_json":'[{"item":"papaya","qty":200,"unit":"g"}]',
          "steps_json":'["Slice and serve"]',
          "flavor_text":"Sunshine on a plate.","rarity":"common"
        },
        {
          "name":"Moong Dal Khichdi","meal_type":"dinner",
          "tags":'["dinner:khichdi","cuisine:north","jain","kid-friendly"]',
          "cook_minutes":30,"difficulty":2,
          "ingredients_json":'[{"item":"rice","qty":120,"unit":"g"},{"item":"moong dal","qty":80,"unit":"g"}]',
          "steps_json":'["Rinse rice+dal","Pressure cook 3 whistles","Ghee tadka"]',
          "flavor_text":"Comfort in a bowl.","rarity":"epic"
        },
        {
          "name":"Paneer Tikki","meal_type":"dinner",
          "tags":'["dinner:protein_farsan","cuisine:north","kid-friendly","jain"]',
          "cook_minutes":20,"difficulty":2,
          "ingredients_json":'[{"item":"paneer","qty":200,"unit":"g"}]',
          "steps_json":'["Mash paneer","Pan-sear patties"]',
          "flavor_text":"Golden and proud.","rarity":"rare"
        },
    ])
    dishes.to_excel("data/dishes.xlsx", index=False)

    slots = pd.DataFrame([
      ("breakfast","main_starch"),("breakfast","protein"),("breakfast","yogurt"),("breakfast","fruit"),
      ("lunch","salad"),("lunch","dal"),("lunch","rice"),("lunch","roti"),("lunch","vegetable"),("lunch","farsan"),
      ("dinner","soup"),("dinner","khichdi"),("dinner","bread"),("dinner","vegetable_west"),("dinner","protein_farsan"),("dinner","digestif")
    ], columns=["meal_type","slot_name"])
    slots.to_excel("data/slots.xlsx", index=False)

    variants = pd.DataFrame([
      ("adult","rice","red/brown rice or quinoa, 1/2 cup"),
      ("kids","rice","white rice with ghee, 1 cup"),
      ("adult","bread","millet roti/thepla, 1 pc"),
      ("kids","bread","wheat roti/thepla, 2 pc with ghee"),
      ("adult","protein","lean tofu/paneer portion"),
      ("kids","protein","paneer cubes or daal with ghee"),
    ], columns=["person_group","slot_name","notes"])
    variants.to_excel("data/variants.xlsx", index=False)

    print("✅ Bootstrapped data/*.xlsx")

if __name__ == "__main__":
    main()
