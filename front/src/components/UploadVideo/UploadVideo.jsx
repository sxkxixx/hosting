import styles from './UploadVideo.module.css';
import {useState} from "react";
import axios from "axios";

const url = process.env.REACT_APP_API_URL;

const UploadVideo = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [preview, setPreview] = useState(null);
    const [video, setVideo] = useState(null);
    const [buttonText, setButtonText] = useState('Загрузить');

    const handleTitleChange = event => setTitle(event.target.value);
    const handleDescriptionChange = event => setDescription(event.target.value);

    const handlePreviewChange = event => {
        const preview = event.target.files[0];
        setPreview(preview);
    };

    const handleVideoChange = event => {
        const video = event.target.files[0];
        setVideo(video);
    }

    const clearFields = event => event.target.reset();

    const handleSubmit = (event) => {
        event.preventDefault();
        if (!(title && description && preview && video)) {
            return;
        }
        setButtonText('Видео загружается...');
        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('preview_file', preview);
        formData.append('video_file', video);

        const instance = axios.create({withCredentials: true});
        instance.post(`${url}/api/v1/upload_video`, formData)
            .then(response => {
                setButtonText('Видео загружено');
                setTimeout(() => window.location.reload(), 1500);
            })
            .catch(err => {
                setButtonText('Произошла ошибка во время загрузки');
                clearFields(event);
                setTimeout(() => setButtonText('Загрузить'), 1500);
            });
    }

    return (<form className={styles.upload_video_form} method="post" onSubmit={handleSubmit}>
        <textarea className={`${styles.upload_textarea} ${styles.upload_title_textarea}`} onChange={handleTitleChange} placeholder="Введите название"/>
        <textarea className={`${styles.upload_textarea} ${styles.upload_description_textarea}`} onChange={handleDescriptionChange} placeholder="Введите описание"
        cols="10" rows="5"/>
        <div className={styles.container}>
            <label className={styles.input_file}>
                <input type="file" name="file[]" accept="image/*" onChange={handlePreviewChange}></input>
                <span>{preview ? 'Файл прикреплен' : 'Прикрепите превью'}</span>
            </label>
            <label className={styles.input_file}>
                <input className={styles.input} type="file" name="file[]" accept="video/*" onChange={handleVideoChange}></input>
                <span>{video ? 'Видео прикреплено' : 'Прикрепите видео'}</span>
            </label>
        </div>
        <button className={styles.btn} type="submit">{buttonText}</button>
    </form>)
};

export default UploadVideo;