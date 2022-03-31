from datetime import datetime
from bson.objectid import ObjectId

from response import Response


class Post:
    def __init__(self, config):
        self.title = None
        self.content = None
        self.collection = config.POSTS_COLLECTION
        self.response = Response()

    def get_all(self):
        try:
            # relation with users
            posts = self.collection.aggregate(
                [
                    {
                        "$lookup":
                            {
                                "from": "users",
                                "localField": "user_id",
                                "foreignField": "_id",
                                "as": "owner"
                            }
                    }
                ]
            )
            self.response.data = posts
        except:
            self.response.add_error('error')

        return self.response

    def add(self, title, description, user_id, privacy='public'):
        try:
            record = {
                'user_id': user_id,
                'privacy': privacy,
                'title': title,
                'description': description,
                'created_at': datetime.today()
            }
            self.collection.insert_one(record)
            self.response.data = record
        except:
            self.response.add_error('error')

        return self.response

    def delete(self, id):
        try:
            self.collection.delete_one({'_id': ObjectId(id)})
            return True
        except:
            return False
