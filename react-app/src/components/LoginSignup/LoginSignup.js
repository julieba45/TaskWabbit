import React, { useState } from "react";
import OpenModalButton from "../OpenModalButton";
import SignupFormModal from "../SignupFormModal";
import LoginFormModal from "../LoginFormModal";
import { useSelector } from "react-redux";
import { Redirect, useParams, Link } from "react-router-dom";
import "./LoginSignup.css"



function LoginSignup() {
    const { taskTypeId } = useParams();
    // console.log(taskTypeId, "TASKTYPEID********************")
    const sessionUser = useSelector((state) => state.session.user);
    if (sessionUser) return <Redirect to={`/tasks/new/${taskTypeId}`} />;
    // console.log(taskTypeId, "tasktypeID ______________")


    return (
        <div className="login-signup-root">
            <div className="login-signup-container">
                <div className="login-signup-inner">
                    <div className="taskwabbit-title">taskWabbit</div>
                    <Link to={`/signup/${taskTypeId ?? ''}`} >
                        <button className="signup-button">
                            Sign up
                        </button>
                    </Link>


                    <Link to={`/login/${taskTypeId ?? ''}`}>
                        <button className='login-button'>Log in</button>
                    </Link>

                    <div className="agreement-section">
                        By signing up you agree to our Terms of Use and Privacy Policy.
                    </div>
                </div>
            </div>
        </div>
    )
}

export default LoginSignup;
