import * as THREE from '@modules/three';
export const camera = new THREE.PerspectiveCamera( 75, 
    window.innerWidth / window.innerHeight, 
    0.0001, 1000 
    );
camera.position.z = 5;

export default camera