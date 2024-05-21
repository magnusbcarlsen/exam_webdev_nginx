var markers = [];
var map;

const getPropertyData = async () =>
	fetch('/properties')
		.then((res) => res.json())
		.then((properties) => properties);

const getMapboxToken = async () =>
	fetch('/mapbox_token')
		.then((res) => res.json())
		.then((data) => {
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
	console.log('added new properties', properties);
	newMarker(properties);
}

function newMarker(properties) {
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

		const marker = new mapboxgl.Marker()
			.setLngLat([
				properties[index].property_lat,
				properties[index].property_lon,
			])
			.setPopup(popup)
			.addTo(map);

		markers.push(marker);
		console.log(markers, 'marker');
		document
			.getElementById('property_' + properties[index].property_pk)
			.addEventListener('click', function () {
				console.log(markers);
				markers.forEach((marker) => marker.getPopup().remove());
				map.flyTo({
					center: [
						properties[index].property_lat,
						properties[index].property_lon,
					],
					zoom: 15,
					speed: 5,
					curve: 1,
				});
				marker.togglePopup();
			});
	}
}
const modal = document.querySelector('#page_modal');

function showModal() {
	modal.showModal();
	const closeButton = document.querySelector('#modal_close');
	closeButton.addEventListener('click', () => {
		modal.close();
	});

	window.addEventListener('click', function (event) {
		const modal = document.querySelector('#page_modal');
		if (event.target == modal) {
			modal.close();
		}
	});
}

function closeModal() {
	modal.close();
}
