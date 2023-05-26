import styles from './AdminPage.module.css';
import CommentInfo from "./CommentInfo";
import VideoInfo from "./VideoInfo";
import {useEffect, useState} from "react";
import axios from "axios";
import getAxiosBody from "../sendData";
import {useNavigate} from "react-router-dom";
import {ReactComponent as Logo} from "../../img/play.svg";

const AdminPage = () => {
    const [commentClaims, setCommentClaims] = useState([]);
    const [videoClaims, setVideoClaims] = useState([]);
    const navigate = useNavigate();
    const [isCommentClaims, setIsCommentClaims] = useState(true);

    useEffect(() => {
        const body = getAxiosBody('admin_claims');
        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/api/v1/admin', body)
            .then(response => {
                const data = response.data;
                if ('error' in data){
                    throw new Error();
                }
                setCommentClaims(data.result.comment_claims);
                setVideoClaims(data.result.video_claims)
            })
            .catch(err => {
                navigate('/');
            })
    }, [])

    const commentCards = commentClaims.map((claim) => (<CommentInfo id={claim.id} comment={claim.comment} claim_text={claim.claim}/>))
    const videoCards = videoClaims.map((claim) => (<VideoInfo id={claim.id} claim_text={claim.claim} video_id={claim.video_id}/>))

    return (
        <div className={styles.page}>
            <div className={styles.logo} onClick={() => navigate('/')}>
                <Logo/>
            </div>
            <div className={styles.header}>
                <p className={styles.title}>На странице администратора вы можете просматривать жалобы пользователей на видео или комментарии и реагировать на них. Данная возможность есть только у пользователей с разрешением.</p>
            </div>
            <div className={styles.view_btns}>
                <button onClick={() => setIsCommentClaims(true)} className={styles.view_btn}>Комментарии</button>
                <button onClick={() => setIsCommentClaims(false)} className={styles.view_btn}>Видео</button>
            </div>
            <div className={styles.main}>
                <div className={styles.cards}>
                    {isCommentClaims ? commentCards : videoCards}
                </div>
            </div>
        </div>
    )
};

export default AdminPage
