const logo = document.getElementById('logo');

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
  `;
};

renderLogo();

const saveQuizData = async (data) => {
  console.log('Data sent to server:', data);

  const isValid = data.questions.every((question) => {
    if (!question.text || question.text.trim() === '') {
      console.error('Question text is empty');
      return false;
    }
    return question.answers.every((answer) => {
      if (!answer.text || answer.text.trim() === '') {
        console.error('Answer text is empty');
        return false;
      }
      return true;
    });
  });

  if (isValid) {
    const quizData = {
      title: data.title,
      questions: data.questions.map((question) => {
        return {
          text: question.text,
          answers: question.answers.map((answer) => {
            return {
              text: answer.text,
              id: answer.id,
              is_correct: answer.is_correct,
            };
          }).filter((answer) => answer.text),
        };
      }).filter((question) => question.text),
    };

    try {
      const response = await fetch('/form-submission/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(quizData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      console.log(responseData);
    } catch (error) {
      console.error(error.message);
    }
  }
};

$(document).ready(() => {
  $('#quiz-form').submit(async (event) => {
    event.preventDefault();

    const questionData = [];
    $('#quiz-form .question').each(function() {
      const questionText = $(this).find('label[for^="question-input-"]').text();
      const answers = $(this).find('.answer');
      const answerData = [];
      answers.each(function() {
        const answerText = $(this).find('label[for^="option-"]').text();
        const answerId = $(this).find('input[type="radio"]').attr('id');
        const isCorrect = $(this).find('input[type="radio"]').is(':checked');
        answerData.push({
          text: answerText,
          id: answerId,
          is_correct: isCorrect,
        });
      });
      questionData.push({
        text: questionText,
        answers: answerData.filter((answer) => answer.text),
      });
    });

    const quizData = {
      title: $('#quiz-title').text(),
      questions: questionData.filter((question) => question.text)
    };

    await saveQuizData(quizData);

    $('#quiz-form')[0].reset();
  });
});