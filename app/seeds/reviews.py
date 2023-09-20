from app.models.review import db, Review , environment, SCHEMA
from sqlalchemy.sql import text


# Adds a review
def seed_reviews():
    review1 = Review(
        description='Great job!  Arrived on time and was very professional and fast.',
        rating=5,
        user_id=1,
        tasker_id=3,
        task_id=2
    )
    review2 = Review(
        description='Tasker was very professional and worked fast.  Left a scuff mark on my wall.',
        rating=4,
        user_id=2,
        tasker_id=1,
        task_id=3
    )
    review3 = Review(
        description='Tasker arrived late but did complete the task as requested.',
        rating=3,
        user_id=2,
        tasker_id=3,
        task_id=4
    )
    review4 = Review(
        description='Did not Arrive on time and was very professional and fast.',
        rating=3,
        user_id=1,
        tasker_id=2,
        task_id=1
    )
    review5 = Review(
        description='Great job! was not professional.',
        rating=4,
        user_id=2,
        tasker_id=1,
        task_id=3
    )
    review6 = Review(
        description='Great job! and fast.',
        rating=5,
        user_id=3,
        tasker_id=5,
        task_id=6
    )
    review7 = Review(
        description='Arrived on time and was very professional and fast.',
        rating=5,
        user_id=9,
        tasker_id=6,
        task_id=11
    )
    review8 = Review(
        description='Great job!.',
        rating=5,
        user_id=3,
        tasker_id=1,
        task_id=3
    )
    review9 = Review(
        description='Arrived late and was not professional and fast.',
        rating=3,
        user_id=13,
        tasker_id=6,
        task_id=12
    )




    db.session.add(review1)
    db.session.add(review2)
    db.session.add(review3)
    db.session.add(review4)
    db.session.add(review5)
    db.session.add(review6)
    db.session.add(review7)
    db.session.add(review8)
    db.session.add(review9)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))

    db.session.commit()
