
var HIST_ENDPOINT = '/api/data/user_hist';
var SCORE_ENDPOINT = '/api/data/score_distribution'

var REDIRECT_USER_ENDPOINT = '/analise?'

var final_height = 925;
var final_width = 2500;


function getHistogramValues(){
  var hist_score = document.getElementById("cowbell_value").innerHTML;
  var checkedValue = $("#verified").is(":checked");  
  (checkedValue) ? checkedValue = "True" : checkedValue = "False";
  return [hist_score,checkedValue];
}


document.addEventListener("DOMContentLoaded", function(event){
  var rl = $("input:radio[name ='distributionValue']:checked").val();
  drawScoreDistribution(rl);

  var hist_score = document.getElementById("cowbell_value");
  drawHistogram();
  
  document.getElementById("cowbell").addEventListener('input', function(){
    hist_score.innerHTML = this.value;
    drawHistogram();
  });  
  document.getElementById("verified").addEventListener('click', () => {
    drawHistogram();
  })

  document.querySelectorAll("input[name='distributionValue']").forEach((input) => {
    input.addEventListener('change', () => {
      var rl = $("input:radio[name ='distributionValue']:checked").val();
      drawScoreDistribution(rl);

    });
});
});


function drawHistogram(){
  var hist_values = getHistogramValues();
  value = hist_values[0]
  verified = hist_values[1]
  console.log(value, verified)
  
  var final_endpoint =  HIST_ENDPOINT + `?verified=${verified}&score=${value}`;
  fetch(final_endpoint, {method: 'GET'})
  .then(response => response.json())
  .then(response => {generateHistogram(response, value)})
  .catch(error => console.log(error));  
}

function generateHistogram(data, score){  
  let chartStatus = Chart.getChart("histogramUser");
  if (chartStatus != undefined) {
    chartStatus.destroy();
  };
  
  var ctx = document.getElementById("histogramUser");  
  
  ctx.height = final_height;
  ctx.width = final_width;
  
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Object.keys(data),
        datasets: [{
            label: `Quantidade de Tweets acima do score ${score}`,
            data: Object.values(data),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',

            ],
            borderWidth: 1
          }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Identificador do usuário',
            font: {
              family: 'Times',
              size: 20,
              weight: 'bold',
              lineHeight: 1.2,
            }
          }
        },
        y: {
          title: {
            display: true,
            text: 'Quantidade de Tweets',
            font: {
              family: 'Times',
              size: 20,
              weight: 'bold',
              lineHeight: 1.2,
            },
            
          }
        }
      },
      'onClick': function (evt, item) {
        try {
          var clicked_bar = item[0]['index'];
          var user_id = Object.keys(data)[clicked_bar];          
          fetch(REDIRECT_USER_ENDPOINT + new URLSearchParams({
          search_bar: `{{%${user_id}%}}|`,
          min_value: "",
          score_min: score
          }), {method: 'GET'}).then(response => {
            window.open(response.url, '_blank');
          });
        } catch (TypeError) {
          console.log('Não foi clicado em uma parte válida do gráfico.');
        }
      },
    },
  });
}





function drawScoreDistribution(value=7){  
  var final_endpoint =  SCORE_ENDPOINT + `?days=${value}`;
  fetch(final_endpoint, {method: 'GET'})
  .then(response => response.json())
  .then(response => {generateScoreDistribution(response)})
  .catch(error => console.log(error));  
}


function generateScoreDistribution(data){  
  let chartStatus = Chart.getChart("scoreDistribution");
  if (chartStatus != undefined) {
    chartStatus.destroy();
  };
  
  var ctx = document.getElementById("scoreDistribution");  
  
  ctx.height = final_height;
  ctx.width = final_width;
  
  console.log(Object.keys(data))

  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels:Object.keys(data),
        datasets: [{
            label: `Quantidade de Tweets`,
            data: Object.values(data),
            backgroundColor: [
              'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
              'rgb(201, 203, 207)'
            ],
            borderWidth: 1
          }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Scores',
            font: {
              family: 'Times',
              size: 20,
              weight: 'bold',
              lineHeight: 1.2,
            }
          },
          ticks: {
            
            callback: (value, index, values) => { 
              if(index % 5 === 0 || index === Object.keys(data).length - 1){
                return Object.keys(data)[index]
              }
            }      
          }
        },
        y: {
          title: {
            display: true,
            text: 'Quantidade de Tweets',
            font: {
              family: 'Times',
              size: 20,
              weight: 'bold',
              lineHeight: 1.2,
            },
          }
        }
      }
    },
  });
}

