import { createContext, useEffect, useState } from "react"
import { Link, useNavigate } from "react-router"
import { getAuthHeader } from "../Util/AuthUtil"
import Cookies from "js-cookie"

const userContext = createContext({});



const PageHeader = (outline) => {

    const [token, setToken] = useState(Cookies.get("Host-access_token") || "");
    const [username, setUsername] = useState("");
    const [detail, setDetail] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        if (token === ""){
            navigate('/login')
            return
        }
        
        if (username===""){
            fetch("http://localhost:8000/user/account",{
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response)=>response.json())
            .then((data)=>{
                setUsername(data["username"])
            })
            .catch((err)=>console.log(err))
    
            fetch("http://localhost:8000/user/detail",{
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response)=>response.json())
            .then((data)=>{
                setDetail(data)
            })
            .catch((err)=>console.log(err))
        }
    },[username, token, navigate])

    const logout = () => {
        Cookies.remove("Host-access_token",{path:"/"});
        setToken("");
    }

    return(
        <div>
            <div className="header">
                <span><Link to="/">Home</Link></span>
                <span className="userInfo">Welcome <Link to="/userdetail">{username}</Link>, Balance: {detail.balance}, <button onClick={logout}>Logout</button></span>
            </div>
            <userContext.Provider value={detail}>
                    {outline.children}
            </userContext.Provider>
        </div>
    )
}

export default PageHeader
export {userContext}