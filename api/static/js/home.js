document.addEventListener('DOMContentLoaded', function() {
  const copyButtons = document.querySelectorAll('.copy-id-btn');
  copyButtons.forEach(button => {
    button.addEventListener('click', function() {
      const quizId = this.getAttribute('data-quizid');
      navigator.clipboard.writeText(quizId).then(() => {
        alert('Quiz ID copied to clipboard!');
      }).catch(err => {
        console.error('Failed to copy: ', err);
      });
    });
  });
});
