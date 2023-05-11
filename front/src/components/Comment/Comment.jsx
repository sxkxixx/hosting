import styles from './Comment.module.css';

const Comment = ({id, owner, text}) => {
    return (
        <div key={id} className={styles.comment}>
            <span className={styles.owner}>{owner}</span>
            <p className={styles.text}>{text}</p>
        </div>
    )
};

export default Comment