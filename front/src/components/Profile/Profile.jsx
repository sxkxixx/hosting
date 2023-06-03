import styles from './Profile.module.css';
import { ReactComponent as UserAvatar } from '../../img/user-logo.svg';
import {useNavigate} from 'react-router-dom';
import VideoCard from "../VideoCard/VideoCard";
import UploadVideo from "../UploadVideo/UploadVideo";
import {useEffect, useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";

const url = process.env.REACT_APP_API_URL;

const Profile =  () => {
    const navigate = useNavigate();
    const [videos, setVideos] = useState([]);
    const [user, setUser] = useState({});
    const [avatar, setAvatar] = useState('');

    useEffect(() => {
        const body = getAxiosBody('profile');
        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/user`, body)
            .then((response) => {
                if (response.status === 200) {
                    return response.data
                }
                throw new Error();
            })
            .then((data) => {
                setVideos(data['result']['videos'])
                setUser({'username': data['result'].username, 'email': data['result'].email});
                setAvatar(data['result'].avatar);
                document.title = data['result'].email;
            })
            .catch((err) => {
                navigate('/login');
            })
    }, []);

    const Logout = async () => {
        navigate('/');
        const body = getAxiosBody('logout');
        const instance = axios.create({withCredentials: true});
        await instance.post(`${url}/api/v1/user`, body);
        localStorage.clear();
    };

    const chooseAvatar = () => {
        document.getElementById('avatarInput').click();
    }

    const handleAvatarInput = (event) => {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('avatar', file);
        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/upload_avatar`, formData)
            .then((response) => {
                const avatar = response.data['avatar'];
                setAvatar(avatar);
            })
            .catch((error) => {
                console.log(error);
            });
    };

    return (
        <div className={styles.main_container_profile}>
            <div className={styles.container_left}>
                <div className={styles.user_info}>
                    <div onClick={chooseAvatar}>
                        <button className={styles.user_avatar} type="button">
                            {avatar ? <img className={styles.user_avatar} src={avatar}/> : <UserAvatar/>}
                        </button>
                        <input type="file" id="avatarInput" accept="image/*" hidden onChange={handleAvatarInput}></input>
                    </div>
                    <div className={styles.user_info_profile}>
                        <p className={styles.user_name}>Username: {user.username}</p>
                        <p className={styles.user_email}>Email: {user.email}</p>
                    </div>
                </div>
                <h3 className=''>Мои видео:</h3>
                <div className={styles.videos_container}>
                    { videos.map((video) => <VideoCard id={video.id} title={video.title} preview={video.preview} owner={user.email} isUsersPage={true}/>) }
                </div>
            </div>

            <div className={styles.container_right}>
                <div className={styles.button_container}>
                    <button className={`${styles.back_to_search} ${styles.btn}`} type='button'
                        onClick={() => navigate('/', {replace: false})}>Вернуться к поиску</button>
                    <button className={`${styles.log_out_in} ${styles.btn}`} onClick={Logout} type='button'>Выйти</button>
                </div>
                <h3>Загрузить видео:</h3>
                <UploadVideo/>
            </div>
        </div>
    )
}

export default Profile;
