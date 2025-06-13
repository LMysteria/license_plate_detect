import PageHeader from "../../Components/PageHeader"
import { data, Form, useNavigate } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import { userContext } from "../../Components/PageHeader";
import { getBackendContext, getAuthHeader } from "../../Util/AuthUtil";
import Cookies from "js-cookie"

const TransactionPage = () => {
    const usercontext = useContext(userContext)
    const navigate = useNavigate()
    const [token,] = useState(Cookies.get("Host-access_token") || "");
    const [transactionList, setTransactionList] = useState([])

    useEffect(() => {
        if(transactionList.length === 0){
            fetch(`${getBackendContext()}/user/transactions`,{
                method: "GET",
                headers: getAuthHeader(token)
            })
            .then((response)=> response.json()) 
            .then((data) => {
                console.log(data)
                setTransactionList(data)})
        }

    },[transactionList])

    if(!usercontext){
        navigate("/")
    }

    const transactionListMap = transactionList.map((val) => (
        <div className="form">
            <p>
                transaction id: {val.id?val.id:""}<br/>
                parking fee: {val.balancechanges?val.balancechanges:""}<br/>
                description: {val.description?val.description:""}
            </p>
        </div>
    ))

    return(
        <PageHeader>
            <div>
                {transactionListMap}
            </div>
        </PageHeader>
    )
}

export default TransactionPage