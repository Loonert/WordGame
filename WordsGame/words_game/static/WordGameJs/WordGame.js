///*
////document.addEventListener('DOMContentLoaded', function() {
////    const gameInterface = document.getElementById('game-interface');
////    console.log("test")
////    // Замените 'your-api-url' на реальный URL вашего API
////    const apiUrl = 'http://localhost:8000/your-app/api/';
////
////    // Функция для отправки POST-запросов на API
////    async function postData(url = '', data = {}) {
////        const response = await fetch(url, {
////            method: 'POST',
////            headers: {
////                'Content-Type': 'application/json',
////            },
////            body: JSON.stringify(data),
////        });
////
////        return response.json();
////    }
////
////    // Пример использования функции для создания игрока
////    postData(apiUrl + 'player', { name: 'Player1' })
////        .then(data => {
////            console.log('Player ID:', data.playerID);
////        })
////        .catch(error => {
////            console.error('Error:', error);
////        });
////
////    // Продолжайте добавлять взаимодействие с API для других функций игры
////});
//*/
//
//console.log("tets1111111111");
//    // После отправки формы создания игрока
//    document.addEventListener("DOMContentLoaded", function() {
//        document.querySelector('.CreatePlayerForm').addEventListener('submit', function (event) {
//            event.preventDefault();
//            console.log("test")
//            // Отправка POST-запроса на создание игрока
//            fetch('http://127.0.0.1:8000/api/player', {
//                method: 'POST',
//                headers: {
//                    'Content-Type': 'application/x-www-form-urlencoded',
//                },
//                body: new URLSearchParams(new FormData(this)).toString(),
//            })
//            .then(response => response.json())
//            .then(data => {
//                // Получение playerID из ответа
//                const playerID = data.playerID;
//
//                // Сохранение playerID (можете использовать localStorage, sessionStorage или куки)
//                sessionStorage.setItem('playerID', playerID);
//
//                // Перенаправление на страницу игры
//                window.location.href = `/your-app/api/games/${playerID}/start`;
//            })
//            .catch(error => {
//                console.error('Error:', error);
//            });
//        });sdfsdfasfadadfffdadsfdsfsaas
//    })


$(document).ready(function() {
  // Вешаем обработчик события на отправку формы
  $(".CreatePlayerForm").submit(function(event) {
    // Отменяем стандартное действие формы, чтобы страница не перезагружалась
    event.preventDefault();

    // Получаем значение поля ввода с именем игрока
    var playerName = $("#player_name").val();

    // Выполняем AJAX-запрос к вашему методу create_player
    $.ajax({
      type: "POST",
      url: "/your-url-for-create-player/",
      data: { name: playerName },
      success: function(response) {
        // Делаем что-то с полученными данными, например, выводим ID игрока
        console.log("Player ID: " + response.playerID);
      },
      dataType: "json"
    });
  });
});
