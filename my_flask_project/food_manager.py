foods = []

def add_food(food):
    foods.append(food)

def get_foods():
    return foods

def update_food(index, updated_food):
    foods[index] = updated_food

def delete_food(index):
    return foods.pop(index)
