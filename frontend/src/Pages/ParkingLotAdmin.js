import { useEffect, useState } from "react";
import AdminHeader from "../Components/AdminHeader";

const ParkingLotAdmin = () => {
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(0)
    const [displayParkingArea, setParkingArea] = useState([])
    const [editParkingLot, setEditParkingLot] = useState({})
    const [editParkingLotImage, setEditParkingLotImage] = useState()
    const [editParkingArea, setEditParkingArea] = useState({})
    const [input, setInputs] = useState("")

    const getParkinglotlist = (search="") => {
        fetch(`http://localhost:8000/parkinglot/list?search=${search}`,{
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

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }

    const Search = () => {
        getParkinglotlist(input.searchParkinglot)
    }

    const EditParkingLot = (event) => {
        const parkinglotid = event.target.parentElement.getAttribute("parkinglotid")
        const parkinglot = parkinglotlist.find((val) => val.id===parkinglotid)
        setEditParkingLot(parkinglot)
    }
    
    const EditParkingArea = (event) => {
        const parkingareaid = event.target.parentElement.getAttribute("parkingareaid")
        const parkingarea = parkingareas.find((val) => val.id===parkingareaid)
        setEditParkingArea(parkingarea)
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
                <img src={val.image_path? `http://localhost:8000/${val.image_path}`:undefined} alt="No img" className="parkinglotimage"/>
                <button type="button" onClick={EditParkingLot}>Edit</button>
            </div>
    ))

    const parkingareas = displayParkingArea.map((val) => (
        <div key={val.id} parkingareaid={val.id} className="parkinglotitem">
            <p>Area name: {val.area}<br />
            Type: {val.iscar ? "car":"motorbike"}<br />
            Remaining Space: {val.remainingspace}<br />
            </p>
            <img src={val.imagepath?`http://localhost:8000/${val.imagepath}`:undefined} alt="No img" className="parkinglotimage"/>
            <button type="button" onClick={editParkingArea}>Edit</button>
        </div>
))

    return(
        <div>
            <AdminHeader />
            <div className="parkinglotdiv">
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
            <div className="edit">
                <h1>Parking Lot Edit</h1>
                <div>
                    <label for="name">Name: </label><input type="text" name="parkinglotname" value={editParkingLot.name}/>
                </div>
                <div>
                    <label for="address">Address: </label><input type="text" name="parkinglotaddress" value={editParkingLot.address}/>
                </div>
                <div>
                    <label for="daymotorbikefee">Day Motorbike Fee: </label><input type="text" name="parkinglotmotorbikefee" value={editParkingLot.dayfeemotorbike}/>
                </div>
                <div>
                    <label for="nightmotorbikefee">Name: </label><input type="text" name="nightmotorbikefee" value={editParkingLot.nightfeemotorbike}/>
                </div>
                <div>
                    <label for="carfee">Name: </label><input type="text" name="carfee" value={editParkingLot.carfee}/>
                </div>
                <img src={editParkingLotImage?URL.createObjectURL(selectedImage):
                    (val.imagepath?`http://localhost:8000/${val.imagepath}`:undefined)} alt="No img" className="parkinglotimage"/>
                <input
                    type="file"
                    name="img"
                    // Event handler to capture file selection and update the state
                    onChange={(event) => {
                        setSelectedImage(event.target.files[0]); // Update the state with the selected file
                    }}
                />
                <div>
                    <button>Cancel</button>
                    <button>Save</button>
                </div>
            </div>
            <div className="edit">

            </div>
        </div>
    )
}



export default ParkingLotAdmin