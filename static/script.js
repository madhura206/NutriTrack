document.addEventListener("DOMContentLoaded", function () {
  const ring = document.querySelector('.progress-ring__circle');
  const label = document.getElementById('progress-label');

  if (!ring) return; // Exit if no ring found
  
  // Get all required data
  const totalWater = parseFloat(ring.dataset.totalWater) || 0;
  const waterGoal = parseFloat(ring.dataset.waterGoal) || 8;
  const totalCalories = parseFloat(ring.dataset.totalCalories) || 0;
  const calorieGoal = parseFloat(ring.dataset.calorieGoal) || 2000;
  
  // Calculate progress percentages
  const waterProgress = waterGoal > 0 ? Math.min(totalWater / waterGoal, 1) : 0;
  const calorieProgress = calorieGoal > 0 ? Math.min(totalCalories / calorieGoal, 1) : 0;
  
  // Calculate combined progress (weighted average)
  const overallProgress = (waterProgress + calorieProgress) / 2;
  const progressPercentage = Math.round(overallProgress * 100);

  // Set up the progress ring
  const radius = ring.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;

  ring.style.strokeDasharray = `${circumference}`;
  ring.style.strokeDashoffset = `${circumference - (circumference * overallProgress)}`;

  // Update label
  if (label) {
    label.innerHTML = `${progressPercentage}%<br><small>Overall</small>`;
  }
});

window.onload = function() {
    var form = document.querySelector('form');
    if (form) form.reset();
};
