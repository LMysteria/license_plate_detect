import { useEffect, useState } from "react";
import { getBackendContext } from "../Util/AuthUtil";
import { useMap } from "@vis.gl/react-google-maps";

const ParkingLot = ({setParkingLotMarker}) => {
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(0)
    const [displayParkingArea, setParkingArea] = useState([])
    const [input, setInputs] = useState("")

    const getParkinglotlist = (search="") => {
        fetch(`${getBackendContext()}/parkinglot/list?search=${search}`,{
            method: "GET",
        })
        .then((response) => response.json())
        .then((data) => setParkinglotlist(data))
        .catch((err)=> console.log(err))
        setParkingArea([]);
    }

    useEffect(() => {
        if(parkinglotlist.length === 0){
            getParkinglotlist()
        }
    }, [parkinglotlist])


    useEffect(() => {
        if (clickedParkinglot>0){
            const result = parkinglotlist.filter((parkinglot) => {return parkinglot.id===clickedParkinglot})[0]
            setParkingLotMarker({lat: result.lat, lng: result.lng})
            fetch(`${getBackendContext()}/parkinglot/parkingarea/list?parkinglotid=${clickedParkinglot}`, {
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
        console.log(event.target.getAttribute("parkinglotid"))
        setClickedParkinglot(parseInt(event.target.getAttribute("parkinglotid")))
    }
    
    const parkinglots = parkinglotlist.map((val) => (
            <div key={val.id} parkinglotid={val.id} className="parkinglotitem" onClick={onClickParkingLot}>
                <p parkinglotid={val.id}>Name: {val.name}<br />
                Address: {val.address}<br />
                Car Remaining Space: {val.car_remaining_space}<br />
                Motorbike Remaining Space: {val.motorbike_remaining_space}</p>
            </div>
    ))

    const parkingareas = displayParkingArea.map((val) => (
        <div key={val.id} className="parkinglotitem">
            <p>Area name: {val.area}<br />
            Type: {val.iscar ? "car":"motorbike"}<br />
            Remaining Space: {val.remainingspace}<br />
            </p>
            <img src={val.imagepath?`${getBackendContext()}/${val.imagepath}`:undefined} alt="No img" className="parkinglotimage"/>
        </div>
))

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }

    const Search = () => {
        getParkinglotlist(input.searchParkinglot)
    }

    return(
        <div>
            <div className="parkinglotsearch">
                <input type="text" name="searchParkinglot" placeholder="parkinglot search" onChange={handleChange} className="ParkinglotSearch"/>
                <button name="Search" onClick={Search}>Search</button>
            </div>
            <div className="parkinglotdisplay">
                <div className="parkinglot">
                    {parkinglots}
                </div>
                <div className="parkinglot">
                    {parkingareas}
                </div>
            </div>
        </div>
    )
}



export default ParkingLot