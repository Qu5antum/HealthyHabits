// =====================
// API CONFIG
// =====================
const API_BASE = "http://127.0.0.1:8000";

// =====================
// LOGIN
// =====================
async function login() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!username || !password) {
        alert("Kullanıcı adı ve şifre zorunludur");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch(`${API_BASE}/user/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData
    });

    const data = await res.json();

    if (res.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("message").innerText = data.detail || "Login hatası";
    }
}

// =====================
// REGISTER
// =====================
async function register() {
    const body = {
        username: document.getElementById("reg-username").value.trim(),
        usergmail: document.getElementById("reg-email").value.trim(),
        password: document.getElementById("reg-password").value.trim()
    };

    if (!body.username || !body.usergmail || !body.password) {
        alert("Tüm alanları doldurun");
        return;
    }

    const res = await fetch(`${API_BASE}/user/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    const data = await res.json();
    document.getElementById("message").innerText =
        res.ok ? "Kayıt başarılı" : data.detail;
}

// =====================
// UPDATE HEART RISK FORM
// =====================
document.getElementById("riskForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    if (!token) {
        alert("Giriş yapmanız gerekiyor");
        return;
    }

    const formData = new FormData(e.target);

    // ===== REQUIRED NUMBERS =====
    const age = Number(formData.get("age"));
    const heightCm = Number(formData.get("height"));
    const weightKg = Number(formData.get("weight"));

    if (!age || !heightCm || !weightKg) {
        alert("Yaş, boy ve kilo zorunludur");
        return;
    }

    const heightM = heightCm / 100;
    const BMI = +(weightKg / (heightM * heightM)).toFixed(2);

    const data = {
        age: Number(age),                      // ОБЯЗАТЕЛЬНО число
        sex: formData.get("sex"),
        smoke: formData.get("smoke"),
        alcohol: formData.get("alcohol"),
        height: Number(formData.get("height")),
        weight: Number(formData.get("weight")),
        stroke: formData.get("stroke"),

        physical_health: Number(formData.get("physical_health")) || 0,
        mental_health: Number(formData.get("mental_health")) || 0,

        difficulty_walking: formData.get("difficulty_walking"),
        physical_activity: formData.get("physical_activity"),
        general_health: formData.get("general_health"),

        sleep: Number(formData.get("sleep")) || 0,
        high_sugar_level: formData.get("high_sugar_level"),

        asthma: formData.get("asthma"),
        kidney_problems: formData.get("kidney_problems"),
        skin_diseases: formData.get("skin_diseases"),
    };  

    const res = await fetch(`${API_BASE}/heart_risk_form/update`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(data)
    });
    window.location.href = "result.html";
});

// =====================
// AGE CATEGORY MAP
// =====================
function mapAge(age) {
    if (age < 25) return "18-24";
    if (age < 30) return "25-29";
    if (age < 35) return "30-34";
    if (age < 40) return "35-39";
    if (age < 45) return "40-44";
    if (age < 50) return "45-49";
    if (age < 55) return "50-54";
    if (age < 60) return "55-59";
    if (age < 65) return "60-64";
    if (age < 70) return "65-69";
    if (age < 75) return "70-74";
    if (age < 80) return "75-79";
    return "80 or older";
}

// =====================
// LOAD RESULTS
// =====================
async function loadResults() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/heart_risk_form`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();

        // 1. Отрисовка текстовой части
        let html = `
            <div class="result-card">
                <p><b>Risk:</b> ${data.User_risk_percent}</p>
                <p><b>Seviye:</b> ${data.User_risk_level}</p>
                <p><b>Kulanıcı ile aynı yaş ve cinsiyet olan insanlar:</b> ${data.group_size_by_user_age_and_sex}</p>
                <p><b>Ortalama grubun risk sevieysi</b> ${data.average_group_risk}</p>
                <p><b>İnme sonuçları:</b> ${data.interpretation}</p>
                <p><b>Yorum:</b> ${data.difference}</p>
            </div>
            <h3>Sizin gibi aynı yaşı ve cinsiyeti hem düşük riskli olan insanların farklılıklar</h3>
            <ul class="diff-list">
        `;

        data["Sizin yaş ve cinsiyet grubundaki kişilerin"].forEach(i => {
            html += `<li>${i}</li>`;
        });
        html += "</ul>";
        
        document.getElementById("result").innerHTML = html;

        // 2. Создание графика
        renderChart(
            parseFloat(data.User_risk_percent), 
            parseFloat(data.average_group_risk)
        );

        const strokeData = parseStrokePercentages(data.interpretation);
        if (strokeData) {
            renderStrokeChart(
                strokeData.strokeYes,
                strokeData.strokeNo
            );
        }

        if (data.differences_numeric) {
            renderDiffChart(data.differences_numeric);
        }

    } catch (error) {
        console.error("Hata:", error);
    }
}

function renderChart(userRisk, groupAvg) {
    const ctx = document.getElementById('riskChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar', // Столбчатая диаграмма
        data: {
            labels: ['Sizin Riskiniz', 'Grup Ortalaması'],
            datasets: [{
                label: 'Risk Oranı (%)',
                data: [userRisk, groupAvg],
                backgroundColor: [
                    userRisk > 50 ? '#ef4444' : '#3b82f6', // Красный если риск > 50%, иначе синий
                    '#94a3b8' // Серый для группы
                ],
                borderRadius: 8,
                barThickness: 40
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { callback: value => value + '%' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: true }
            }
        }
    });
}


function parseStrokePercentages(text) {
    const matches = text.match(/(\d+(\.\d+)?)/g);

    if (!matches || matches.length < 2) return null;

    return {
        strokeYes: parseFloat(matches[0]),
        strokeNo: parseFloat(matches[1])
    };
}


function renderStrokeChart(yes, no) {
    const ctx = document.getElementById("strokeChart");

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["İnme Geçirmiş", "Geçirmemiş"],
            datasets: [{
                data: [yes, no],
                backgroundColor: ["#ef4444", "#22c55e"]
            }]
        }
    });
}

function renderDiffChart(diffData) {
    if (!diffData) return;

    const labels = [];
    const values = [];

    if (diffData.BMI != null) {
        labels.push("BMI farkı");
        values.push(diffData.BMI);
    }

    if (diffData.MentalHealth != null) {
        labels.push("Mental sağlık (gün)");
        values.push(diffData.MentalHealth);
    }

    if (diffData.Smoking != null) {
        labels.push("Sigara oranı (%)");
        values.push(diffData.Smoking);
    }

    if (diffData.PhysicalActivity != null) {
        labels.push("Fiziksel aktivite");
        values.push(diffData.PhysicalActivity);
    }

    if (diffData.Alcohol != null) {
        labels.push("Alkol oranı (%)");
        values.push(diffData.Alcohol);
    }

    if (diffData.Sleep != null) {
        labels.push("Uyku farkı (saat)");
        values.push(diffData.Sleep);
    }

    if (labels.length === 0) return;

    const ctx = document.getElementById("diffChart");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: "#3b82f6",
                borderRadius: 8
            }]
        },
        options: {
            indexAxis: "y",
            plugins: { legend: { display: false } }
        }
    });
}


// =====================
// LOGOUT
// =====================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}
