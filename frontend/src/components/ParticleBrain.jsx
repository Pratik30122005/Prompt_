import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export const DISPERSE_MS = 900;

// The reference (dala.craftedbygc.com) describes itself as "a 3D brain composed of many small
// pyramidal particles", so this is the same thing: wireframe tetrahedra instanced over a brain
// shell. The glowing silhouette is not drawn - near the rim the shell turns edge-on and the
// pyramids pile up in projection, while face-on in the middle they spread thin.
//
// public/brain.svg is Wikimedia Commons "Brain-outline-lateral.svg", CC0 / public domain.
const AMBER = 0xffb829;      // Saffron Spark, on the black canvas
const PALE = 0xe6e6e6;       // near-white interior, so the amber rim carries the silhouette
const ACCENTS = [0x8052ff, 0xd1348c, 0x15846e, 0x4d7cff];   // iris, magenta, verdant, blue
const COUNT = 4200;
const MAP = 640;        // depth-map resolution; too low and the artwork blurs into a blob
const DEPTH = 0.55;     // how far the shell bulges, relative to half the brain's width
const RIM = 0.16;       // below this share of max depth a pyramid is on the rim: ~26% of the brain
const REACH = 7;        // world units the pyramids travel when dispersing

/**
 * Silhouette mask plus true distance-from-edge, at MAP resolution.
 *
 * Deliberately uses no ctx.filter. Canvas filters are specified in user space (so they shrink
 * under a transform) and are quietly dropped by software canvas backends, and a blur-plus-
 * threshold never closed the gaps between the gyri anyway - what came out was the line drawing,
 * which made every pixel edge-adjacent and turned the whole brain amber. Flood fill and a
 * chamfer distance transform are exact, need no tuning, and behave the same everywhere.
 */
