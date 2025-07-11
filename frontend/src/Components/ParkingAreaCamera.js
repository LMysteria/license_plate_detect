import { useEffect, useState } from "react";
import { getWebsocketContext } from "../Util/AuthUtil";

const ParkingAreaCamera = (props) => {
    const [imageData, setImageData] = useState(null)

    useEffect(() => {
        const ws = new WebSocket(`${getWebsocketContext()}/parkinglot/parkingarea/camera?parkingareaid=${props.parkingareaid}&ischeckin=${props.ischeckin}&camera_num=${props.camera_num}`);

        ws.binaryType = "arraybuffer"

        ws.onmessage = (event) => {
            const blob = new Blob([event.data], {type: "image/jpeg"});
            const imageUrl = URL.createObjectURL(blob);
            setImageData(imageUrl);
        };

        ws.onerror = (err) => {
            console.error("Websocket error:", err)
        };

        ws.onclose = (err) => {
            console.warn("Websocket closed", err.code, err.reason)
        }

        return () => {
            console.log("Websocket clean up")
            ws.close()}
    }, [props]);
    
    return(
        <div>
            <h2>Camera number: {props.camera_num} parkingareaid: {props.parkingareaid}</h2>
            {imageData && (<img src={imageData} alt="Camera stream" style={{width: '640px', height:'480px'}} />)}
        </div>
    )
}

export default ParkingAreaCamera