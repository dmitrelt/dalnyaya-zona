ymaps.ready(function () {
    var myMap = new ymaps.Map("map", {
        center: [55.997864, 37.226230],
        zoom: 15
    });

    var myPlacemark = new ymaps.Placemark([55.997864, 37.226230], {
        hintContent: 'Дальняя Зона',
        balloonContent: 'г. Москва, г. Зеленоград, ул. Юности, д.15'
    });

    myMap.geoObjects.add(myPlacemark);
});