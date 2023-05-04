import './ProfilePage.css';
import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { useNavigate } from 'react-router-dom';

export const UnauthorizedProfilePage = () => {
  const navigate = useNavigate();

  return (
    <div className='main-container-profile'>

      <div className='container-left'>
        <div className='user-info'>
          <button className='user-avatar' type="button"><UserAvatar/></button>
          <div className='user-info-profile'>
            <button className='log-out-in btn' type='button'>Войти | Зарегистрироваться</button>
          </div>
        </div>
        <h3 className=''>Мои видео:</h3>
        <ul className='videos-container'>
          {/* <li className='video' ></li> */}
          
        </ul>
      </div>

      <div className='container-right'>
        <div className='button-container'>
          <button type="button" className='back-to-search btn'
                  onClick={() => navigate('/', {replace: false})}>Вернуться к поиску</button>
        </div>
        <h3>Загрузить видео:</h3>
        <form className='upload-video-form' method="post">
          <textarea className="upload-textarea upload-title-textarea" placeholder="Введите название"/>
          <textarea className="upload-textarea upload-description-textarea" placeholder="Введите описание"/>
          <label className="input-file">
            <input type="file" name="file[]" multiple accept="video/*"></input>		
            <span>Загрузить видео</span>
          </label>
          <div className="input-file-list"></div>  
        </form>
      </div>
    </div>
    )
}
