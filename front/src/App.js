import './App.css'
import { MainPage } from './components/MainPage/MainPage';
import OpenVideo from './components/OpenVideo/OpenVideo';
import Profile from './components/Profile/Profile';
import {Route, Routes} from 'react-router-dom'
import Register from "./components/Register/Register";
import Login from "./components/Login/Login";
import ClaimPopup from "./components/ClaimPopup/ClaimPopup";
import AdminLogin from "./components/Login/AdminLogin";
import AdminClaimsPage from "./components/AdminPage/AdminClaimsPage";
import UserPage from "./components/UserPage/UserPage";
import AdminMain from "./components/AdminPage/AdminMain";

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage/>}></Route>
        <Route path="/profile" element={<Profile/>}></Route>
        <Route path="/watch/:id" element={<OpenVideo/>}></Route>
        <Route path="/register" element={<Register/>}></Route>
        <Route path="/login" element={<Login/>}></Route>
        <Route path="/popup" element={<ClaimPopup/>}></Route>
        <Route path="/admin/login" element={<AdminLogin/>}></Route>
        <Route path="/admin/claims" element={<AdminClaimsPage/>}></Route>
        <Route path="/user/:id" element={<UserPage/>}></Route>
        <Route path="/admin/main" element={<AdminMain/>}/>
      </Routes>
    </div>
  );
}

export default App;