function rasterise(img) {
  const surface = () => {
    const c = document.createElement('canvas');
    c.width = c.height = MAP;
    return c.getContext('2d');
  };
  const sw = img.naturalWidth || 1200;   // the asset is pinned to its viewBox
  const N = MAP * MAP;

  // pass 1: draw whole, find the ink's bounding box so the brain fills the frame
  const probe = surface();
  probe.drawImage(img, 0, 0, MAP, MAP);
  const raw = probe.getImageData(0, 0, MAP, MAP).data;
  let x0 = MAP, y0 = MAP, x1 = 0, y1 = 0;
  for (let y = 0; y < MAP; y++) {
    for (let x = 0; x < MAP; x++) {
      if (raw[(y * MAP + x) * 4 + 3] > 8) {
        if (x < x0) x0 = x;
        if (x > x1) x1 = x;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
  }
  const k = sw / MAP;
  const bw = Math.max(1, (x1 - x0) * k);
  const bh = Math.max(1, (y1 - y0) * k);

  // pass 2: crop to that box and scale to fill the frame, in one transform-free drawImage
  const art = surface();
  const s = Math.min(MAP / bw, MAP / bh) * 0.94;
  const dw = bw * s;
  const dh = bh * s;
  art.drawImage(img, x0 * k, y0 * k, bw, bh, (MAP - dw) / 2, (MAP - dh) / 2, dw, dh);

  const px = art.getImageData(0, 0, MAP, MAP).data;
  const ink = new Uint8Array(N);
  for (let i = 0; i < N; i++) ink[i] = px[i * 4 + 3] > 8 ? 1 : 0;

  // Flood the background inward from the border. The drawing's outer contour is closed, so
  // whatever the flood cannot reach is the brain - gyri gaps included. That is the silhouette,
  // exactly, with no threshold to tune.
  const outside = new Uint8Array(N);
  const stack = new Int32Array(N);
  let sp = 0;
  const seed = (p) => {
    if (!ink[p] && !outside[p]) { outside[p] = 1; stack[sp++] = p; }
  };
  for (let i = 0; i < MAP; i++) {
    seed(i);                    // top
    seed((MAP - 1) * MAP + i);  // bottom
    seed(i * MAP);              // left
    seed(i * MAP + MAP - 1);    // right
  }
  while (sp) {
    const p = stack[--sp];
    const x = p % MAP;
    if (x > 0 && !outside[p - 1] && !ink[p - 1]) { outside[p - 1] = 1; stack[sp++] = p - 1; }
    if (x < MAP - 1 && !outside[p + 1] && !ink[p + 1]) { outside[p + 1] = 1; stack[sp++] = p + 1; }
    if (p >= MAP && !outside[p - MAP] && !ink[p - MAP]) { outside[p - MAP] = 1; stack[sp++] = p - MAP; }
    if (p < N - MAP && !outside[p + MAP] && !ink[p + MAP]) { outside[p + MAP] = 1; stack[sp++] = p + MAP; }
  }

  const solid = new Uint8Array(N);
  for (let i = 0; i < N; i++) solid[i] = outside[i] ? 0 : 1;

  // Chamfer 3-4 distance transform: two sweeps give distance from the silhouette edge, which is
  // what the shell is inflated along. Unlike a blurred mask this really is 0 at the boundary.
  const dist = new Int32Array(N);
  const INF = 1 << 28;
  for (let i = 0; i < N; i++) dist[i] = solid[i] ? INF : 0;
  for (let y = 0; y < MAP; y++) {
    for (let x = 0; x < MAP; x++) {
      const p = y * MAP + x;
      if (!solid[p]) continue;
      let b = dist[p];
      if (y > 0) {
        if (x > 0) b = Math.min(b, dist[p - MAP - 1] + 4);
        b = Math.min(b, dist[p - MAP] + 3);
        if (x < MAP - 1) b = Math.min(b, dist[p - MAP + 1] + 4);
      }
      if (x > 0) b = Math.min(b, dist[p - 1] + 3);
      dist[p] = b;
    }
  }
  let max = 1;
  for (let y = MAP - 1; y >= 0; y--) {
    for (let x = MAP - 1; x >= 0; x--) {
      const p = y * MAP + x;
      if (!solid[p]) continue;
      let b = dist[p];
      if (y < MAP - 1) {
        if (x < MAP - 1) b = Math.min(b, dist[p + MAP + 1] + 4);
        b = Math.min(b, dist[p + MAP] + 3);
        if (x > 0) b = Math.min(b, dist[p + MAP - 1] + 4);
      }
      if (x < MAP - 1) b = Math.min(b, dist[p + 1] + 3);
      dist[p] = b;
      if (b > max) max = b;
    }
  }

  return { solid, dist, max };
}

/** Scatter pyramids over the inflated shell. */
function build(img) {
  const { solid, dist, max } = rasterise(img);
  const half = MAP / 2;
  const pos = [];
  const col = [];
  const scale = [];
  const dir = [];
  let guard = COUNT * 60;

  while (pos.length < COUNT * 3 && guard-- > 0) {
    const mx = (Math.random() * MAP) | 0;
    const my = (Math.random() * MAP) | 0;
    const i = my * MAP + mx;
    if (!solid[i]) continue;

    const d = dist[i] / max;                                         // 0 at rim, 1 deep inside
    const x = (mx - half) / half;
    const y = -(my - half) / half;                                   // canvas y is flipped
    const z = Math.sqrt(d) * DEPTH * (Math.random() < 0.5 ? 1 : -1)
      + (Math.random() - 0.5) * 0.025;                               // a shell with thickness

    pos.push(x, y, z);
    scale.push(0.015 + Math.random() * 0.016);

    const hue = Math.random() < 0.14
      ? ACCENTS[(Math.random() * ACCENTS.length) | 0]
      : (d < RIM ? AMBER : PALE);
    col.push(hue);

    // outward, away from the middle, for the dispersal
    const len = Math.hypot(x, y, z) || 1;
    const j = 0.35;
    dir.push(
      x / len + (Math.random() - 0.5) * j,
      y / len + (Math.random() - 0.5) * j,
      z / len + (Math.random() - 0.5) * j,
    );
  }
  return { pos, col, scale, dir, n: pos.length / 3 };
}

/**
 * The constellation. `dispersing` throws the pyramids outward across the whole viewport;
 * `onDone` fires once they are gone, which is the cue to change route.
 */
export default function ParticleBrain({ className = '', dispersing = false, onDone }) {
  const canvasRef = useRef(null);
  const dispersingRef = useRef(false);
  const startRef = useRef(0);
  const originRef = useRef(null);
  const doneRef = useRef(false);
  const onDoneRef = useRef(onDone);
  const [loose, setLoose] = useState(false);  // true = canvas covers the viewport

  onDoneRef.current = onDone;

  // Remember where the brain sits before the canvas goes fullscreen, so it can be pinned back to
  // the same spot on screen instead of jumping to the middle.
  useEffect(() => {
    if (!dispersing || dispersingRef.current) return;
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;
    originRef.current = { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
    dispersingRef.current = true;
    startRef.current = performance.now();
    setLoose(true);
  }, [dispersing]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.z = 3.9;
    const group = new THREE.Group();
    scene.add(group);

    const still = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    let mesh;
    let frame;
    let dead = false;

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      renderer.setSize(rect.width, rect.height, false);
      camera.aspect = rect.width / rect.height;
      camera.updateProjectionMatrix();

      // once fullscreen, shift the group so the brain stays where it was on screen
      const o = originRef.current;
      if (o) {
        const perPx = (2 * camera.position.z * Math.tan((camera.fov * Math.PI) / 360)) / rect.height;
        group.position.set((o.x - rect.width / 2) * perPx, -(o.y - rect.height / 2) * perPx, 0);
      }
    };

    const start = ({ pos, col, scale, dir, n }) => {
      // a wireframe tetrahedron is the reference's outlined pyramid; instancing keeps 9000 of
      // them to a single draw call
      const geo = new THREE.TetrahedronGeometry(1, 0);
      const mat = new THREE.MeshBasicMaterial({ wireframe: true, transparent: true });
      mesh = new THREE.InstancedMesh(geo, mat, n);
      mesh.frustumCulled = false;

      const m = new THREE.Matrix4();
      const q = new THREE.Quaternion();
      const v = new THREE.Vector3();
      const sv = new THREE.Vector3();
      const colour = new THREE.Color();
      const e = new THREE.Euler();
      for (let i = 0; i < n; i++) {
        v.set(pos[i * 3], pos[i * 3 + 1], pos[i * 3 + 2]);
        sv.setScalar(scale[i]);
        q.setFromEuler(e.set(Math.random() * 6.28, Math.random() * 6.28, 0));
        mesh.setMatrixAt(i, m.compose(v, q, sv));
        mesh.setColorAt(i, colour.setHex(col[i]));
      }
      mesh.instanceMatrix.needsUpdate = true;
      if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
      group.add(mesh);
      resize();

      const base = new THREE.Vector3();
      const render = (t) => {
        const gone = dispersingRef.current
          ? Math.min(1, (t - startRef.current) / DISPERSE_MS)
          : 0;

        if (gone > 0) {
          const eased = gone * gone;  // holds together for a beat, then flies apart
          mat.opacity = 1 - gone;
          for (let i = 0; i < n; i++) {
            base.set(
              pos[i * 3] + dir[i * 3] * eased * REACH,
              pos[i * 3 + 1] + dir[i * 3 + 1] * eased * REACH,
              pos[i * 3 + 2] + dir[i * 3 + 2] * eased * REACH,
            );
            sv.setScalar(scale[i]);
            q.setFromEuler(e.set(eased * 9, eased * 7, 0));
            mesh.setMatrixAt(i, m.compose(base, q, sv));
          }
          mesh.instanceMatrix.needsUpdate = true;
        } else {
          // idle costs nothing per pyramid - the whole shell just turns
          group.rotation.y = still ? 0.3 : Math.sin(t * 0.00012) * 0.45;
          group.rotation.x = still ? 0 : Math.sin(t * 0.00007) * 0.06;
        }

        renderer.render(scene, camera);
        if (gone >= 1 && !doneRef.current) {
          doneRef.current = true;
          onDoneRef.current?.();
        }
      };

      const loop = (t) => {
        render(t);
        frame = requestAnimationFrame(loop);
      };
      frame = requestAnimationFrame(loop);
    };

    const img = new Image();
    img.src = '/brain.svg';
    img.decode().then(() => { if (!dead) start(build(img)); }).catch(() => {});

    window.addEventListener('resize', resize);
    const observer = new ResizeObserver(resize);
    observer.observe(canvas);

    return () => {
      dead = true;
      if (frame) cancelAnimationFrame(frame);
      window.removeEventListener('resize', resize);
      observer.disconnect();
      mesh?.geometry.dispose();
      mesh?.material.dispose();
      renderer.dispose();
    };
    // built once: rebuilding on a prop change would reshuffle the shell mid-animation
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      className={
        loose
          ? 'fixed inset-0 z-50 w-screen h-screen pointer-events-none'
          : `w-full h-full ${className}`
      }
    />
  );
}
