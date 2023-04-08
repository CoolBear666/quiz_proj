const logo = document.getElementById('logo')
const reg = document.getElementById('reg')

const renderLogo = () => {
    logo.innerHTML = `
    <a href="/" class="d-flex align-items-center link-body-emphasis text-decoration-none">
            <span class="fs-4">КвизФактори</span>
    </a>
    <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
        <a class="me-3 py-2 link-body-emphasis text-decoration-none" href="/accounts/login/">Личный кабинет</a>
        <a class="py-2 link-body-emphasis text-decoration-none" href="/questions/">Создать Квиз</a>
    </nav>
    `
}
renderLogo()

const renderReg = () => {
    reg.innerHTML = `
        <a class="btn btn-primary btn-lg" href="/signup">Регистрация</a>
    `
}
renderReg()