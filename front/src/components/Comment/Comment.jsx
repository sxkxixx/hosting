import styles from './Comment.module.css';
import getAxiosBody from "../sendData";
import axios from "axios";
import {findDOMNode, unmountComponentAtNode} from "react-dom";

const Comment = ({id, owner, text}) => {
    const user = localStorage.getItem('user');

    const deleteComment = () => {
        const body = getAxiosBody('delete_comment', {comment_id: id});
        const instance = axios.create({withCredentials: true});
        instance.post('http://127.0.0.1:8000/api/v1/video', body)
            .then((response) => {
                if (response.data['result'].status !== 'deleted')
                    throw new Error();
                unmountComponentAtNode(findDOMNode(id));
            })
            .catch((err) => {
                console.log(err);
            })
    };




    return (
        <div key={`comment${id}`} className={styles.comment}>
            <div className={styles.container}>
                <span className={styles.owner}>{owner}</span>
                <div className={styles.inner_container}>
                    <img className={styles.claim} src={require("./claim.png")} width={20} height={20} alt={'Пожаловаться'}/>
                { user === owner
                    ? <img className={styles.del_comment} src={require('../../img/delete.png')} onClick={deleteComment} width={20} height={20} alt={'Удалить комментарий'}/>
                    : null}
                </div>

            </div>
            <p className={styles.text}>{text}</p>
        </div>
    )
};

export default Comment