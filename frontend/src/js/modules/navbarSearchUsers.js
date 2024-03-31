import {getCSRFToken} from "./utils.js";

export function navbarSearchUsers() {
    const navbarUserNameInput = document.querySelector('[name=navbar_user_name]');
    const token = getCSRFToken();

    if (navbarUserNameInput) {
        navbarUserNameInput.addEventListener('input', () => {
            let navbarUserName = navbarUserNameInput.value.trim();

            fetch(`?user_name=${navbarUserName}`, {
                method: 'GET',
                headers: {
                    "X-CSRFToken": token,
                }
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                renderResultSearchList(data);
            });
        });
    }
}

const resultBlock = document.querySelector('.search-result');
function renderResultSearchList(data) {
    document.querySelector('.search-result-list').innerHTML = '';
    if (data.users && data.users.length !== 0) {
        resultBlock.style.display = 'block';
        data.users.forEach(item => {
            document.querySelector('.search-result-list').insertAdjacentHTML('beforeend', template(item.profile_url, item.cropped_photo_url, item.last_name, item.first_name, item.patronymic))
        })
    } else {
        resultBlock.style.display = 'none';
    }
}

function template(profile_url, cropped_photo_url, last_name, first_name, patronymic) {
    return `
        <a href="${profile_url}">
            <li>
                <img src="${cropped_photo_url}?timestamp=${Date.now()}">
                <p>${last_name} ${first_name} ${patronymic ? patronymic : ''}</p>
            </li>
        </a>
    `
}

document.addEventListener('mouseup', function(event) {;
    if (!resultBlock.contains(event.target)) {
        resultBlock.style.display = 'none';
    }
});