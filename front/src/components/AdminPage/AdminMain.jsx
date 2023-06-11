import styles from './AdminMain.module.css';
import {useEffect, useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import {ReactComponent as User} from "../../img/user-logo.svg";
import SearchBar from "../SearchBar/SearchBar";

const url = process.env.REACT_APP_API_URL;

const AdminMain = () => {
    const [videos, setVideos] = useState([]);
    const [users, setUsers] = useState([]);
    const [filter, setFilter] = useState('videos');

    const navigate = useNavigate();

    useEffect(() => {
        onPageLoad('get_videos', setVideos);
    }, [])

    useEffect(() => {
        onPageLoad('get_users', setUsers);
    }, [])

    const onPageLoad = (method, setter) => {
        const body = getAxiosBody(method);
        axios.post(`${url}/api/v1/admin`, body, {withCredentials: true})
            .then(response => {
                const data = response.data;
                if ('error' in data){
                    navigate('/');
                } else {
                    setter(data.result);
                }
            })
    }

    const videoCard = ({id, preview, title, owner}) => {
        return <div id={id} className={styles.card__video} onClick={() => navigate(`/watch/${id}`)}>
            <img src={preview} alt="" width={300} height={200}/>
            <div className={styles.info}>
                <div>
                    <p className={styles.card__text}>{title}</p>
                    <p>{owner}</p>
                </div>
                <div onClick={(event) => deleteVideo(event, id)}>
                    <img src={require('../../img/delete.png')} width={20} height={20} alt=''/>
                </div>
            </div>
        </div>
    };

    const deleteVideo = (event, id) => {
        event.stopPropagation();
        const body = getAxiosBody('delete_video', {video_id : id});
        axios.post(`${url}/api/v1/admin`, body, {withCredentials: true})
            .then((response) => {
                const data = response.data;
                if ('error' in data) {
                    if (data.error.code === -32003){
                        navigate('/');
                        return;
                    }
                }
                if (data.result.status === 'deleted'){
                    window.location.reload();
                }
            })
    }

    const deleteUser = (event, id) => {
        event.stopPropagation();
        const body = getAxiosBody('delete_user', {user_id : id});
        axios.post(`${url}/api/v1/admin`, body, {withCredentials: true})
            .then((response) => {
                const data = response.data;
                if ('error' in data) {
                    if (data.error.code === -32003){
                        navigate('/');
                        return;
                    }
                }
                if (data.result.status === 'deleted'){
                    window.location.reload();
                }
            })
    }

    const userCard = ({id, avatar, email}) => {
        return <div id={id} className={styles.card__user} onClick={() => navigate(`/user/${id}`)}>
            <div>
                {avatar ? <img src={avatar} className={styles.avatar} alt=""/> : <User/>}
            </div>
            <div>
                <p>{email}</p>
            </div>
            <div onClick={(event) => deleteUser(event, id)}><img src={require('../../img/delete.png')} width={20} height={20} alt=''/></div>
        </div>
    };

    return (
        <div>
            <SearchBar/>
            <div className={styles.header}>
                <p>На этой странице админ может удалять аккаунты пользователей или их видео.</p>
            </div>
            <div className={styles.main}>
                <div className={styles.buttons}>
                    <button className={`${styles.button} ${styles.active}`} id='videos'
                    onClick={() => {
                        document.getElementById('videos').classList.add(styles.active);
                        document.getElementById('users').classList.remove(styles.active);
                        setFilter('videos');
                    }}
                    >Видео</button>
                    <button className={styles.button} id='users'
                    onClick={() => {
                        document.getElementById('users').classList.add(styles.active);
                        document.getElementById('videos').classList.remove(styles.active);
                        setFilter('users');
                    }}
                    >Пользователи</button>
                </div>
                <div className={styles.objects__container}>
                    {
                        filter === 'videos'
                        ? videos.map(video => videoCard(video))
                        : users.map(user => userCard(user))
                    }
                </div>

            </div>
        </div>
    )
};

export default AdminMain
