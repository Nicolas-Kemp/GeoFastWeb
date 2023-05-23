import * as THREE from '@modules/three';
import { MapControls } from 'three/addons/controls/MapControls.js';
import { renderer } from '@core/renderer.ts'
import { camera } from '@core/camera.ts'


export const controls = new MapControls( camera, renderer.domElement );

controls.mouseButtons.LEFT = THREE.MOUSE.PAN;
controls.mouseButtons.RIGHT = THREE.MOUSE.ROTATE;
controls.mouseButtons.MIDDLE = THREE.MOUSE.DOLLY,

controls.touches.ONE = THREE.TOUCH.PAN;
controls.touches.TWO = THREE.TOUCH.DOLLY_ROTATE;

controls.keys = {
	LEFT: 'ArrowLeft', //left arrow
	UP: 'ArrowUp', // up arrow
	RIGHT: 'ArrowRight', // right arrow
	BOTTOM: 'ArrowDown' // down arrow
}

controls.maxPolarAngle = Math.PI/2;
controls.zoomSpeed = 0.4;
controls.position0 = 0;
controls.screenSpacePanning = false;
