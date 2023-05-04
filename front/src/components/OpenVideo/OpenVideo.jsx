import './OpenVideo.css';
import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { ReactComponent as Like } from '../../img/like.svg';
import { ReactComponent as Arrow } from '../../img/arrow.svg'
import { SearchBar } from '../SearchBar/SearchBar';

export const OpenVideo = () => {

  return (
    <div>
      <SearchBar/>
      <div className='main-container'>
        <div className='container-render-video'>
          <div className='big-video' name='big-video'></div>
          <div className="users-info-and-likes">
            <button className='user-profile-icon-render' alt=''><UserAvatar/></button>
            <p className='user-name'>@username</p>
            <button type="button" className='likes-btn'><Like/>503</button>
          </div>
          <div className='description-box' name='description-box'>
            <p className='title-video'>Название видео</p>
            <p className='description-video'>Описаниеописаниеописаниеописаниео</p>
          </div>
        </div>

          <div className='comments' name='comments'>
            <p className='comments-title'>Комментарии</p>
            <div className="line"></div>
            <div className='comments-container'></div>
            <form className='comment-form' action="" method="post">
              <input className="comment-input" placeholder="Напишите комментарий"/>
              <button className='comment-send-btn' type='submit'><Arrow/></button>
            </form>
          </div>
      </div>
    </div>
    )
}
