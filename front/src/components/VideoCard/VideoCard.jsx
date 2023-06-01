import styles from './VideoCard.module.css';
import {ReactComponent as Eye} from "../../img/eye.svg";
import {useNavigate} from "react-router-dom";

const VideoCard = ({id, title, preview, owner, views}) => {
    const navigate = useNavigate();
    return <div key={id} className={styles.card} onClick={() => navigate(`/watch/${id}`)}>
        <img className={styles.preview} src={preview} alt={title}/>
        <div className={styles.container}>
            <img className={styles.avatar} src={preview} width={40} height={40}/>
            <div className={styles.container__info}>
                <div className={styles.info}>
                    <h3 className={styles.title}>{title.length > 20 ? title.slice(0, 20) + '...' : title}</h3>
                    <div className={styles.views}>
                        <span>{views}</span><Eye/>
                    </div>
                </div>
                <h3 className={styles.owner}>{owner}</h3>
            </div>
        </div>
    </div>
};


export default VideoCard;
