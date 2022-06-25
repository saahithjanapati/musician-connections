


//from https://d3-graph-gallery.com/graph/barplot_horizontal.html



function barChart(data){
    if(data.length ==0){
        return
    }
    // console.log(data)
    data.sort(function(a, b){
        return (a["num_collabs"] - b["num_collabs"]);
    });
    data.reverse();

// set the dimensions and margins of the graph
var margin = {top: 20, right: 30, bottom: 40, left: 200},
    width = 1000 - margin.left - margin.right,
    height = 1000*(data.length/92) - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_barchart")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Parse the Data
// d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/7_OneCatOneNum_header.csv", function(data) {

  // Add X axis
  var x = d3.scaleLinear()
    .domain([0, data[0]["num_collabs"]*1.2])
    .range([ 0, width]);
  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
      .attr("transform", "translate(-10,0)rotate(-45)")
      .style("text-anchor", "end")

      

  // Y axis
  var y = d3.scaleBand()
    .range([ 0, height ])
    .domain(data.map(function(d) { return d.name; }))
    .padding(.1);
  svg.append("g")
    .call(d3.axisLeft(y))

  //Bars
  svg.selectAll("myRect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", x(0) )
    .attr("y", function(d) { return y(d.name); })
    .attr("width", function(d) { return x(d.num_collabs); })
    .attr("height", y.bandwidth() )
    .attr("fill", "#69b3a2")
}