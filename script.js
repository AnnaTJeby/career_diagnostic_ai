/**
 * CareerLens AI - Frontend Logic
 */

const API_BASE = "http://127.0.0.1:8000";
let currentQuestion = "";

// --- UI Helpers ---

function toggleLoading(btnId, isLoading) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    const span = btn.querySelector('span');
    if (isLoading) {
        btn.disabled = true;
        btn.dataset.originalText = span.innerText;
        span.innerHTML = '<div class="loader"></div> Processing...';
    } else {
        btn.disabled = false;
        span.innerText = btn.dataset.originalText;
    }
}

function updateDisplay(elementId, content, isError = false) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.innerText = content;
    el.style.color = isError ? 'var(--error)' : 'inherit';
}

// --- File Upload Logic ---

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('resumeFile');
    const fileNameDisplay = document.getElementById('file-name');

    if (dropZone && fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, e => { e.preventDefault(); e.stopPropagation(); }, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', e => {
            const files = e.dataTransfer.files;
            if (files.length) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) handleFileSelect(fileInput.files[0]);
        });
    }

    function handleFileSelect(file) {
        if (fileNameDisplay) {
            fileNameDisplay.innerText = `Selected: ${file.name}`;
            fileNameDisplay.style.display = 'block';
        }
    }
});

// --- API Handlers ---

async function handleAnalyzeResume() {
    const fileInput = document.getElementById('resumeFile');
    const file = fileInput ? fileInput.files[0] : null;

    if (!file) return alert("Please upload a resume file first.");

    toggleLoading("btn-analyze", true);
    updateDisplay("skills-output", "Analyzing resume...");

    try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch(`${API_BASE}/parse-resume`, {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        const skillsArray = data.extracted_skills || [];
        const skillsString = skillsArray.join(", ");
        
        // Save for next step
        localStorage.setItem("careerSkills", JSON.stringify(skillsArray));
        updateDisplay("skills-output", skillsString);
    } catch (err) {
        updateDisplay("skills-output", "Something went wrong. Make sure your FastAPI server is running.", true);
    } finally {
        toggleLoading("btn-analyze", false);
    }
}

async function handleSkillGap() {
    const savedSkills = JSON.parse(localStorage.getItem("careerSkills") || "[]");
    const role = document.getElementById("targetRole").value;

    if (!role.trim()) return alert("Please enter a target role.");
    if (savedSkills.length === 0) return alert("Please analyze your resume first.");

    toggleLoading("btn-gap", true);
    try {
        const res = await fetch(`${API_BASE}/check-skill-gap`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                target_role: role, 
                extracted_skills: savedSkills 
            })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        const content = `Score: ${data.job_fit_score}%\n\nMissing: ${data.missing_skills.join(", ")}`;
        updateDisplay("gap-output", content);
    } catch (err) {
        updateDisplay("gap-output", "Something went wrong during gap analysis.", true);
    } finally {
        toggleLoading("btn-gap", false);
    }
}

async function handleStartInterview() {
    const role = document.getElementById("targetRole").value || "Professional";
    
    toggleLoading("btn-start-interview", true);
    try {
        const res = await fetch(`${API_BASE}/interview-start`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role: role })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        currentQuestion = data.question;
        
        document.getElementById("ai-question-text").innerText = currentQuestion;
        document.getElementById("ai-question-container").style.display = "block";
        document.getElementById("interview-input-group").style.display = "block";
        document.getElementById("btn-interview").style.display = "block";
        document.getElementById("btn-start-interview").style.display = "none";
        
        updateDisplay("interview-output", "Interview started. AI is waiting for your answer.");
    } catch (err) {
        updateDisplay("interview-output", "Failed to start interview. Check your backend.", true);
    } finally {
        toggleLoading("btn-start-interview", false);
    }
}

async function handleInterview() {
    const answerInput = document.getElementById("interviewAnswer");
    const answer = answerInput.value;
    const role = document.getElementById("targetRole").value || "Professional";

    if (!answer.trim()) return alert("Please type an answer first.");

    toggleLoading("btn-interview", true);
    try {
        const res = await fetch(`${API_BASE}/interview`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                role: role,
                question: currentQuestion, 
                answer: answer 
            })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        updateDisplay("interview-output", `Previous Score: ${data.score}/10\n\nFeedback: ${data.feedback}`);
        
        currentQuestion = data.next_question;
        document.getElementById("ai-question-text").innerText = currentQuestion;
        answerInput.value = "";
    } catch (err) {
        updateDisplay("interview-output", "Something went wrong during interview simulation.", true);
    } finally {
        toggleLoading("btn-interview", false);
    }
}

// --- Voice Input (Mic) Logic ---

let recognition;
let isRecording = false;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
        const resultBox = document.getElementById("interviewAnswer");
        let finalTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            }
        }
        if (finalTranscript) {
            resultBox.value += (resultBox.value ? " " : "") + finalTranscript;
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        stopBtnRecording();
    };

    recognition.onend = () => {
        if (isRecording) {
            isRecording = false;
            document.getElementById("btn-mic").classList.remove("recording");
        }
    };
}

function toggleMic() {
    if (!recognition) {
        return alert("Speech Recognition is not supported in this browser. Please try Chrome or Edge.");
    }

    if (isRecording) {
        stopBtnRecording();
    } else {
        startBtnRecording();
    }
}

function startBtnRecording() {
    try {
        isRecording = true;
        recognition.start();
        document.getElementById("btn-mic").classList.add("recording");
        updateDisplay("interview-output", "Listening... Speak your answer now.");
    } catch (e) {
        console.error("Start recording failed:", e);
    }
}

function stopBtnRecording() {
    isRecording = false;
    recognition.stop();
    document.getElementById("btn-mic").classList.remove("recording");
    updateDisplay("interview-output", "Microphone turned off.");
}