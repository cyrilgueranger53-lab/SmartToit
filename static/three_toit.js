let scene, camera, renderer, controls;
let roofMesh = null;
function initRoof3D(lat, lng, width=10, height=5, ardoises=[]) {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 600/400, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({antialias:true});
    renderer.setSize(600,400);
    document.getElementById('roof3d').appendChild(renderer.domElement);
    controls = new THREE.OrbitControls(camera, renderer.domElement);

    const geometry = new THREE.BoxGeometry(width, 0.5, height);
    const material = new THREE.MeshBasicMaterial({color: 0xcccccc});
    roofMesh = new THREE.Mesh(geometry, material);
    scene.add(roofMesh);

    ardoises.forEach(a => {
        const geo = new THREE.BoxGeometry(0.5,0.5,0.5);
        const mat = new THREE.MeshBasicMaterial({color:0xff0000});
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(a.x,0.5,a.z);
        scene.add(mesh);
    });

    camera.position.set(width,10,height*2);
    controls.update();
    function animate(){
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();
}
