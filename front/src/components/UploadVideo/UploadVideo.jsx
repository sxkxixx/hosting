import styles from './UploadVideo.module.css';


const UploadVideo = () => {
    return <form className={styles.upload_video_form} method="post">
        <textarea className={`${styles.upload_textarea} ${styles.upload_title_textarea}`} placeholder="Введите название"/>
        <textarea className={`${styles.upload_textarea} ${styles.upload_description_textarea}`} placeholder="Введите описание"/>
        <label className={styles.input_file}>
            <input type="file" name="file[]" multiple accept="image/*"></input>
            <span>Загрузить превью</span>
        </label>
        <label className={styles.input_file}>
            <input type="file" name="file[]" multiple accept="video/*"></input>
            <span>Загрузить видео</span>
        </label>
        <div className={styles.input_file_list}></div>
    </form>;
};

export default UploadVideo;