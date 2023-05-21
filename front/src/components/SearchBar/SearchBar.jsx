import styles from './SearchBar.module.css';
import {ReactComponent as Arrow} from '../../img/arrow.svg';
import {ReactComponent as UserAvatar} from '../../img/user-avatar.svg';
import { useNavigate } from 'react-router-dom';
import {useEffect, useState} from "react";
import axios from "axios";
import getAxiosBody from "../sendData";

const SearchBar = () => {
  const navigate = useNavigate();
  const [isAuth, setIsAuth] = useState(false);


  useEffect(() => {
      if (localStorage.getItem('user') !== null) {
          setIsAuth(true);
          return;
      }
      const body = getAxiosBody('current_user');
          const instance = axios.create({withCredentials: true});
          instance.post('http://127.0.0.1:8000/api/v1/user', body)
              .then((response) => {
                  setIsAuth(true);
                  localStorage.setItem('user', response.data['result'].email);
              })
              .catch(() => {
                  setIsAuth(false);
                  localStorage.removeItem('user');
              })

  });

  return (
    <div className={styles.container}>
      <form action="" method="post">
        <input className={styles.search_input} type="search" name="search" placeholder="Поиск"/>
        <button className={styles.search_btn} type="submit"><Arrow/></button>
      </form>
        {isAuth
      ? <button className={styles.user_profile_icon} type="button" onClick={() => navigate('/profile')}><UserAvatar/></button>
      : <div className={styles.container_btn}>
          <button className={styles.btn} onClick={() => navigate('/login')} type="button">Log In</button>
          <button className={styles.btn} onClick={() => navigate('/register')} type="button">Sign Up</button>
      </div>}
    </div>
  )
};

export default SearchBar;
