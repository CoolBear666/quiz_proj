const logo = document.getElementById('logo')
const renderLogo = () => {
    logo.innerHTML = `
    <a href="/" class="d-flex align-items-center link-body-emphasis text-decoration-none">
            <span class="fs-4">КвизФактори</span>
    </a>
    <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto">
        <a class="me-3 py-2 link-body-emphasis text-decoration-none" href="/accounts/login/">Личный кабинет</a>
        <a class="py-2 link-body-emphasis text-decoration-none" href="/questions/">Создать Квиз</a>
    </nav>
    <nav class="d-inline-flex mt-2 mt-md-0 ms-auto">         
        <a class="py-2 link-body-emphasis text-decoration-none" href="/questions/questions_list/">Мои квизы</a>
    </nav>
    `
}
renderLogo()


async function getQuizzes() {
  try {
    const response = await fetch('/quizzes/');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const quizzes = await response.json();
    return quizzes;
  } catch (error) {
      console.error(error);
    }
}

// Вывод списка квизов на странице
async function displayQuizzes() {
  const quizList = $('#quiz-list');
  quizList.empty();

  const quizzes = await getQuizzes();
    quizzes.forEach((quiz) => {
      const row = $('<tr>');
      const title = $('<td>').text(quiz.title);
      const editButton = $('<button>').addClass('btn btn-primary').text('Edit');
      editButton.click(() => {
        window.location.href = /quizzes/${quiz.id}/edit/;
      });
      const deleteButton = $('<button>').addClass('btn btn-danger').text('Delete');
      deleteButton.click(async () => {
        try {
          const response = await fetch(/quizzes/${quiz.id},{
            method: 'DELETE'
        });
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          row.remove();
        } catch (error) {
          console.error(error);
          }
      });
      const actions = $('<td>').append(editButton, deleteButton);
      row.append(title, actions);
      quizList.append(row);
    });
}

$(document).ready(async function() {
await displayQuizzes();
});