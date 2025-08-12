/**
 * AI Readiness Assessment Script
 * * This script handles the logic for the creative agency AI readiness quiz.
 * It validates that all questions are answered, calculates the score,
 * determines the readiness level, and displays the appropriate results.
 */
document.addEventListener('DOMContentLoaded', () => {

    // --- DOM Element Selection ---
    const quizForm = document.getElementById('quiz-form');
    const resultsSection = document.getElementById('results');
    const mainContent = document.querySelector('main');
    
    // Result display elements
    const scoreDisplay = document.getElementById('score-display');
    const levelIndicator = document.getElementById('level-indicator');
    const levelName = document.getElementById('level-name');
    const levelText = document.getElementById('level-text');
    
    // Error message element
    const errorMessage = document.getElementById('error-message');

    // --- Event Listener for Form Submission ---
    if (quizForm) {
        quizForm.addEventListener('submit', (event) => {
            // Prevent the default form submission which reloads the page
            event.preventDefault();

            // --- Validation ---
            const totalQuestions = 10;
            const selectedOptions = quizForm.querySelectorAll('input[type="radio"]:checked');

            if (selectedOptions.length < totalQuestions) {
                // If not all questions are answered, show the error message
                errorMessage.classList.remove('hidden');
                errorMessage.textContent = 'Please answer all questions before submitting.';
                return; // Stop the function execution
            }

            // If validation passes, hide the error message
            errorMessage.classList.add('hidden');

            // --- Score Calculation ---
            let totalScore = 0;
            selectedOptions.forEach(option => {
                // Add the integer value of the selected option to the total score
                totalScore += parseInt(option.value, 10);
            });

            // --- Display Results ---
            displayResults(totalScore);
        });
    }

    /**
     * Calculates and displays the final results based on the score.
     * @param {number} score - The user's total score.
     */
    function displayResults(score) {
        // Update the score display in the results section
        scoreDisplay.textContent = score;

        // Remove any previous color classes from the indicator
        levelIndicator.classList.remove('level-red', 'level-amber', 'level-green');

        // --- Determine Readiness Level and Set Content ---
        if (score <= 18) {
            // RED LIGHT: 10-18 points
            levelIndicator.classList.add('level-red');
            levelName.textContent = 'Red Light';
            levelText.textContent = "Your agency is at the beginning of its AI journey. There's a significant risk of being outpaced by more agile competitors. It's crucial to start building foundational AI literacy and exploring tools to avoid falling behind.";
        } else if (score <= 29) {
            // AMBER LIGHT: 19-29 points
            levelIndicator.classList.add('level-amber');
            levelName.textContent = 'Amber Light';
            levelText.textContent = "You're making some progress. Your agency has started to experiment with AI, but adoption is likely inconsistent. To gain a true competitive edge, you need a more structured strategy for training, tool integration, and workflow automation.";
        } else {
            // GREEN LIGHT: 30-40 points
            levelIndicator.classList.add('level-green');
            levelName.textContent = 'Green Light';
            levelText.textContent = "Excellent! Your agency is embracing the future. You have a strong foundation and are likely already seeing the benefits of AI. The next step is to scale your successes, explore advanced AI applications, and solidify your position as an industry leader.";
        }

        // --- UI Transition ---
        // Hide the quiz form and show the results section
        if (mainContent) mainContent.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        // Scroll the results into view for a smooth user experience
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});
