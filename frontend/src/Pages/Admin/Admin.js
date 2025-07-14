import AdminHeader from "../../Components/AdminHeader";

const AdminPage = () => {

    return(
        <div>
            <AdminHeader />
            <a href="/admin/parkinglot">Parking Lot</a><br/>
            <a href="/admin/parkingarea/1">Manage Parking Area 1</a>
        </div>
    )
}

export default AdminPage