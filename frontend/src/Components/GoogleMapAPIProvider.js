import { APIProvider } from "@vis.gl/react-google-maps"
import CustomGoogleMap from "./GoogleMap"

const GooglemapAPIProvider = () => {
    return(
        <APIProvider apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
            <CustomGoogleMap/>
        </APIProvider>
    )
}

export default GooglemapAPIProvider