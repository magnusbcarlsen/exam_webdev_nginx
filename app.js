function newMarker(properties) {
  properties = JSON.parse(properties);
  for (let index = 0; index < properties.length; index++) {
    console.log(properties[index]);

    var marker = new mapboxgl.Marker()
      .setLngLat([properties[index].property_lat, properties[index].property_lon])
      .addTo(map);

    markers.push(marker);
  }
}
