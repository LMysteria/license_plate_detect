import { useParams } from "react-router-dom"
import AdminHeader from "../../Components/AdminHeader"
import ParkingAreaCamera from "../../Components/ParkingAreaCamera"

const ManageParkingStation = () => {
    const params = useParams()

    return(
        <div>
            <AdminHeader />
            <ParkingAreaCamera parkingareaid={params.id} ischeckin={true} camera_num={0}/>
        </div>
    )
}

export default ManageParkingStation