import styles from './SearchBar.module.css';
import {ReactComponent as Arrow} from '../../img/arrow.svg';
import {ReactComponent as UserAvatar} from '../../img/user-avatar.svg';
import { useNavigate } from 'react-router-dom';

const SearchBar = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.container}>
      <form action="" method="post">
        <input className={styles.search_input} type="search" name="search" placeholder="Поиск"/>
        <button className={styles.search_btn} type="submit"><Arrow/></button>
      </form>
      <button className={styles.user_profile_icon} type="button" onClick={() => navigate('/profile', { replace: false })}><UserAvatar/></button>
    </div>
  )
};

export default SearchBar;
