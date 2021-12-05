<template>
  <div class="container" id="search">
    <div class="w-100 shadow p-3 rounded bg-body">
      <h3 class="text-center">Поиск</h3>
      <div class="row mt-3">
        <div class="col-sm-12 col-md-6 col-xl-4">
          <p class="mb-3 fw-bold fs-4 text-center">Дата пропажи</p>
          <div class="input-group">
            <span class="input-group-text" id="basic-addon1">📅</span>
            <input
              type="text"
              name="date"
              id="date"
              class="form-control datepicker"
              data-date-end-date="0d"
              data-date-format="dd.mm.yyyy"
            />
          </div>
        </div>
        <div class="col-sm-12 col-md-6 col-xl-4">
          <p class="mb-3 fw-bold fs-4 text-center">Время пропажи</p>
          <div class="input-group">
            <span class="input-group-text" id="basic-addon1">🕜</span>
            <input type="text" name="time" id="time" class="form-control" />
          </div>
        </div>
        <div
          class="
            col-sm-12 col-md-6 col-xl-4
            offset-md-3 offset-xl-0
            mt-md-3 mt-xl-0
          "
        >
          <p class="mb-3 fw-bold fs-4 text-center">Адрес</p>
          <div class="form-group">
            <input type="text" name="time" id="time" class="form-control" />
          </div>
        </div>
      </div>
      <div class="row mt-3">
        <div class="col-sm-12 col-md-6 col-xl-4">
          <p class="mb-3 fw-bold fs-4 text-center">Окрас</p>
          <div class="d-flex justify-content-center">
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                v-model="color"
                value="light"
                name="colorRadio"
                id="colorRadio1"
              />
              <label class="form-check-label" for="colorRadio1"> Белый </label>
            </div>
            <div class="form-check ms-3">
              <input
                class="form-check-input"
                type="radio"
                value="dark"
                v-model="color"
                name="colorRadio"
                id="colorRadio2"
              />
              <label class="form-check-label" for="colorRadio"> Тёмный </label>
            </div>
            <div class="form-check ms-3">
              <input
                class="form-check-input"
                type="radio"
                v-model="color"
                value="multicolor"
                name="colorRadio"
                id="colorRadio3"
              />
              <label class="form-check-label" for="colorRadio3">
                Разноцветный
              </label>
            </div>
          </div>
        </div>
        <div class="col-sm-12 col-md-6 col-xl-4">
          <p class="mb-3 fw-bold fs-4 text-center">Длина хвоста</p>
          <div class="d-flex justify-content-center">
            <div class="form-check">
              <input
                class="form-check-input"
                type="radio"
                v-model="tail"
                value="short"
                name="tailRadio"
                id="tailRadio1"
              />
              <label class="form-check-label" for="tailRadio1">
                Короткий
              </label>
            </div>
            <div class="form-check ms-3">
              <input
                class="form-check-input"
                type="radio"
                v-model="tail"
                value="long"
                name="tailRadio"
                id="tailRadio2"
              />
              <label class="form-check-label" for="tailRadio2"> Длинный </label>
            </div>
          </div>
        </div>
        <div
          class="
            col-sm-12 col-md-6 col-xl-4
            offset-md-3 offset-xl-0
            mt-md-3 mt-xl-0
          "
        >
          <p class="mb-3 fw-bold fs-4 text-center">Порода</p>
          <select
            name="breed"
            id="breedSelect"
            class="form-select"
            v-model="breed"
          >
            <option selected disabled>Выберите породу</option>
            <option
              v-for="breed in breeds"
              :key="breed.value"
              :value="breed.value"
            >
              {{ breed.display }}
            </option>
          </select>
        </div>
      </div>
      <div class="d-flex justify-content-end mt-4">
        <button type="button" class="btn btn-primary" @click="onSubmit">
          Искать
        </button>
      </div>
    </div>
  </div>
  <div class="container mt-5" id="searchResult">
    <div v-if="searchResults.length > 0">
      <h3 class="text-center">Результаты поиска</h3>
      <div class="row">
        <div
          class="col-sm-12 col-md-6 col-xl-4"
          v-for="image in searchResults"
          :key="image.id"
        >
          <div class="search-result-item">
            <div class="search-result-item__image">
              <img
                :src="`http://127.0.0.1:8000/api/v1/images/${image.id}`"
                alt=""
                style="max-height: 400px"
                class="w-100"
              />
            </div>
            <div class="search-result-item__info">
              <p class="mb-0">
                <span class="fw-bold">Порода: </span
                >{{ image.attribute_values.breed }}
              </p>
              <p class="mb-0">
                <span class="fw-bold">Цвет: </span
                >{{ image.attribute_values.color }}
              </p>
              <p class="mb-0">
                <span class="fw-bold">Хвост: </span
                >{{ image.attribute_values.tail }}
              </p>
              <p class="mb-0">
                <span class="fw-bold">Адрес: </span
                >{{ image.attribute_values.address.address }}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex justify-content-center mt-3">
        <button type="button" class="btn btn-warning fs-4">
          Показать на карте
        </button>
      </div>
      <div class="w-100 mt-5">
        <h2 class="text-center">Карта городских камер</h2>
        <div id="map" style="height: 700px"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ymaps from "ymaps";

const HOST = "http://localhost:8000";

export default {
  name: "Search",
  data() {
    return {
      breeds: [],
      color: "light",
      tail: "short",
      breed: "",
      searchResults: [],
    };
  },
  methods: {
    init(maps) {
      let map = new maps.Map("map", {
        center: [55.735852, 37.543258],
        zoom: 10,
      });
      this.searchResults.forEach(function (result) {
        let geoData = JSON.parse(result.attribute_values.address.geoData.replaceAll("'", '"'));
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
    onSubmit() {
      let payload = { color: this.color, tail: this.tail };
      if (this.breed != "") payload.breed = this.breed;
      axios
        .get(HOST + "/api/v1/images/", { params: payload })
        .then((response) => {
          if (response.status == 200) {
            this.searchResults = response.data;
            ymaps.load().then(this.init);
          }
        });
    },
  },
  mounted() {
    axios.get(HOST + "/api/v1/common/breeds").then((response) => {
      this.breeds = response.data;
    });
  },
};
</script>