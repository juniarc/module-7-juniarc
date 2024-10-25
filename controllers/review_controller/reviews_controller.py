from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from connectors.db import Session
from models.review.reviews import ReviewModel

reviewBp = Blueprint('reviewBp', __name__)

session = Session()

@reviewBp.route('/home/review', methods=['POST'])
@login_required
def add_review():
    if current_user.role != 'admin':
        return "Access Denied", 403
    
    description = request.form.get('description')
    rating = request.form.get('rating')

    with Session() as session:
        try:
            new_review = ReviewModel(description=description, user_email=current_user.email, rating=rating)

            session.add(new_review)
            session.commit()
        except Exception as e:
            print(e)

    return redirect(url_for('home'))

@reviewBp.route('/home/review/update/<int:review_id>', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
    with Session() as session:
        review = session.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()

        if request.method == 'POST':
            review.description = request.form.get('description')
            review.rating = request.form.get('rating')
            session.commit()
            return redirect(url_for('home'))
    
    return render_template('update_review.html', review=review)

@reviewBp.route('/home/review/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    with Session() as session:
        review = session.query(ReviewModel).filter(ReviewModel.review_id == review_id).first()
        if review:
            session.delete(review)
            session.commit()
    return redirect(url_for('home'))