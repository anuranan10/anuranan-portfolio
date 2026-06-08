"use strict";
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

//  ------------------------ Setup ------------------------

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xFD5E53);

// Extra - Fog
scene.fog = new THREE.Fog(0xffd9a3, 30, 250);


// Overview Camera
const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set(22,18,28);

// FPS Camera
const fpsCamera = new THREE.PerspectiveCamera(
    70,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

fpsCamera.position.set(0, 2.0, 20);

let activeCamera = camera;
let usingFPSCamera = false;


const keys = {};
window.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    keys[key] = true;

    if(key == "c") {
        usingFPSCamera = !usingFPSCamera;

        if(usingFPSCamera) {
            activeCamera = fpsCamera;
            controls.enabled = false;
        }
        else {
            activeCamera = camera;
            controls.enabled = true;
        }
    }

    if (key === "t") {
    animationOn = !animationOn;
    }
});
window.addEventListener("keyup", (event) => {
    keys[event.key.toLowerCase()] = false;
});


// Render
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.style.margin = '0';
document.body.appendChild(renderer.domElement);

// Orbit Controls
const controls = new OrbitControls(camera, renderer.domElement);

// Global Variables - animation
let animationOn = true;

let fuelTruckGroup;
let fuelTruckDirection = 1;
let fuelTruckMinX = -10;
let fuelTruckMaxX = 12;

let aircraftBeaconMesh;
let aircraftBeaconLight;

// Global Variables - raycasting
const selectableObjects = [];
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

let hangarDoor;
let hangarDoorOpen = false;
let hangarDoorClosedX = 0;
let hangarDoorOpenX = -4.5;

// ------------------------ Helper Functions ------------------------

// Wheel Function
function makeWheel(radius, tubeRadius) {
    const geo = new THREE.CylinderGeometry(radius, radius, tubeRadius * 2, 20).rotateZ(Math.PI / 2);
    const mat = new THREE.MeshPhongMaterial({ color: 0x111111 });

    const wheel = new THREE.Mesh(geo, mat);
    wheel.rotation.y = Math.PI / 2;
    wheel.castShadow = true;
    wheel.receiveShadow = true;
    return wheel;
}

// Ambient Light
function makeAmbientLight() {
    return new THREE.AmbientLight(0x9bb6d1, 0.28);
}

// Directional Light
function makeDirectionalLight() {
    const light = new THREE.DirectionalLight(0xff8c42, 0.7);
    light.position.set(-35, 18, 12);
    light.castShadow = true;

    light.shadow.mapSize.width = 2048;
    light.shadow.mapSize.height = 2048;

    light.shadow.camera.left = -60;
    light.shadow.camera.right = 60;
    light.shadow.camera.top = 60;
    light.shadow.camera.bottom = -60;

    return light;
}

// Spot Light
function makeSpotLight() {
    const light = new THREE.SpotLight(0xffffff, 8.0, 80, Math.PI / 6, 0.3, 1.0);

    light.position.set(0, 22, -19);
    light.target.position.set(0, 10, -19);
    light.castShadow = true;

    light.shadow.mapSize.width = 1024;
    light.shadow.mapSize.height = 1024;

    
    scene.add(light.target);

    return light;
}


// Plane
function makePlane() {

    // Texture setup
    const textureLoader = new THREE.TextureLoader();
    const groundTexture = textureLoader.load('https://threejs.org/examples/textures/terrain/grasslight-big.jpg');

    groundTexture.wrapS = THREE.RepeatWrapping;
    groundTexture.wrapT = THREE.RepeatWrapping;
    groundTexture.repeat.set(12, 12);

    // Plane
    const geo = new THREE.PlaneGeometry(120, 120);
    const mat = new THREE.MeshPhongMaterial({
        map: groundTexture
    });

    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI/2;
    mesh.receiveShadow = true;

    return mesh;
}
scene.add(makePlane());


