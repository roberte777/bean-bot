from dataclasses import dataclass
import dataclasses
import json
from dataclass_wizard import JSONWizard
@dataclass
class User(JSONWizard):
    id: str
    name: str
    bean_bucks: int

def load_users() -> list[User]:
    try:
        with open("users.json") as fp:
            # users = json.load(fp)
            users = User.from_json(fp.read())
            return users
    except Exception as e:
        print(e)
        users = {}
        return users

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)
def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, cls=EnhancedJSONEncoder, indent=4)

def add_user(user_id, user_name, users):
    new_user = User(user_id, user_name, 500)
    users.append(new_user)
    save_users(users)
    return users

def get_sorted_users(users: list[User]) -> list[User]:
    sorted_users = sorted(users, key=lambda x: x.bean_bucks, reverse=True)
    return sorted_users


