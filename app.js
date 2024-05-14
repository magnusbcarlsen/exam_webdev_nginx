function newMarker(properties) {
  properties = JSON.parse(properties);
  for (let index = 0; index < properties.length; index++) {
    console.log(properties[index]);

    var popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
      '<div class="property-card">' +
        '<img src="../images/' +
        properties[index].property_images +
        '" alt="property image" class="w-full aspect-square object-cover rounded-lg">' +
        '<div class="property-info flex flex-col-2">' +
        '<div>' +
        '<h3 class="font-bold">' +
        properties[index].property_name +
        '</h3>' +
        '<p>' +
        properties[index].property_description +
        '</p>' +
        '</div>' +
        '<div class="property-price font-semibold">' +
        properties[index].property_price_pr_night +
        ' DKK' +
        '</div>' +
        '</div>' +
        '</div>'
    );

    var marker = new mapboxgl.Marker()
      .setLngLat([properties[index].property_lat, properties[index].property_lon])
      .setPopup(popup)
      .addTo(map);

    markers.push(marker);
  }
}
