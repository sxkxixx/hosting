import styles from './MainPage.module.css';
import SearchBar from "../SearchBar/SearchBar";
import VideoCard from "../VideoCard/VideoCard";
import array from "../utils";


export const MainPage = () => {
  const videos = array.slice().map((video) =>
    <li className={styles.video_preview_container}><VideoCard id={video.id} title={video.title} preview={video.preview}/></li>
  )


  return (
  <div>
    <SearchBar/>
    <ul className={styles.videos_container}>
      {videos}
    </ul>
  </div>
  )
}
