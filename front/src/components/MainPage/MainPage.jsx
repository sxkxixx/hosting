import styles from './MainPage.module.css';
import SearchBar from "../SearchBar/SearchBar";
import VideoCard from "../VideoCard/VideoCard";
import React, {useEffect, useState} from "react";
import getAxiosBody from "../sendData";
import axios from "axios";
import {Link} from "react-router-dom";


export const MainPage = () => {
  const [videos, setVideos] = useState([]);
  // const [user, setUser] = useState('')

  useEffect( () => {
    const body = getAxiosBody('main_page')
    const instance = axios.create({withCredentials: true})

    instance.post('http://127.0.0.1:8000/api/v1/video', body)
        .then(response => {
            const video = response.data['result'].videos;
            setVideos(video);
            document.title = 'Video Hosting'
        })
        .catch((err) => {
            console.log(err);
        })
  }, [setVideos]);

  const videosList = videos.map((video) => <Link to={`/watch/${video.id}`} style={{ textDecoration: 'none', color: 'gray' }}><VideoCard id={video.id} title={video.title} preview={video.preview} owner={video.owner.email}/></Link>);

  return (
  <div>
    <SearchBar/>
    <div className={styles.videos_container}>
      {videosList}
    </div>
  </div>
  )
}
