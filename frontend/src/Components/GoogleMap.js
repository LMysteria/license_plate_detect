import {Map, Marker} from '@vis.gl/react-google-maps';
import { useState, useEffect, useRef } from 'react';
import {fromAddress} from 'react-geocode'
import { getBackendContext } from "../Util/AuthUtil";
import DirectionDisplay from './DirectionDisplay';

const CustomGoogleMap = () => {
    const mapRef = useRef(null);
    const [currentMarker, setCurrentMarkers] = useState()
    const [input, setInputs] = useState("")
    const [parkinglotMarker, setParkingLotMarker] = useState()
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(null)
    const [displayParkingArea, setParkingArea] = useState([])
    const [geolocation, setGeolocation] = useState()

    const getGeolocation = () => {
        const map = mapRef.current.map
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((position) => {
                const pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude,
                };
                map.setCenter(pos)
                setGeolocation(pos)
                getParkinglotList(pos)
            })
        }
    }

    const getParkinglotList = ({lat, lng}) => {
        fetch(`${getBackendContext()}/parkinglot/list?lat=${lat}&lng=${lng}&search=${input.searchParkinglot}`,{
            method: "GET",
        })
        .then((response) => response.json())
        .then((data) => setParkinglotlist(data))
        .catch((err)=> console.log(err))
        unClickedParkinglot()
    }

    const unClickedParkinglot = () => {
        setParkingArea([]);
        setClickedParkinglot(null)
        document.getElementById("parkinglotdetail").style.display = "none"
        document.getElementById("parkinglot").style.display = "flex"
    }

    useEffect(() => {
        if (clickedParkinglot !== null){
            fetch(`${getBackendContext()}/parkinglot/parkingarea/list?parkinglotid=${clickedParkinglot.id}`, {
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

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }


    const center = {
    lat: 10.762622,  // Example: Ho Chi Minh City
    lng: 106.660172
    };

    const PositionSearch = () => {
        const map = mapRef.current.map
        fromAddress(input.currentposition)
        .then(({ results }) => {
            const pos = results[0].geometry.location;
            map.setCenter(pos)
            setCurrentMarkers(pos)
            const parkinglotsearch = input.searchParkinglot
            console.log(parkinglotsearch)
            if((parkinglotsearch === undefined) | (parkinglotsearch === "")){
                getParkinglotList(pos)
            }
        })
        .catch(console.error);
    }  

    const Search = () => {
        const map = mapRef.current.map
        const destination = input.searchParkinglot
        if(destination){
            fromAddress(destination)
            .then(({ results }) => {
                const pos = results[0].geometry.location;
                
                getParkinglotList(pos)
            })
            .catch(console.error);
        }

        else{
            if(geolocation){
                map.setCenter(geolocation)
                getParkinglotList(geolocation)
            } else {
                getGeolocation()
            }
        }
    }

    const onClickParkingLot = (event) => {
        const map = mapRef.current.map
        const clicked = parseInt(event.target.getAttribute("parkinglotid"))
        const result = parkinglotlist.filter((parkinglot) => {return parkinglot.id===clicked})[0]
        setClickedParkinglot(result)
        console.log(result)
        const pos = {lat: result.lat, lng: result.lng}
        map.setCenter(pos)
        setParkingLotMarker(pos)
        document.getElementById("parkinglotdetail").style.display = "flex"
        document.getElementById("parkinglot").style.display = "none"
    }
    
    const parkinglots = parkinglotlist.map((val) => (
            <div key={val.id} parkinglotid={val.id} className="parkinglotitem" onClick={onClickParkingLot}>
                <p parkinglotid={val.id}><strong parkinglotid={val.id}>Name:</strong> {val.name}<br />
                <strong parkinglotid={val.id}>Address:</strong> {val.address}<br />
                <strong parkinglotid={val.id}>Car Remaining Space:</strong> {val.car_remaining_space}<br />
                <strong parkinglotid={val.id}>Motorbike Remaining Space:</strong> {val.motorbike_remaining_space}</p>
            </div>
    ))

    const parkingareas = displayParkingArea.map((val) => (
        <div key={val.id} className="parkinglotdetailareaitem">
            <p><strong>Area name:</strong> {val.area}<br />
            <strong>Type:</strong> {val.iscar ? "car":"motorbike"}<br />
            <strong>Remaining Space:</strong> {val.remainingspace}<br />
            </p>
            <img src={val.imagepath?`${getBackendContext()}/${val.imagepath}`:undefined} alt="No img" className="parkinglotimage"/>
        </div>
    ))

    return (
        <div>
            <div className='googlemap'>
                <Map 
                    id='map'
                    disableDefaultUI={true}
                    defaultZoom={13}
                    defaultCenter={ center }
                    onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
                    onTilesLoaded={(map) => {mapRef.current = map; console.log("Ref loaded", mapRef.current); getGeolocation()}}
                >
                    <Marker position={currentMarker}/>
                    <Marker position={parkinglotMarker}/>
                    <DirectionDisplay origin={currentMarker} destination={parkinglotMarker}/>
                </Map>
            </div>
            <div className="parkinglotdiv">
                <div className="parkinglotsearch">
                    <input type="text" name="currentposition" placeholder="current position" className="ParkinglotSearch" onChange={handleChange}/>
                    <button onClick={PositionSearch}>Enter</button>
                </div>
                <div>
                    <div className="parkinglotsearch">
                        <input type="text" name="searchParkinglot" placeholder="Destination for search" onChange={handleChange} className="ParkinglotSearch"/>
                        <button name="Search" onClick={Search}>Search</button>
                    </div>
                    <div className="parkinglotdisplay" id="parkinglotdisplay">
                        <div className="parkinglot" id="parkinglot">
                            {parkinglots}
                        </div>
                        <div className='parkinglotdetail' id="parkinglotdetail">
                            <button type='button' onClick={unClickedParkinglot}>Back</button>
                            <img src={clickedParkinglot ? `${getBackendContext()}/${clickedParkinglot.image_path}` : undefined} alt="No img" className="parkinglotddetailimage" />
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Name: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.name:""}</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Address: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.address:""}</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Day Motorbike Fee: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.dayfeemotorbike:""}/4h</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Night Motorbike Fee: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.nightfeemotorbike:""}/4h</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Car Fee: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.carfee:""}/4h</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Car Remaining Space: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.car_remaining_space:""}</span>
                            </div>
                            <div className='parkinglotdetailinfo'>
                                <span className='parkinglotdetailinfotitle'>Motorbike Remaining Space: </span>
                                <span className='parkinglotdetailinfovalue'>{clickedParkinglot?clickedParkinglot.motorbike_remaining_space:""}</span>
                            </div>
                            {parkingareas}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}


export default CustomGoogleMap
