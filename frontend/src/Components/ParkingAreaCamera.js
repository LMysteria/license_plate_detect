import { useEffect, useState } from "react";
import { getWebsocketContext } from "../Util/AuthUtil";
import { getAuthHeader, getBackendContext } from "../Util/AuthUtil";
import Cookies from "js-cookie"

const ParkingAreaCamera = (props) => {
    const [imageData, setImageData] = useState(null)
    const [input, setInputs] = useState("")
    const [parkingData, setParkingData] = useState({})
    const [token] = useState(Cookies.get("Host-access_token") || "");
    const [manualExitImg, setManualExitImg] = useState()
    const [log, setLog] = useState([])


    useEffect(() => {
        const ws = new WebSocket(`${getWebsocketContext()}/parkinglot/parkingarea/camera?parkingareaid=${props.parkingareaid}&ischeckin=${props.ischeckin}&camera_num=${props.camera_num}`);

        ws.binaryType = "arraybuffer"

        ws.onmessage = (event) => {
            const wsdata = event.data
            if(typeof wsdata === "string"){
                console.log("wsmessage: ",wsdata)
                const timestamp = new Date().toLocaleTimeString();
                const newlog = `${timestamp} ${wsdata}`
                setLog((prevlog) => [...prevlog, newlog]);
            }
            if(wsdata instanceof ArrayBuffer){
            const blob = new Blob([event.data], {type: "image/jpeg"});
            const imageUrl = URL.createObjectURL(blob);
            setImageData(imageUrl);}
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

    const  handleChange = (event) => {
        const name = event.target.name;
        const value = event.target.value;
        setInputs(values => ({...values, [name]: value}))
    }
    
    const idSearch = () => {
        const userid = parseInt(input.findUserid)
        if(userid){
            fetch(`${getBackendContext()}/admin/parkinglot/parkingarea/parkingdata/last?parkingareaid=${props.parkingareaid}&userid=${userid}`, {
            method: "GET",
            headers: getAuthHeader(token)
        })
            .then((response) => response.json())
            .then((data) => {
                setParkingData(data)
                console.log(data)})
            .catch((err) => console.log(err))
        }
    }

    const licenseSearch = () => {
        const licensePlate = input.findLicenseplate
        if(licensePlate){
            fetch(`${getBackendContext()}/admin/parkinglot/parkingarea/parkingdata/last?parkingareaid=${props.parkingareaid}&licenseplate=${licensePlate}`, {
            method: "GET",
            headers: getAuthHeader(token)
        })
            .then((response) => response.json())
            .then((data) => {
                setParkingData(data)
                console.log(data)})
            .catch((err) => console.log(err))
        }
    }

    const manualexit = () => {
        setManualExitImg(imageData)
        document.getElementById("manualexit").style.display="flex"
        document.getElementById("editbackground").style.display="block"
    }

    const sendManualExit = () => {
        try {
            fetch(manualExitImg)
            .then((response) => response.blob())
            .then((data) => {
                const form = new FormData()
                form.append("parkingdataid", parkingData.id)
                form.append("img",data)
                fetch(`${getBackendContext()}/admin/parkinglot/parkingarea/parkingdata/exit/manual`, {
                    method: "POST",
                    body: form,
                    headers: getAuthHeader(token)
                })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                    cancelManualExit()
                    setParkingData(data)
                })
            })
        } catch (error) {
            console.error(error)
        }
    }

    const cancelManualExit = () => {
        setManualExitImg(null)
        document.getElementById("manualexit").style.display="none"
        document.getElementById("editbackground").style.display="none"
    }

    const displayLogs = log.map((log, index) => (
        <div key={index}>{log}<br/></div>
    ))

    return(
        <div>
            <div className="manageBody">
                <div>
                    <h2>Camera number: {props.camera_num} parkingareaid: {props.parkingareaid} Type:{props.ischeckin?"Check in":"Check out"}</h2>
                    <div className="manageDisplay">
                        <div className="displayContent">
                            <h3>Camera</h3>
                            {imageData && (<img src={imageData} alt="Camera stream" className="imageSize"/>)}
                        </div>
                        <div className="displayContent">
                            <h3>Entry Image</h3>
                            <div className="imageSize">
                                    <img src={parkingData.entry_path ? `${getBackendContext()}/admin/${parkingData.entry_path}` : undefined} alt="No img"/>
                            </div>
                        </div>
                        <div className="displayContent">
                            <h3>Exit Image</h3>
                            <div className="imageSize">
                                <img src={parkingData.exit_path ? `${getBackendContext()}/admin/${parkingData.exit_path}` : undefined} alt="No img"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="inputdiv">
                    <div className="editdiv">
                        <span>Find by User ID: </span>
                        <input type="text" name="findUserid" onChange={handleChange} />
                        <button onClick={idSearch}>Search</button>
                    </div>
                    <div className="editdiv">
                        <span>Find by License Plate: </span>
                        <input type="text" name="findLicenseplate" onChange={handleChange} />
                        <button onClick={licenseSearch}>Search</button>
                    </div>
                </div>
                <div className="parkingDataDisplay">
                    <span><strong>Parking Data:</strong></span>
                    <div className="dataDetail">
                        <span>UserID: {parkingData.userid}</span>
                        <span>License: {parkingData.license}</span>
                        <span>EntryTime: {parkingData.entry_time}</span>
                        <span>Exit Time: {parkingData.exit_time}</span>
                    </div>
                </div>
                <div>
                    <button type="button" onClick={manualexit}>Manual Exit</button>
                </div>
                <div style={{overflowY:"auto"}}>
                    <h2 style={{textAlign:"left"}}>Log:</h2>
                    {displayLogs}
                </div>
            </div>
            <div className="editbackground" id="editbackground">
                <div className="Manageedit" id="manualexit">
                    <h1 className="warning">WARNING: PLEASE CHECK PARKING DATA CAREFULLY BEFORE SUBMIT MANUAL EXIT</h1>
                    <div className="parkingDataDisplay">
                        <span className><strong>Parking Data:</strong></span>
                        <div className="dataDetail">
                            <span>UserID: {parkingData.userid}</span>
                            <span>License: {parkingData.license}</span>
                            <span>EntryTime: {parkingData.entry_time}</span>
                        </div>
                    </div>
                    <div className="manageDisplay">
                        <div className="displayContent">
                            <h3>Entry Image</h3>
                            <div className="imageSize">
                                    <img src={parkingData.entry_path ? `${getBackendContext()}/admin/${parkingData.entry_path}` : undefined} alt="No img"/>
                            </div>
                        </div>
                        <div className="displayContent">
                            <h3>Exit Image</h3>
                            <div className="imageSize">
                                <img src={manualExitImg ? manualExitImg : undefined} alt="No img"/>
                            </div>
                        </div>
                    </div>
                    <div className="Manageeditdiv">
                        <button type="button" onClick={cancelManualExit}>Cancel</button>
                        <button type="button" onClick={sendManualExit}>Confirm</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ParkingAreaCamera