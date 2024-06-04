ymaps.ready(init);
function init() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function (position) {
            let coordLat = position.coords.latitude;
            let coordLong = position.coords.longitude;


        let myMap = new ymaps.Map("map", {
            center: [coordLat, coordLong],
            zoom: 15
        }, {
            searchControlProvider: 'yandex#search'
        });

        let req = new XMLHttpRequest();

        req.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let contacts = JSON.parse(this.responseText);

                for (const cont of Object.values(contacts)) {
                    let object = ymaps.geocode(`${cont['addr'][0]['PROVINCE']}, ${cont['addr'][0]['CITY']}, ${cont['addr'][0]['ADDRESS_1']}`)
                    object.then(function (res) {
                        let coor = res.geoObjects.properties._data.metaDataProperty.GeocoderResponseMetaData.Point.coordinates
                        let photo_tag = ''
                        if (cont['photo']) {
                            photo_tag = `<img src="https://pamtestrukkk.bitrix24.ru/${cont['photo']}" width="50" height="50">`
                        }
                        myMap.geoObjects.add(new ymaps.Placemark([coor[1], coor[0]], {balloonContent:
                                `<a href="https://pamtestrukkk.bitrix24.ru/crm/contact/details/${cont['cont_id']}/"><strong>${cont['name']}</strong></a>`
                                + '<br/>' + `${cont['addr'][0]['PROVINCE']}, ${cont['addr'][0]['ADDRESS_1']}` + '<br/>' + `${photo_tag}`},));
                    })
                }
            }
        };

        req.open("GET", "/my_company_on_map/handler/");
        req.send();
        });
    }
}
