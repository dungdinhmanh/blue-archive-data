document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('data/students.json');
        const students = await response.json();
        
        const grid = document.getElementById('student-grid');
        
        students.forEach(student => {
            const card = document.createElement('div');
            card.className = 'student-card';
            
            card.innerHTML = `
                <img src="images/student/icon/${student.Id}.webp" 
                     alt="${student.Name}" 
                     class="student-icon"
                     onerror="this.src='images/student/portrait/${student.Id}.webp'">
                <div class="student-name">${student.Name}</div>
                <div class="student-school">${student.School}</div>
            `;
            
            grid.appendChild(card);
        });
        
    } catch (error) {
        console.error('Error loading student data:', error);
    }
});