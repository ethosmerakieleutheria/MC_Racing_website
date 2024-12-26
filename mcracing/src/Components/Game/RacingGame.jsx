// src/Components/Game/RacingGame.jsx
import React, { useRef, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';

// Car component
const Car = () => {
  const carRef = useRef();
  const [position, setPosition] = useState([0, 0.5, 0]);
  const [rotation, setRotation] = useState([0, 0, 0]);

  useEffect(() => {
    const handleKeyPress = (e) => {
      const speed = 0.5;
      const rotationSpeed = 0.05;

      switch(e.key) {
        case 'ArrowUp':
          setPosition(prev => [
            prev[0] - Math.sin(rotation[1]) * speed,
            prev[1],
            prev[2] - Math.cos(rotation[1]) * speed
          ]);
          break;
        case 'ArrowDown':
          setPosition(prev => [
            prev[0] + Math.sin(rotation[1]) * speed,
            prev[1],
            prev[2] + Math.cos(rotation[1]) * speed
          ]);
          break;
        case 'ArrowLeft':
          setRotation(prev => [prev[0], prev[1] + rotationSpeed, prev[2]]);
          break;
        case 'ArrowRight':
          setRotation(prev => [prev[0], prev[1] - rotationSpeed, prev[2]]);
          break;
        default:
          // Do nothing for other keys
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [rotation]);

  return (
    <mesh ref={carRef} position={position} rotation={rotation}>
      {/* Car body */}
      <group>
        {/* Main body */}
        <mesh position={[0, 0.4, 0]}>
          <boxGeometry args={[2, 0.8, 4]} />
          <meshStandardMaterial color="red" />
        </mesh>
        {/* Cabin */}
        <mesh position={[0, 0.8, -0.5]}>
          <boxGeometry args={[1.5, 0.5, 2]} />
          <meshStandardMaterial color="black" />
        </mesh>
        {/* Wheels */}
        <Wheels />
      </group>
    </mesh>
  );
};

// Wheels component
const Wheels = () => {
  const wheelPositions = [
    [-1, 0, -1.5], // front left
    [1, 0, -1.5],  // front right
    [-1, 0, 1.5],  // back left
    [1, 0, 1.5],   // back right
  ];

  return (
    <>
      {wheelPositions.map((position, index) => (
        <mesh key={index} position={position}>
          <cylinderGeometry args={[0.4, 0.4, 0.3, 16]} rotation={[Math.PI / 2, 0, 0]} />
          <meshStandardMaterial color="black" />
        </mesh>
      ))}
    </>
  );
};

// Track component
const Track = () => {
  return (
    <group>
      {/* Ground */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.1, 0]} receiveShadow>
        <planeGeometry args={[100, 100]} />
        <meshStandardMaterial color="#2c2c2c" />
      </mesh>
      
      {/* Track markings */}
      <group position={[0, 0.01, 0]}>
        {/* Outer boundaries */}
        {[...Array(20)].map((_, i) => (
          <group key={i} position={[Math.sin(i / 3) * 20, 0, i * 5 - 50]}>
            <mesh position={[-10, 0.1, 0]} castShadow receiveShadow>
              <boxGeometry args={[0.5, 0.2, 5]} />
              <meshStandardMaterial color="white" />
            </mesh>
            <mesh position={[10, 0.1, 0]} castShadow receiveShadow>
              <boxGeometry args={[0.5, 0.2, 5]} />
              <meshStandardMaterial color="white" />
            </mesh>
          </group>
        ))}
        
        {/* Center line */}
        {[...Array(40)].map((_, i) => (
          <mesh 
            key={i} 
            position={[0, 0.1, i * 2.5 - 50]} 
            receiveShadow
          >
            <boxGeometry args={[0.2, 0.1, 1]} />
            <meshStandardMaterial color="yellow" />
          </mesh>
        ))}
      </group>
    </group>
  );
};

// Main Racing Game component
const RacingGame = () => {
  return (
    <div className="h-[60vh] w-full relative">
      <Canvas shadows>
        {/* Lights */}
        <ambientLight intensity={0.5} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        
        {/* Camera and Controls */}
        <PerspectiveCamera makeDefault position={[0, 10, 20]} />
        <OrbitControls 
          enableZoom={false} 
          maxPolarAngle={Math.PI / 2.5}
          minPolarAngle={Math.PI / 4}
        />
        
        {/* Game Elements */}
        <Car />
        <Track />
        
        {/* Environment Effects */}
        <fog attach="fog" args={['#fff', 30, 100]} />
      </Canvas>
      
      {/* Controls UI */}
      <div className="absolute bottom-4 left-4 bg-black/50 text-white p-4 rounded-lg backdrop-blur-sm">
        <h3 className="font-bold mb-2">Game Controls</h3>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>↑</div><div>Accelerate</div>
          <div>↓</div><div>Brake/Reverse</div>
          <div>←</div><div>Turn Left</div>
          <div>→</div><div>Turn Right</div>
        </div>
      </div>
    </div>
  );
};

export default RacingGame;