// Tarmac
function makeTarmac() {
    
    // Texture setup
    const textureLoader = new THREE.TextureLoader();
    const groundTexture = textureLoader.load('./tarmac.jpg');

    groundTexture.wrapS = THREE.RepeatWrapping;
    groundTexture.wrapT = THREE.RepeatWrapping;
    groundTexture.repeat.set(12, 12);

    const geo = new THREE.PlaneGeometry(55, 55);
    const mat = new THREE.MeshPhongMaterial({ map: groundTexture });

    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI/2;
    mesh.position.y = 0.02; // avoid flickering
    mesh.receiveShadow = true;

    return mesh;
}
scene.add(makeTarmac());


// Aircraft
function makeAircraft() {
    const group = new THREE.Group();

    const bodyMat = new THREE.MeshPhongMaterial( {color: 0xd9d9d9 });
    const accentMat = new THREE.MeshPhongMaterial( {color: 0x1f4e79 });

    // Fuselage
    const fuselage = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 14, 24), bodyMat);
    fuselage.rotation.z = Math.PI/2;
    fuselage.position.y = 3.2;
    fuselage.castShadow = true;
    fuselage.receiveShadow = true;
    group.add(fuselage);


    // Nose
    const nose = new THREE.Mesh(new THREE.ConeGeometry(1.2, 2.5, 24), bodyMat);
    nose.rotation.z = -Math.PI / 2;
    nose.position.set(8.2, 3.2, 0);
    nose.castShadow = true;
    nose.receiveShadow = true;
    group.add(nose);


    // Wings
    const wing = new THREE.Mesh(new THREE.BoxGeometry(11, 0.25, 3.2), accentMat);
    wing.rotation.y = Math.PI/2;
    wing.position.set(1.0, 3.2, 0);
    wing.castShadow = true;
    wing.receiveShadow = true;
    group.add(wing);


    // Horizontal Tail
    const hTail = new THREE.Mesh(new THREE.BoxGeometry(4.0, 0.18, 1.4), accentMat);
    hTail.rotation.y = Math.PI/2;
    hTail.position.set(-6.0, 3.8, 0);
    hTail.castShadow = true;
    hTail.receiveShadow = true;
    group.add(hTail);


    // Vertical Tail
    const vTail = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.5, 1.8), accentMat);
    vTail.rotation.y = Math.PI/2;
    vTail.position.set(-6.0, 4.8, 0);
    vTail.castShadow = true;
    vTail.receiveShadow = true;
    group.add(vTail);

    
    // Engines
    const engine1 = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 2.2, 20), bodyMat);
    engine1.rotation.z = Math.PI / 2;
    engine1.position.set(1.5, 2.54, 2.8);
    engine1.castShadow = true;
    engine1.receiveShadow = true;
    group.add(engine1);

    const engine2 = engine1.clone();
    engine2.position.z = -2.8;
    group.add(engine2);


    // Landing Gear Struts
    const gearMat = new THREE.MeshPhongMaterial({ color: 0x333333 });

    const gear1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.3, 12), gearMat);
    gear1.position.set(3.5, 1.4, 0);
    gear1.castShadow = true;
    gear1.receiveShadow = true;
    group.add(gear1);

    const gear2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.7, 12), gearMat);
    gear2.position.set(-1.0, 1.78, 1.0);
    gear2.castShadow = true;
    gear2.receiveShadow = true;
    group.add(gear2);

    const gear3 = gear2.clone();
    gear3.position.set(-1.0, 1.78, -1.0);
    group.add(gear3);


    // Wheels
    const wheel1 = makeWheel(0.35, 0.12);
    wheel1.position.set(3.5, 0.7, 0);
    group.add(wheel1);

    const wheel2 = makeWheel(0.3, 0.1);
    wheel2.position.set(-1.0, 0.63, 1.0);
    group.add(wheel2);

    const wheel3 = makeWheel(0.3, 0.1);
    wheel3.position.set(-1.0, 0.63, -1.0);
    group.add(wheel3);


    // Beacon
    const beaconMat = new THREE.MeshPhongMaterial({ color: 0xff0000 });

    const beacon = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), beaconMat);
    beacon.position.set(0, 4.5, 0);
    beacon.castShadow = true;
    beacon.receiveShadow = true;
    group.add(beacon);

    const beaconLight = new THREE.PointLight(0xff0000, 1.5, 8);
    beaconLight.position.set(0, 5.2, 0);
    group.add(beaconLight);

    aircraftBeaconMesh = beacon;
    aircraftBeaconLight = beaconLight;


    group.position.set(0, -0.33, 0);
    return group;
}
scene.add(makeAircraft());


