import {getCSRFToken} from "./modules/utils.js";
import {useFoundUserTemplate} from "./modules/templates.js";
import {useTeamMemberTemplate} from "./modules/templates.js";

const createTeamModal = document.querySelector('#create-team');
const editTeamModal = document.querySelector('#edit-team');
const deleteTeamModal = document.querySelector('#delete-team');
const openCreateTeamModalBtn = document.querySelector('#create-team-btn-modal');
const openDeleteTeamModalBtns = document.querySelectorAll('.delete-team-btn');
const openEditTeamModalBtns = document.querySelectorAll('.edit-team-btn');
const createTeamBtn = document.querySelector('#create-team-btn');
const editTeamBtn = document.querySelector('#edit-team-btn');
const teamNameInputs = document.querySelectorAll('[name=team_name]');
const userNameInputs = document.querySelectorAll('[name=user_name]');

/* СЛАЙДЕР */
const swiperList = document.querySelectorAll('.slider-container');
let count = 1;
swiperList.forEach((swiper) => {
    let swiper_slider_id = count;
    swiper.childNodes[1].classList.add(`swiper-${swiper_slider_id}`);
    swiper.childNodes[1].childNodes[3].classList.add(`swiper-pagination-${swiper_slider_id}`);
    swiper.childNodes[3].childNodes[1].classList.add(`slider-button-prev-${swiper_slider_id}`);
    swiper.childNodes[3].childNodes[3].classList.add(`slider-button-next-${swiper_slider_id}`);

    const teamSwiper = new Swiper(`.swiper-${swiper_slider_id}`, {
        direction: 'horizontal',
        loop: true,
        slidesPerView: 5,
        slideToClickedSlide: false,
        spaceBetween: 15,
        initialSlide: 0,
        centerInsufficientSlides: true,

        pagination: {
            el: `.swiper-pagination-${swiper_slider_id}`,
        },

        navigation: {
            nextEl: `.slider-button-next-${swiper_slider_id}`,
            prevEl: `.slider-button-prev-${swiper_slider_id}`,
        },
    });
    count++;
})

/* СОЗДАНИЕ КОМАНДЫ - МОДАЛЬНОЕ ОКНО */
const modalCreate = new bootstrap.Modal(createTeamModal);
openCreateTeamModalBtn.addEventListener('click', () => {
    createTeamModal.querySelector('[name=team_name]').value = '';
    createTeamModal.querySelector('.not-unique-warning').style.display = 'none';
    createTeamModal.querySelector('.members-text').style.display = 'none';
    createTeamModal.querySelector('.members').innerHTML = '';
    createTeamModal.querySelector('[name=user_name]').value = '';
    createTeamModal.querySelector('.searched-users').innerHTML = '';
    createTeamBtn.disabled = true;
    modalCreate.show();
});

/* РЕДАКТИРОВАНИЕ КОМАНДЫ - МОДАЛЬНОЕ ОКНО */
const modalEdit = new bootstrap.Modal(editTeamModal);
openEditTeamModalBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        editTeamModal.querySelector('[name=team_id]').value = '';
        editTeamModal.querySelector('[name=team_name]').value = '';
        editTeamModal.querySelector('.not-unique-warning').style.display = 'none';
        editTeamModal.querySelector('.members-text').style.display = 'none';
        editTeamModal.querySelector('.members').innerHTML = '';
        editTeamModal.querySelector('[name=user_name]').value = '';
        editTeamModal.querySelector('.searched-users').innerHTML = '';
        editTeamBtn.disabled = true;
        insertTeamInfo(e)
        modalEdit.show();
    });
});

/* УДАЛЕНИЕ КОМАНДЫ - МОДАЛЬНОЕ ОКНО */
const modalDelete = new bootstrap.Modal(deleteTeamModal);
openDeleteTeamModalBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        deleteTeamModal.querySelector('span').innerHTML = e.currentTarget.dataset.teamName;
        deleteTeamModal.querySelector('[name=team_id]').value = e.currentTarget.dataset.teamId;
        modalDelete.show();
    });
});

/* ПРОВЕРКА НАЛИЧИЯ НАИМЕНОВАНИЯ КОМАНДЫ И ЕГО УНИКАЛЬНОСТИ */
teamNameInputs.forEach(input => {
    input.addEventListener('input', () => {
        let action = input.dataset.action;
        let form, btn;
        [form, btn] = action == 'create-team' ? [createTeamModal, createTeamBtn] : [editTeamModal, editTeamBtn];

        let teamName = form.querySelector('[name=team_name]').value;
        if (!teamName.trim()) {
            btn.disabled = true;
            return;
        }

        let url = `?team_name=${teamName}`;
        if (action == 'edit-team') {
            url = url + `&team_id=${form.querySelector('[name=team_id]').value}`;
        }

        fetch(url, {
            method: 'GET',
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (!data.unique) {
                    form.querySelector('.not-unique-warning').style.display = 'block';
                    btn.disabled = true;
                } else {
                    form.querySelector('.not-unique-warning').style.display = 'none';
                    btn.disabled = false;
                }
            });
    });
});

