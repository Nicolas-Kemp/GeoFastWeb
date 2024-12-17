<template>
    <div ref="container" id="webgl_id"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { camera } from '@core/camera'
  import { renderer } from '@core/renderer'
  import { controls } from '@core/controls'
  import { cube } from '@core/geometries'
  import { ambientLight, directionalLight } from '@core/lights'
  //import { renderer, onWindowResize } from '@core/renderer.ts'
  
  import axios from 'axios';
  
  import fishRiverImg from '@assets/image/fishriver_walk_ex.jpeg'
  import fishRiverImg_Alpha from '@assets/image/fishriver_walk_ex_alpha.jpeg'
  
  export default {
  name: 'ThreeJsExample',
  
  data: function () {
  
    return {
  
    }
  
  },
  
  methods: {
  
    async getAPI(url_ext) {
        try {
  
        const response = await axios.get(
            `http://127.0.0.1:80/`.concat(url_ext), {
              params: {
                        default_tiff: 'fishriver_hike_ex.tif',
                        bbox_str: ''

              }
            }
        );
  
        return response.data;
  
        } catch (error) {
        console.log(error);
        }
    },
  
    getTerrain3D(){
        return this.getAPI('threetiff')
    },
  
    getTerrainGeom(terrainDict){
  
        let geom = new THREE.BufferGeometry();
        geom.setIndex(terrainDict.aoi_indices);
        geom.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(terrainDict.aoi_vertices), 3 ) );
        // geom.setAttribute( 'color', new THREE.BufferAttribute( new Float32Array(terrainDict.aoi_colour), 3 ) );
        geom.setAttribute( 'uv', new THREE.BufferAttribute( new Float32Array(terrainDict.aoi_uvs), 2 ) );
        geom.computeVertexNormals();
        return geom
  
    },
  
    async getTerrainMat(terrainImg, terrainMap){

        // load a resource
        var loader = new THREE.TextureLoader();
        loader.load(
            // resource URL
            terrainImg,
  
            // onLoad callback
            function ( texture ) {
            // in this example we create the material when the texture is loaded
            terrainMap.material.map = texture;
            terrainMap.material.vertexColors = false;
            terrainMap.material.needsUpdate = true;
            
            //console.log(terrainMap)         
            },
  
            // onProgress callback currently not supported
            undefined,
  
            // onError callback
            function ( err ) {
            console.error( 'An error happened.' );
            
            },
        
        );

        // loader.load(
        //     // resource URL
        //     fishRiverImg_Alpha,
  
        //     // onLoad callback
        //     function ( texture ) {
        //     // in this example we create the material when the texture is loaded
        //     // terrainMap.material.alphaMap = texture;
        //     // terrainMap.material.transparent = true;
        //     // terrainMap.material.depthTest = false;
        //     // // terrainMap.material.roughness = 1;
        //     // // terrainMap.material.alphaTest = 0.5;
        //     // terrainMap.material.needsUpdate = true;
            

            
        //     //console.log(terrainMap)         
        //     },
  
        //     // onProgress callback currently not supported
        //     undefined,
  
        //     // onError callback
        //     function ( err ) {
        //     console.error( 'An error happened.' );
            
        //     },
        
        // );
        
        
    },
  
  },
  
  
  
  async mounted() {
  
    const scene = new THREE.Scene();
    const canvas = document.getElementById("webgl_id").appendChild(renderer.domElement);
  
    // scene.add( cube );
  
  
    scene.add( ambientLight );
  
    function animate() {
        requestAnimationFrame( animate );
        cube.rotation.x += 0.001;
        cube.rotation.y += 0.001;
        controls.update();
        renderer.render( scene, camera );
    }
  
    let aoi_centroid = [0,0]
    controls.target.set(aoi_centroid[1],0,aoi_centroid[0]);
    controls.update();
  
    animate();
  
    let fishRiverDict = JSON.parse(await this.getTerrain3D())
   
    let tcTerrainDict = {
                            color: 0xA6A4A1,
                            vertexColors: true
                        };
  
    let material_aoi = new THREE.MeshBasicMaterial(
                                    tcTerrainDict
                                );
  
    let geometry_aoi = this.getTerrainGeom(fishRiverDict)
    let aoi_map = new THREE.Mesh( geometry_aoi, material_aoi );
    this.getTerrainMat(fishRiverImg, aoi_map)
    scene.add( aoi_map );
                       
    camera.position.x = fishRiverDict.aoi_lry;
    camera.position.y = 0.01;
    camera.position.z = fishRiverDict.aoi_lrx;

    console.log(camera.position.x);
    console.log(camera.position.z);
    console.log(camera.position.y);
    console.log(geometry_aoi);


    controls.target.set(fishRiverDict.aoi_centroid[1],0.001,fishRiverDict.aoi_centroid[0]);
    controls.update();
  
  
  },
  };
  </script>