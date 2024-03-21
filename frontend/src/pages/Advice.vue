<template>
    <div class="iphone-container">
        <!-- Your Home Page Content -->
        <div class="home-content">
            <div class="center">
                <div class="chat">
                    <div class="contact bar">
                        <div class="pic stark"></div>
                        <div class="name">
                            Friendly AI Chat
                        </div>
                        <div class="seen">
                            Ask right away
                        </div>
                    </div>
                    <div class="messages" id="chat">
                        <div class="time">
                            Today at {{  new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}
                        </div>
                        <div class="message parker">
                            Hey, man! What's up, Mr Stark? 👋
                        </div>
                        <div class="message stark">
                            Kid, where'd you come from?
                        </div>
                        <div class="message parker">
                            Field trip! 🤣
                        </div>
                        <div class="message parker">
                            Uh, what is this guy's problem, Mr. Stark? 🤔
                        </div>
                        <div class="message stark">
                            Uh, he's from space, he came here to steal a necklace from a wizard.
                        </div>
                        <div class="message stark">
                            <div class="typing typing-1"></div>
                            <div class="typing typing-2"></div>
                            <div class="typing typing-3"></div>
                        </div>
                    </div>
                    <div class="input">
                        <i class="fas fa-camera"></i><i class="far fa-laugh-beam"></i><input
                            placeholder="Type your message here!" type="text" /><i class="fas fa-microphone"></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

// var chat = document.getElementById('chat');
// chat.scrollTop = chat.scrollHeight - chat.clientHeight;

export default defineComponent({
    data() {
        return {
            title: "Home",
        }
    },
    methods: {
        checkAuthStatus() {
            fetch('/check_auth/')
                .then(response => response.json())
                .then(data => {
                    if (!data.authenticated) {
                        window.location.href = '/login/';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    },
    mounted() {
        this.checkAuthStatus();
    }
})
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Red+Hat+Display:400,500,900&display=swap");

body,
html {
    font-family: Red hat Display, sans-serif;
    font-weight: 400;
    line-height: 1.25em;
    letter-spacing: 0.025em;
    color: #333;
    background: #f7f7f7;
}

.center {
    position: relative;
    margin-bottom: 100%;
}

.pic {
    width: 4rem;
    height: 4rem;
    background-size: cover;
    background-position: center;
    border-radius: 50%;
}

.contact {
    position: relative;
    margin-bottom: 1rem;
    padding-left: 5rem;
    height: 4.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.contact .pic {
    position: absolute;
    left: 0;
}

.contact .name {
    font-weight: 500;
    margin-bottom: 0.125rem;
}

.contact .message,
.contact .seen {
    font-size: 0.9rem;
    color: #999;
}

.contact .badge {
    box-sizing: border-box;
    position: absolute;
    width: 1.5rem;
    height: 1.5rem;
    text-align: center;
    font-size: 0.9rem;
    padding-top: 0.125rem;
    border-radius: 1rem;
    top: 0;
    left: 2.5rem;
    background: #333;
    color: white;
}

.contacts {
    position: absolute;
    top: 50%;
    left: 0;
    transform: translate(-6rem, -50%);
    width: 24rem;
    height: 32rem;
    padding: 1rem 2rem 1rem 1rem;
    box-sizing: border-box;
    border-radius: 1rem 0 0 1rem;
    cursor: pointer;
    background: white;
    box-shadow: 0 0 8rem 0 rgba(0, 0, 0, 0.1), 2rem 2rem 4rem -3rem rgba(0, 0, 0, 0.5);
    transition: transform 500ms;
}

.contacts h2 {
    margin: 0.5rem 0 1.5rem 5rem;
}

.contacts .fa-bars {
    position: absolute;
    left: 2.25rem;
    color: #999;
    transition: color 200ms;
}

.contacts .fa-bars:hover {
    color: #666;
}

.contacts .contact:last-child {
    margin: 0;
}

.contacts:hover {
    transform: translate(-23rem, -50%);
}

.chat {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 24rem;
    height: 100%;
    z-index: 2;
    box-sizing: border-box;
    border-radius: 1rem;
    background: white;
    box-shadow: 0 0 8rem 0 rgba(0, 0, 0, 0.1), 0rem 2rem 4rem -3rem rgba(0, 0, 0, 0.5);
}

.chat .contact.bar {
    flex-basis: 3.5rem;
    flex-shrink: 0;
    margin: 1rem;
    box-sizing: border-box;
}

.chat .messages {
    padding: 1rem;
    background: #f7f7f7;
    flex-shrink: 2;
    overflow-y: auto;
    box-shadow: inset 0 2rem 2rem -2rem rgba(0, 0, 0, 0.05), inset 0 -2rem 2rem -2rem rgba(0, 0, 0, 0.05);
}

.chat .messages .time {
    font-size: 0.8rem;
    background: #eee;
    padding: 0.25rem 1rem;
    border-radius: 2rem;
    color: #999;
    width: -webkit-fit-content;
    width: -moz-fit-content;
    width: fit-content;
    margin: 0 auto;
}

.chat .messages .message {
    box-sizing: border-box;
    padding: 0.5rem 1rem;
    margin: 1rem;
    background: #fff;
    border-radius: 1.125rem 1.125rem 1.125rem 0;
    min-height: 2.25rem;
    width: -webkit-fit-content;
    width: -moz-fit-content;
    width: fit-content;
    max-width: 66%;
    box-shadow: 0 0 2rem rgba(0, 0, 0, 0.075), 0rem 1rem 1rem -1rem rgba(0, 0, 0, 0.1);
}

.chat .messages .message.parker {
    margin: 1rem 1rem 1rem auto;
    border-radius: 1.125rem 1.125rem 0 1.125rem;
    background: #333;
    color: white;
}

.chat .messages .message .typing {
    display: inline-block;
    width: 0.8rem;
    height: 0.8rem;
    margin-right: 0rem;
    box-sizing: border-box;
    background: #ccc;
    border-radius: 50%;
}

.chat .messages .message .typing.typing-1 {
    -webkit-animation: typing 3s infinite;
    animation: typing 3s infinite;
}

.chat .messages .message .typing.typing-2 {
    -webkit-animation: typing 3s 250ms infinite;
    animation: typing 3s 250ms infinite;
}

.chat .messages .message .typing.typing-3 {
    -webkit-animation: typing 3s 500ms infinite;
    animation: typing 3s 500ms infinite;
}

.chat .input {
    box-sizing: border-box;
    flex-basis: 4rem;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding: 0 0.5rem 0 1.5rem;
}

.chat .input i {
    font-size: 1.5rem;
    margin-right: 1rem;
    color: #666;
    cursor: pointer;
    transition: color 200ms;
}

.chat .input i:hover {
    color: #333;
}

.chat .input input {
    border: none;
    background-image: none;
    background-color: white;
    padding: 0.5rem 1rem;
    margin-right: 1rem;
    border-radius: 1.125rem;
    flex-grow: 2;
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1), 0rem 1rem 1rem -1rem rgba(0, 0, 0, 0.2);
    font-family: Red hat Display, sans-serif;
    font-weight: 400;
    letter-spacing: 0.025em;
}

.chat .input input:placeholder {
    color: #999;
}

@-webkit-keyframes typing {

    0%,
    75%,
    100% {
        transform: translate(0, 0.25rem) scale(0.9);
        opacity: 0.5;
    }

    25% {
        transform: translate(0, -0.25rem) scale(1);
        opacity: 1;
    }
}

@keyframes typing {

    0%,
    75%,
    100% {
        transform: translate(0, 0.25rem) scale(0.9);
        opacity: 0.5;
    }

    25% {
        transform: translate(0, -0.25rem) scale(1);
        opacity: 1;
    }
}

.pic.stark {
    background-image: url("https://png.pngtree.com/png-clipart/20190904/original/pngtree-cartoon-illustration-free-light-bulb-png-image_4472964.jpg");
}

.iphone-container {
    display: flex;
    justify-content: center;
    /* align-items: center; */
    height: 100vh;
    /* Use full viewport height */
}

.iphone {
    width: 375px;
    /* iPhone X width */
    height: 812px;
    /* iPhone X height */
    background-color: #fff;
    border-radius: 39px;
    /* iPhone X border radius */
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}

.iphone-inner {
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    border: 5px solid #ccc;
    /* Add inner border */
    border-radius: 29px;
    /* Adjust border-radius to match inner part */
    overflow: hidden;
    position: relative;
}

.iphone-bottom {
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: absolute;
    bottom: 20px;
    width: calc(100% - 5px);
}

.iphone-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: none;
    border: none;
    padding: 8px;
    cursor: pointer;
    outline: none;
}

.iphone-button img {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
}
</style>
