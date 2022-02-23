
var hist_endpoint = '/api/data/';
var default_score = 0.8;

var final_hist_endpoint = hist_endpoint + String(default_score);



function generateHistogram(data){
  console.log(data);

}

$.ajax({
  method: "GET",
  url: final_hist_endpoint,
  success: function(data){
    generateHistogram(data);
  },
  error: function(error_data){
    console.log(error_data);
  }
})
