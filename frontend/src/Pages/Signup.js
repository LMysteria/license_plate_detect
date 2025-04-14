import { useState } from "react"
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const Signup = () => {
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
        let warningmsg = ""

        const checksignup = () => {
            const usernamepattern = /^[a-zA-z0-9]{6,}$/;
            const passwordpattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

            if(input.username !== input.username.match(usernamepattern)[0]){
                warningmsg += "Username must contain atleast 6 character and no non-special character\n"
            }

            if(input.password !== input.password.match(passwordpattern)[0]){
                warningmsg += "Password must contain atleast 8 character. At least 1 uppercase character. At least 1 lowercase character. At least 1 digit. At least 1 special character\n"
            }

            if(input.password !== input.confirmpassword){
                warningmsg += "Confirm password not match"
            }

            if(warningmsg !== ""){
                console.log(warningmsg)
                setWarning (warningmsg)
                return false
            }
            return true
        }

        if(!checksignup()){
            return
        }

        const signupData = new FormData(event.target)
        fetch("http://localhost:8000/signup",{
            method: "POST",
            body: signupData
        })
        .then((response) => {
            if(response.ok){
                return response.json()
            }
            throw response.json()
        })
        .then(()=>{
            fetch("http://localhost:8000/login",{
                method: "POST",
                body: signupData
            })
            .then((response) => {
                if(response.status === 401){
                    setWarning("Incorrect username or password")
                    throw new Error(response.json())
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
                const expiredate = new Date(data["expire"])
                Cookies.set("__Host-access_token", data["access_token"], {path:"/", secure:true, expires:expiredate, sameSite:"None"})
                navigate("/")
            })
        })
        .catch(err => console.log(err))
    }


    return(
    <div className="signUp">
        <h1>Sign Up</h1>
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
            <div>
                <label>Confirm Password</label>
                <input 
                type="password" 
                name="confirmpassword"
                value={input.confirmpassword || ""}
                onChange={handleChange}
                />
            </div>
            <button type="submit">Signup</button>
        </form>
        <span>{warning}</span>
        <div>
        <span>Have an account? </span><Link to="/login">Login</Link>
        </div>
    </div>
    )
}
export default Signup