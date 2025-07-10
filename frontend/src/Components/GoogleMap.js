import {APIProvider, Map, Marker} from '@vis.gl/react-google-maps';
import { useRef, useState, useEffect } from 'react';
import ParkingLot from './ParkingLot';
import {fromAddress} from 'react-geocode'
import { getBackendContext } from "../Util/AuthUtil";

const CustomGoogleMap = () => {
    const mapRef = useRef(null);
    const [currentMarker, setCurrentMarkers] = useState()
    const [input, setInputs] = useState("")
    const [parkinglotMarker, setParkingLotMarker] = useState()
    const [parkinglotlist, setParkinglotlist] = useState([])
    const [clickedParkinglot, setClickedParkinglot] = useState(0)
    const [displayParkingArea, setParkingArea] = useState([])

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
        const map = mapRef.current.map;
        fromAddress(input.currentposition)
        .then(({ results }) => {
            const pos = results[0].geometry.location;
            map.setCenter(pos)
            setCurrentMarkers(pos)
        })
        .catch(console.error);
    }  

    const Search = () => {
        getParkinglotlist(input.searchParkinglot)
    }

    const onClickParkingLot = (event) => {
        const map = mapRef.current.map;
        const clicked = parseInt(event.target.getAttribute("parkinglotid"))
        setClickedParkinglot(clicked)
        const result = parkinglotlist.filter((parkinglot) => {return parkinglot.id===clickedParkinglot})[0]
        console.log(result)
        const pos = {lat: result.lat, lng: result.lng}
        map.setCenter(pos)
        setParkingLotMarker(pos)
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

    return (
        <div>
            <APIProvider apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
                <div className='googlemap'>
                    <Map 
                        id='map'
                        disableDefaultUI={true}
                        defaultZoom={13}
                        defaultCenter={ center }
                        onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
                        onTilesLoaded={(map) => {mapRef.current = map; console.log("Ref loaded", mapRef.current)}}
                    >
                        <Marker position={currentMarker}/>
                        <Marker position={parkinglotMarker}/>
                    </Map>
                </div>
                <div className="parkinglotdiv">
                    <div>
                        <input type="text" name="currentposition" placeholder="current position" className="ParkinglotSearch" onChange={handleChange}/>
                        <button onClick={PositionSearch}>Search</button>
                    </div>
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
                </div>
            </APIProvider>
        </div>
    );
}


export default CustomGoogleMap