// Hangar
function makeHangar() {
    const group = new THREE.Group();

    const wallMat = new THREE.MeshPhongMaterial({ color: 0x7b8a8b });
    const roofMat = new THREE.MeshPhongMaterial({ color: 0x5c6770 });

    // Body
    const body = new THREE.Mesh(new THREE.BoxGeometry(25, 10, 12), wallMat);
    body.position.y = 4;
    body.castShadow = true;
    body.receiveShadow = true;
    group.add(body);


    // Roof
    const roof = new THREE.Mesh(new THREE.ConeGeometry(8.5, 6, 4), roofMat);
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 11;
    roof.castShadow = true;
    roof.receiveShadow = true;
    group.add(roof);


    // Door
    hangarDoor = new THREE.Mesh(new THREE.BoxGeometry(24, 9, 0.3), new THREE.MeshPhongMaterial({ color: 0x2f3e46 }));
    hangarDoor.position.set(0, 4, 6.2);
    hangarDoor.castShadow = true;
    hangarDoor.receiveShadow = true;
    group.add(hangarDoor);

    // Raycasting
    hangarDoorClosedX = hangarDoor.position.x;
    hangarDoorOpenX = hangarDoorClosedX - 20.0;

    hangarDoor.userData.type = "hangarDoor";
    selectableObjects.push(hangarDoor);

    group.position.set(0, 0, -19);
    return group;
}
scene.add(makeHangar());


//Light Poles
function makeLightPoles() {
    const group = new THREE.Group();

    const poleMat = new THREE.MeshPhongMaterial({ color: 0x555555 });
    const lampMat = new THREE.MeshPhongMaterial({ color: 0xe6e6e6, emissive: 0xfff2cc, emissiveIntensity: 0.25 });

    function makePole1(x, z) {
        const poleGroup = new THREE.Group();

        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 10, 16), poleMat);
        pole.position.y = 5;
        pole.castShadow = true;
        pole.receiveShadow = true;
        poleGroup.add(pole);


        const arm = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.15, 0.15), poleMat);
        arm.position.set(-1.0, 9.6, 0);
        arm.castShadow = true;
        arm.receiveShadow = true;
        poleGroup.add(arm);


        const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.4, 0.6),lampMat);
        lamp.position.set(-2.0, 9.4, 0);
        lamp.castShadow = true;
        lamp.receiveShadow = true;
        poleGroup.add(lamp);


        // Point Light
        const pointLight = new THREE.PointLight(0xfff2cc, 300, 28);
        pointLight.position.set(-2.0, 9.15, 0);
        pointLight.castShadow = true;
        pointLight.shadow.mapSize.width = 1024;
        pointLight.shadow.mapSize.height = 1024;
        poleGroup.add(pointLight);


        // Raycasting
        lamp.userData.type = "lightPole";
        lamp.userData.pointLight = pointLight;
        selectableObjects.push(lamp);


        poleGroup.position.set(x, 0, z);
        return poleGroup;
    }

    function makePole2(x, z) {
        const poleGroup = new THREE.Group();

        const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 10, 16), poleMat);
        pole.position.y = 5;
        pole.castShadow = true;
        pole.receiveShadow = true;
        poleGroup.add(pole);


        const arm = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.15, 0.15), poleMat);
        arm.position.set(1.0, 9.6, 0); // Changes
        arm.castShadow = true;
        arm.receiveShadow = true;
        poleGroup.add(arm);


        const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.4, 0.6),lampMat);
        lamp.position.set(2.0, 9.4, 0); // Changes
        lamp.castShadow = true;
        lamp.receiveShadow = true;
        poleGroup.add(lamp);


        // Point Light
        const pointLight = new THREE.PointLight(0xfff2cc, 300, 28);
        pointLight.position.set(2.0, 9.15, 0);
        pointLight.castShadow = true;
        pointLight.shadow.mapSize.width = 1024;
        pointLight.shadow.mapSize.height = 1024;
        poleGroup.add(pointLight);


        // Raycasting
        lamp.userData.type = "lightPole";
        lamp.userData.pointLight = pointLight;
        selectableObjects.push(lamp);


        poleGroup.position.set(x, 0, z);
        return poleGroup;
    }

    group.add(makePole1(25, 2.0));
    group.add(makePole1(25, -20));
    group.add(makePole1(25, 20));
    group.add(makePole2(-25, 2.0));
    group.add(makePole2(-25, -20));
    group.add(makePole2(-25, 20));

    return group;
}
scene.add(makeLightPoles());
scene.add(makeAmbientLight());
scene.add(makeDirectionalLight());
scene.add(makeSpotLight());


