<template>
    <div class="iphone-container">
        <div class="home-content">
            <div class="center">
                <div class="chat">
                    <div class="contact bar">
                        <div class="pic stark"></div>
                        <div class="name">
                            WattSmart Chat Assistant
                        </div>
                        <div class="seen">
                            Ask right away
                        </div>
                    </div>
                    <div class="messages" id="chat">
                        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
                            <div>{{ message.content }}</div>
                        </div>
                    </div>
                    <div class="input">
                        <input placeholder="Type your message here!" v-model="newMessage" @keyup.enter="sendMessage"
                            type="text" />
                        <button class="button-13" role="button" @click="sendMessage">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

interface Message {
    role: 'user' | 'ai';
    content: string;
}

export default defineComponent({
    data() {
        return {
            title: "Home",
            newMessage: '',
            messages: [] as Message[],
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
        },
        getConversationHistory() {
            fetch('/get_conversation_history/')
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    
                    this.messages = data.conversation_history.slice(1);
                    this.$nextTick(() => {
                        const chatContainer = this.$el.querySelector("#chat");
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    });
                })
                .catch(error => console.error('Error:', error));
        },
        sendMessage() {
            if (this.newMessage.trim() === '') return;

            const userMessage: Message = {
                role: 'user',
                content: this.newMessage,
            };

            this.messages.push(userMessage);
            this.sendToServer(this.newMessage);
            this.newMessage = '';
        },
        sendToServer(message: string) {
            fetch('/send_message/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);

                    this.messages.push({
                        role: 'ai',
                        content: data.message,
                    });
                    this.$nextTick(() => {
                        const chatContainer = this.$el.querySelector("#chat");
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    });
                })
                .catch(error => console.error('Error:', error));
        },
    },
    mounted() {
        this.checkAuthStatus();
        this.getConversationHistory();
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
    max-height: 34em;
    height: 43em;
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

.chat .messages .message.user {
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
    height: 100vh;
}

.iphone {
    width: 375px;
    height: 812px;
    background-color: #fff;
    border-radius: 39px;
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
    border-radius: 29px;
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

.button-13 {
    background-image: linear-gradient(92.83deg, #ff7426 0, #f93a13 100%);
  border: 1px solid #d5d9d9;
  border-radius: 8px;
  box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: Eina01,sans-serif;
  font-size: 16px;
  font-weight: 600;
  line-height: 35px;
  padding: 0 10px 0 11px;
  position: relative;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
  width: 100px;
}

.button-13:hover {
  background-color: #f7fafa;
}

.button-13:focus {
  border-color: #008296;
  box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
  outline: 0;
}
</style>
