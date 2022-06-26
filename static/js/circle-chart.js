//Adatped from: https://d3-graph-gallery.com/graph/circularpacking_template.html

let width = 1000;
let height = 1000;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
    // .attr("display", block)
    // .attr(auto);
    // .attr("class")
// svg {
//         display: block;
//         margin: 0 auto;
//     }
function circleChart(data){
    const color = d3.scaleOrdinal()
    .range(d3.schemeSet1);
    console.log(data);

    data.sort(function(a, b){
        return (a["num_collabs"] - b["num_collabs"]);
    });
    data.reverse();

    function getYPosition(){
        var top  = window.pageYOffset || document.documentElement.scrollTop
        return top;
      }

  // Size scale for countries
  const size = d3.scaleLinear()
    .domain([0, data[0]["num_collabs"]])
    .range([7,100])  // circle will be between 7 and 55 px wide

  // create a tooltip
  const Tooltip = d3.select("#my_dataviz")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("padding", "5px")

  // Three function that change the tooltip when user hover / move / leave a cell
  const mouseover = function(event, d) {
    Tooltip
      .style("opacity", 1)
  }

  const mousemove = function(event, d) {
    Tooltip
      .html(d.name + "<br>" + d.num_collabs + " collaborations")
      .style("left", (event.x)+40 + "px")
      .style("top", (event.y)+40+getYPosition() + "px")
      .style("color", "black")
      .style("font-size", "1vw")  }

  var mouseleave = function(event, d) {
    Tooltip
      .style("opacity", 0)
  }

  // Initialize the circle: all located at the center of the svg area
  var node = svg.append("g")
    .selectAll("circle")
    .data(data)
    .join("circle")
      .attr("class", "node")
      .attr("r", d => size(d.num_collabs))
      .attr("cx", width / 2)
      .attr("cy", height / 2)
      .style("fill", d => color(d.num_collabs))
      .style("fill-opacity", 0.8)
      .attr("stroke", "black")
      .style("stroke-width", 1)
      .on("mouseover", mouseover) // What to do when hovered
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave)
      .call(d3.drag() // call specific function when circle is dragged
           .on("start", dragstarted)
           .on("drag", dragged)
           .on("end", dragended));

  // Features of the forces applied to the nodes:
  const simulation = d3.forceSimulation()
      .force("center", d3.forceCenter().x(width / 2).y(height / 2)) // Attraction to the center of the svg area
      .force("charge", d3.forceManyBody().strength(.1)) // Nodes are attracted one each other of value is > 0
      .force("collide", d3.forceCollide().strength(.2).radius(function(d){ return (size(d.num_collabs)+3) }).iterations(1)) // Force that avoids circle overlapping

  // Apply these forces to the nodes and update their positions.
  // Once the force algorithm is happy with positions ('alpha' value is low enough), simulations will stop.
  simulation
      .nodes(data)
      .on("tick", function(d){
        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
      });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(.03).restart();
        d.fx = d.x;
        d.fy = d.y;
      }
      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }
      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(.03);
        d.fx = null;
        d.fy = null;
      }
    

}