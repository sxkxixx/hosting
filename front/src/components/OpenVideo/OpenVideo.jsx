import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { ReactComponent as Like } from '../../img/like.svg';
import { ReactComponent as Arrow } from '../../img/arrow.svg'
import SearchBar from '../SearchBar/SearchBar';
import styles from './OpenVideo.module.css';
import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import getAxiosBody from "../sendData";
import axios from "axios";
import Comment from "../Comment/Comment";
import VideoPlayer from "../VideoPLayer/VideoPlayer";

const OpenVideo = () => {
  const [isLiked, setIsLiked] = useState(false);
  const [likes, setLikes] = useState(0);
  const [video, setVideo] = useState([]);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');

  const {id} = useParams();

  useEffect( () => {
    const body = getAxiosBody('get_video', {'id': Number(id)})
    const instance = axios.create({withCredentials: true})
    instance.post('http://127.0.0.1:8000/api/v1/video', body)
        .then(response => {
          setComments(response.data['result'].comments)
          setVideo(response.data['result'].video)
          setIsLiked(response.data['result'].is_liked)
          setLikes(response.data['result'].video['likes']);
          document.title = video['title'];
        })
        .catch(err => {
          console.log(err);
        })
  }, []);

  const setRemoveLike = () => {
      const body = getAxiosBody('change_like_status', {'video_id': Number(id)})
      const instance = axios.create({withCredentials: true});
      instance.post('http://127.0.0.1:8000/api/v1/video', body)
          .then((response) => {
              const data = response.data['result'];
              if (data['status'] === 'Added') {
                  setLikes(likes + 1);
              }
              else {
                setLikes(likes - 1);
              }
          })
          .catch((err) => {
              console.log(err);
          });
  };

  const handleCommentTextChange = event => setCommentText(event.target.value);
  const clearFields = event => event.target.reset();

  const sendComment = (event) => {
      event.preventDefault();
      if (!commentText)
          return;
      const body = getAxiosBody('upload_comment', {comment_data: {video_id: Number(id), comment_text: commentText}})
      const instance = axios.create({withCredentials: true});
      instance.post('http://127.0.0.1:8000/api/v1/video', body)
          .then((response) => {
              const data = response.data['result'];
              setComments([...comments, {id: data['comment'], owner: data['user'], text: commentText}])
              setCommentText('');
          })
          .catch()
          .finally(() => {
              clearFields(event);
          });
  };

  const commentList = comments.slice().map(comment =>
    <Comment id={comment.id} owner={comment.owner} text={comment.text}/>
  );

  return (
    <div>
      <SearchBar/>
      <div className={styles.main}>
        <div className={styles.render}>
            <div className={styles.video_player}>
                <VideoPlayer id={id} src={video.url} preview={video.preview}/>
            </div>
          <div className={styles.users_info_and_likes}>
            <button className={styles.user_profile_icon_render}><UserAvatar/></button>
            <p className={styles.user_name}>{video.owner}</p>
            <button type="button" className={styles.likes_btn} onClick={setRemoveLike}><Like/>{likes}</button>
          </div>
          <div className={styles.description_box} name='description-box'>
            <p className={styles.title_video}>{video.title}</p>
            <p className={styles.description_video}>{video.description}</p>
          </div>
        </div>
          <div className={styles.comments} name='comments'>
            <p className={styles.comments_title}>Комментарии</p>
            <div className={styles.line}></div>
            <div className={styles.comments_container}>
              {commentList}
            </div>
            <form className={styles.comment_form} onSubmit={sendComment} action="" method="post">
              <input className={styles.comment_input} onChange={handleCommentTextChange} placeholder="Напишите комментарий"/>
              <button className={styles.comment_send_btn} type='submit'><Arrow/></button>
            </form>
          </div>
      </div>
    </div>
    )
}

export default OpenVideo;
