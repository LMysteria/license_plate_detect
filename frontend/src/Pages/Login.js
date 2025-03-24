import { useState } from "react"
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

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
        fetch("http://localhost:8000/login",{
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
            Cookies.set("__Host-access_token", data["access_token"], {path:"/", secure:true, expires:expiredate, sameSite:"None"})
            navigate("/")
        })
        .catch((err) => console.log(err))
    }


    return(
    <div>
        <form onSubmit={handleSubmit}>
            <label>Username</label>
            <input 
            type="text" 
            name="username"
            value={input.username || ""}
            onChange={handleChange}
            />
            <br />
            <label>Password</label>
            <input 
            type="password" 
            name="password"
            value={input.password || ""}
            onChange={handleChange}
            />
            <br />
            <button type="submit">Login</button>
        </form>
        <p>{warning}</p>
    </div>
    )
}
export default Login