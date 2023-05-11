import styles from './UploadVideo.module.css';
import {useState} from "react";
import axios from "axios";


const UploadVideo = () => {
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [preview, setPreview] = useState(null);
    const [video, setVideo] = useState(null);

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
        const formData = new FormData();
        formData.append('title', title);
        formData.append('description', description);
        formData.append('preview_file', preview);
        formData.append('video_file', video);

        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/upload_video', formData)
            .then(response => console.log(response.data))
            .catch(err => console.log(err))
            .finally(() => clearFields(event));

    }

    return <form className={styles.upload_video_form} method="post" onSubmit={handleSubmit}>
        <textarea className={`${styles.upload_textarea} ${styles.upload_title_textarea}`} onChange={handleTitleChange} placeholder="Введите название"/>
        <textarea className={`${styles.upload_textarea} ${styles.upload_description_textarea}`} onChange={handleDescriptionChange} placeholder="Введите описание"/>
        <label className={styles.input_file}>
            <input type="file" name="file[]" accept="image/*" onChange={handlePreviewChange}></input>
            <span>{preview ? preview.name : 'Прикрепите превью'}</span>
        </label>
        <label className={styles.input_file}>
            <input type="file" name="file[]" accept="video/*" onChange={handleVideoChange}></input>
            <span>{video ? video.name : 'Прикрепите видео'}</span>
        </label>
        <div className={styles.input_file_list}></div>
        <button type="submit">Загрузить</button>
    </form>;
};

export default UploadVideo;