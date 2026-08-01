const donorDatabase = [
    { name: "Rahul Sharma", blood: "O+", city: "Delhi", distance: 2.3, phone: "9876543210" },
    { name: "Priya Patel", blood: "A+", city: "Delhi", distance: 4.1, phone: "9876543211" },
    { name: "Amit Kumar", blood: "B+", city: "Gurgaon", distance: 5.7, phone: "9876543212" },
    { name: "Vikram Reddy", blood: "O+", city: "Delhi", distance: 1.8, phone: "9876543214" },
    { name: "Karan Joshi", blood: "O+", city: "Delhi", distance: 0.9, phone: "9876543218" },
    { name: "Sneha Gupta", blood: "A-", city: "Delhi", distance: 3.5, phone: "9876543215" },
    { name: "Ananya Rao", blood: "A+", city: "Bangalore", distance: 10.5, phone: "9876543219" },
];

const compatibilityMatrix = {
    'A+': ['A+', 'AB+'], 'A-': ['A+', 'A-', 'AB+', 'AB-'],
    'B+': ['B+', 'AB+'], 'B-': ['B+', 'B-', 'AB+', 'AB-'],
    'AB+': ['AB+'], 'AB-': ['AB+', 'AB-'],
    'O+': ['A+', 'B+', 'AB+', 'O+'],
    'O-': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
};

function findDonors(bloodGroup, city, urgency) {
    const compatibleGroups = compatibilityMatrix[bloodGroup] || [];
    let compatible = donorDatabase.filter(d => compatibleGroups.includes(d.blood));
    compatible = compatible.filter(d => d.city === city);
    if (compatible.length === 0) compatible = donorDatabase.filter(d => compatibleGroups.includes(d.blood));
    compatible.sort((a, b) => a.distance - b.distance);
    const multiplier = { 'critical': 0.3, 'urgent': 0.6, 'normal': 1.0 }[urgency] || 1.0;
    compatible = compatible.slice(0, 5).map(d => ({ ...d, priority: d.distance / 5 * multiplier }));
    return compatible;
}

document.getElementById('demoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const bloodGroup = document.getElementById('bloodGroup').value;
    const city = document.getElementById('city').value;
    const urgency = document.getElementById('urgency').value;
    const resultDiv = document.getElementById('demoResult');
    const errorDiv = document.getElementById('demoError');
    const donorListDiv = document.getElementById('donorList');
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    const donors = findDonors(bloodGroup, city, urgency);
    if (donors.length === 0) { errorDiv.style.display = 'block'; return; }
    let html = '<p style="margin-bottom:10px;color:#555;">✅ Found compatible donors:</p>';
    const emojis = ['🥇', '🥈', '🥉', '📍', '📍'];
    donors.forEach((d, i) => {
        html += `<div class="donor-item" style="display:flex;justify-content:space-between;background:white;padding:12px 18px;border-radius:8px;margin:8px 0;border-left:4px solid #2e7d32;">
            <span style="font-weight:700;color:#d7263d;">${emojis[i]}</span>
            <div style="flex:1;margin:0 15px;"><strong>${d.name}</strong><div style="font-size:0.85rem;color:#777;">🩸 ${d.blood} | 📍 ${d.city}</div></div>
            <span style="font-weight:600;color:#2e7d32;">${d.distance.toFixed(1)} km</span>
        </div>`;
    });
    donorListDiv.innerHTML = html;
    resultDiv.style.display = 'block';
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

document.querySelectorAll('.navbar a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.getElementById(this.getAttribute('href').substring(1));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});
