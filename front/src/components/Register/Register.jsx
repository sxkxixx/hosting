import styles from './Register.module.css';
import React, {useState} from 'react';
import getAxiosBody from "../sendData";
import axios from "axios";

const Register = () => {
    document.title = 'Sign Up';
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordR, setPasswordR] = useState('');

    const [emailError, setEmailError] = useState('');
    const [usernameError, setUsernameError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const [passwordRError, setPasswordRError] = useState('');

    const validateEmail = email => {
        const emailRegex = /^\S+@\S+\.\S+$/;
        if (!email) {
            setEmailError('Email is required');
        } else if (!emailRegex.test(email)) {
            setEmailError('Please enter a valid email');
        } else {
            setEmailError('');
        }
    };

    const validateUsername = username => {
        if (!username) {
            setUsernameError('Username is required');
        } else if (username.length < 6) {
            setUsernameError('Username must be at least 6 characters long');
        } else {
            setUsernameError('');
        }
    };

    const validatePassword = password => {
        if (!password) {
            setPasswordError('Password is required');
        } else if (password.length < 6) {
            setPasswordError('Password must be at least 6 characters long');
        }
        else {
            setPasswordError('');
        }
    };

    const validatePasswordR = passwordR => {
        if (passwordR !== password) {
            setPasswordRError('Passwords must be equals!');
        }
    };

    const handleSubmit = async event => {
        event.preventDefault();
        validateEmail(email);
        validateUsername(username);
        validatePassword(password);
        validatePasswordR(passwordR);
        if (emailError || usernameError || passwordError || passwordRError) {
          return;
        }
        const data = getAxiosBody('register',
            {'user': {'email': email,
                    'username':username,
                    'password':password,
                    'password_repeat':passwordR
                  }
            }
            )
        axios.post('http://127.0.0.1:8000/api/v1/user', data)
            .then((response) => {
              console.log(response.data)
            })
            .catch((error) => {
              console.log(error)
            })
    };

    const handleEmailChange = event => setEmail(event.target.value);
    const handleUsernameChange = event => setUsername(event.target.value);
    const handlePasswordChange = event => setPassword(event.target.value);
    const handlePasswordRChange = event => setPasswordR(event.target.value);


  return (
    <form onSubmit={handleSubmit}>
      <label>
        Email:
        <input type="text" value={email} onChange={handleEmailChange} />
        {emailError && <div style={{ color: 'red' }}>{emailError}</div>}
      </label><br/>
      <label>
        Username:
        <input type="text" value={username} onChange={handleUsernameChange} />
        {usernameError && <div style={{ color: 'red' }}>{usernameError}</div>}
      </label><br/>
      <label>
        Password:
        <input type="password" value={password} onChange={handlePasswordChange} />
        {passwordError && <div style={{ color: 'red' }}>{passwordError}</div>}
      </label><br/>
      <label>
        Repeat your password:
        <input type="password" value={passwordR} onChange={handlePasswordRChange} />
        {passwordRError && <div style={{ color: 'red' }}>{passwordRError}</div>}
      </label><br/>
      <button type="submit">Submit</button>
    </form>
  );
};

export default Register