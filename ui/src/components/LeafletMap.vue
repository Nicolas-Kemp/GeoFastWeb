<template>
    <div id="container">
      <div id="mapContainer"></div>
    </div>
</template>


<script>

import axios from 'axios';
import "leaflet/dist/leaflet.css";
import L from "leaflet";

export default {
    name: 'leafletMap',

    data: function () {

        return {
        map: null,
        fastapiResponse: null,
        textVal: ' with text param',
        lfZoom: 4,
        lfBbox: [10.8984375, -37.94677734375, 37.41943359375, -16.8310546875],
        center: [-30.36, 25.14],
        hexData: [],
        uber_hex: L.geoJSON(),
        uber_hex_l2: L.geoJSON(),
        
        }

    },

    methods: {

    setupLeafletMap: function () {
        this.map = L.map("mapContainer").setView(this.center, this.lfZoom);
        L.tileLayer(
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution:
                'Map data (c) <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
            }
        ).addTo(this.map);

        this.mapElements();
    },

    async mapElements(){
      let mapElement = this.map;
      let ref = this;
      mapElement.on('zoomend, moveend', async function(e) {
        ref.run()
      });

    },

    async run() {

        let nowZoom = this.map.getZoom() - 3;
        let nowBbox = this.map.getBounds().toBBoxString();
        nowBbox = nowBbox.split(',');
        nowBbox = nowBbox.map(element => {
        return Number(element);
        });
        console.log(nowZoom)
        console.log(nowBbox)

        // this.hexData = await this.getData(nowZoom, nowBbox[1], nowBbox[3], nowBbox[0], nowBbox[2]);
        this.hexData = await this.getData(nowZoom, nowBbox[0], nowBbox[1], nowBbox[2], nowBbox[3]);

        this.map.removeLayer(this.uber_hex);
        this.uber_hex = JSON.parse(this.hexData);

        this.uber_hex = L.geoJSON(this.uber_hex);
        this.uber_hex.setStyle({ 
                                color: "#B39102",
                                weight:1,
                                fillOpacity:0
                            });
        this.uber_hex.addTo(this.map);
    },
    
    /*'southwest_lng,southwest_lat,northeast_lng,northeast_lat'*/
    async getData(zoomLevel, leftLong, bottomLat, rightLong, topLat) {
        try {
        const response = await axios.get(
            `http://127.0.0.1:80/h3_on_the_fly`, {
            params: {
                bottom_lat: bottomLat,
                top_lat: topLat,
                left_long: leftLong,
                right_long: rightLong,
                z_level: zoomLevel
            }
            }
        );

        return response.data;

        } catch (error) {
        console.log(error);
        }
    },

    },

    async mounted() {
        this.setupLeafletMap();
        this.uber_hex.addTo(this.map);
        this.hexData = await this.run();  
    },


};

</script>

<style scoped>
#mapContainer {
 width: 80vw;
 height: 100vh;
}
</style>