from pyArango.connection import Connection
from inarious.config import settings


conn = Connection(
    arangoURL=settings.ARANGO_URL,
    username=settings.ARANGO_USERNAME,
    password=settings.ARANGO_ROOT_PASSWORD,
)


# create the database and collection if they do not exist
def initialize_db_collection():
    global conn
    if not conn.hasDatabase(name=settings.ARANGO_DATABASE):
        db = conn.createDatabase(name=settings.ARANGO_DATABASE)
    else:
        db = conn[settings.ARANGO_DATABASE]

    if not db.hasCollection("Users"):
        db.createCollection(name="Users")

