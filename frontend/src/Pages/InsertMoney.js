import PageHeader from "../Components/PageHeader"
import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { userContext } from "../Components/PageHeader";
import { getBackendContext, getAuthHeader } from "../Util/AuthUtil";
import Cookies from "js-cookie"

const InsertMoneyPage = () => {
    const [input, setInputs] = useState("");
    const usercontext = useContext(userContext)
    const navigate = useNavigate()
    const [token,] = useState(Cookies.get("Host-access_token") || "");

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }
    
    if(!usercontext){
        navigate("/")
    }

    const cancelForm = () => {
        navigate("/userdetail")
    }

    const saveForm = () => {
        const form = new FormData()
        form.append("insertmoney", input.insertmoney)
        fetch(`${getBackendContext()}/user/balance/insert`,{
            method: "POST",
            body: form,
            headers: getAuthHeader(token)
        })
        .then((response) => {
            if(response.ok){
                return response.json()
            }
            throw response.json()
        })
        .then((data)=>{
            navigate("/userdetail")
            console.log(data)
        })
        .catch(err => console.log(err))
    }

    return(
        <PageHeader>
            <div className="form">
                <h1>Insert Money</h1>
                <div>
                    <label htmlFor="insertmoney">Insert Money: </label>
                    <input type="number" name="insertmoney" value={input.insertmoney || 0} onChange={handleChange} />
                </div>
                <div>
                    <button onClick={cancelForm}>Cancel</button>
                    <button onClick={saveForm}>Submit</button>
                </div>
            </div>
        </PageHeader>
    )
}

export default InsertMoneyPage