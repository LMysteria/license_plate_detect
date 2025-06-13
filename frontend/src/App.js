import {BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import Login from "./Pages/Login";
import DetectLicense from "./Pages/DetectLicense";
import Home from "./Pages/Home";
import SignUp from "./Pages/Signup";
import UserPage from "./Pages/User/User";
import "./App.css";
import AdminPage from './Pages/Admin/Admin';
import ParkingLotAdmin from './Pages/Admin/ParkingLotAdmin';
import FeedBackPage from './Pages/User/FeedBack';
import InsertMoneyPage from './Pages/User/InsertMoney';
import TransactionPage from './Pages/User/Transaction';

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/detectedlicense" element={<DetectLicense />} />
        <Route path="/userdetail" element={<UserPage />} />
        <Route path="/feedback" element={<FeedBackPage />} />
        <Route path="/insertmoney" element={<InsertMoneyPage />} />
        <Route path="/transaction" element={<TransactionPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path='/admin/parkinglot' element={<ParkingLotAdmin />} />
        <Route path="*" element={<Navigate to="/"/>} />
      </Routes>
    </Router>
  )
}


export default App;
