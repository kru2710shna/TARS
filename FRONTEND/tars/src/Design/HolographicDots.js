// src/Design/HolographicDots.js
import React, { useRef, useEffect } from "react";

const HolographicDots = () => {
  const canvasRef = useRef(null);
  const dots = useRef([]);
  const zoomRef = useRef(1);
  const mouse = useRef({ x: null, y: null });

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    class Dot {
      constructor() {
        this.reset();
      }

      reset() {
        this.centerX = centerX;
        this.centerY = centerY;
        this.angle = Math.random() * 2 * Math.PI;
        this.orbitRadius = Math.random() * (canvas.height * 0.4) + 80;
        this.radius = Math.random() * 2 + 0.5;
        this.speed = 0.001 + Math.random() * 0.003;

        // Determine behavior: 'orbit', 'shoot', or 'revolve'
        const chance = Math.random();
        this.behavior = chance < 0.15 ? "shoot" : chance < 0.3 ? "revolve" : "orbit";
        this.resetShoot();

        this.originalColor = "rgba(0, 191, 255, 1)";
        this.currentColor = this.originalColor;
        this.colorFadeTimeout = null;
        this.updatePosition();
      }

      resetShoot() {
        if (this.behavior === "shoot") {
          this.x = Math.random() * canvas.width;
          this.y = Math.random() * canvas.height;
          const angle = Math.random() * 2 * Math.PI;
          this.vx = Math.cos(angle) * 0.5;
          this.vy = Math.sin(angle) * 0.5;
        }
      }

      updatePosition() {
        this.x =
          this.centerX +
          Math.cos(this.angle) * this.orbitRadius * zoomRef.current;
        this.y =
          this.centerY +
          Math.sin(this.angle) * this.orbitRadius * zoomRef.current;
      }

      update() {
        if (this.behavior === "orbit") {
          this.angle += this.speed;
          this.updatePosition();
        }

        else if (this.behavior === "revolve") {
          this.angle -= this.speed * 1.5; // anticlockwise
          this.orbitRadius -= 0.05; // slowly pulled inward
          if (this.orbitRadius < 20) this.orbitRadius = Math.random() * 300 + 100;
          this.updatePosition();
        }

        else if (this.behavior === "shoot") {
          this.x += this.vx;
          this.y += this.vy;

          // Bounce or reset
          if (
            this.x < 0 || this.x > canvas.width ||
            this.y < 0 || this.y > canvas.height
          ) {
            this.resetShoot();
          }
        }

        // Vortex pull (applies to all)
        const dx = this.centerX - this.x;
        const dy = this.centerY - this.y;
        this.x += dx * 0.0008;
        this.y += dy * 0.0008;

        // Mouse interaction
        if (mouse.current.x !== null && mouse.current.y !== null) {
          const mx = mouse.current.x - this.x;
          const my = mouse.current.y - this.y;
          const dist = Math.sqrt(mx * mx + my * my);
          if (dist < 30) {
            this.currentColor = "rgba(255, 50, 50, 1)";
            clearTimeout(this.colorFadeTimeout);
            this.colorFadeTimeout = setTimeout(() => {
              this.currentColor = this.originalColor;
            }, 500);
          }
        }
      }

      draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.currentColor;
        ctx.shadowColor = this.currentColor;
        ctx.shadowBlur = 10;
        ctx.fill();
      }
    }

    // Create initial dots
    const totalDots = 350;
    for (let i = 0; i < totalDots; i++) {
      dots.current.push(new Dot());
    }

    // Mouse events
    const handleMouseMove = (e) => {
      mouse.current.x = e.clientX;
      mouse.current.y = e.clientY;
    };
    const handleMouseLeave = () => {
      mouse.current.x = null;
      mouse.current.y = null;
    };

    // Zoom interaction
    const handleWheel = (e) => {
      const delta = -e.deltaY * 0.001;
      zoomRef.current += delta;
      zoomRef.current = Math.min(Math.max(zoomRef.current, 0.4), 2.5);
    };

    // Resize canvas
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    // Animate loop
    const animate = () => {
      ctx.fillStyle = "black";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      dots.current.forEach((dot) => {
        dot.update();
        dot.draw(ctx);
      });

      requestAnimationFrame(animate);
    };

    // Event Listeners
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseleave", handleMouseLeave);
    window.addEventListener("resize", handleResize);
    window.addEventListener("wheel", handleWheel);

    animate();

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("wheel", handleWheel);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        display: "block",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 0,
        background: "black",
        width: "100vw",
        height: "100vh",
      }}
    />
  );
};

export default HolographicDots;
