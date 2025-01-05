// {% if not data %}
// let questionIndex = 1;
// {% else %}
// let questionIndex = {{ data['questions']|length }}
// {% endif %}
const addBtn = document.getElementById('add-question-btn');
const removeBtn = document.getElementById('remove-question-btn');
const container = document.getElementById('questions-container');

addBtn.addEventListener('click', function() {
    const fieldset = document.createElement('fieldset');
    fieldset.classList.add('question-block');
    fieldset.innerHTML = `
        <legend>Question ${questionIndex + 1}</legend>
        <label>Question Text: <input type="text" class="question-text" required></label><br>
        <label>Option 1: <input type="text" class="option" required></label><br>
        <label>Option 2: <input type="text" class="option" required></label><br>
        <label>Option 3: <input type="text" class="option"></label><br>
        <label>Option 4: <input type="text" class="option"></label><br>
        <label>Correct Answer: <input type="text" class="answer" required></label><br>
        <label>Score (optional, default 1): <input type="text" class="score"></label><br>
    `;
    container.appendChild(fieldset);
    questionIndex++;
});

removeBtn.addEventListener('click', function() {
    const questionBlocks = container.querySelectorAll('.question-block');
    if (questionBlocks.length > 1) {
        container.removeChild(questionBlocks[questionBlocks.length - 1]);
        questionIndex--;
    } else {
        alert("You must have at least one question.");
    }
});

const form = document.getElementById('createQuizForm');
form.addEventListener('submit', function(e) {
    const title = form.querySelector('[name="title"]').value.trim();
    const description = form.querySelector('[name="description"]').value.trim();
    const category = form.querySelector('[name="category"]').value.trim();
    const time_limit_str = form.querySelector('[name="time_limit"]').value.trim();
    const time_limit = time_limit_str ? parseInt(time_limit_str, 10) : 0;

    // let questionsData = {};
    let questionsData = []
    const questionBlocks = container.querySelectorAll('.question-block');
    questionBlocks.forEach((block, idx) => {
        const questionText = block.querySelector('.question-text').value.trim();
        const optionElements = block.querySelectorAll('.option');
        let options = [];
        optionElements.forEach(opt => {
            const val = opt.value.trim();
            if (val) options.push(val);
        });
        const answer = block.querySelector('.answer').value.trim();
        const scoreStr = block.querySelector('.score').value.trim();
        const score = scoreStr ? parseInt(scoreStr, 10) : 1;

        // questionsData[`question${idx}`] = {
        //     "question": questionText,
        //     "options": options,
        //     "answer": answer,
        //     "score": score
        // };
        questionsData.push({
            "question": questionText,
            "options": options,
            "answer": answer,
            "score": score
        });
    });

    const quizJson = {
        "title": title,
        "description": description,
        "category": category,
        "time_limit": time_limit,
        "questions": questionsData
    };

    document.getElementById('quiz_json').value = JSON.stringify(quizJson);
});
