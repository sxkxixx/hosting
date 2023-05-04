import './App.css'
import { MainPage } from './components/MainPage/MainPage';
import { OpenVideo } from './components/OpenVideo/OpenVideo';
import { AuthorizedProfilePage } from './components/ProfilePage/AuthorizedProfilePage';
import { UnauthorizedProfilePage } from './components/ProfilePage/UnauthorizedProfilePage';
import {Route, Routes} from 'react-router-dom'

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<MainPage/>}></Route>
        <Route path="authProfilePage" element={<AuthorizedProfilePage/>}></Route>
        <Route path="unauthProfilePage" element={<UnauthorizedProfilePage/>}></Route>
        <Route path="openVideo" element={<OpenVideo/>}></Route>
      </Routes>
    </div>
  );
}

export default App;
