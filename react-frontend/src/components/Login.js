import React, { useState } from 'react'
import axios from 'axios';
import Cookies from 'js-cookie';

export default function Login() {

    const [username, setUsername] = useState(null);
    const [password, setPassword] = useState(null);

    function handleLogin(event) {
        event.preventDefault();
        
        axios.post('http://localhost:5000/login', {},
        {
            headers: {
                'Authorization': 'Basic ' + btoa(`${username}:${password}`),
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log(response);
            const access_token = response.data.access_token;
            // Set the expiry for the access_token to 30 mins.
            Cookies.set('access_token', access_token, {expires: new Date(Date.now() + (30 * 60 * 1000)), sameSite: 'none', secure: true});
        })
        .catch(error => {
            console.log(error);
        });
    }

    return (
        <div>
            <form>
                <label htmlFor="imageInput">Username: </label>
                <input type="text" id="usernameInput" onChange={(event) => {setUsername(event.target.value)}}/>
                <input type="password" id="passwordInput" onChange={(event) => {setPassword(event.target.value)}}/>
                <button type="submit" onClick={handleLogin}>Login</button>
            </form>
        </div>
    )
}
