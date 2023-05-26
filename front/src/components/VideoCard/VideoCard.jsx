import styles from './VideoCard.module.css';
import {Link} from "react-router-dom";

const VideoCard = ({id, title, preview, owner}) => {
    const currentUser = localStorage.getItem('user');

    return <Link to={`/watch/${id}`} style={{ textDecoration: 'none' }}><div key={id} className={styles.card}>
        <img className={styles.preview} src={preview} alt={title}/>
        <div className={styles.container}>
            <img className={styles.avatar} src={preview} width={40} height={40}/>
            <div>
                <h3 className={styles.title}>{title.length > 27 ? title.slice(0, 27) + '...' : title}</h3>
                <h3 className={styles.owner}>{owner}</h3>
            </div>
        </div>
    </div></Link>
};


export default VideoCard;
