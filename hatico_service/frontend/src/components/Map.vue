<template>
  <div class="w-100 mt-5">
    <h2 class="text-center">Карта городских камер</h2>
    <div id="map" style="height: 700px"></div>
  </div>
</template>

<style>
.vue-map-container {
  height: 100%;
}
</style>

<script>
import axios from "axios";
import ymaps from "ymaps";

const HOST = "http://localhost:8000";

export default {
  name: "Map",
  data() {
    return {
      cameras: [],
    };
  },
  methods: {
    init(maps) {
      let map = new maps.Map("map", {
        center: [55.735852, 37.543258],
        zoom: 10,
      });
      this.cameras.forEach(function (camera) {
          let geoData = JSON.parse(camera.geoData.replaceAll("'", '"'));
          let longitude = geoData.coordinates[0];
          let latitude = geoData.coordinates[1];
        var myGeoObject = new maps.GeoObject({
          geometry: {
            type: "Point", // тип геометрии - точка
            coordinates: [latitude, longitude], // координаты точки
          },
        });

        // Размещение геообъекта на карте.
        map.geoObjects.add(myGeoObject);
      });
    },
  },
  mounted() {
    axios.get(HOST + "/api/v1/common/cameras").then((response) => {
      this.cameras = response.data;
      ymaps.load().then(this.init);
    });
  },
};
</script>