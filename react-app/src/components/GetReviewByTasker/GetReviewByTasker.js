import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getReviewByTaskerId } from "../../store/reviews";
import { useParams } from "react-router-dom/cjs/react-router-dom";
import { getTaskers } from "../../store/taskers";


const ReviewsByTasker_id = () => {

    const dispatch = useDispatch()

    const list = useSelector(state => Object.values(state.reviewReducer))
    const taskerData = useSelector(state => Object.values(state.taskers))
    let {tasker_id} = useParams()
    tasker_id = Number(tasker_id)
    // console.log(list, tasker_id, typeof(tasker_id),'state in compo')
    // console.log(taskerData, 'Data-----')

    useEffect(() => {
        dispatch(getReviewByTaskerId((tasker_id)))
        dispatch(getTaskers())
    }, [dispatch])

    let tasker = []
    taskerData.forEach( data => {
        // console.log(data.id, 'data ID')
        if(data.id === tasker_id){
            return tasker.push(data)
        }
    })

    if(!tasker.length){
        return(
            <p>...loading</p>
        )
    }
    // console.log(tasker, 'tasker data')
    // console.log(tasker[0], 'testing')

    let avg = 0
    let numReview = 0
    list.forEach(review => {
        // console.log(review.rating)
        numReview++
        avg = avg+ review.rating
    })

    // console.log(avg, numReview, 'test')

    const taskstypesobj = {
        1:"General Mounting",
        2: "Minor Home Repairs",
        3: 'Cleaning',
        4: "Yard Work",
        5: "Plumbing Help",
        6: "Indoor Painting",
        7: "Heavy Lifting and Loading",
        8: "Waiting in Line",
        9: "Pet Sitting",
        10: "Cooking/Baking"
    }


    return (
        <>
            <h1>Tasker's Reviews</h1>
            <div>
            <h2>Tasker Detail</h2>
                <p>Name: {tasker[0].lastName}, {tasker[0].firstName}</p>
                {/* <p>Hourly Rate: ${tasker[0].taskerTaskTypes.find(taskType => taskType.taskType_id === YOUR_TASK_TYPE_ID).hourlyRate}/hr</p> */}
                <p>Member Since: {new Date(tasker[0].createdAt).toDateString()}</p>
                <p>{(avg/numReview).toFixed(1)} ★</p>
            </div>
            <div>
                {list.map(rev => (
                    <div>
                        <div>
                            Review: {rev.description}
                        </div>
                        <div>Rating: {rev.rating}</div>
                        <div>
                            {new Date(rev.created_at).toDateString()}
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}


export default ReviewsByTasker_id
