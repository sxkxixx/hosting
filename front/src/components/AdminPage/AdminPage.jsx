import styles from './AdminPage.module.css';
import CommentInfo from "./CommentInfo";
import VideoInfo from "./VideoInfo";
import {useEffect, useState} from "react";
import axios from "axios";
import getAxiosBody from "../sendData";
import {useNavigate} from "react-router-dom";


const AdminPage = () => {
    const [commentClaims, setCommentClaims] = useState([]);
    const [videoClaims, setVideoClaims] = useState([]);
    const navigate = useNavigate();


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

    return (
        <div className={styles.page}>
            <div className={styles.header}>
                <p className={styles.title}>На странице администратора вы можете просматривать жалобы пользователей на видео или комментарии и реагировать на них. Данная возможность есть только у пользователей с разрешением.</p>
            </div>
            <div className={styles.main}>
                <div className={styles.cards}>
                    { commentClaims.map((claim) => (
                        <CommentInfo id={claim.id} comment={claim.comment} claim_text={claim.claim}/>
                    ))}
                    { videoClaims.map((claim) => (
                        <VideoInfo id={claim.id} claim_text={claim.claim} video_id={claim.video_id}/>
                    ))}
                </div>
            </div>
        </div>
    )
};

export default AdminPage
