import { useState } from "react";

const ParkingLot = () => {
    const [parkinglotlist, setParkinglotlist] = useState([])

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
    
    const parkinglots = parkinglotlist.map((val) => (
            <div key={val.id} className="parkinglotitem">
                <p>Name: {val.name}<br />
                Address: {val.address}<br />
                Day Motorbike Fee: {val.dayfeemotorbike}<br />
                Night Motorbike Fee: {val.nightfeemotorbike}<br />
                Car Fee: {val.carfee}<br />
                Car Remaining Space: {val.car_remaining_space}<br />
                Motorbike Remaining Space: {val.motorbike_remaining_space}</p>
                <img src={`http://localhost:8000/${val.image_path}`} alt="loading" className="parkinglotimage"/>
            </div>
    ))

    return(
        <div className="parkinglot">
            {parkinglots}
        </div>
    )
}



export default ParkingLot