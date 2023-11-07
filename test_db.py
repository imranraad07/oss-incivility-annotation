from database import Database

DATABASE_PATH = "annotation.db"
db = Database(DATABASE_PATH)

# db.create_user('ramtin_123', 352750519, 869840472, 352750519)
# db.update_current_issue('ramtin_123', 352750519)
user = db.get_all_comment_annotations()
# user = db.get_all_issue_annotations()

print(user)
