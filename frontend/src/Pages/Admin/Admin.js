import AdminHeader from "../../Components/AdminHeader";

const AdminPage = () => {

    return(
        <div>
            <AdminHeader />
            <a href="/admin/parkinglot" className="button">Parking Lot</a><br/>
            <a href="/admin/parkingarea/1?ischeckin=1" className="button">Manage Parking Area 1</a>
        </div>
    )
}

export default AdminPage