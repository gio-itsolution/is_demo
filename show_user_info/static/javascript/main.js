"use strict";


let buttonSelectUser = document.getElementById("select_User");
let buttonGetInfo = document.getElementById("infoButton");
let user_id;

buttonSelectUser.onclick = function () {
    BX24.selectUser(function (res) {
        buttonSelectUser.innerHTML = res['name'];
        buttonSelectUser.style.backgroundColor = 'red';
        buttonGetInfo.disabled = false;
        user_id = res['id'];
    })
}

function getHeaderName(key) {
    // Можете использовать switch или if-else конструкцию для определения названия заголовка по ключу
    switch (key) {
        case 'NAME':
            return 'Имя';
        case 'LAST_NAME':
            return 'Фамилия';
        case 'SECOND_NAME':
            return "Отчество";
        case 'EMAIL':
            return 'Почта';
        case 'DATE_REGISTER':
            return 'Дата регистрации на портале';
        case 'PERSONAL_BIRTHDAY':
            return 'Дата рождения'
        case 'PERSONAL_PHOTO':
            return 'Фото профиля'
        case 'PERSONAL_MOBILE':
            return 'Номер мобильного телефона'
        default:
            return '';
    }
}

function getInfo(url) {
    let formData = new FormData();
    formData.append('id', user_id)
    let options = {
        method: 'POST',
        body: formData,
    };

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'ok') {
                let tbody = document.getElementById('user_info_tbody');
                let html = '';
                let headerName;
                for (let [key, value] of Object.entries(data['res'])) {
                    headerName = getHeaderName(key)
                    // Здесь создаем строки с ячейками для каждого значения
                    if (key==='PERSONAL_PHOTO') {
                        html += `<tr><td>${headerName}</td><td><img src='${value}'></td></tr>`;
                    } else if (headerName !== '' && value !== '') {
                        html += `<tr><td>${headerName}</td><td>${value}</td></tr>`;
                    }
                }
                // Обновляем содержимое tbody
                tbody.innerHTML = html;
            }
        });
}