/* ПОИСК ПОЛЬЗОВАТЕЛЕЙ (ДЛЯ ДОБАВЛЕНИЯ В КОМАНДУ) */
userNameInputs.forEach(input => {
    input.addEventListener('input', () => {
        let action = input.dataset.action;
        let form = action == 'create-team' ? createTeamModal : editTeamModal;
        let resultBlock = form.querySelector('.searched-users');

        let userName = input.value.trim()
        if (!userName) {
            resultBlock.innerHTML = '';
            return;
        }

        let membersId = [];
        form.querySelectorAll('.member').forEach(member => {
            membersId.push(+member.dataset.memberId);
        });

        fetch(`?user_name=${userName}&members_id=${JSON.stringify(membersId)}`, {
            method: 'GET',
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        })
            .then(response => {
                return response.json();
            })
            .then(data => {
                resultBlock.innerHTML = '';
                if (data.users && data.users.length !== 0) {
                    data.users.forEach(item => {
                        resultBlock.insertAdjacentHTML('beforeend',
                            useFoundUserTemplate(
                                `/profile/${item.id}/`,
                                item.id,
                                item.cropped_photo,
                                `${item.last_name} ${item.first_name} ${item.patronymic ? item.patronymic : ''}`,
                                action
                            )
                        );
                    });
                }
                form.querySelectorAll('.addMemberBtn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        addMember(e);
                    });
                });
            });
    });
});

/* ОЧИЩЕНИЕ РЕЗУЛЬТАТОВ ПОИСКА */
function clearSearchResults(form) {
    form.querySelector('[name=user_name]').value = '';
    form.querySelector('.searched-users').innerHTML = '';
}

/* ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В КОМАНДУ */
function addMember(e) {
    let action = e.currentTarget.dataset.action;
    let form = action == 'create-team' ? createTeamModal : editTeamModal;
    let userId = e.currentTarget.dataset.userId;
    let chosenUser = document.querySelector(`.searched-user[data-user-id="${userId}"]`);
    form.querySelector('.members-text').style.display = 'block';
    form.querySelector('.members').insertAdjacentHTML('beforeend',
        useTeamMemberTemplate(
            chosenUser.querySelector('a').href,
            userId,
            chosenUser.querySelector('img').src,
            chosenUser.querySelector('p').innerHTML,
            action
        ));

    document.querySelector(`.delete-member-btn[data-member-id="${userId}"]`).addEventListener('click', (e) => {
        deleteMember(e)
    });

    clearSearchResults(form);
    if (action == 'edit-team') {
        editTeamBtn.disabled = false;
    }
}

/* УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ ИЗ КОМАНДЫ */
function deleteMember(e) {
    let action = e.currentTarget.dataset.action;
    let form = action == 'create-team' ? createTeamModal : editTeamModal;
    let memberId = e.currentTarget.dataset.memberId;
    let chosenMember = document.querySelector(`.member[data-member-id="${memberId}"]`);
    chosenMember.remove();

    if (!form.querySelector('.member')) {
        form.querySelector('.members-text').style.display = 'none';
    }

    clearSearchResults(form);
    if (action == 'edit-team') {
        editTeamBtn.disabled = false;
    }
}

/* СОЗДАНИЕ КОМАНДЫ */
createTeamBtn.addEventListener('click', () => {
    let teamName = createTeamModal.querySelector('[name=team_name]').value;

    let membersId = [];
    createTeamModal.querySelectorAll('.member').forEach(member => {
        membersId.push(+member.dataset.memberId);
    });

    let formData = new FormData();
    formData.append('team_name', teamName);
    formData.append('members_id', JSON.stringify(membersId));

    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
        .then(() => {
            document.location.reload();
        });
});

/* ВСТАВКА ДАННЫХ О КОМАНДЕ ДЛЯ РЕДАКТИРОВАНИЯ */
function insertTeamInfo(e) {
    let teamId = e.currentTarget.dataset.teamId;

    fetch(`?team_id=${teamId}`, {
        method: 'GET',
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
        .then(response => {
            return response.json();
        })
        .then(data => {
            editTeamModal.querySelector('[name=team_id]').value = teamId;
            editTeamModal.querySelector('[name=team_name]').value = data.name;
            if (data.members && data.members.length !== 0) {
                editTeamModal.querySelector('.members-text').style.display = 'block';
                data.members.forEach(member => {
                    editTeamModal.querySelector('.members').insertAdjacentHTML('beforeend',
                        useTeamMemberTemplate(
                            `/profile/${member.id}/`,
                            member.id,
                            member.cropped_photo + '?timestamp=' + Date.now(),
                            `${member.last_name} ${member.first_name} ${member.patronymic ? member.patronymic : ''}`,
                            'edit-team'
                        )
                    )
                });
            }

            editTeamModal.querySelectorAll('.delete-member-btn').forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    deleteMember(e)
                });
            });
        });
}

/* РЕДАКТИРОВАНИЕ КОМАНДЫ */
editTeamBtn.addEventListener('click', () => {
    let teamId = editTeamModal.querySelector('[name=team_id]').value;
    let teamName = editTeamModal.querySelector('[name=team_name]').value;

    let membersId = [];
    editTeamModal.querySelectorAll('.member').forEach(member => {
        membersId.push(+member.dataset.memberId);
    });

    let formData = new FormData();
    formData.append('team_id', teamId);
    formData.append('team_name', teamName);
    formData.append('members_id', JSON.stringify(membersId));

    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(),
        }
    })
        .then(() => {
            document.location.reload();
        });
});
