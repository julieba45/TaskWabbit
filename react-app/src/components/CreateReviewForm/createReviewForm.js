import { useEffect, useState } from "react";
import { createNewReviewByUser, getReviewForLoggedIn } from "../../store/reviews";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom/cjs/react-router-dom";
import "./CreateReviewForm.css"

const CreateReviewForm = ({test, taskId}) => {

    // console.log(test, typeof(test),'tasker_id in form')
    const [description, setDescription] = useState('')
    const [rating, setRating] = useState('')
    const [tasker_id, setTasker_id] = useState('')
    const [validation, setValidation] = useState('')

    const dispatch = useDispatch()
    const history = useHistory()

    useEffect( () => {
        dispatch(getReviewForLoggedIn())
    }, [dispatch])

    const sessionUser = useSelector( (state) => state.session.user)
    // console.log(typeof(sessionUser), sessionUser, 'session//////////////')

    const sessiontest = useSelector( state => state)
    // console.log(sessiontest, 'test---------')

    const handleSubmit = async (e) => {
        e.preventDefault();

        const errors = {}
        if(description.length < 5 || description.length > 100) errors['description'] = 'Review requires atleast 5 characters or below 100 characters'
        if(rating < 1 || rating > 5) errors['rating'] = 'Rating must be between 1 and 5'

        if(Object.values(errors).length){
            setValidation(errors)
            return alert('can not submit')
        }

        const payload = {
            description,
            rating,
            user_id: sessionUser.id,
            tasker_id: test,
            task_id:taskId,
        }

        let newReviewByUser = await dispatch(createNewReviewByUser(payload))
        // console.log(newReviewByUser, 'handle submit')

        if (newReviewByUser) {
            return history.push('/reviews/currentUser')
        }

        setValidation({})
    }

    return (
        <>
        <div className="mainForm">
            <h2>Write a Review</h2>

            <div className="gapAfterTitle"></div>

            <form onSubmit={handleSubmit}>
                <div>
                    <h4>How was the service?</h4>
                    <p>Please describe your experience</p>
                    <label>
                        <textarea
                            id='descriptionCreate'
                            placeholder="maximum 100 characters"
                            required
                            value={description}
                            type="text"
                            onChange={ e => setDescription(e.target.value)}/>
                            {
                                validation.description && (
                                    <div style={{color: 'red'}}
                                    >{validation.description}</div>
                                )
                            }
                    </label>
                </div>
                <div>
                    <h4>Please leave a rating</h4>
                    <label>
                        <input
                            id='rating'
                            required
                            placeholder="Rate between 1 & 5"
                            value={rating}
                            type="integer"
                            onChange={ e => setRating(e.target.value)}
                            />
                            {
                                validation.rating && (
                                    <div style={{color: 'red'}}>
                                        {validation.rating}
                                    </div>
                                )
                            }
                    </label>
                </div>
                <div className="buttonDiv">
                    <button className='postBtn' type="submit">Post Your Review</button>
                </div>
            </form>
        </div>
        </>
    )
}

export default CreateReviewForm
