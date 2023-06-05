import styles from "./ClaimPopup.module.css";
import {ReactComponent as Cross} from "../../img/cross.svg";
import getAxiosBody from "../sendData";
import axios from "axios";
import {useState} from "react";

const url = process.env.REACT_APP_API_URL;


const ClaimPopup = ({active, setActive, id, type}) => {
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
        const body = getAxiosBody('create_claim', {"claim_schema": {
            "description": claimText, "claim_type": type, "claim_object_id": id}});
        instance.post(`${url}/api/v1/user`, body)
            .then((response) => {
                const data = response.data;
                if ('error' in data) {
                    throw new Error();
                }
                setException('');
                setMsg('Жалоба отправлена');
                setClaimText('');
                setTimeout(() => {
                    setActive(false);
                    setMsg('');
                    setException('');
                }, 1500);
            })
            .catch((err) => {
                setException('Жалоба не отправлена');
                setMsg('');
            });
    }

    const closePopup = () => {
        setActive(false);
        setClaimText('');
        setMsg('');
        setException('');
    }

    return (
        active ?
        (<div className={styles.container} onClick={() => setActive(false)}>
            <div className={styles.popup} onClick={e => e.stopPropagation()}>
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