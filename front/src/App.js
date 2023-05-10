import './App.css'
import { MainPage } from './components/MainPage/MainPage';
import OpenVideo from './components/OpenVideo/OpenVideo';
import { Profile } from './components/ProfilePage/Profile';
import {Route, Routes} from 'react-router-dom'

const App = () => {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage/>}></Route>
        <Route path="/profile" element={<Profile/>}></Route>
        <Route path="/watch/:id" element={<OpenVideo/>}></Route>
      </Routes>
    </div>
  );
}

export default App;
