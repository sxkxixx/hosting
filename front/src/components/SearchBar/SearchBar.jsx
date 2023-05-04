import './SearchBar.css';
import {ReactComponent as Arrow} from '../../img/arrow.svg';
import {ReactComponent as UserAvatar} from '../../img/user-avatar.svg';
import { useNavigate } from 'react-router-dom';

export const SearchBar = () => {
  const navigate = useNavigate();

  return (
    <div className='container'>
      <form action="" method="post">
        <input className="search-input" type="search" name="search" placeholder="Поиск"/>
        <button className="search-btn" type="submit"><Arrow/></button>
      </form>
      <button className='user-profile-icon' type="button" onClick={() => navigate('authProfilePage', { replace: false })}><UserAvatar/></button>
      {/* <button className='user-profile-icon' type="button" onClick={() => navigate('unauthProfilePage', { replace: false })}><UserAvatar/></button> */}
    </div>
  )
};
