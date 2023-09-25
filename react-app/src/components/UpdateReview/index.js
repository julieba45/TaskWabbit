import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux"
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { getRevById } from "../../store/reviews";
import UpdateReview from "./UpdateReview";
import { useHistory } from "react-router-dom/cjs/react-router-dom";


const Update = () => {
    const dispatch = useDispatch();
    const history = useHistory()

    const {id} = useParams()
    // console.log(id, 'test')
    const review = useSelector(state => state.reviewReducer[id])

    const userSession = useSelector(state => state.session.user)
    // console.log(review, userSession, 'review update')

    useEffect(() => {

        dispatch(getRevById(id))
        // console.log(id, 'idTest')
    }, [dispatch, userSession])

    if(!review){
        return(
            <>
            <p>Review</p>
            <p>NOT FOUND</p>

            </>
        )
    }

    if(!userSession || userSession.id !== review.user_id){
        // alert('Resticted')
        return(
            <>
                {history.push('/')}
                </>
            )
        }


    // converting to Object
    let reviewObj = review
    // console.log(reviewObj, 'reviewObj --------')

    return(
        // <p>Test</p>
        <UpdateReview reviewObj={reviewObj} />
    )
}

export default Update
