from db import User,Task,Base,engine


print("Creating database......")


Base.metadata.create_all(bind=engine)