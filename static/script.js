// Handle form submission
const form = document.getElementById("interview-form");
const feedbackSection = document.getElementById("feedback-section");
const feedback = document.getElementById("feedback");

form.onsubmit = async function (e) {
    e.preventDefault(); // Prevent the default form submission

    // Get form values
    const category = document.getElementById("category").value;
    const response = document.getElementById("response").value;

    // Validate form fields
    if (!category || !response) {
        alert("Please fill out all fields.");
        return;
    }

    try {
        // Send POST request to backend
        const res = await fetch("/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ category, response }),
        });

        // Handle backend response
        if (res.ok) {
            const data = await res.json();
            feedback.innerHTML = `
                <strong>Sentiment:</strong> ${data.sentiment}<br>
                <strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%<br>
                <strong>Relevance:</strong> ${data.relevance}<br>
                <strong>Relevance Score:</strong> ${(data.relevance_score * 100).toFixed(2)}%
            `;
            feedbackSection.style.display = "block";
        } else {
            throw new Error("Failed to fetch feedback from server.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again later.");
    }
};
