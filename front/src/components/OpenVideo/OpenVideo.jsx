import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { ReactComponent as Like } from '../../img/like.svg';
import { ReactComponent as Arrow } from '../../img/arrow.svg'
import SearchBar from '../SearchBar/SearchBar';
import styles from './OpenVideo.module.css';

const OpenVideo = () => {

  return (
    <div>
      <SearchBar/>
      <div className={styles.main}>
        <div className={styles.render}>
          <div className={styles.big_video} name='big-video'></div>
          <div className={styles.users_info_and_likes}>
            <button className={styles.user_profile_icon_render} alt=''><UserAvatar/></button>
            <p className={styles.user_name}>@username</p>
            <button type="button" className={styles.likes_btn}><Like/>503</button>
          </div>
          <div className={styles.description_box} name='description-box'>
            <p className={styles.title_video}>Название видео</p>
            <p className={styles.description_video}>Описаниеописаниеописаниеописаниео</p>
          </div>
        </div>
          <div className={styles.comments} name='comments'>
            <p className={styles.comments_title}>Комментарии</p>
            <div className={styles.line}></div>
            <div className={styles.comments_container}></div>
            <form className={styles.comment_form} action="" method="post">
              <input className={styles.comment_input} placeholder="Напишите комментарий"/>
              <button className={styles.comment_send_btn} type='submit'><Arrow/></button>
            </form>
          </div>
      </div>
    </div>
    )
}

export default OpenVideo;
