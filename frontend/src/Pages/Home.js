import { createElement, useState } from "react";
import { Navigate } from "react-router-dom";
import Cookies from "js-cookie";
import getAuthHeader from "../Util/FetchUtil";

const Home = () => {
    const [token,] = useState(Cookies.get("__Host-access_token") || "");
    const [username, setUsername] = useState("")
    const [detail, setDetail] = useState({})
    const [parkinglotlist, setParkinglotlist] = useState([])

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
            console.log(data)
            setUsername(data["username"])
        })
        .catch((err)=>console.log(err))

        fetch("http://localhost:8000/user/detail",{
            method: "GET",
            headers: getAuthHeader(token)
        })
        .then((response)=>response.json())
        .then((data)=>{
            console.log(data)
            setDetail(data)
        })
        .catch((err)=>console.log(err))
    }
    
    if(parkinglotlist.length === 0){
        fetch("http://localhost:8000/parkinglot/list",{
            method: "GET",
        })
        .then((response)=>response.json())
        .then((data)=>{
            setParkinglotlist(data)
        })
        .catch((err)=>console.log(err))
    }

    console.log(parkinglotlist)
    
    const Parkinglot = () => {
        if(parkinglotlist.length>0){
            const parkinglots = parkinglotlist.map((val) => (
                <div key={val.id}>
                    <p>Name: {val.name}</p>
                    <p>Address: {val.address}</p>
                    <p>Day Motorbike Fee: {val.dayfeemotorbike}</p>
                    <p>Night Motorbike Fee: {val.nightfeemotorbike}</p>
                    <p>Car Fee: {val.carfee}</p>
                    <p>Car Remaining Space: {val.car_remaining_space}</p>
                    <p>Motorbike Remaining Space: {val.motorbike_remaining_space}</p>
                </div>
            ));

            return(
                <div>
                    {parkinglots}
                </div>
            )}
        return(
            <div>

            </div>
        )
    }

    return(
    <div>
        <label>Welcome {username}, Balance: {detail.balance}</label>
        <Parkinglot />
    </div>
    )
}

export default Home