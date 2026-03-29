/**
 * CareerLens AI - Frontend Logic
 */

const API_BASE = "http://127.0.0.1:8000";

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

// We delay getting elements until DOM is ready or handles specifically
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

        const res = await fetch(`${API_BASE}/analyze-resume/`, {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        const skillsString = Array.isArray(data.skills) ? data.skills.join(", ") : data.skills;
        localStorage.setItem("careerSkills", skillsString);
        updateDisplay("skills-output", skillsString);
    } catch (err) {
        updateDisplay("skills-output", "Something went wrong. Please check if the backend is running and supports file uploads.", true);
    } finally {
        toggleLoading("btn-analyze", false);
    }
}

async function handleSkillGap() {
    const savedSkills = localStorage.getItem("careerSkills");
    const role = document.getElementById("targetRole").value;

    if (!role.trim()) return alert("Please enter a target role.");
    if (!savedSkills) return alert("Please analyze your resume first to extract skills.");

    toggleLoading("btn-gap", true);
    try {
        const res = await fetch(`${API_BASE}/skill-gap/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ skills: savedSkills, role })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        updateDisplay("gap-output", data.analysis || "No analysis returned from engine.");
    } catch (err) {
        updateDisplay("gap-output", "Something went wrong during gap analysis.", true);
    } finally {
        toggleLoading("btn-gap", false);
    }
}

async function handleInterview() {
    const answer = document.getElementById("interviewAnswer").value;
    const role = document.getElementById("targetRole").value || "Professional";

    if (!answer.trim()) return alert("Please type an answer first.");

    toggleLoading("btn-interview", true);
    try {
        const res = await fetch(`${API_BASE}/interview/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role, answer })
        });

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();
        updateDisplay("interview-output", data.reply || "No feedback returned.");
    } catch (err) {
        updateDisplay("interview-output", "Something went wrong during interview simulation.", true);
    } finally {
        toggleLoading("btn-interview", false);
    }
}