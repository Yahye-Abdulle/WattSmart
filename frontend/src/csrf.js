export function getCsrfToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split('; csrftoken=');
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}