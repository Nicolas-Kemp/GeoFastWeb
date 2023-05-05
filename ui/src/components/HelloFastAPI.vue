<template>
    <div>
        <h1>{{ fastapiResponse }}</h1>
    </div>
</template>


<script>

import axios from 'axios';

export default {
    name: 'HelloFastAPI',

    data: function () {

        return {
        fastapiResponse: null,
        textVal: ' with text param',
        zoomLevel: 2,
        lfZoom: 3,
        lfBbox: [10.8984375, -37.94677734375, 37.41943359375, -16.8310546875],
        
        }

    },

    methods: {
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


};

</script>