// Fuel Truck
function makeFuelTruck() {
    const group = new THREE.Group();

    const bodyMat = new THREE.MeshPhongMaterial({ color: 0xFFFF00 });
    const tankMat = new THREE.MeshPhongMaterial({ color: 0xFF9800 });


    // Cab
    const cab = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.7, 2.1), bodyMat);
    cab.position.set(2.2, 1.7, 0);
    cab.castShadow = true;
    cab.receiveShadow = true;
    group.add(cab);


    // Fuel Tank
    const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 4.0),tankMat);
    tank.rotation.z = Math.PI / 2;
    tank.position.set(-0.8, 1.85, 0);
    tank.castShadow = true;
    tank.receiveShadow = true;
    group.add(tank);


    // Base
    const base = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.3, 2.0), new THREE.MeshPhongMaterial({ color: 0xFFFFFFFF }));
    base.position.set(-0.2, 1.0, 0);
    base.castShadow = true;
    base.receiveShadow = true;
    group.add(base);


    // Wheels
    const wheel1 = makeWheel(0.4, 0.11);
    wheel1.position.set(1.3, 0.43, -1.0);
    group.add(wheel1);

    const wheel2 = makeWheel(0.4, 0.11);
    wheel2.position.set(1.3, 0.43, 1.0);
    group.add(wheel2);

    const wheel3 = makeWheel(0.4, 0.11);
    wheel3.position.set(-1.9, 0.43, -1.0);
    group.add(wheel3);

    const wheel4 = makeWheel(0.4, 0.11);
    wheel4.position.set(-1.9, 0.43, 1.0);
    group.add(wheel4);


    group.position.set(-10, 0, 10);
    fuelTruckGroup = group;
    return group;
}
scene.add(makeFuelTruck());


// Baggage Cart
function makeBaggageCart() {
    const group = new THREE.Group();

    const cartMat = new THREE.MeshPhongMaterial({ color: 0xFFFFFFFF });
    const frameMat = new THREE.MeshPhongMaterial({ color: 0x666666 });

    // Bed
    const bed = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.35, 2.5), cartMat);
    bed.position.y = 1.0;
    bed.castShadow = true;
    bed.receiveShadow = true;
    group.add(bed);


    // Boxes
    const box1 = new THREE.Mesh(new THREE.BoxGeometry(1.3, 1.1, 1.2), new THREE.MeshPhongMaterial({ color: 0xaa3333 }));
    box1.position.set(-1.1, 1.8, 0);
    box1.castShadow = true;
    box1.receiveShadow = true;
    group.add(box1);

    const box2 = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.9, 1.0), new THREE.MeshPhongMaterial({ color: 0x3366aa }));
    box2.position.set(0.8, 1.7, 0.2);
    box2.castShadow = true;
    box2.receiveShadow = true;
    group.add(box2);


    // Hitch
    const hitch = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.15, 0.15), frameMat);
    hitch.position.set(-3.0, 0.9, 0);
    hitch.castShadow = true;
    hitch.receiveShadow = true;
    group.add(hitch);

    
    // Wheels
    const wheel1 = makeWheel(0.35, 0.1);
    wheel1.position.set(-1.5, 0.45,  1.2);
    group.add(wheel1);

    const wheel2 = makeWheel(0.35, 0.1);
    wheel2.position.set(-1.5, 0.45, -1.2);
    group.add(wheel2);

    const wheel3 = makeWheel(0.35, 0.1);
    wheel3.position.set(1.5, 0.45,  1.2);
    group.add(wheel3);

    const wheel4 = makeWheel(0.35, 0.1);
    wheel4.position.set(1.5, 0.45, -1.2);
    group.add(wheel4);

    group.position.set(20, -0.1, 3);
    return group;
}
scene.add(makeBaggageCart());

