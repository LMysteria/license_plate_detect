import { useContext } from "react"
import {userContext} from "../Components/PageHeader"

const UserDetail = () => {
    const usercontext = useContext(userContext)

    return(
        <div className="userDetail">
            <p>
                phonenumber: {usercontext.phonenumber} <br/>
                balance: {usercontext.balance} <br/>
                role: {usercontext.role}
            </p>
        </div>
    )
}

export default UserDetail