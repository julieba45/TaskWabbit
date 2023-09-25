import { useDispatch } from "react-redux";
import { useParams } from "react-router-dom";
import { createTask } from "../../store/tasks";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { getTaskers } from "../../store/taskers";
import StepIndicator from "../StepIndicator";
import { NavLink, Link } from "react-router-dom";
import logo from "../Navigation/images/tWabbitLogo.png";


import Step1 from "../Step1";
import Step2 from "../Step2";
import Step3 from "../Step3";
import Step4 from "../Step4";
import './CreateTaskForm.css';


function CreateTaskForm() {
  const dispatch = useDispatch();
  const { taskTypeId } = useParams();
  const [step, setStep] = useState(1);
  const [errors, setErrors] = useState([]);
  const [stepIsValid, setStepIsValid] = useState({ 1: false, 2: false, 3: false, 4: false }); //keep track whether each step is valid(stepindicator)

  const [formData, setFormData] = useState({
    taskTypeId: taskTypeId,
  });

  const [isMounted, setIsMounted] = useState(true);

  //Fetcha all Taskers
  useEffect(() => {
    const data = dispatch(getTaskers())
    // taskers.current = data || [];
  }, [dispatch]);

  useEffect(() => {
    return () => {
      setIsMounted(false);
    };
  }, []);


  const taskers = Object.values(useSelector(state => state.taskers));

  const handleStepComplete = (stepData) => {
    setStepIsValid(prevStepIsValid => ({ ...prevStepIsValid, [step]: true }));
    if (stepData.back) {
      setStep(prevStep => prevStep - 1);
    } else {
      setFormData(prevData => ({ ...prevData, ...stepData })); //stepData, the data form each step
      setStep(prevStep => prevStep + 1);
    }
  };

  //Moving through steps using StepIndicator
  const handleStepClick = (step) => {
    for (let i = 1; i < step; i++) {
      if (!stepIsValid[i]) {
        return;
      }
    }
    setStep(step);
  }

  const submitForm = async () => {
    const taskData = {
      taskTypeId: formData.taskTypeId,
      title: formData.title,
      description: formData.description,
      totalPrice: formData.totalPrice,
      location: formData.location,
      task_date: formData.task_date,
      tasker_id: formData.tasker_id,
      timeDiff: new Date().getTimezoneOffset()
    }
    const data = await dispatch(createTask(taskData))
    // console.log("Create task Form in the component", data);
    if(isMounted){
      if (data) {
        setErrors(data)
      } else {
        setStep(step + 1);
        // console.log("Form submitted successfully");
      }
    }
  }

    return (
      <>
        <div className="logo-step-indicator">
          <Link to="/">
            <img src={logo} alt="TaskRabbit logo" className="logo" />
          </Link>
          <StepIndicator currentStep={step} onStepClick={handleStepClick}/>
        </div>
        <div className="task-form-container">
          <form className="create-task-form" onSubmit={submitForm}>
            {step === 1 && (
              <Step1
                onStepComplete={handleStepComplete}
                existingData={formData}
              />
            )}
            {step === 2 && (
              <Step2
                taskers={taskers}
                onStepComplete={handleStepComplete}
                existingData={formData}
              />
            )}
            {step === 3 && (
              <Step3
                onStepComplete={handleStepComplete}
                existingData={formData}
              />
            )}
            {step === 4 && (
              <Step4
                handleSubmit={submitForm}
                onStepComplete={handleStepComplete}
                hourlyRate={formData.hourlyRate}
                location={formData.location}
                taskDate={formData.task_date}
                taskerName={formData.tasker_name}
                trustAndSupportFee={formData.trustAndSupportFee}
              />
            )}
          </form>
        </div>
      </>
      );
}





export default CreateTaskForm
