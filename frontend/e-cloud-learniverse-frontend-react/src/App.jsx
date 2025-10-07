import { useState } from 'react'
import reactLogo from './assets/react.svg'
import eCloudLearniverseLogo from '/favicon.png'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>
          <img src={eCloudLearniverseLogo} alt="Logo" className="logo"/>
          E-Cloud-Learniverse
      </h1>


      <form action="/" method="post">
          <input type="text" name="username" placeholder="Your name" required/>
          <textarea name="content" placeholder="Write a message..." rows="3" cols="40" required></textarea>
          <button type="submit">Post Message</button>
      </form>

      <h2>Existing Messages:</h2>
          {/* <ul>
              <li><strong>{{ msg.username }}</strong>: {{ msg.content }}</li>
          </ul>
          <p>No messages yet. Be the first to post!</p> */}
      
    </>
  )
}

export default App;
