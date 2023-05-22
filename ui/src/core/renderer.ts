import {WebGLRenderer} from '@modules/three';

export const renderer = new WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor( 0x263740, 1);

window.addEventListener( 'resize', onWindowResize, false );
export function onWindowResize(){

    renderer.setSize( (window.innerWidth) , window.innerHeight );
    renderer.setClearColor( 0x263740, 1 );

}