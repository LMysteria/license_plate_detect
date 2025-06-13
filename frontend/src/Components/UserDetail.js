import { useContext } from "react"
import {userContext} from "../Components/PageHeader"
import { useNavigate } from "react-router-dom"

const UserDetail = () => {
    const usercontext = useContext(userContext)
    const navigate = useNavigate()

    if(!userContext){
        navigate("/")
    }

    return(
        <div className="userDetail form">
            <p>
                username: {userContext?usercontext.username:""} <br/>
                phonenumber: {userContext?usercontext.phonenumber:""} <br/>
                balance: {userContext?usercontext.balance:""} <br/>
                role: {userContext?usercontext.role:""}
            </p>
            <a href="/feedback">Feedback</a>
            <a href="/insertmoney">Insert Money</a>
            <a href="/transaction">Transaction History</a>
        </div>
    )
}

export default UserDetail