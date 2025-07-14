import { useEffect, useState, useRef } from "react";
import AdminHeader from "../../Components/AdminHeader";
import Cookies from "js-cookie"
import { getAuthHeader, getBackendContext } from "../../Util/AuthUtil";
import { fromAddress } from "react-geocode";
import { Map, Marker, APIProvider } from "@vis.gl/react-google-maps";

const ParkingLotAdmin = () => {
    const [token] = useState(Cookies.get("Host-access_token") || "");
    const mapRef = useRef(null);
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(0)
    const [isCreate, setIsCreate] = useState(true)
    const [parkingLotForm, setParkingLotForm] = useState({})
    const [formImage, setFormImage] = useState()
    const [displayParkingArea, setParkingArea] = useState([])
    const [parkingAreaForm, setParkingAreaForm] = useState({})
    const [input, setInputs] = useState("")

    const getParkinglotlist = (search = "") => {
        fetch(`${getBackendContext()}/parkinglot/list?search=${search}`, {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) => setParkinglotlist(data))
            .catch((err) => console.log(err))
        setParkingArea([]);
    }

    useEffect(() => {
        if (parkinglotlist.length === 0) {
            getParkinglotlist()
        }
    }, [parkinglotlist])


    useEffect(() => {
        if (clickedParkinglot > 0) {
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

    const closeForm = () => {
        setParkingAreaForm({})
        setParkingLotForm({})
        setFormImage(undefined)
        document.getElementById("parkingareaform").style.display="none"
        document.getElementById("parkinglotform").style.display="none"
        document.getElementById("editbackground").style.display="none"
    }

    const onCancelParkingLotForm = () => {
        closeForm()
    }

    const onCancelParkingAreaForm = () => {
        closeForm()
    }

    const onSaveParkingLotForm = () => {
        try {
            const form = new FormData()
            form.append("name", parkingLotForm.name)
            form.append("address", parkingLotForm.address)
            form.append("lat", parkingLotForm.lat)
            form.append("lng", parkingLotForm.lng)
            if(parkingLotForm.dayfeemotorbike)
            form.append("dayfeemotorbike", parkingLotForm.dayfeemotorbike)
            if(parkingLotForm.nightfeemotorbike)
            form.append("nightfeemotorbike", parkingLotForm.nightfeemotorbike)
            if(parkingLotForm.carfee)
            form.append("carfee", parkingLotForm.carfee)
            if (formImage) {
                form.append("img", formImage)
            };
            const headers = getAuthHeader(token)
            console.log(Object.fromEntries(form.entries()))
            if(isCreate){
                fetch(`${getBackendContext()}/admin/parkinglot/create`, {
                    method: "POST",
                    body: form,
                    headers: headers
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data) {
                            getParkinglotlist()
                        }
                })
            }
            else{
                form.append("parkinglotid", parkingLotForm.id)
                fetch(`${getBackendContext()}/admin/parkinglot/update`, {
                    method: "POST",
                    body: form,
                    headers: headers
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data) {
                            getParkinglotlist()
                        }
                })
            }
        } catch (error) {
            console.error(error)
        } finally {
            closeForm()
        }
    }

    const onSaveParkingAreaForm = () => {
        try {
            const form = new FormData()
            form.append("area", parkingAreaForm.area)
            form.append("maxspace", parkingAreaForm.maxspace)
            form.append("remainingspace", parkingAreaForm.remainingspace)
            if(parkingAreaForm.iscar === undefined){
                form.append("iscar", false)}
            else{
            form.append("iscar", parkingAreaForm.iscar)}
            if (formImage) {
                form.append("img", formImage)
            };
            const headers = getAuthHeader(token)
            console.log(Object.fromEntries(form.entries()))
            if(isCreate){
                form.append("parkinglotid",parkingLotForm.id)
                fetch(`${getBackendContext()}/admin/parkinglot/parkingarea/create`, {
                    method: "POST",
                    body: form,
                    headers: headers
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data) {
                            getParkinglotlist()
                        }
                })
            }else{
                form.append("parkingareaid",parkingAreaForm.id)
                fetch(`${getBackendContext()}/admin/parkinglot/parkingarea/update`, {
                    method: "POST",
                    body: form,
                    headers: headers
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data) {
                            getParkinglotlist()
                        }
                    })
            }
        } catch (error) {
            console.error(error)
        } finally {
            closeForm()
        }
    }

    const onClickParkingLot = (event) => {
        setClickedParkinglot(event.target.getAttribute("parkinglotid"))
    }

    const onChangeParkingLotForm = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setParkingLotForm(values => ({ ...values, [name]: value }))
    }

    const onChangeParkingAreaForm = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setParkingAreaForm(values => ({ ...values, [name]: value }))
    }


    const handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({ ...values, [name]: value }))
    }

    const Search = () => {
        getParkinglotlist(input.searchParkinglot)
    }

    const EditParkingLot = (event) => {
        const parkinglotid = parseInt(event.target.parentElement.getAttribute("parkinglotid"));
        const parkinglot = parkinglotlist.find((val) => val.id === parkinglotid);
        setIsCreate(false)
        setParkingLotForm(parkinglot)
        document.getElementById("parkinglotform").style.display="flex"
        document.getElementById("editbackground").style.display="block"
        console.log(parkinglot)
    }

    const EditParkingArea = (event) => {
        const parkingareaid = parseInt(event.target.parentElement.getAttribute("parkingareaid"))
        const parkingarea = displayParkingArea.find((val) => val.id === parkingareaid);
        setIsCreate(false)
        setParkingAreaForm(parkingarea)
        document.getElementById("parkingareaform").style.display="flex"
        document.getElementById("editbackground").style.display="block"
        console.log(parkingarea)
    }

    const createParkingLot = () => {
        setIsCreate(true)
        document.getElementById("parkinglotform").style.display="flex"
        document.getElementById("editbackground").style.display="block"
    }

    const createParkingArea = (event) => {
        const parkinglotid = parseInt(event.target.parentElement.getAttribute("parkinglotid"));
        const parkinglot = parkinglotlist.find((val) => val.id === parkinglotid);
        setParkingLotForm(parkinglot)
        setIsCreate(true)
        document.getElementById("parkingareaform").style.display="flex"
        document.getElementById("editbackground").style.display="block"
    }

    const parkinglots = parkinglotlist.map((val) => (
        <div key={val.id} parkinglotid={val.id} className="adminparkinglotitem" onClick={onClickParkingLot}>
            <p parkinglotid={val.id}>Name: {val.name}<br />
                Address: {val.address}<br />
                Day Motorbike Fee: {val.dayfeemotorbike}/4h<br />
                Night Motorbike Fee: {val.nightfeemotorbike}/4h<br />
                Car Fee: {val.carfee}/4h<br />
                Car Remaining Space: {val.car_remaining_space}<br />
                Motorbike Remaining Space: {val.motorbike_remaining_space}</p>
            <div parkinglotid={val.id}>
                <img parkinglotid={val.id} src={val.image_path ? `${getBackendContext()}/${val.image_path}` : undefined} alt="No img" className="parkinglotimage" />
                <button type="button" onClick={EditParkingLot}>Edit</button>
                <button type="button" onClick={createParkingArea}>Create Parking Area</button>
            </div>
        </div>
    ))

    const parkingareas = displayParkingArea.map((val) => (
        <div key={val.id} parkingareaid={val.id} className="adminparkinglotitem">
            <p >Area name: {val.area}<br />
                Type: {val.iscar ? "car" : "motorbike"}<br />
                Remaining Space: {val.remainingspace}<br />
            </p>
            <div>
                <img src={val.imagepath ? `${getBackendContext()}/${val.imagepath}` : undefined} alt="No img" className="parkinglotimage" />
                <button type="button" onClick={EditParkingArea}>Edit</button>
            </div>
        </div>
    ))

    const ParkingGeocodeSearch = (type) => {
        const map = mapRef.current.map;
        if((parkingLotForm.address !== undefined)){
        if (parkingLotForm.address !== ""){
            fromAddress(parkingLotForm.address)
            .then(({ results }) => {
                const pos = results[0].geometry.location;
                map.setCenter(pos)
                console.log(pos)
                parkingLotForm.lat = pos.lat
                parkingLotForm.lng = pos.lng
                setParkingLotForm(parkingLotForm)
            })
            .catch(console.error);
        }}
    }

    return (
        <div>
            <AdminHeader />
            <div className="parkinglotdiv">
                <div className="parkinglotsearch">
                    <input type="text" name="searchParkinglot" placeholder="parkinglot search" onChange={handleChange} className="ParkinglotSearch" />
                    <button name="Search" onClick={Search}>Search</button>
                    <button onClick={createParkingLot}>Create Parking Lot</button>
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
            <div className="editbackground" id="editbackground">
                <div className="edit" id="parkinglotform">
                    <h1>{isCreate ? "New" : "Edit"} Parking Lot</h1>
                    <div className="editdiv">
                        <label htmlFor="name">Name: </label>
                        <input type="text" name="name" value={parkingLotForm.name ? parkingLotForm.name : ""} onChange={onChangeParkingLotForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="address">Address: </label>
                        <input type="text" name="address" value={parkingLotForm.address ? parkingLotForm.address : ""} onChange={onChangeParkingLotForm} onBlur={ParkingGeocodeSearch}/>
                    </div>
                    <div className='admingooglemap'>
                        <APIProvider apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
        
                            <Map 
                                id='map'
                                disableDefaultUI={true}
                                defaultZoom={13}
                                defaultCenter={ {lat: parkingLotForm.lat?parkingLotForm.lat:10.762622, lng: parkingLotForm.lng?parkingLotForm.lng:106.660172} }
                                onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
                                onTilesLoaded={(map) => {mapRef.current = map; console.log("Ref loaded", mapRef.current)}}
                            >
                                <Marker position={parkingLotForm.lat?{lat:parkingLotForm.lat,lng:parkingLotForm.lng}:{lat:0,lng:0}}/>
                            </Map>
                        </APIProvider>
                    </div>
                    <div className="editdiv">
                        <label htmlFor="dayfeemotorbike">Day Motorbike Fee: </label>
                        <input type="text" name="dayfeemotorbike" value={parkingLotForm.dayfeemotorbike ? parkingLotForm.dayfeemotorbike : ""} onChange={onChangeParkingLotForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="nightfeemotorbike">Night Motorbike Fee: </label>
                        <input type="text" name="nightfeemotorbike" value={parkingLotForm.nightfeemotorbike ? parkingLotForm.nightfeemotorbike : ""} onChange={onChangeParkingLotForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="carfee">Car Fee: </label>
                        <input type="text" name="carfee" value={parkingLotForm.carfee ? parkingLotForm.carfee : ""} onChange={onChangeParkingLotForm} />
                    </div>
                    <span>Image:</span>
                    <img src={formImage ? URL.createObjectURL(formImage) :
                        (parkingLotForm.image_path ? `${getBackendContext()}/${parkingLotForm.image_path}` : undefined)} alt="No img" className="parkinglotimage" />
                    <input
                        type="file"
                        name="img"
                        id="parkingLotFormImage"
                        // Event handler to capture file selection and update the state
                        onChange={(event) => {
                            setFormImage(event.target.files[0]); // Update the state with the selected file
                        }}
                    />
                    <div className="editdiv">
                        <button onClick={onCancelParkingLotForm}>Cancel</button>
                        <button onClick={onSaveParkingLotForm}>Save</button>
                    </div>
                </div>
                <div className="edit" id="parkingareaform">
                    <h1>{isCreate ? "New" : "Edit"} Parking Area</h1>
                    <div className="editdiv">
                        <label htmlFor="area">Area: </label>
                        <input type="text" name="area" value={parkingAreaForm.area ? parkingAreaForm.area : ""} onChange={onChangeParkingAreaForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="maxspace">Maximum Space: </label>
                        <input type="text" name="maxspace" value={parkingAreaForm.maxspace ? parkingAreaForm.maxspace : ""} onChange={onChangeParkingAreaForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="remainingspace">Remaining Space: </label>
                        <input type="text" name="remainingspace" value={parkingAreaForm.remainingspace ? parkingAreaForm.remainingspace : ""} onChange={onChangeParkingAreaForm} />
                    </div>
                    <div className="editdiv">
                        <label htmlFor="iscar">Vehicle Type: </label>
                        <select name="iscar" onChange={onChangeParkingAreaForm}>
                            <option value={true} selected={parkingAreaForm.iscar ? "selected" : undefined}>Car</option>
                            <option value={false} selected={parkingAreaForm.iscar ? undefined : "selected"}>Motorbike</option>
                        </select>
                    </div>
                    <span>Image:</span>
                    <img src={formImage ? URL.createObjectURL(formImage) :
                        (parkingAreaForm.imagepath ? `${getBackendContext()}/${parkingAreaForm.imagepath}` : undefined)} alt="No img" className="parkinglotimage" />
                    <input
                        type="file"
                        name="img"
                        id="parkingAreaFormImage"
                        // Event handler to capture file selection and update the state
                        onChange={(event) => {
                            setFormImage(event.target.files[0]); // Update the state with the selected file
                        }}
                    />
                    <div className="editdiv">
                        <button onClick={onCancelParkingAreaForm}>Cancel</button>
                        <button onClick={onSaveParkingAreaForm}>Save</button>
                    </div>
                </div>
            </div>
        </div>
    )
}



export default ParkingLotAdmin