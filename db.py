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
