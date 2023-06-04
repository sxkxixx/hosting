import styles from './Register.module.css';
import React, {useState} from 'react';
import getAxiosBody from "../sendData";
import axios from "axios";
import {Link, useNavigate} from "react-router-dom";
import {ReactComponent as Play} from "../../img/play.svg";

const url = process.env.REACT_APP_API_URL;

const Register = () => {
    document.title = 'Sign Up';
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordR, setPasswordR] = useState('');

    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const validateEmail = email => {
        const emailRegex = /^\S+@\S+\.\S+$/;
        if (!emailRegex.test(email)) {
            setError('Please enter a valid email');
            return false;
        }
        setError('');
        return true;
    };

    const handleSubmit = event => {
        event.preventDefault();
        if (!(email && username && passwordR && password)) {
            setError('Заполните поля!');
            return;
        }
        if (!validateEmail(email))
            return;
        if (password !== passwordR){
            setError('Пароли не совпадают');
            return;
        }
        const data = getAxiosBody('register',
            {'user': {'email': email,
                    'username':username,
                    'password':password,
                    'password_repeat':passwordR
                  }})
        axios.post(`${url}/api/v1/user`, data)
            .then((response) => {
                if ('error' in response.data) {
                    const code = response.data.error.code;
                    if (code === -32001){
                        setError('Пользователь с такими данными уже существует');
                    }
                    else {
                        setError('Введите корректные данные');
                    }
                }
                else {
                    setSuccess('Пользователь успешно создан');
                    setTimeout(() => navigate('/'), 1500);
                }
            });
    };

    const handleEmailChange = event => {
        setEmail(event.target.value);
        setError('');
    }
    const handleUsernameChange = event => {
        setUsername(event.target.value);
        setError('');
    }
    const handlePasswordChange = event => {
        setPassword(event.target.value);
        setError('');
    }
    const handlePasswordRChange = event => {
        setPasswordR(event.target.value);
        setError('');
    }

  return (
      <div className={styles.container}>
          <div onClick={() => navigate('/')} style={{cursor: "pointer"}}><Play/></div>
          <form className={styles.form} onSubmit={handleSubmit}>
              <h1 className={styles.title}>Sign Up</h1>
              {success && <div style={{ color: 'green' }}>{success}</div>}
              {error && <div style={{ color: 'red' }}>{error}</div>}
              <label className={styles.label}>
                  Email:
                  <input className={styles.input} type="text" value={email} onChange={handleEmailChange} />
              </label><br/>
              <label className={styles.label}>
                  Username:
                  <input className={styles.input} type="text" value={username} onChange={handleUsernameChange} />
              </label><br/>
              <label className={styles.label}>
                  Password:
                  <input className={styles.input} type="password" value={password} onChange={handlePasswordChange} />
              </label><br/>
              <label className={styles.label}>
                  Repeat your password:
                  <input className={styles.input} type="password" value={passwordR} onChange={handlePasswordRChange} />
              </label><br/>
              <button className={styles.btn} type="submit">Submit</button>
              <p>Уже есть аккаунт? <Link to={'/login'}>Войдите</Link></p>
          </form>
      </div>
  );
};

export default Register