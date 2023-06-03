import styles from './Login.module.css';
import React, {useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const url = process.env.REACT_APP_API_URL;
const AdminLogin = () => {
  document.title = 'Admin LogIn'
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const validateEmail = email => {
    const emailRegex = /^\S+@\S+\.\S+$/;
    if (!email) {
      setEmailError('Email is required!')
    }
    else if (!emailRegex.test(email)){
      setEmailError('Enter the valid Email')
    }
    else {
      setEmailError('');
    }
  };

  const validatePassword = password => {
    if (!password)
      setPasswordError('Password is required!')
    else if (password.length < 6)
      setPasswordError('Password must be at least 6 characters long')
    else setPasswordError('');
  };

  const handleEmailChange = event => setEmail(event.target.value);
  const handlePasswordChange = event => setPassword(event.target.value);

  const handleSubmit = async event => {
    event.preventDefault();
    validateEmail(email);
    validatePassword(password);
    if (emailError || passwordError){
      return;
    }
    const data = getAxiosBody('admin_login',
        {'admin_schema': {'email': email, 'password': password }})
    const instance = axios.create({withCredentials: true})
    instance.post(`${url}/api/v1/admin`, data)
        .then(response => {
          navigate('/');
          localStorage.removeItem('admin');
          localStorage.setItem('admin', email);
        })
        .catch(error => {
          console.log(error);
        })
  };

  return (
      <div className={styles.container}>
        <form className={styles.form} onSubmit={handleSubmit}>
      <h1 className={styles.title}>Log In</h1>
      <label className={styles.label}>
        Email:
        <input className={styles.input} type="text" value={email} onChange={handleEmailChange} />
        {emailError && <div style={{ color: 'red' }}>{emailError}</div>}
      </label><br/>
      <label className={styles.label}>
        Password:
        <input className={styles.input} type="password" value={password} onChange={handlePasswordChange} />
        {passwordError && <div style={{ color: 'red' }}>{passwordError}</div>}
      </label><br/>
      <button className={styles.btn} type="submit">Submit</button>
    </form>
      </div>

  );
};

export default AdminLogin