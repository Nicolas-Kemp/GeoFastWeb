<template>
    <div ref="container" id="webgl_id"></div>
</template>
  
<script>
import * as THREE from 'three';
import { MapControls } from 'three/addons/controls/MapControls.js';
import axios from 'axios';

import tableMountainImg from '@assets/image/tablemountain.jpeg'

export default {
name: 'ThreeJsExample',

data: function () {

    return {

    }

},

methods: {

    async getTerrain3D() {
        try {

        const response = await axios.get(
            `http://127.0.0.1:80/threetiff`, {
            params: {

            }
            }
        );

        return response.data;

        } catch (error) {
        console.log(error);
        }
    },

    

},

mounted() {

    window.addEventListener( 'resize', onWindowResize, false );
    function onWindowResize(){

        camera.aspect = (window.innerWidth)  / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize( (window.innerWidth) , window.innerHeight );
        renderer.setClearColor( 0x263740, 1 );

    }




    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.0001, 1000 );

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    renderer.setClearColor( 0x263740, 1);
    document.getElementById("webgl_id").appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry( 1, 1, 1 );
    const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    const cube = new THREE.Mesh( geometry, material );
    scene.add( cube );

    camera.position.z = 5;
    const light = new THREE.AmbientLight( 0xFFFF00, 0.5 ); // soft white light
    scene.add( light );

    function animate() {
    requestAnimationFrame( animate );

    cube.rotation.x += 0.001;
    cube.rotation.y += 0.001;
        controls.update();
    renderer.render( scene, camera );
    }

    let aoi_centroid = [0,0]
    const controls = new MapControls( camera, renderer.domElement );
    controls.target.set(aoi_centroid[1],0,aoi_centroid[0]);
    controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
    controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;

    controls.touches.ONE = THREE.TOUCH.PAN;
    controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;



    controls.maxPolarAngle = Math.PI/2;
    controls.zoomSpeed = 0.04;
    controls.position0 = 0;
    controls.screenSpacePanning = false;
    
    controls.update();
    animate();

    let tableMountainDict = "";
    this.getTerrain3D().then(function(result) {
                                                tableMountainDict = JSON.parse(result);
                                                console.log(tableMountainDict)
                                                
                                                let geometry_aoi = new THREE.BufferGeometry();
                                                geometry_aoi.setIndex(tableMountainDict.aoi_indices);
                                                geometry_aoi.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(tableMountainDict.aoi_vertices), 3 ) );
                                                // geometry_aoi.setAttribute( 'color', new THREE.BufferAttribute( new Float32Array(tableMountainDict.aoi_colour), 3 ) );
                                                geometry_aoi.setAttribute( 'uv', new THREE.BufferAttribute( new Float32Array(tableMountainDict.aoi_uvs), 2 ) );
                                                geometry_aoi.computeVertexNormals();
                                                console.log(tableMountainImg)

                                                // instantiate a loader
                                                var tc_fishriver_walk = {};
                                                var loader = new THREE.TextureLoader();

                                                // load a resource
                                                loader.load(
                                                    // resource URL
                                                    tableMountainImg,
                                                    // Function when resource is loaded
                                                    function ( texture ) {
                                                        // do something with the texture
   
                                                            tc_fishriver_walk = {
                                                                            map: texture,
                                                                            vertexColors: false

                                                                    };
                                                                                         // let texture = new THREE.TextureLoader().load('static/images/hermanus.jpg');
                                                console.log(tc_fishriver_walk)                        
                                                const material_aoi = new THREE.MeshBasicMaterial(
                                                    tc_fishriver_walk
                                                                            );
                                                let aoi_map = new THREE.Mesh( geometry_aoi, material_aoi );
                                                scene.add( aoi_map );
                                                //aoi_map.material.map = texture;
                                                //material_aoi.color.set(0xff0000);
                                                aoi_map.material.displacementScale = 0;
                                                aoi_map.material.transparent=false;

                                                aoi_map.material.needsUpdate = true;

                                                const directLight_slected_area = new THREE.DirectionalLight( 0xFFFFFF, 0.2);
                                                directLight_slected_area.position.set(tableMountainDict.aoi_lry,0.5,tableMountainDict.aoi_lrx+0.008);
                                                directLight_slected_area.target.position.set(tableMountainDict.aoi_lry,0,tableMountainDict.aoi_lrx);
                                                // scene.add( directLight_slected_area );
                                                // scene.add(directLight_slected_area.target);

                                                camera.position.x = tableMountainDict.aoi_lry;
                                                camera.position.y = 0.00001;
                                                camera.position.z = tableMountainDict.aoi_lrx;

                                                controls.target.set(tableMountainDict.aoi_centroid[1],0.001,tableMountainDict.aoi_centroid[0]);
                                                controls.update();
                                                    },
                                                    // Function called when download progresses
                                                    function ( xhr ) {
                                                        console.log( (xhr.loaded / xhr.total * 100) + '% loaded' );
                                                    },
                                                    // Function called when download errors
                                                    function ( xhr ) {
                                                        console.log( 'An error happened' );
                                                        if (img_fishriverwalk['image']===null) {
                                                                console.log('texture is undefined');
                                                                tc_fishriver_walk = {
                                                                color: 0xA6A4A1,
                                                                roughness: 3,
                                                                metalness: 0.6,
                                                                vertexColors: true
                                                                        };
                                                                    }
                                                    }
                                                );


                           
                                                });
},
};
</script>