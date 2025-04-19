import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getAuthHeader } from "../Util/AuthUtil"
import Cookies from "js-cookie"



const AdminPage = () => {
    const [input, setInputs] = useState("");
    const [fetchValue, setFetchValue] = useState("");
    const [token, setToken] = useState(Cookies.get("Host-access_token") || "");
    const [username, setUsername] = useState("");
    const navigate = useNavigate()

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }

    const handleSubmit = (action) => {
        if(action === "getRole"){
            fetch(`http://localhost:8000/admin/role/details?roleid=${input.getRole_Roleid}`, {
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response) => response.json())
            .then((data)=>setFetchValue(values => ({...values, ["fetchGetRole"]: data})))
            .catch((err)=>console.log(err))
        }
    }

    useEffect(() => {
        if (token === ""){
            navigate("/login")
        }

        if (username===""){
            fetch("http://localhost:8000/checkadmin",{
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

    const getRole = (
        <p>
            Name: {fetchValue.fetchGetRole?fetchValue.fetchGetRole.name:""}<br />
            Description: {fetchValue.fetchGetRole?fetchValue.fetchGetRole.description:""}
        </p>
    )


    return(
        <div>
            <div className="header">
                <span><Link to="/">Home</Link></span>
                <span className="userInfo">Welcome {username}, <button onClick={logout}>Logout</button></span>
            </div>
            <div>
                <div>
                    <h3>Get Role</h3>
                    <input type="number" name="getRole_Roleid" onChange={handleChange}/>
                    <button onClick={()=>handleSubmit("getRole")}>Submit</button>
                    <div>
                        {getRole}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default AdminPage