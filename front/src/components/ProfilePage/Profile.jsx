import styles from './Profile.module.css';
import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { useNavigate } from 'react-router-dom';
import VideoCard from "../VideoCard/VideoCard";
import UploadVideo from "../UploadVideo/UploadVideo";
import array from "../utils";

export const Profile =  () => {
  const navigate = useNavigate();

  const videos = array.map((video) =>
      <VideoCard id={video.id} title={video.title} preview={video.preview}/>
  )

  return (
    <div className={styles.main_container_profile}>
      <div className={styles.container_left}>
        <div className={styles.user_info}>
          <button className={styles.user_avatar} type="button"><UserAvatar/></button>
          <div className={styles.user_info_profile}>
            <p className={styles.user_name}>@username</p>
            <p className={styles.user_email}>users@mail.ru</p>
          </div>
        </div>
        <h3 className=''>Мои видео:</h3>
        <div className={styles.videos_container}>
          { videos }
        </div>

      </div>

      <div className={styles.container_right}>
        <div className={styles.button_container}>
          <button className={`${styles.back_to_search} ${styles.btn}`} type='button'
                  onClick={() => navigate('/', {replace: false})}>Вернуться к поиску</button>
          <button className={`${styles.log_out_in} ${styles.btn}`} type='button'>Выйти</button>
        </div>
        <h3>Загрузить видео:</h3>
        <UploadVideo/>
      </div>
    </div>
    )
}
