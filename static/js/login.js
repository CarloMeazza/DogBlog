window.addEventListener('DOMContentLoaded', () => {
    const btnLogin = document.getElementById('login')
    btnLogin.addEventListener('click', () => {
        const username = document.getElementById('username').value
        const password = document.getElementById('password').value

        if (username === 'admin' && password === 'password') {
            localStorage.setItem('username', username)
            localStorage.setItem('password', password)
            window.location.href = '/admin';
        }
    })
    if (localStorage.getItem('username') && localStorage.getItem('password')) {
        window.location.href = '/admin';
    }
})