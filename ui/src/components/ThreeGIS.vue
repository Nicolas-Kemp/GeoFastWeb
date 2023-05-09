<template>
    <div ref="container" id="webgl_id"></div>
</template>
  
<script>
import * as THREE from 'three';
import { MapControls } from 'three/addons/controls/MapControls.js';

export default {
name: 'ThreeJsExample',
mounted() {

    window.addEventListener( 'resize', onWindowResize, false );
    function onWindowResize(){

        camera.aspect = (window.innerWidth)  / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize( (window.innerWidth) , window.innerHeight );
        renderer.setClearColor( 0xFFA03B, 0 );

    }

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

    const renderer = new THREE.WebGLRenderer();
    renderer.setSize( window.innerWidth, window.innerHeight );
    document.getElementById("webgl_id").appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry( 1, 1, 1 );
    const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
    const cube = new THREE.Mesh( geometry, material );
    scene.add( cube );

    camera.position.z = 5;


    function animate() {
    requestAnimationFrame( animate );

    cube.rotation.x += 0.001;
    cube.rotation.y += 0.001;
        controls.update();
    renderer.render( scene, camera );
    }

    const controls = new MapControls( camera, renderer.domElement );
    controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
    controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;

    controls.touches.ONE = THREE.TOUCH.PAN;
    controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;



    controls.maxPolarAngle = Math.PI/2;
    controls.zoomSpeed = 0.4;
    controls.position0 = 0;
    controls.screenSpacePanning = false;
    
    controls.update();
    animate();
},
};
</script>