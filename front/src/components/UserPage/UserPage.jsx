import {useNavigate, useParams} from "react-router-dom";
import SearchBar from "../SearchBar/SearchBar";
import {useEffect, useState} from "react";
import getAxiosBody from "../sendData";
import styles from './UserPage.module.css';
import axios from "axios";
import VideoCard from "../VideoCard/VideoCard";
import {ReactComponent as UserAvatar} from "../../img/user-logo.svg";

const url = process.env.REACT_APP_API_URL;

const UserPage = () => {
    const {id} = useParams();
    const [userInfo, setUserInfo] = useState({});
    const [videosInfo, setVideosInfo] = useState([]);
    const [subscribed, setSubscribed] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const body = getAxiosBody('get_user_page', {user_id: id})
        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/user`, body)
            .then((response) => {
                if ('error' in response.data)
                    throw new Error();
                const data = response.data.result;
                setUserInfo(data.user);
                setVideosInfo(data.videos);
                setSubscribed(data.subscribed);
                document.title = userInfo.username;
            })
            .catch((error) => {
                navigate('/');
            })
    }, []);

    const setSubscribe = (event) => {
        event.preventDefault();
        const body = getAxiosBody('set_subscribe', {user_id: id});
        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/user`, body)
            .then((response) => {
                if ('error' in response.data)
                    throw new Error();
                const result = response.data.result;
                if (result.status === 'subscribed'){
                    setSubscribed(true);
                }
            })
            .catch((err) => {
                setSubscribed(false);
            })
    };

    const deleteSubscribe = (event) => {
        event.preventDefault();
        const body = getAxiosBody('delete_subscribe', {user_id: id});
        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/user`, body)
            .then((response) => {
                if ('error' in response.data)
                    throw new Error();
                const data = response.data.result;
                if (data.status === 'deleted'){
                    setSubscribed(false);
                }
            })
            .catch((err) => {
                setSubscribed(true);
            })
    };

    return (
        <div>
            <SearchBar/>
            <div className={styles.header}>
                {userInfo.avatar ? <img src={userInfo.avatar} className={styles.avatar}/> : <div className={styles.avatar}><UserAvatar/></div>}
                <div className={styles.info}>
                    <p className={styles.info__text}>{userInfo.email}</p>
                    <p className={styles.info__text}>{userInfo.username}</p>
                </div>
                {subscribed
                    ? <button className={styles.btn__subscribe} onClick={deleteSubscribe}>Отписаться</button>
                    : <button className={styles.btn__subscribe} onClick={setSubscribe}>Подписаться</button>}
            </div>
            <div className={styles.main}>
                <p className={styles.info__text} style={{marginBottom: "20px", marginLeft: "100px"}}>Видео пользователя</p>
                <div className={styles.main__videos}>
                    {videosInfo.slice().map((video) => <VideoCard id={video.id} owner={userInfo.email} preview={video.preview_url} title={video.title} isUsersPage={true}/>)}
                </div>
            </div>

        </div>
    )
};

export default UserPage;
