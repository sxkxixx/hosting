import styles from "./ClaimPopup.module.css";
import {ReactComponent as Cross} from "../../img/cross.svg";
import getAxiosBody from "../sendData";
import axios from "axios";
import {useState} from "react";


const ClaimPopup = ({id, type}) => {
    const [isOpened, setIsOpened] = useState(true);
    const [claimText, setClaimText] = useState('');
    const [exception, setException] = useState('');
    const [msg, setMsg] = useState('');

    const handleClaimText = event => setClaimText(event.target.value);

    const sendClaim = (event) => {
        event.preventDefault();
        if (!claimText) {
            setException('Заполните поле описания')
            return;
        }
        const instance = axios.create({withCredentials: true});
        const body = getAxiosBody('create_claim', {"claim": {
            "description": claimText, "claim_type": type, "claim_object_id": id}});
        instance.post('http://127.0.0.1:8000/api/v1/user', body)
            .then((response) => {
                const data = response.data;
                if ('error' in data) {
                    throw new Error();
                }
                setMsg('Жалоба отправлена');
            })
            .catch((err) => {

                setException('Жалоба не отправлена')
            })

    }

    const closePopup = () => {
        setIsOpened(false);
        setClaimText('');
    }

    return (
        isOpened ?
        (<div className={styles.container}>
            <div className={styles.popup}>
                <div className={styles.nav}>
                    <h1 className={styles.title}>Отправить жалобу</h1>
                    <p className={styles.cross} onClick={closePopup}><Cross/></p>
                </div>
                <form className={styles.inner} onSubmit={sendClaim}>
                    <p className={styles.text}>Опишите причину жалобы</p>
                    <textarea className={styles.area} onChange={handleClaimText}/>
                    {exception && <div className={styles.error}>{exception}</div>}
                    {msg && <div className={styles.error}>{msg}</div>}
                    <button className={styles.btn} type="submit">Отправить жалобу</button>
                </form>
            </div>
        </div>) : null
    )
}

export default ClaimPopup