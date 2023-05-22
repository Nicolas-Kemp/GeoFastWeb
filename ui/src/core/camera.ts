import {PerspectiveCamera} from '@modules/three';

export const camera = new PerspectiveCamera( 75, 
    window.innerWidth / window.innerHeight, 
    0.0001, 1000 
    );
camera.position.z = 5;

export default camera

window.addEventListener( 'resize', onWindowResize, false );
export function onWindowResize(){

    camera.aspect = (window.innerWidth)  / window.innerHeight;
    camera.updateProjectionMatrix();

}