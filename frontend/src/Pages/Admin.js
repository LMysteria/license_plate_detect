import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getAuthHeader } from "../Util/AuthUtil"
import AdminHeader from "../Components/AdminHeader";
import Cookies from "js-cookie"

const AdminPage = () => {
    const [input, setInputs] = useState("");
    const [token, setToken] = useState(Cookies.get("Host-access_token") || "");
    const [fetchValue, setFetchValue] = useState("");
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

    const getRole = (
        <p>
            Name: {fetchValue.fetchGetRole?fetchValue.fetchGetRole.name:""}<br />
            Description: {fetchValue.fetchGetRole?fetchValue.fetchGetRole.description:""}
        </p>
    )


    return(
        <div>
            <AdminHeader />
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
            <a href="/admin/parkinglot">Parking Lot</a>
        </div>
    )
}

export default AdminPage