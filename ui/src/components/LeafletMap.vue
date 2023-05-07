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
        fastapiResponse: null,
        textVal: ' with text param',
        zoomLevel: 2,
        lfZoom: 3,
        lfBbox: [10.8984375, -37.94677734375, 37.41943359375, -16.8310546875],
        center: [-30.36, 25.14]
        
        }

    },

    methods: {

    setupLeafletMap: function () {
        const mapDiv = L.map("mapContainer").setView(this.center, this.zoomLevel);
        L.tileLayer(
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            {
                attribution:
                'Map data (c) <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
            }
        ).addTo(mapDiv);
    },

    async getData() {
        try {
                const response = await axios.get(
                    `http://127.0.0.1:80/h3_on_the_fly`, {
                        params: {
                            z_level: this.zoomLevel,
                        }
                    }
                );

                this.fastapiResponse = response.data;

        } catch (error) {
            console.log(error);
        }

        },

    },

    beforeMount() {
       this.getData()
    },
    mounted() {
        this.setupLeafletMap();
    },


};

</script>

<style scoped>
#mapContainer {
 width: 80vw;
 height: 100vh;
}
</style>