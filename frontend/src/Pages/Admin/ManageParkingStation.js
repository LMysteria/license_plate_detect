import { useParams, useSearchParams } from "react-router-dom"
import AdminHeader from "../../Components/AdminHeader"
import ParkingAreaCamera from "../../Components/ParkingAreaCamera"

const ManageParkingStation = () => {
    const [searchParams] = useSearchParams();

    const params = useParams()
    const ischeckin = searchParams.get("ischeckin")
    

    return(
        <div>
            <AdminHeader />
            <ParkingAreaCamera parkingareaid={params.id} ischeckin={ischeckin !== "0"?true:false} camera_num={0}/>
        </div>
    )
}

export default ManageParkingStation