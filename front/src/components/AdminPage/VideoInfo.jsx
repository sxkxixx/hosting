import styles from "./AdminPage.module.css";
import getAxiosBody from "../sendData";
import axios from "axios";
import {useState} from "react";

const VideoInfo = ({id, video_id, claim_text}) => {
    const [showed, setShowed] = useState(true);

    const setClaimStatus = (event, status) => {
        event.preventDefault();
        const body = getAxiosBody('change_claim_status', {claim_id: id, status: status})
        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/api/v1/admin', body)
            .then(() => {

            });
    };



    return (
        showed ?
        (<div id={id} className={styles.card__video}>
            <div className={styles.info}>
                <div>
                    <p className={styles.text}>Видео<br/></p>
                    <div className={styles.sign}>
                        <a href={`http://127.0.0.1:3000/watch/${video_id}`}>Cсылка на видео</a>
                    </div>
                </div>
                <div>
                    <p className={styles.text}>Причина жалобы:<br/></p>
                    <div className={styles.sign}>
                        <p>{claim_text}</p>
                    </div>
                </div>
            </div>
            <div className={styles.btn__container}>
                <button className={`${styles.btn} ${styles.btn__approve}`} onClick={(e) => setClaimStatus(e, 'approved')} type="submit">Подтвердить</button>
                <button className={`${styles.btn} ${styles.btn__disapprove}`} onClick={(e) => setClaimStatus(e, 'denied')} type="submit">Отклонить</button>
            </div>
        </div>) : null
    )
}

export default VideoInfo