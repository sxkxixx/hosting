import styles from './VideoCard.module.css';

const VideoCard = ({id, title, preview, owner}) => {
    return <div key={id} className={styles.card}>
        <img className={styles.preview} src={preview} alt={title}/>
        <h3 className={styles.title}>{title}</h3>
        <h3 className={styles.onwer}>{owner}</h3>
    </div>
};


export default VideoCard;
