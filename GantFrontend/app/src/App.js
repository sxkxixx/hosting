import s from './App.module.css'
import Header from './Components/Header/Header'
import Footer from './Components/Footer/Footer'
import Main from './Components/Main/Main'

function App() {
  return (
      <div className={s.container}>
        <Header/>
        <Main/>
        <Footer/>
      </div>
  )
}

export default App
