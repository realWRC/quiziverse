(function() {

  const countdownElement = document.getElementById("countdown");
  const optionsList = document.getElementById("options-list");
  const submitButton = document.getElementById("submit-btn");
  const skipButton = document.getElementById("skip-btn");
  const backButton = document.getElementById("back-btn");
  const answerForm = document.getElementById("answer-form");
  const answerInput = document.getElementById("answerpayload");

  const startTimeStr = SETTINGS.startTime;
  const duration = SETTINGS.duration;
  const currentQID = SETTINGS.currentQuestionId;
  const currentScore = SETTINGS.currentQuestionScore;
  const currentQuizID = SETTINGS.quizID;

  let selectedOption = null;

  if (optionsList) {
    optionsList.addEventListener("click", (event) => {
      const clicked = event.target;
      if (!clicked) return;

      const li = clicked.closest("li.option-item");
      if (!li) return;

      const prevSelected = optionsList.querySelector("li.selected");
      if (prevSelected && prevSelected !== li) {
        prevSelected.classList.remove("selected");
        const oldRadio = prevSelected.querySelector("input[type=radio]");
        if (oldRadio) oldRadio.checked = false;
      }

      if (li.classList.contains("selected")) {
        li.classList.remove("selected");
        const radio = li.querySelector("input[type=radio]");
        if (radio) radio.checked = false;
        selectedOption = null;
        submitButton.disabled = true;
      } else {
        li.classList.add("selected");
        const radio = li.querySelector("input[type=radio]");
        if (radio) {
          radio.checked = true;
          selectedOption = radio.value;
        }
        submitButton.disabled = false;
      }
    });
  }


  function buildPayload(questionId, selected, scoreVal, skipVal, backVal) {
    return {
      "answer": { [questionId]: selected },
      "time": new Date().toISOString(),
      "timeoutstatus": false,
      "score": scoreVal,
      "skip": skipVal,
      "back": backVal
    };
  }

  if (submitButton) {
    submitButton.addEventListener("click", () => {
      if (!selectedOption) return;

      const payload = buildPayload(currentQID, selectedOption, currentScore, false, false);
      answerForm.setAttribute("action", `/submitanswer/${currentQuizID}`);
      answerInput.value = JSON.stringify(payload);
      answerForm.submit();
    });
  }

  if (skipButton) {
    skipButton.addEventListener("click", () => {
      const payload = buildPayload(currentQID, "none", currentScore, true, false);
      answerForm.setAttribute("action", `/skip/${currentQuizID}`);
      answerInput.value = JSON.stringify(payload);
      answerForm.submit();
    });
  }

  if (backButton) {
    backButton.addEventListener("click", () => {
      const payload = buildPayload(currentQID, "none", currentScore, false, true);
      answerForm.setAttribute("action", `/previous/${currentQuizID}`);
      answerInput.value = JSON.stringify(payload);
      answerForm.submit();
    });
  }


  let timeRemaining = duration;

  if (duration > 0 && countdownElement) {
    displayTime(countdownElement, timeRemaining);
    const intervalId = setInterval(() => {
      if (timeRemaining <= 0) {
        clearInterval(intervalId);
        displayTime(countdownElement, 0);
        return;
      }
      timeRemaining--;
      displayTime(countdownElement, timeRemaining);
    }, 1000);
  }

  function displayTime(element, secondsLeft) {
    const minutes = Math.floor(secondsLeft / 60);
    const seconds = secondsLeft % 60;
    element.textContent = `Time Left: ${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
  }

})();
