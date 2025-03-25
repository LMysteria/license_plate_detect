import React, { useState } from "react";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Login from "./Pages/Login";
import DetectLicense from "./Pages/DetectLicense";
import Home from "./Pages/Home";
import SignUp from "./Pages/Signup";

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/detectedlicense" element={<DetectLicense />} />
      </Routes>
    </Router>
  )
}


export default App;
