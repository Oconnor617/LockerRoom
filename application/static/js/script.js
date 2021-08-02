// Our labels along the x-axis
var date = ["7/15","7/16","7/17","7/18","7/19","7/20","7/21","7/22","7/23","7/24","7/25","7/26","7/27","7/28",
"7/29","7/30","7/31"];
// For drawing the lines
var weight = [235,235.3,234.8,234.8,234.5,235.3,234.6,234.2,233.9,233.5,233.1,232.8,232.4,231.6,230.6,230,229.6];

var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: date,
    datasets: [
      { 
        data: weight,
        label: "My Weight",
        borderColor: "#3e95cd",
        fill: false
      }
    ]
  }
});