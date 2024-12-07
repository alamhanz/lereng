// Set SVG dimensions
const width = 800, height = 600;
const svg = d3.select(".map").attr("width", width).attr("height", height);

// Load GeoJSON file
d3.json("map_with_data.geojson").then(function(geojson) {
    // Define projection and path generator
    const projection = d3.geoMercator().fitSize([width, height], geojson);
    const path = d3.geoPath().projection(projection);

    // Define color scale based on 'numbers'
    const colorScale = d3.scaleSequential(d3.interpolateBlues)
        .domain(d3.extent(geojson.features, d => d.properties.numbers)); // Extent of the 'numbers'

    // Draw map
    svg.selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("fill", d => colorScale(d.properties.numbers)) // Color based on 'numbers'
        .attr("stroke", "#000")
        .attr("stroke-width", 0.5);

    // Add tooltips
    svg.selectAll("path")
        .on("mouseover", (event, d) => {
            const tooltip = `${d.properties.shp_file_name}: ${d.properties.numbers}`;
            console.log(tooltip); // Replace with a proper tooltip if needed
        });
});