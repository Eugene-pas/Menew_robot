import numpy
import pymongo
import secret

client = pymongo.MongoClient(secret.DB_URL)
db = client[secret.DB_NAME]
users = db["users"]


def get_user_ingredients(user_id: int):
    return users.find_one({'userTelegramId': user_id})["ingredients"]


def db_user_exist(user_id):
    if users.find_one({'userTelegramId': user_id}) != None:
        return True
    else:
        return False


def create_user(user_id, user_name):
    if users.find_one({'userTelegramId': user_id}) == None:
        users.insert_one(
            {
                'userName': user_name,
                'userTelegramId': user_id,
                'recipe': [],
                'ingredients': []
            }
        )


def add_ingredients(user_id: int, ingredients: []):
    if users.find_one({'userTelegramId': user_id}) != None:
        user = {'userTelegramId': user_id}
        old_user_ingredients = users.find_one({'userTelegramId': user_id})["ingredients"]

        if len(old_user_ingredients) != 0 and len(ingredients) != 0:
            new_user_ingredients = numpy.unique(
                numpy.concatenate((old_user_ingredients, ingredients))
            ).tolist()
            users.update_one(user, {"$set": {"ingredients": list(map(lambda x: x.lower(), new_user_ingredients))}})
        elif len(old_user_ingredients) == 0 and len(ingredients) != 0:
            users.update_one(user, {"$set": {"ingredients": list(map(lambda x: x.lower(), ingredients))}})
