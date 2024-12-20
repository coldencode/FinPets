import pandas as pd
from pet import Pet

# Pet Loader
def load_pet_info():
    df = pd.read_excel("data/pet_goals.xlsx")
    lst = []
    for index, row in df.iterrows():
        pet = row['name']
        goal = int(row['goal'])
        saved = int(row['saved'])
        goal_name = row['goal_name']
        days = int(row['days'])
        # Load the image and scale it to fit the tile size
        saved_pet = Pet(pet, goal, saved, goal_name, days)
        lst.append(saved_pet)

    return lst

if __name__ == '__main__':
    print(load_pet_info())