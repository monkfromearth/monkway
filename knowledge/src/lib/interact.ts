// Shared helpers for the interactive demos. Keep them tiny and dependency-light.
import { gsap } from 'gsap';

export { gsap };

export const REDUCED =
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const clamp = (v: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, v));

/** Pointer event -> SVG user-space coordinates. */
export function svgPoint(svg: SVGSVGElement, e: PointerEvent) {
  const pt = svg.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;
  return pt.matrixTransform(svg.getScreenCTM()!.inverse());
}

/**
 * Make an SVG handle draggable. `cb` receives SVG-space (x, y) on press and on move
 * (pointer capture keeps it firing even when the pointer leaves the handle).
 */
export function draggable(
  svg: SVGSVGElement,
  handle: SVGElement,
  cb: (x: number, y: number) => void,
) {
  handle.addEventListener('pointerdown', (e) => {
    e.preventDefault();
    handle.setPointerCapture(e.pointerId);
    handle.classList.add('mt-grabbing');
    const p = svgPoint(svg, e);
    cb(p.x, p.y);
  });
  handle.addEventListener('pointermove', (e) => {
    if (!handle.hasPointerCapture(e.pointerId)) return;
    const p = svgPoint(svg, e);
    cb(p.x, p.y);
  });
  const end = (e: PointerEvent) => { handle.releasePointerCapture?.(e.pointerId); handle.classList.remove('mt-grabbing'); };
  handle.addEventListener('pointerup', end);
  handle.addEventListener('pointercancel', end);
}

/** Tween a numeric text element from its current value to `to`. */
export function countTo(el: HTMLElement | SVGTextElement, to: number, digits = 2, dur = 0.3) {
  const from = parseFloat((el.textContent || '0').replace(/[^\d.-]/g, '')) || 0;
  if (REDUCED) { el.textContent = to.toFixed(digits); return; }
  const o = { v: from };
  gsap.to(o, { v: to, duration: dur, ease: 'power2.out', onUpdate: () => (el.textContent = o.v.toFixed(digits)) });
}
