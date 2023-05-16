import './App.css'
import { MainPage } from './components/MainPage/MainPage';
import OpenVideo from './components/OpenVideo/OpenVideo';
import Profile from './components/Profile/Profile';
import {Route, Routes} from 'react-router-dom'
import Register from "./components/Register/Register";
import Login from "./components/Login/Login";

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage/>}></Route>
        <Route path="/profile" element={<Profile/>}></Route>
        <Route path="/watch/:id" element={<OpenVideo/>}></Route>
          <Route path="/register" element={<Register/>}></Route>
          <Route path="/login" element={<Login/>}></Route>
      </Routes>
    </div>
  );
}

export default App;
