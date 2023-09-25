// constants

//TASKERPROFILE ACTION TYPES

    //GET all tasktypes of curr tasker
const GET_TASKERTASKTYPES = "taskertasktypes/getTaskerTaskTypes";
    //GET specific tasktype by Id
const GET_TASKERTASKTYPE = "taskertasktypes/getTaskerTaskType";
    //DELETE a tasktype of curr user
const DELETE_TASKERTASKTYPE = "taskertasktypes/deleteTaskerTaskType";
    //EDIT a tasktype of curr user
const UPDATE_TASKERTASKTYPE = "taskertasktypes/updateTaskerTaskType"
    //CREATE a tasktype for curr user
const CREATE_TASKERTASKTYPE = "taskertasktypes/createTaskerTaskType"

//TASKERPROFILE ACTION CREATORS

const getTaskerTaskTypesAction = (taskerTaskTypes) => {

    return  {
        type: GET_TASKERTASKTYPES,
        payload: taskerTaskTypes
    }
}
const getTaskerTaskTypeAction = (taskerTaskTypeId) => {

    return  {
        type: GET_TASKERTASKTYPE,
        payload: taskerTaskTypeId
    }
}

const deleteTaskerTaskTypeAction = (taskerTaskTypeId) => {

    return {
        type: DELETE_TASKERTASKTYPE,
        payload: taskerTaskTypeId
    }
}

const updateTaskerTaskTypeAction = (taskerTaskTypeId) => {
    return {
        type:UPDATE_TASKERTASKTYPE,
        payload: taskerTaskTypeId
    }
}

const createTaskerTaskTypeAction = (newTaskerTaskType) => {

    return {
        type: CREATE_TASKERTASKTYPE,
        payload: newTaskerTaskType
    }
}

//TASKERPROFILE THUNK ACTIONS
export const getTaskerTaskTypes = () => async(dispatch) => {
    const response = await fetch('/api/taskerTaskTypes/current');
    if(response.ok){
        const data = await response.json();
        dispatch(getTaskerTaskTypesAction(data.TaskerTaskTypes))
        return data;
    }
}
export const getTaskerTaskType = (taskerTaskTypeId) => async(dispatch) => {
    const response = await fetch(`/api/taskerTaskTypes/${taskerTaskTypeId}`);
    if(response.ok){
        const taskerTaskType = await response.json();
        dispatch(getTaskerTaskTypeAction(taskerTaskType))
        return taskerTaskType;
    }
}

export const updateTaskerTaskType = (taskerTaskTypeId, taskerTaskTypeData) => async(dispatch) =>{

    const response = await fetch(`/api/taskerTaskTypes/${taskerTaskTypeId}`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(taskerTaskTypeData)
    })

    if(response.ok){
        const updatedTaskerTaskType = await response.json();
        dispatch(updateTaskerTaskTypeAction(updatedTaskerTaskType));

        return updatedTaskerTaskType;
    } else if (response.status < 500){


        const data = response.json();

        if(data.errors){
            return data.errors;
        } else {
            return ('An error occurred. Please try again')
        }
    }
}

export const deleteTaskerTaskType = (taskerTaskTypeId) => async(dispatch) => {
    const response = await fetch(`/api/taskerTaskTypes/${taskerTaskTypeId}`, {
        method: "DELETE"
    })
    if(response.ok){
        const data = await response.json();
        dispatch(deleteTaskerTaskTypeAction(taskerTaskTypeId))
    }else if(response.status < 500){
        const data = await response.json()
        if(data.errors){
            return data.errors;
        }
    }else {
        return ('An error occurred. Please try again')
    }
}


export const fetchCreateTaskerTaskType = (taskerTaskTypeData) => async(dispatch) =>{
    // console.log("********INSIDE CREATE TASKTYPE THUNK******")
    try {
        const response = await fetch('/api/taskerTaskTypes', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskerTaskTypeData)
        });
        if(response.ok){
            const newTaskerTaskType = await response.json();
            dispatch(createTaskerTaskTypeAction(newTaskerTaskType));
            return newTaskerTaskType
        } else if (response.status <= 500){
            // console.log("FAILED BODY", JSON.stringify(taskerTaskTypeData))
            const data = await response.json();
            if (data.errors) {
                return data.errors;
            }
        }else {
            return ('An error occurred. Please try again')
        }
    } catch (error) {
        console.error('Network error: ', error);
        return error;
    }
}

//TASKERPROFILE REDUCER

const initialState = {
    taskerTaskTypes: null,
    taskerTaskType: [null]
};

export default function taskerProfileReducer(state = initialState, action){
    let newState = {};
    switch(action.type){
        case GET_TASKERTASKTYPES:
            return{
                ...state,
                taskerTaskTypes: action.payload
            }
        case GET_TASKERTASKTYPE:
            return{
                ...state,
                taskerTaskType: action.payload
            }
        case CREATE_TASKERTASKTYPE:
            newState = {...state,
                taskerTaskTypes: [...state.taskerTaskTypes, action.payload]
                };
            return newState
        case UPDATE_TASKERTASKTYPE:

            return {
                ...state,
                taskerTaskType: action.payload,
                taskerTaskTypes: state.taskerTaskTypes?.map(taskerTaskType => taskerTaskType.id === action.payload.id ? action.payload : taskerTaskType)
        }
        case DELETE_TASKERTASKTYPE:

            return {
                ...state,
                taskerTaskTypes: state.taskerTaskTypes.filter(taskerTaskType => taskerTaskType.id != action.payload)
            }
        default:
            return state
    }
}
