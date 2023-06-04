import styles from './Login.module.css';
import React, {useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";
import {Link, useNavigate} from "react-router-dom";
import {ReactComponent as Play} from "../../img/play.svg";

const url = process.env.REACT_APP_API_URL;

const Login = () => {
  document.title = 'Log In'

  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleEmailChange = event => {
      setEmail(event.target.value);
      setError('');
  }
  const handlePasswordChange = event => {
      setPassword(event.target.value);
      setError('');
  }

  const handleSubmit = event => {
    event.preventDefault();
    if (!(email && password)){
        setError('Заполните поля!')
        return;
    }
    const data = getAxiosBody('login',
        {'user': {'email': email, 'password': password }})
    const instance = axios.create({withCredentials: true})
    instance.post(`${url}/api/v1/user`, data)
        .then(response => {
            if ('error' in response.data){
                throw new Error();
            }
            setSuccess('Вы успешно вошли!');
            setTimeout(() => navigate('/'), 1500);
            localStorage.removeItem('user');
            localStorage.setItem('user', email);
        })
        .catch(error => {
          setError('Проверьте логин или пароль.');
        })
  };

  return (
      <div className={styles.container}>
          <div onClick={() => navigate('/')} style={{cursor: "pointer"}}><Play/></div>
          <form className={styles.form} onSubmit={handleSubmit}>
              <h1 className={styles.title}>Log In</h1>
              {success && <div style={{ color: 'green' }}>{success}</div>}
              {error && <div style={{ color: 'red' }}>{error}</div>}
              <label className={styles.label}>
                  Email:
                  <input className={styles.input} type="text" value={email} onChange={handleEmailChange} />
              </label><br/>
              <label className={styles.label}>
                  Password:
                  <input className={styles.input} type={"password"} value={password} onChange={handlePasswordChange}/>
              </label><br/>
              <button className={styles.btn} type="submit">Submit</button>
              <p>Нет аккаунта? <Link to={'/register'}>Зарегистрируйтесь</Link></p>
    </form>
      </div>

  );
};

export default Login