// ДЛЯ ВЫВОДА НАЙДЕННЫХ ПОЛЬЗОВАТЕЛЕЙ ПРИ ПОИСКЕ В НАВБАРЕ
export function useNavbarFoundUserTemplate(profile_url, cropped_photo_url, name) {
    return `
        <a href="${profile_url}">
            <li>
                <img src="${cropped_photo_url}?timestamp=${Date.now()}">
                <p>${name}</p>
            </li>
        </a>
    `
}

// ДЛЯ ВЫВОДА НАЙДЕННЫХ ПОЛЬЗОВАТЕЛЕЙ ПРИ СОЗДАНИИ И РЕДАКТИРОВАНИИ КОМАНДЫ
export function useFoundUserTemplate(profile_url, id, cropped_photo_url, name, action) {
    return `
        <div data-user-id="${id}" class="searched-user">
            <div class="searched-user__inner">
                <a href="${profile_url}" target="_blank">
                    <img src="${cropped_photo_url}?timestamp=${Date.now()}">
                </a>
                <p>${name}</p>
                <button data-action="${action}" data-user-id="${id}" class="addMemberBtn add-btn-team">
                    <svg width="28" height="28" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8.77778 15H15M15 15H21.2222M15 15V21.2222M15 15V8.77778M15 29C13.1615 29 11.341 28.6379 9.64243 27.9343C7.94387 27.2307 6.40053 26.1995 5.10051 24.8995C3.80048 23.5995 2.76925 22.0561 2.06569 20.3576C1.36212 18.659 1 16.8385 1 15C1 13.1615 1.36212 11.341 2.06569 9.64243C2.76925 7.94387 3.80048 6.40053 5.10051 5.1005C6.40053 3.80048 7.94387 2.76925 9.64243 2.06569C11.341 1.36212 13.1615 1 15 1C18.713 1 22.274 2.475 24.8995 5.1005C27.525 7.72601 29 11.287 29 15C29 18.713 27.525 22.274 24.8995 24.8995C22.274 27.525 18.713 29 15 29Z" stroke="#D96A10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        </div>
    `
}

// ДЛЯ ВЫВОДА УЧАСТНИКОВ КОМАНДЫ
export function useTeamMemberTemplate(profile_url, id, cropped_photo_url, name, action) {
    return `
        <div data-member-id="${id}" class="member">
            <div class="member-user__inner d-flex align-items-center">
                <a href="${profile_url}" target="_blank">
                    <img src="${cropped_photo_url}?timestamp=${Date.now()}">
                </a>
                <p>${name}</p>
                <button data-action="${action}" data-member-id="${id}" class="delete-member-btn delete-btn-team">
                    <svg style="width="28" height="28"  viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8.77778 15H21.2222M15 29C13.1615 29 11.341 28.6379 9.64243 27.9343C7.94387 27.2307 6.40053 26.1995 5.10051 24.8995C3.80048 23.5995 2.76925 22.0561 2.06569 20.3576C1.36212 18.659 1 16.8385 1 15C1 13.1615 1.36212 11.341 2.06569 9.64243C2.76925 7.94387 3.80048 6.40053 5.10051 5.1005C6.40053 3.80048 7.94387 2.76925 9.64243 2.06569C11.341 1.36212 13.1615 1 15 1C18.713 1 22.274 2.475 24.8995 5.1005C27.525 7.72601 29 11.287 29 15C29 18.713 27.525 22.274 24.8995 24.8995C22.274 27.525 18.713 29 15 29Z" stroke="#D96A10" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            </div>
        </div>
    `
}