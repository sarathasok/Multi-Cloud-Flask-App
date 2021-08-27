var incircle = {
  x: x,
  y: dat,
  type: 'scatter',
  name: 'Estimated pi'
};

var pie = {
  x: x,
  y: pie,
  type: 'scatter',
  name: 'Real Pi'
};



var data = [incircle,pie];

Plotly.newPlot('myDiv', data);