// Baggage Cart 2
const baggageCart2 = makeBaggageCart();
baggageCart2.rotation.y = Math.PI / 2;
baggageCart2.position.set(10, -0.1, 20);
scene.add(baggageCart2);


// FPS Camera function
function updateFPSCamera() {
    if (!usingFPSCamera) return;

    const speed = 0.4;

    if (keys["w"]) fpsCamera.position.z -= speed;
    if (keys["s"]) fpsCamera.position.z += speed;
    if (keys["a"]) fpsCamera.position.x -= speed;
    if (keys["d"]) fpsCamera.position.x += speed;
    if (keys["q"]) fpsCamera.position.y += speed;
    if (keys["e"]) fpsCamera.position.y -= speed;

    // fpsCamera.lookAt(
    //     fpsCamera.position.x,
    //     fpsCamera.position.y,
    //     fpsCamera.position.z - 10
    // );
}


// ------------------------ Animation ------------------------
function animateFuelTruck() {
    if (!fuelTruckGroup) return;

    fuelTruckGroup.position.x += 0.03 * fuelTruckDirection;

    if (fuelTruckGroup.position.x > fuelTruckMaxX || fuelTruckGroup.position.x < fuelTruckMinX) {
        fuelTruckDirection *= -1;
    }
}

function animateAircraftBeacon() {
    if (!aircraftBeaconMesh || !aircraftBeaconLight) return;

    // Blinking effect - converting sine wave to binary signal
    const time = Date.now() * 0.005; // returns time in milliseconds
    const pulse = Math.sin(time); // repeating wave/smooth oscillating value

    aircraftBeaconMesh.visible = true;

    if (pulse > 0) { //converting the smooth sine wave into a binary signal
        aircraftBeaconLight.intensity = 5.5;
    } else {
        aircraftBeaconLight.intensity = 0.0;
    }
}


// Raycasting
function toggleLightPole(mesh) {
    const pointLight = mesh.userData.pointLight;
    if (!pointLight) return;

    pointLight.visible = !pointLight.visible;
}

function toggleHangarDoor() {
    if (!hangarDoor) return;

    if (hangarDoorOpen) {
        hangarDoor.position.x = hangarDoorClosedX;
        hangarDoorOpen = false;
    } else {
        hangarDoor.position.x = hangarDoorOpenX;
        hangarDoorOpen = true;
    }
}

renderer.domElement.addEventListener("click", onMouseClick);

function onMouseClick(event) {
    const rect = renderer.domElement.getBoundingClientRect();

    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, activeCamera);

    const hits = raycaster.intersectObjects(selectableObjects, false);

    if (hits.length === 0) return;

    const clickedObject = hits[0].object;

    if (clickedObject.userData.type === "lightPole") {
        toggleLightPole(clickedObject);
    }

    if (clickedObject.userData.type === "hangarDoor") {
        toggleHangarDoor();
    }
}


// Render Loops
function renderLoop() {
    requestAnimationFrame(renderLoop);

    if (!usingFPSCamera) {
        controls.update();
    }

    updateFPSCamera();

    if (animationOn) {
        animateFuelTruck();
        animateAircraftBeacon();
    }
    else {
        if (aircraftBeaconMesh) {
            aircraftBeaconMesh.visible = true;
        }
        if (aircraftBeaconLight) {
            aircraftBeaconLight.intensity = 0.6;
        }
    }

    renderer.render(scene, activeCamera);
}
renderLoop();


// Resize Handling
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    fpsCamera.aspect = window.innerWidth / window.innerHeight;
    fpsCamera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);
});