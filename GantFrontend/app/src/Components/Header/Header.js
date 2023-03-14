import React from 'react'
import s from './Header.module.css'
import logo from '../../Assets/img/logo_big.png'
import { AiOutlineUser, AiOutlineCloseCircle } from "react-icons/ai";

const Header = () => {
    return (
        <div className={s.container}>
            <div className={s.left}>
                <img src={logo} alt="logo" width="50" height="50"/>
                <p>Хогвартс</p>
            </div>
            <div className={s.right}>
                <div className={s.elements}>
                    <AiOutlineUser/><p>Рубеус Хагрид</p>
                </div>
                <div className={s.elements}>
                    <AiOutlineUser/><p>выйти</p>
                </div>
            </div>
        </div>
    )
}

export default Header
