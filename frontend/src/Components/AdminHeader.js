import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getAuthHeader } from "../Util/AuthUtil"
import Cookies from "js-cookie"

const AdminHeader = () => {
    const [token, setToken] = useState(Cookies.get("Host-access_token") || "");
    const [username, setUsername] = useState("");
    const navigate = useNavigate()

    useEffect(() => {
        if (token === ""){
            navigate("/login")
        }

        if (username===""){
            fetch("http://localhost:8000/admin/",{
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response)=>{
                if(response.status === 401){
                    throw new Error("Access Denied")
                }
                return response.json()})
            .then((data)=>{
                console.log(data)
                if(data.username)
                    setUsername(data.username)
            })
            .catch((err)=>{
                if (err.message === "Access Denied"){
                    navigate("/")
                }
                console.log(err)
            })
        }
    },[username, token, navigate])

    const logout = () => {
        Cookies.remove("Host-access_token",{path:"/"});
        setToken("");
    }
    return(
        <div className="header">
            <span><Link to="/">Home</Link><span>, </span><Link to="/admin">Admin</Link></span>
            <span className="userInfo">Welcome {username}, <button onClick={logout}>Logout</button></span>
        </div>
    )
}

export default AdminHeader