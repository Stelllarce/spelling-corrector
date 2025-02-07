let typingTimer;
const debounceDelay = 300; 
let autoCorrectEnabled = false;
let lastSuggestions = []; 

document.addEventListener("DOMContentLoaded", function () {
    const inputBox = document.getElementById("wordInput");
    const outputBox = document.getElementById("correctedOutput");

    inputBox.addEventListener("input", function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(getSuggestions, debounceDelay);
    });

    inputBox.addEventListener("keydown", function (event) {
        // When space is pressed and auto-correct is enabled with available suggestions
        if (event.key === " " && autoCorrectEnabled && lastSuggestions.length > 0) {
            event.preventDefault(); 
            // Use the top suggestion as the best candidate
            const topSuggestion = lastSuggestions[0];  
            replaceWord(topSuggestion);
            // Ensure a space is appended if it isn’t already
            if (!inputBox.value.endsWith(" ")) {
                inputBox.value += " ";
            }
            clearSuggestions();
        }
    });

    inputBox.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            const text = inputBox.value.trim();
            if (text !== "") {
                outputBox.value = text; 
            }
            inputBox.value = ""; 
        }
    });
});

function toggleAutoCorrect() {
    autoCorrectEnabled = !autoCorrectEnabled;
    const button = document.getElementById("autoCorrectToggle");
    button.textContent = `Auto Correct: ${autoCorrectEnabled ? "ON" : "OFF"}`;
    button.classList.toggle("active", autoCorrectEnabled);
}

async function getSuggestions() {
    const inputBox = document.getElementById("wordInput");
    const suggestionsDiv = document.getElementById("suggestions");
    let inputText = inputBox.value.trim();

    // Show the loading spinner
    suggestionsDiv.innerHTML = `<div class="spinner"></div>`;
    lastSuggestions = []; 

    if (inputText === "") {
        suggestionsDiv.innerHTML = "";
        return;
    }

    let words = inputText.split(" ");
    let lastWord = words[words.length - 1];

    // If the last word is empty (due to trailing space), clear suggestions.
    if (lastWord === "") {
        suggestionsDiv.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/correct?word=${lastWord}`);
        const data = await response.json();
        // Get the suggestions from the server
        const suggestions = data.suggestions || [];

        if (suggestions.length === 0) {
            suggestionsDiv.innerHTML = "<p>No suggestions found.</p>";
            return;
        }

        // Arrange suggestions (alternating order)
        let suggestionsCopy = [...suggestions];
        let arrangedSuggestions = [];
        let left = true;
        while (suggestionsCopy.length > 0) {
            if (left) {
                arrangedSuggestions.unshift(suggestionsCopy.shift());
            } else {
                arrangedSuggestions.push(suggestionsCopy.shift());
            }
            left = !left;
        }

        lastSuggestions = arrangedSuggestions;

        suggestionsDiv.innerHTML = arrangedSuggestions.map(word =>
            `<span class="suggestion" onclick="replaceWord('${word}')">${word}</span>`
        ).join("");

    } catch (error) {
        console.error("Error fetching suggestions:", error);
        suggestionsDiv.innerHTML = "<p>Error loading suggestions.</p>";
    }
}

function replaceWord(suggestion) {
    const inputBox = document.getElementById("wordInput");
    // Split the text into words.
    let words = inputBox.value.split(" ");
    
    // If the last element is an empty string (trailing space), replace the word before it.
    let indexToReplace = words.length - 1;
    if (words[indexToReplace] === "" && words.length > 1) {
        indexToReplace = words.length - 2;
    }
    if (indexToReplace < 0) return;

    let targetWord = words[indexToReplace];

    let correctedWord;
    if (targetWord === targetWord.toUpperCase()) {
        correctedWord = suggestion.toUpperCase();
    } else if (targetWord.charAt(0) === targetWord.charAt(0).toUpperCase()) {
        correctedWord = suggestion.charAt(0).toUpperCase() + suggestion.slice(1);
    } else {
        correctedWord = suggestion.toLowerCase();
    }

    words[indexToReplace] = correctedWord; 
    // Reassemble the words with a space separator.
    inputBox.value = words.join(" ");
}

function clearSuggestions() {
    setTimeout(() => {
        lastSuggestions = [];
        document.getElementById("suggestions").innerHTML = "";
    }, 100);
}
