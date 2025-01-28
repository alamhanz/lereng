const geojsonData = {{ geojson_data | safe }};

const width = 800;
const height = 400;

const svg = d3.select("#map").attr("width", width).attr("height", height);
const mapGroup = svg.append("g");

const colorScale = d3.scaleSequential()
    .interpolator(d3.interpolateRgbBasis(["red", "white", "blue"]))
    .domain([0, 100]);

const projection = d3.geoMercator().translate([width / 2, height / 2]).scale(100);
const path = d3.geoPath().projection(projection);

const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .on("zoom", (event) => mapGroup.attr("transform", event.transform));

svg.call(zoom);

// Extract all numbers and dynamically set the color scale domain
const numbers = geojsonData.features.map(d => d.properties.numbers || 0);
const minValue = d3.min(numbers);
const maxValue = d3.max(numbers);

const adjustedColorScale = d3.scaleSequential()
    .interpolator(d3.interpolateRgbBasis(["red", "white", "blue"]))
    .domain([minValue, maxValue]);

const legendContainer = d3.select("#legend-container");

legendContainer.append("div").text(minValue);
legendContainer.append("div")
    .style("height", "10px")
    .style("width", "100px")
    .style("background", "linear-gradient(to right, red, white, blue)");
legendContainer.append("div").text(maxValue);

projection.fitSize([width, height], geojsonData);

mapGroup.selectAll("path")
    .data(geojsonData.features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", d =>
        d.properties.numbers === undefined || d.properties.numbers === null
            ? "yellow"
            : adjustedColorScale(d.properties.numbers || 0)
    )
    .attr("stroke", "#333")
    .attr("stroke-width", 0.5)
    .on("mouseover", function(event, d) {
        d3.select(this).classed("hovered", true);
        tooltip.style("opacity", 1)
            .html(`
                <strong>Area:</strong> ${d.properties.area_name || 'Unknown'}<br>
                <strong>Value:</strong> ${d.properties.numbers !== undefined && d.properties.numbers !== null ? d.properties.numbers : 'N/A'}
            `)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 20) + "px");
    })
    .on("mousemove", function(event) {
        tooltip.style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 20) + "px");
    })
    .on("mouseout", function() {
        d3.select(this).classed("hovered", false);
        tooltip.style("opacity", 0);
    });
