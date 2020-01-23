$(document).ready(function () {
  $('.msger-input').keyup(function (e) {
    if (e.keyCode == 13) {
      enviar();
    }
  });

});


var msgerChat, msgBot
const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :("
];


const BOT_IMG = "https://image.flaticon.com/icons/svg/2040/2040653.svg";
const PERSON_IMG = "https://image.flaticon.com/icons/svg/145/145867.svg";
const BOT_NAME = "BOT";
const PERSON_NAME = "YOU";


function enviar() {
  const msgerInput = get(".msger-input");
  msgerChat = get(".msger-chat");
  const msgText = msgerInput.value;
  if (!msgText) return;
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
  enviar_mensaje(msgText);
  msgerInput.value = "";
  botResponse();
}


function enviar_mensaje(msgText) {
  $.ajax({
    url: '/input/' + msgText,
    dataType: 'json',
    type: 'GET',
    success: function (response) {
      msgBot = response;
    }
  });
}



function appendMessage(name, img, side, text) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}


function botResponse() {
  /*const delay = msgText.split(" ").length * 100;*/
  const delay = 500;

  setTimeout(() => {
    appendMessage(BOT_NAME, BOT_IMG, "left", msgBot);
  }, delay);
}


// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}