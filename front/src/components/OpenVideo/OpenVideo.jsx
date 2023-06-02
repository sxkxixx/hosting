import { ReactComponent as UserAvatar } from '../../img/user-avatar.svg';
import { ReactComponent as Like } from '../../img/like.svg';
import { ReactComponent as Arrow } from '../../img/arrow.svg'
import SearchBar from '../SearchBar/SearchBar';
import styles from './OpenVideo.module.css';
import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import getAxiosBody from "../sendData";
import axios from "axios";
import VideoPlayer from "../VideoPLayer/VideoPlayer";
import ClaimPopup from "../ClaimPopup/ClaimPopup";


const OpenVideo = () => {
    const [commentText, setCommentText] = useState('');
    const [modalActive, setModalActive] = useState(false);
    const [objectToClaim, setObjectToClaim] = useState(0);
    const [claimType, setClaimType] = useState('');
    const [likes, setLikes] = useState(0);
    const [userInfo, setUserInfo] = useState({});
    const [videoInfo, setVideoInfo] = useState({});
    const [comments, setComments] = useState([]);

    const navigate = useNavigate();
    const {id} = useParams();
    const currentUser = localStorage.getItem('user');

    useEffect( () => {
        const body = getAxiosBody('get_video', {'id': Number(id)})
        const instance = axios.create({withCredentials: true})
        instance.post('http://127.0.0.1:8000/api/v1/video', body)
            .then(response => {
                const data = response.data.result;
                setUserInfo(data.user);
                setVideoInfo(data.video);
                setComments(data.video.comments);
                setLikes(data.video.likes);
                document.title = videoInfo.title;
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

    const deleteComment = (comment_id) => {
        const body = getAxiosBody('delete_comment', {comment_id: comment_id});
        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/api/v1/video', body)
            .then((response) => {
                if (response.data['result'].status !== 'deleted')
                    throw new Error();
                window.location.reload();
            })
            .catch((err) => {
                console.log(err);
            })
    };

    const commentList = comments.slice().map(comment =>
        (<div key={`comment${comment.id}`} className={styles.comment}>
            <div className={styles.container}>
                <span className={styles.owner}>{comment.owner}</span>
                <div className={styles.inner_container}>
                    <img className={styles.claim} onClick={() => {
                        setObjectToClaim(comment.id);
                        setClaimType('comment');
                        setModalActive(true);
                    }} src={require("../../img/claim.png")} width={20} height={20} alt={'Пожаловаться'}/>
                { currentUser === comment.owner
                    ? <img className={styles.del_comment} src={require('../../img/delete.png')} onClick={() => deleteComment(comment.id)} width={20} height={20} alt={'Удалить комментарий'}/>
                    : null}
                </div>
            </div>
            <p className={styles.text}>{comment.text}</p>
        </div>)
  );

    const deleteVideo = () => {
        const body = getAxiosBody('delete_video', {video_id: id});
        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/api/v1/video', body)
            .then(response => {
                const data = response.data;
                if ('error' in data) {
                    throw new Error();
                }
                if (data.result.status === 'deleted') {
                    navigate('/');
                }
            })
    };

    return (
        <div>
          <div>
              <SearchBar/>
              <div className={styles.main}>
        <div className={styles.render}>
            <div className={styles.video_player}>
                <VideoPlayer id={id} src={videoInfo.url} preview={videoInfo.preview}/>
            </div>
          <div className={styles.users_info_and_likes}>
            <button className={styles.user_profile_icon_render} onClick={() => navigate(`/user/${userInfo.owner_id}`)}>
                {userInfo.owner_avatar ? <img className={styles.avatar} src={userInfo.owner_avatar}/> : <UserAvatar/>}
            </button>
            <p className={styles.user_name}>{userInfo.owner_email}</p>
              <img className={styles.claim} onClick={() => {
                  setObjectToClaim(id);
                  setClaimType('video');
                  setModalActive(true);
              }} style={{marginRight: 20}} src={require('../../img/claim.png')} width={20} height={20} alt={"Пожаловаться на видео"}/>
              {localStorage.getItem('user') === userInfo.owner_email ?
                  <img className={styles.trashcan}
                       onClick={deleteVideo}
                       src={require('../../img/delete.png')} width={20} height={20}/>
                  : null}
            <button type="button" className={styles.likes_btn} onClick={setRemoveLike}><Like/>{likes}</button>
          </div>
          <div className={styles.description_box} name='description-box'>
              <div className={styles.container_views__title}>
                  <p className={styles.title_video}>{videoInfo.title}</p>
                  <p>Просмотров: {videoInfo.views}</p>
              </div>
            <p className={styles.description_video}>{videoInfo.description}</p>
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
          <ClaimPopup active={modalActive} setActive={setModalActive} id={objectToClaim} type={claimType}/>
      </div>
    )
}

export default OpenVideo;
