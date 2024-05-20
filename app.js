var markers = [];
var map;

const getPropertyData = async () =>
  fetch('/properties')
    .then(res => res.json())
    .then(properties => properties);

const getMapboxToken = async () =>
  fetch('/mapbox_token')
    .then(res => res.json())
    .then(data => {
      return data.mapbox_token;
    });

const fetches = async () => {
  const properties = await getPropertyData();
  mapboxgl.accessToken = await getMapboxToken();
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [12.5683, 55.6761],
    zoom: 12,
  });

  newMarker(properties);
};

fetches();

function addProperties(properties) {
  properties = JSON.parse(properties);

  for (let index = 0; index < properties.length; index++) {
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
    document
      .getElementById('property_' + properties[index].property_pk)
      .addEventListener('click', function () {
        map.flyTo({
          center: [properties[index].property_lat, properties[index].property_lon],
          zoom: 15,
          speed: 5,
          curve: 0,
        });
      });
  }

  markers.push(marker);
}

function newMarker(properties, mapbox_token) {
  for (let index = 0; index < properties.length; index++) {
    console.log(properties);

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

    const marker = new mapboxgl.Marker()
      .setLngLat([properties[index].property_lat, properties[index].property_lon])
      .setPopup(popup)
      .addTo(map);

    markers.push(marker);
    document
      .getElementById('property_' + properties[index].property_pk)
      .addEventListener('click', function () {
        map.flyTo({
          center: [properties[index].property_lat, properties[index].property_lon],
          zoom: 15,
          speed: 5,
          curve: 1,
        });
      });
  }
}
