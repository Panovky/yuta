import {getCSRFToken} from "./modules/utils.js";
import {useNavbarFoundUserTemplate} from "./modules/templates.js";

const navbarUserNameInput = document.querySelector('[name=navbar_user_name]');
const resultBlock = document.querySelector('.search-result');
const resultList = document.querySelector('.search-result-list');

function navbarSearchUsers() {
    let navbarUserName = navbarUserNameInput.value.trim();
    if (!navbarUserName) {
        resultBlock.style.display = 'None';
        resultList.innerHTML = '';
        return;
    }

    fetch(`?user_name=${navbarUserName}`, {
        method: 'GET',
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            resultList.innerHTML = '';
            if (data.users && data.users.length !== 0) {
                data.users.forEach(item => {
                    resultList.insertAdjacentHTML('beforeend',
                        useNavbarFoundUserTemplate(
                            `/profile/${item.id}/`,
                            item.cropped_photo,
                            `${item.last_name} ${item.first_name} ${item.patronymic ? item.patronymic : ''}`
                        )
                    );
                });
                resultBlock.style.display = 'block';
            } else {
                resultBlock.style.display = 'none';
            }
        });
}

navbarUserNameInput.addEventListener('input', navbarSearchUsers);

document.addEventListener('click', (e) => {
    if (e.target.parentElement != resultList && e.target != navbarUserNameInput) {
        resultBlock.style.display = 'none';
    }
});

navbarUserNameInput.addEventListener('focus', () => {
    resultBlock.style.display = 'block';
});
