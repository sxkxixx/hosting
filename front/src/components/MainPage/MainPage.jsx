import styles from './MainPage.module.css';
import SearchBar from "../SearchBar/SearchBar";
import VideoCard from "../VideoCard/VideoCard";
import React, {useEffect, useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";

const url = process.env.REACT_APP_API_URL;
export const MainPage = () => {
  const [videos, setVideos] = useState([]);

  useEffect( () => {
    const body = getAxiosBody('main_page');
    const instance = axios.create({withCredentials: true});

    instance.post(`${url}/api/v1/video`, body)
        .then(response => {
            const video = response.data['result'].videos;
            setVideos(video);
            document.title = 'Main';
        })
        .catch((err) => {
            console.log(err);
        })
  }, [setVideos]);


  return (
  <div>
    <SearchBar/>
    <div className={styles.videos_container}>
      {videos.map((video) => <VideoCard id={video.id} title={video.title} preview={video.preview} owner={video.owner.email} views={video.views} owner_avatar={video.owner.avatar}/>)}
    </div>
  </div>
  )
}
