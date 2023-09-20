from flask import Flask, Blueprint, jsonify, session, request, Response
from flask_migrate import Migrate
from flask_login import login_required
from app.models.review import Review, db

review_routes = Blueprint('review', __name__)

# get all reviews of the current user, Require Auth: true
@review_routes.route('/current')
@login_required
def reviewData():
    """
    Query for all reviews by the current user and returns them in a list of Review dictionaries
    ordered by updated_at
    """
    reviews = Review.query.filter(Review.user_id == session['_user_id']).order_by(Review.updated_at)
    # print(type(int(session['_user_id'])), 'TEST')
    return {'Reviews': [review.to_dict_im() for review in reviews]}


@review_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    """
    Delete Review by Review.id and loggedIn User must have written the review
    Query for all reviews by the current user and returns them in a list of Review dictionaries
    ordered by updated_at
    """
    rev = Review.query.get(id)
    if not rev or (int(rev.user_id) != int(session['_user_id'])):
        # print(type(int(rev.user_id)), type(int(session['_user_id'])), 'checking type-------------///')
        # print((int(rev.user_id) != int(session['_user_id'])), 'revTEST-------')
        return {'Error': 'Review not found or user not authorized'}
    else:
        db.session.delete(rev)
        db.session.commit()
        return rev.to_dict_del()



    reviews = Review.query.filter(Review.user_id == session['_user_id']).order_by(Review.updated_at)
    return rev.to_dict_im()


# Edit a review
@review_routes.route('/<int:id>', methods=['PUT'])
@login_required
def updateReview(id):
    rev = Review.query.get(id)

    # int(session['_user_id'] and session.get('_user_id') both work
    # check if user wrote the review
    if (rev.user_id) != int(session['_user_id']):
        return {'Error': 'User is not authorized'}

    rev.rating = request.json['rating']
    rev.description = request.json['description']

    # rating b/w 1 and 5
    if rev.rating < 1 or rev.rating > 5:
        return {'Error': 'Review rating must be between 1 and 5'}

    db.session.commit()

    updated = Review.query.filter(Review.id == id)
    return {'Review': [update.to_dict_im() for update in updated]}


# get a review on review id
@review_routes.route('<int:id>')
def getReviewById (id):

    rev = Review.query.get(id)

    # print((Response), dir(Response.status), 'fasdfas----' ,dir(Response.status_code), 'response---------')

    if not rev:
        # Response.status
        return ({ 'Error': 'Review does not exist'}), 404

    return rev.to_dict_im()
