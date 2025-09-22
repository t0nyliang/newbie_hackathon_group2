// POST SECTION
let unlockedEmotes = ["laughing", "cry", "angry", "thumbsup"];
let posts = [];

// Called when someone posts a message
function postMessage(event) {
    event.preventDefault();
    const name = document.getElementById("playerName").value;
    const emote = document.querySelector('input[name="emote"]:checked').value;

    // Save the post
    const post = { name, emote, time: new Date().toLocaleTimeString() };
    posts.push(post);

    renderPosts();
    document.getElementById("postForm").reset();
}

// Render posts to the board
function renderPosts() {
    const postsDiv = document.getElementById("posts");
    postsDiv.innerHTML = "";

    posts.forEach(post => {
        const div = document.createElement("div");
        div.className = "post";
        // Determine image path for emote
        let imagePath = "";
        switch (post.emote) {
            case "laughing":
                imagePath = "images/laughing.png";
                break;
            case "angry":
                imagePath = "images/angry.jpg";
                break;
            case "cry":
                imagePath = "images/cry.jpeg";
                break;
            case "thumbsup":
                imagePath = "images/thumbsup.png";
                break;
            case "Mimimi":
                imagePath = "images/mimimi.png";
                break;
            case "yawn":
                imagePath = "images/PrincessYawning.png";
                break;
            case "nosepick":
                imagePath = "images/freakytony.png";
                break;
            case "trophy":
                imagePath = "images/CleaningTrophy.png";
                break;
            default:
                imagePath = `images/${post.emote}.png`;
        }
        div.innerHTML = `
          <img src="${imagePath}" alt="${post.emote}" width="40"/>
          <strong>${post.name}</strong> 
          <span>posted an emote at ${post.time}</span>
        `;
        postsDiv.appendChild(div);
    });
}

// Unlock a new emote (called from shop purchase)
function unlockEmote(emoteName, imagePath) {
    if (!unlockedEmotes.includes(emoteName)) {
        unlockedEmotes.push(emoteName);
        // Add it to the emote picker (message board)
        const picker = document.getElementById("emotePicker");
        const label = document.createElement("label");
        label.innerHTML = `
                    <input type="radio" name="emote" value="${emoteName}" />
                    <img src="${imagePath}" alt="${emoteName}" />
                `;
        picker.appendChild(label);
    }
}

// GAME SECTION
let cards = [];
let currentCard = null;
let gems = 20;

async function loadCards() {
    const res = await fetch("tony.json");
    const data = await res.json();
    cards = data.cards;
    startRound();
}

function startRound() {
    console.log("execute startRound()")
    // Reset UI
    document.getElementById("result").textContent = "";
    document.getElementById("choices").innerHTML = "";

    // Pick a random card
    currentCard = cards[Math.floor(Math.random() * cards.length)];

    // Display presented card
    const presented = document.getElementById("presented-card");
    presented.innerHTML = `
    <h3>${currentCard.name}</h3>
    <img src="${currentCard.image}" alt="${currentCard.name}" class="card-img">
  `;

    // Build 3 random wrong choices
    let wrongChoices = cards
        .filter(c => c.name !== currentCard.name && c.name !== currentCard.counter)
        .sort(() => 0.5 - Math.random())
        .slice(0, 3);

    // Add the correct answer
    let allChoices = [...wrongChoices, cards.find(c => c.name === currentCard.counter)];

    // Shuffle choices
    allChoices.sort(() => 0.5 - Math.random());

    // Display choices
    const choiceContainer = document.getElementById("choices");
    allChoices.forEach(choice => {
        const btn = document.createElement("button");
        btn.className = "choice-btn";
        btn.innerHTML = `<img src="${choice.image}" alt="${choice.name}" class="card-img"><br>${choice.name}`;
        btn.onclick = () => checkAnswer(choice);
        choiceContainer.appendChild(btn);
    });
}

function checkAnswer(selected) {
    const result = document.getElementById("result");
    if (selected.name === currentCard.counter) {
        gems += 10;
        document.getElementById("gem-count").textContent = gems;
        result.textContent = `✅ Correct! You earned 10 gems.`;
    } else {
        result.textContent = `❌ Wrong! The counter was ${currentCard.counter}.`;
    }
}

document.getElementById("next-round").addEventListener("click", startRound);

loadCards();

//SHOP SECTION

// Update the gem count in the header
function updateGemDisplay() {
    document.getElementById("gem-count").textContent = gems;
}

// Unlock a new emote and add to picker
function unlockEmote(emoteName, imagePath) {
    if (!unlockedEmotes.includes(emoteName)) {
        unlockedEmotes.push(emoteName);
        // Add it to the emote picker (message board)
        const picker = document.getElementById("emotePicker");
        const label = document.createElement("label");
        label.innerHTML = `
          <input type="radio" name="emote" value="${emoteName}" />
          <img src="${imagePath}" alt="${emoteName}" />
        `;
        picker.appendChild(label);
    }
}

// Hook into shop
function setupShop() {
    document.querySelectorAll(".buy-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            console.log("Buy button clicked");
            const emote = btn.parentElement.getAttribute("data-emote");
            const price = parseInt(btn.getAttribute("data-price"));
            let imagePath = btn.parentElement.querySelector('img').getAttribute('src');
            if (gems >= price && !unlockedEmotes.includes(emote)) {
                gems -= price;
                updateGemDisplay();
                btn.disabled = true;
                btn.textContent = "Owned ✅";
                unlockEmote(emote, imagePath);
            }
        });
    });
}

// On load
document.addEventListener("DOMContentLoaded", () => {
    updateGemDisplay();
    setupShop();
    setupDiscussion();
});

// Handle posting messages
function setupDiscussion() {
    const form = document.getElementById("postForm");
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = document.getElementById("playerName").value;
        const emote = document.querySelector('input[name="emote"]:checked').value;
        const postsDiv = document.getElementById("posts");
        const post = document.createElement("div");
        post.className = "post";
        // Use the same image path logic as renderPosts
        let imagePath = "";
        switch (emote) {
            case "laughing":
                imagePath = "images/laughing.png";
                break;
            case "cry":
                imagePath = "images/cry.jpeg";
                break;
            case "angry":
                imagePath = "images/angry.png";
                break;
            case "thumbsup":
                imagePath = "images/thumbsup.png";
                break;
            default:
                imagePath = `images/emotes/${emote}.png`;
        }
        post.innerHTML = `<strong>${name}:</strong> <img src="${imagePath}" alt="${emote}" width="40">`;
        postsDiv.appendChild(post);
        form.reset();
    });
}

// Initialize shop & discussion
document.addEventListener("DOMContentLoaded", () => {
    updateGemDisplay();
    setupShop();
    setupDiscussion();
});

