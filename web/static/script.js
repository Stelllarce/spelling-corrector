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
        if (event.key === " " && autoCorrectEnabled && lastSuggestions.length > 0) {
            event.preventDefault(); 
            const topSuggestion = lastSuggestions[0];
            replaceWord(topSuggestion);
            inputBox.value += " "; 
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

    if (inputText === "") {
        suggestionsDiv.innerHTML = "";
        lastSuggestions = []; 
        return;
    }

    let words = inputText.split(" ");
    let lastWord = words[words.length - 1];

    if (lastWord === "") {
        suggestionsDiv.innerHTML = "";
        lastSuggestions = [];
        return;
    }

    try {
        const response = await fetch(`http://localhost:5000/correct?word=${lastWord}`);
        const data = await response.json();
        lastSuggestions = data.suggestions || [];

        if (lastSuggestions.length === 0) {
            suggestionsDiv.innerHTML = "<p>No suggestions found.</p>";
            return;
        }

        let arrangedSuggestions = [];
        let left = true;
        while (lastSuggestions.length > 0) {
            if (left) {
                arrangedSuggestions.unshift(lastSuggestions.shift());
            } else {
                arrangedSuggestions.push(lastSuggestions.shift());
            }
            left = !left;
        }

        suggestionsDiv.innerHTML = arrangedSuggestions.map(word =>
            `<span class="suggestion" onclick="replaceWord('${word}')">${word}</span>`
        ).join("");

    } catch (error) {
        console.error("Error fetching suggestions:", error);
    }
}

function replaceWord(suggestion) {
    const inputBox = document.getElementById("wordInput");
    let words = inputBox.value.split(" ");

    if (words.length === 0) return;

    let lastWord = words[words.length - 1];

    let correctedWord;
    if (lastWord === lastWord.toUpperCase()) {
        correctedWord = suggestion.toUpperCase();
    } else if (lastWord.charAt(0).toUpperCase() === lastWord.charAt(0)) {
        correctedWord = suggestion.charAt(0).toUpperCase() + suggestion.slice(1);
    } else {
        correctedWord = suggestion.toLowerCase();
    }

    words[words.length - 1] = correctedWord; 
    inputBox.value = words.join(" "); 
}

function clearSuggestions() {
    setTimeout(() => {
        lastSuggestions = [];
        document.getElementById("suggestions").innerHTML = "";
    }, 100);
}