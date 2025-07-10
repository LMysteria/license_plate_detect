import { useMap, useMapsLibrary } from "@vis.gl/react-google-maps";
import { useMemo, useEffect } from "react";

const DirectionDisplay = (props) => {
    const routeServiceLib = useMapsLibrary('routes')
    const map = useMap()
    const directionService = useMemo(() => routeServiceLib && new routeServiceLib.DirectionsService(), [routeServiceLib]);
    const directionRenderer = useMemo(() => routeServiceLib && new routeServiceLib.DirectionsRenderer({map, suppressMarkers:true}), [routeServiceLib, map]);

    useEffect(() => {
        if(!directionService) return;
        if(!props.origin) return;
        if(!props.destination) return;
        if(!directionRenderer) return;
        const request = {
            origin: props.origin,
            destination: props.destination,
            travelMode: routeServiceLib.TravelMode.DRIVING
        }
        directionService.route(request, (response, status) => {
            if(status === routeServiceLib.DirectionsStatus.OK){
                console.log(response)
                directionRenderer.setDirections(response)    
            }
        })
    }, [directionService, props, directionRenderer, routeServiceLib])

    return null;
}

export default DirectionDisplay