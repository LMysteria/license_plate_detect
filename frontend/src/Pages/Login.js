import { useState } from "react"
import Cookies from "js-cookie";
import { Link, useNavigate } from "react-router-dom";
import PageHeader from "../Components/PageHeader";
import { getBackendContext } from "../Util/AuthUtil";

const Login = () => {
    const [input, setInputs] = useState("");
    const [warning, setWarning] = useState("");
    const navigate = useNavigate()

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const loginData = new FormData(event.target)
        fetch(`${getBackendContext()}/login`,{
            method: "POST",
            body: loginData
        })
        .then((response) => {
            if(response.status === 401){
                setWarning("Incorrect username or password")
                throw new Error(response.status)
            }
            return response.json()
        })
        .then((data) => {
            console.log(data)
            const expiredate = new Date(data["expire"])
            Cookies.set("Host-access_token", data["access_token"], {path:"/", secure:true, expires:expiredate, sameSite:"None"})
            navigate(-1)
        })
        .catch((err) => console.log(err))
    }


    return(
    <PageHeader>
        <div className="Login">
            <h1>Login</h1>
            <form onSubmit={handleSubmit} method="POST">
                <div>
                    <label>Username</label>
                    <input 
                    type="text" 
                    name="username"
                    value={input.username || ""}
                    onChange={handleChange}
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input 
                    type="password" 
                    name="password"
                    value={input.password || ""}
                    onChange={handleChange}
                    />
                </div>
                <button type="submit" className="submit">Login</button>
            </form>
            <span>{warning}</span>
            <div>
                <span>Don't have an account? </span><Link to="/signup">Create account</Link>
            </div>
        </div>
    </PageHeader>
    )
}
export default Login