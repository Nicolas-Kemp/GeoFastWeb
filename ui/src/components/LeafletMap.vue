<template>
    <div id="container">
        <img src="https://ogc.afrigis.co.za/mapservice/multichoice/wms?authkey=5ce3869b-5418-4e8c-935d-f7ac5e5bad2e&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER=mc_installer_travel_bands&STYLE=multichoice_travelband_12500" />
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
        //this.wmsCall();
        this.geotripz();
        this.geotripzWMS();
        this.mapElements();
    },

    async mapElements(){
      let mapElement = this.map;
      let ref = this;
    //   mapElement.on('zoomend, moveend', async function(e) {
    //     ref.run()
    //   });

    },

    async geotripz() {

        try {
        const response = await axios.get(
            `http://127.0.0.1:80/geotripz`, {
            params: {

                love_it: 'high_mountains_area',
                like_it: 'Tourism Attraction',
                rather_not: '',
                noway: 'HIGHWAY',

                }
            }
        );

        return response.data;

        } catch (error) {
            console.log(error);
        }
    },

    async geotripzWMS(){

        let url = 'https://dev-ogc.afrigis.co.za/mapservice/demo/wms?authkey=2db8a489-237a-42b0-a075-013780de0180'

        let geotripzLayer = 'geotripz_h3_output'
        let geotripzStyle = 'geotripz_likes'


        let geotripz_prestine_hotspots = L.tileLayer.wms(url, {
            layers: geotripzLayer,
            styles: geotripzStyle,
            transparent: true,
            opacity: 1,
            format: 'image/png',
            tiled: true
        }).addTo(this.map);

        console.log(geotripz_prestine_hotspots)

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

    async wmsCall(){

        let url = 'https://ogc.afrigis.co.za/mapservice/multichoice/wms?authkey=5ce3869b-5418-4e8c-935d-f7ac5e5bad2e'

        let mcInstaller = 'mc_installer_location'
        let mcTravelBand = 'mc_installer_travel_bands'
        let mcInfluenceBand = 'mc_influence_bands'

        let styleTravelband_12500 = 'multichoice_travelband_12500'
        let styleTravelband_25000 = 'multichoice_travelband_25000'
        let styleTravelband_50000 = 'multichoice_travelband_50000'

        // let mcInfluenceBandWMS = L.tileLayer.wms(url, {
        //     layers: mcInfluenceBand,
        //     transparent: true,
        //     opacity: 1,
        //     format: 'image/png',
        //     tiled: true
        // }).addTo(this.map);

        let mcTravelband_50000WMS = L.tileLayer.wms(url, {
            layers: mcTravelBand,
            styles: styleTravelband_50000,
            transparent: true,
            opacity: 1,
            format: 'image/png',
            tiled: true
        }).addTo(this.map);

        let mcTravelband_25000WMS = L.tileLayer.wms(url, {
            layers: mcTravelBand,
            styles: styleTravelband_25000,
            transparent: true,
            opacity: 1,
            format: 'image/png',
            tiled: true
        }).addTo(this.map);

        let mcTravelband_12500WMS = L.tileLayer.wms(url, {
            layers: mcTravelBand,
            styles: styleTravelband_12500,
            transparent: true,
            opacity: 1,
            format: 'image/png',
            tiled: true
        }).addTo(this.map);

        let mcInstallerWMS= L.tileLayer.wms(url, {
            layers: mcInstaller,
            transparent: true,
            opacity: 1,
            format: 'image/png',
            tiled: true
        }).addTo(this.map);

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
        //this.uber_hex.addTo(this.map);
        //this.hexData = await this.run();  
    },


};

</script>

<style scoped>
#mapContainer {
 width: 80vw;
 height: 100vh;
}
</style>