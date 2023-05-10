import styles from './VideoCard.module.css';

const VideoCard = ({id, title, preview}) => {
    return <div key={id} className={styles.card}>
        <img className={styles.preview} src={preview} alt={title}/>
        <h3 className={styles.title}>{title}</h3>
    </div>
};


export default VideoCard;
