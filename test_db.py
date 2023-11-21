import pprint
from database import Database

DATABASE_PATH = "annotation.db"
db = Database(DATABASE_PATH)

# print(db.get_annotation_count())

print(db.get_number_of_issues_annotated_by_user('arevaloh'))
