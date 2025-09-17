// src/App.js
import React from "react";
import Navigation from "./Navigation";
import HolographicDots from "./Design/HolographicDots";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import About from "./About";

function App() {
    return (
        <Router>
            <Navigation />
            <Routes>
                <Route path="/" element={<HolographicDots />} />
                <Route path="/about" element={<About />} />
            </Routes>
        </Router>
    );
}

export default App;
