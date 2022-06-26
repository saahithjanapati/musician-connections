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

    const color = d3.scaleOrdinal()
    .range(d3.schemeSet1);


    function getYPosition(){
        var top  = window.pageYOffset || document.documentElement.scrollTop
        return top;
      }


    const Tooltip = d3.select("#my_barchart")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

    const mouseover = function(event, d) {
        Tooltip
          .style("opacity", 1)
      }
      const mousemove = function(event, d) {
        Tooltip
          .html(d.num_collabs + " collaborations")
          .style("left", (event.x)+20 + "px")
          .style("top", (event.y)+20+ getYPosition()+ "px")
          .style("color", "black")
          .style("font-size", "1vw")
      }
      var mouseleave = function(event, d) {
        Tooltip
          .style("opacity", 0)
      }

// set the dimensions and margins of the graph
var margin = {top: 20, right: 30, bottom: 100, left: 400},
    width = 1750 - margin.left - margin.right,
    height = Math.max(400, 4000*(data.length/92)) - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_barchart")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

  .append("g")

    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Parse the Data

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
        .style("font", "30px times")


  // Y axis
  var y = d3.scaleBand()
    .range([ 0, height ])
    .domain(data.map(function(d) { return d.name; }))
    .padding(.1);
  svg.append("g")
    .call(d3.axisLeft(y))
    .selectAll("text")
    .style("font", "30px times")

  //Bars
  svg.selectAll("myRect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", x(0) )
    .attr("y", function(d) { return y(d.name); })
    .attr("width", function(d) { return x(d.num_collabs); })
    .attr("height", y.bandwidth() )
    .on("mouseover", mouseover) // What to do when hovered
    .on("mousemove", mousemove)
    .on("mouseleave", mouseleave)
    // .attr("fill", "#69b3a2")
    .style("fill", d => color(d.num_collabs))


}

