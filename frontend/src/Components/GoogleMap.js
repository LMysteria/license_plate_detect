import {APIProvider, Map, Marker} from '@vis.gl/react-google-maps';
import { useRef, useState } from 'react';
import ParkingLot from './ParkingLot';
import {fromAddress, setKey} from 'react-geocode'

const CustomGoogleMap = () => {
    const mapRef = useRef(null);
    const [markers, setMarkers] = useState([])
    const [input, setInputs] = useState("")

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }


    const center = {
    lat: 10.762622,  // Example: Ho Chi Minh City
    lng: 106.660172
    };

    const Search = () => {
        const map = mapRef.current.map;
        fromAddress(input.currentposition)
        .then(({ results }) => {
            const pos = results[0].geometry.location;
            map.setCenter(pos)
            if(markers[0] === null){
                markers.push(pos)
            } else {
                markers[0] = pos;
            }
            setMarkers(markers)
        })
        .catch(console.error);
    }  

    const mapMarkers = markers.map((pos) => (
        <Marker position={pos}/>
    ))

    return (
        <div>
            <div className='googlemap'>
                <APIProvider apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>

                    <Map 
                        id='map'
                        disableDefaultUI={true}
                        defaultZoom={13}
                        defaultCenter={ center }
                        onCameraChanged={(ev) => console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)}
                        onTilesLoaded={(map) => {mapRef.current = map; console.log("Ref loaded", mapRef.current)}}
                    >
                        {mapMarkers}
                    </Map>
                </APIProvider>
            </div>
            <div className="parkinglotdiv">
                <div>
                    <input type="text" name="currentposition" placeholder="current position" className="ParkinglotSearch" onChange={handleChange}/>
                    <button onClick={Search}>Search</button>
                </div>
                <ParkingLot/>
            </div>
        </div>
    );
}


export default CustomGoogleMap