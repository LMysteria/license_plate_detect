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
import ManageParkingStation from './Pages/Admin/ManageParkingStation';
import {setDefaults} from 'react-geocode'


function App() {
  setDefaults({
    key: process.env.REACT_APP_GOOGLE_GEOCODE_API_KEY, // Your API key here.
    language: "en", // Default language for responses.
    region: "es", // Default region for responses.
  });

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
        <Route path='/admin/parkingarea/:id' element={<ManageParkingStation />} />
        <Route path="*" element={<Navigate to="/"/>} />
      </Routes>
    </Router>
  )
}


export default App;
