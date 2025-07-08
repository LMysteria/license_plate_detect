import { createContext, useEffect, useState } from "react"
import { useNavigate } from "react-router"
import { getAuthHeader, getBackendContext } from "../Util/AuthUtil"
import Cookies from "js-cookie"

const userContext = createContext({});



const PageHeader = (outline) => {

    const [token, setToken] = useState(Cookies.get("Host-access_token") || "");
    const [detail, setDetail] = useState({});
    const navigate = useNavigate();
    useEffect(() => {
        if (token !== ""){
            fetch(`${getBackendContext()}/user/detail`,{
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response)=>response.json())
            .then((data)=>{
                setDetail(data)
            })
            .catch((err)=>console.log(err))
        }
    },[token, navigate])

    const logout = () => {
        Cookies.remove("Host-access_token",{path:"/"});
        setToken("");
    }
    console.log(detail)
    return(
        <div className="content">
            <div className="header">
                <span><a href="/">Home</a></span>
                {JSON.stringify(detail) !== '{}'?<span className="userInfo">Welcome <a href="/userdetail">{detail.username}</a>, Balance: {detail.balance}, <button onClick={logout}>Logout</button></span>:
                <span className="userInfo"><a href="/login">Login</a>,   <a href="/signup">Create account</a></span>
                }
                
            </div>
            <div className="home-content">
                <userContext.Provider value={detail} >
                        {outline.children}
                </userContext.Provider>
            </div>
        </div>
    )
}

export default PageHeader
export {userContext}