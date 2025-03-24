import { useState } from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";

const Home = () => {
    const [token,] = useState(Cookies.get("__Host-access_token") || "");
    const [username, setUsername] = useState("")

    if (token === ""){
        return(
            <Navigate to="/login"/>
        )
    }

    if (username===""){
        fetch("http://localhost:8000/user/account",{
            method: "GET",
            headers: new Headers({
                    'Authorization': "Bearer "+token,
                    'Content-Type':'application/x-www-form-urlencoded'
            })
        })
        .then((response)=>response.json())
        .then((data)=>{
            console.log(data)
            setUsername(data["username"])
        })
        .catch((err)=>console.log(err))
    }
    return(
    <div>
        <label>username: {username}</label>
    </div>
    )
}

export default Home