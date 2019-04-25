<template>
  <div class="container">
    <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand href="http://localhost:8081/airbnb">Database Final Project</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item href="http://localhost:8081/airbnb">Find Restaurant</b-nav-item>
        <b-nav-item href="http://localhost:8081/yelp">Find Airbnb</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form disable>
          <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
          <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
        </b-nav-form>

      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
    <div class="row">

      <div class="col-sm-10">
        <hr>
        <h1>Restaurants</h1>
        <hr><br><br>
<div :style="{ width:'200px'}">
  <div class="mt-2">Enter Category: {{ rest_cate }}</div>
    <b-form-input v-model="rest_cate" placeholder="Enter Category"></b-form-input>

  </div>
    <div :style="{ width:'120px'}">
    <label for="range-1">Min Price {{ min_price }}</label>
    <b-form-input id="range-1" v-model="min_price" type="range" min="0" max="4"></b-form-input>
  </div>
      <div :style="{ width:'120px'}">
      <label for="range-2">Max Price {{ max_price }}</label>
      <b-form-input id="range-2" v-model="max_price" type="range" min="0" max="4"></b-form-input>
    </div>
        <div :style="{ width:'120px'}">
        <label for="range-2">Min Rating {{ min_rating }}</label>
        <b-form-input id="range-2" v-model="min_rating" type="range" min="1" max="5"></b-form-input>
      </div>
          <div :style="{ width:'120px'}">
          <label for="range-4">Max Rating {{ max_rating }}</label>
          <b-form-input id="range-4" v-model="max_rating" type="range" min="1" max="5"></b-form-input>
        </div>

        <button v-on:click="onSearch" class="btn btn-success btn-sm">Search</button>
        <h3>{{this.errormessage}}</h3>
        <br><br>

        <div>
    <br/>

    <GmapMap style="width: 500px; height: 300px;" :zoom="10" :center="{lat: 40.759, lng: -73.985}">
      <GmapMarker v-for="(marker, index) in markers"
        :key="index"
        :position="marker.position"
        />
    </GmapMap>
  </div>
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Category</th>
              <th scope="col">Price</th>
              <th scope="col">Rating</th>
              <th scope="col">Address</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(restaurant, index) in restaurants" :key="index">
              <td ><a :href="restaurant.url">{{ restaurant.name }}</a></td>
              <td>{{ restaurant.category }}</td>
              <td>{{ restaurant.price }}</td>
              <td>{{ restaurant.rating }}</td>
              <td>{{ restaurant.address }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      restaurants: [],
      rest_cate: '',
      allCate: [],
      min_price: 0,
      max_price: 4,
      min_rating: 1,
      max_rating: 5,
      markers: [],
      place: null,
      errormessage: '',
    };
  },
  methods: {
    getRestaurants() {
      const path = 'http://localhost:8080/allRestaurant';
      axios.get(path)
        .then((res) => {
          this.restaurants = res.data.restaurants;
          this.markers=res.data.markers;
          console.log(this.markers)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCategory() {
      const path = 'http://localhost:8080/allCategory';
      axios.get(path)
        .then((res) => {
          this.allCate = res.data.category;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSearch(evt) {
      evt.preventDefault();
      const path = 'http://localhost:8080/allRestaurant';
      const payload = {
        category: this.rest_cate,
        min_price: this.min_price,
        max_price:this.max_price, // property shorthand
        min_rating: this.min_rating,
        max_rating: this.max_rating,
      };
      axios.post(path,payload)
        .then((res) => {
          if(res.data.status=='success'){
            this.restaurants = res.data.restaurants;
            this.markers=res.data.markers;
            this.errormessage=''
          }
          else{
            this.getRestaurants();
            this.errormessage='No result found!'
          }

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getRestaurants();
  },
};
</script>
