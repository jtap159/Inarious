from pyArango.connection import Connection

conn = Connection(username="root", password="mypass")


# create the database and collection if they do not exist
def initialize_db_collection():
    global conn
    if not conn.hasDatabase(name="inarious"):
        db = conn.createDatabase(name="inarious")
    else:
        db = conn["inarious"]

    if not db.hasCollection("Users"):
        db.createCollection(name="Users")

