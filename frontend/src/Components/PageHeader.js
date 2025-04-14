import { createContext, useState } from "react"
import {Link} from "react-router"
import { Navigate } from "react-router"
import getAuthHeader from "../Util/FetchUtil"
import Cookies from "js-cookie"

const userContext = createContext({});



const PageHeader = (outline) => {

    const [token,] = useState(Cookies.get("__Host-access_token") || "");
    const [username, setUsername] = useState("");
    const [detail, setDetail] = useState({});

    if (token === ""){
        return(
            <Navigate to="/login"/>
        )
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
    return(
        <div>
            <div className="header">
                <span><Link to="/">Home</Link></span>
                <span className="userInfo">Welcome <Link to="/userdetail">{username}</Link>, Balance: {detail.balance}</span>
            </div>
            <userContext.Provider value={detail}>
                    {outline.children}
            </userContext.Provider>
        </div>
    )
}

export default PageHeader
export {userContext}