import PageHeader from "../Components/PageHeader"
import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { userContext } from "../Components/PageHeader";
import { getBackendContext, getAuthHeader } from "../Util/AuthUtil";
import Cookies from "js-cookie"

const FeedBackPage = () => {
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
        form.append("subject", input.subject)
        form.append("detail", input.detail)
        fetch(`${getBackendContext()}/user/feedback/create`,{
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
            console.log(data)
            document.getElementById("successform").style.display = "block"
        })
        .catch(err => console.log(err))
    }

    return(
        <PageHeader>
            <div className="form">
                <h1>Submit Feedback</h1>
                <div>
                    <label htmlFor="subject">Subject: </label>
                    <input type="text" name="subject" value={input.subject || ""} onChange={handleChange} />
                </div>
                <div>
                    <label htmlFor="detail">Detail: </label>
                    <input type="text" name="detail" value={input.detail || ""} onChange={handleChange} />
                </div>
                <div>
                    <button onClick={cancelForm}>Cancel</button>
                    <button onClick={saveForm}>Submit</button>
                </div>
            </div>
            <div className="editbackground" id="successform">
                <div className="form">
                    <p>Feedback sent successfully</p>
                    <a href="/userdetail">ok</a>
                </div>
            </div>
        </PageHeader>
    )
}

export default FeedBackPage