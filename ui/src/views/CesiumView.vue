<template>
    <div>
      <CesiumMap />
    </div>
</template>

<script>

import CesiumMap from '../components/CesiumMap.vue';

export default {
    name: 'cLeafletMap',
    components: {
        CesiumMap,
    },
};
</script>