import './MainPage.css';
import { SearchBar } from '../SearchBar/SearchBar';

export const MainPage = () => {

  return (
  <div>
    <SearchBar/>
    <ul className='videos-container'>
      <li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li>
      <li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li><li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li>
      <li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li>
      <li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li>
      <li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li><li className='video-preview-container'>
        <div className='video-preview'></div>
        <p className='title-video'>Название</p>
      </li>
    </ul>
  </div>
  )
}
