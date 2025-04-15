import { useEffect, useState } from "react";

const ParkingLot = () => {
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(0)
    const [displayParkingArea, setParkingArea] = useState([])

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

    useEffect(() => {
        if (clickedParkinglot>0){
            fetch(`http://localhost:8000/parkinglot/${clickedParkinglot}/parkingarea/list`, {
                method: "GET",
            })
            .then((response) => response.json())
            .then((data) => {
                setParkingArea(data)
                console.log(data)
            })
            .catch((err) => console.log(err))
        }
    }, [clickedParkinglot])

    const onClickParkingLot = (event) => {
        setClickedParkinglot(event.target.getAttribute("parkinglotid"))
    }
    
    const parkinglots = parkinglotlist.map((val) => (
            <div key={val.id} parkinglotid={val.id} className="parkinglotitem" onClick={onClickParkingLot}>
                <p>Name: {val.name}<br />
                Address: {val.address}<br />
                Day Motorbike Fee: {val.dayfeemotorbike}<br />
                Night Motorbike Fee: {val.nightfeemotorbike}<br />
                Car Fee: {val.carfee}<br />
                Car Remaining Space: {val.car_remaining_space}<br />
                Motorbike Remaining Space: {val.motorbike_remaining_space}</p>
                <img src={`http://localhost:8000/${val.image_path}`} alt="No img" className="parkinglotimage"/>
            </div>
    ))

    const parkingareas = displayParkingArea.map((val) => (
        <div key={val.id} className="parkinglotitem">
            <p>Area name: {val.area}<br />
            Type: {val.iscar ? "car":"motorbike"}<br />
            Remaining Space: {val.remainingspace}<br />
            </p>
            <img src={`http://localhost:8000/${val.imagepath}`} alt="No img" className="parkinglotimage"/>
        </div>
))

    return(
        <div className="parkinglotdisplay">
            <div className="parkinglot">
                {parkinglots}
            </div>
            <div className="parkinglot">
                {parkingareas}
            </div>
        </div>
    )
}



export default ParkingLot