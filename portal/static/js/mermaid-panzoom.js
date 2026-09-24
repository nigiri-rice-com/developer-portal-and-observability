/**
 * Nigiri Developer Portal - Mermaid Pan & Zoom Controller (GitHub Style)
 * Provides interactive zoom, 4-way pan (drag & buttons), fullscreen mode, and raw code copy.
 * Modeled after GitHub's native Mermaid diagram viewer.
 */

(function () {
  'use strict';

  const allFitCallbacks = [];

  window.refitAllPanZoom = function () {
    allFitCallbacks.forEach(fn => {
      try { fn(); } catch (e) {}
    });
  };

  // Ensure styles for panzoom viewport and controls are injected
  if (typeof document !== 'undefined' && !document.getElementById('mermaid-panzoom-injected-styles')) {
    const styleEl = document.createElement('style');
    styleEl.id = 'mermaid-panzoom-injected-styles';
    styleEl.textContent = `
      /* Container Box */
      .mermaid-interactive-box {
        position: relative !important;
        border-radius: 14px !important;
        border: 1px solid #e2e8f0 !important;
        background-color: #f8fafc !important;
        margin: 1.5rem 0 !important;
        overflow: hidden !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        transition: box-shadow 0.2s ease !important;
      }
      .dark .mermaid-interactive-box {
        border-color: rgba(6, 78, 59, 0.6) !important;
        background-color: #030d0b !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
      }

      /* Floating Top-Right Toolbar (Fullscreen & Copy) */
      .pz-toolbar {
        position: absolute !important;
        top: 14px !important;
        right: 14px !important;
        z-index: 30 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 8px !important;
        pointer-events: auto !important;
      }

      .pz-btn-toolbar {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        padding: 6px 14px !important;
        height: 34px !important;
        border-radius: 10px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(203, 213, 225, 0.9) !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #334155 !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        cursor: pointer !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.15s ease !important;
        white-space: nowrap !important;
      }
      .pz-btn-toolbar:hover {
        background-color: #ffffff !important;
        color: #059669 !important;
        border-color: #10b981 !important;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.25) !important;
        transform: translateY(-1px) !important;
      }
      .pz-btn-toolbar:active {
        transform: translateY(0) scale(0.97) !important;
      }
      .dark .pz-btn-toolbar {
        background-color: rgba(15, 23, 42, 0.92) !important;
        border-color: rgba(6, 78, 59, 0.8) !important;
        color: #cbd5e1 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
      }
      .dark .pz-btn-toolbar:hover {
        background-color: #0f172a !important;
        color: #34d399 !important;
        border-color: #10b981 !important;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.35) !important;
      }

      /* Floating Bottom-Left Scale Badge */
      .pz-scale-badge-wrap {
        position: absolute !important;
        bottom: 14px !important;
        left: 14px !important;
        z-index: 30 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 8px !important;
        padding: 6px 14px !important;
        height: 34px !important;
        border-radius: 10px !important;
        font-size: 12px !important;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
        border: 1px solid rgba(203, 213, 225, 0.9) !important;
        background-color: rgba(255, 255, 255, 0.92) !important;
        color: #475569 !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
        pointer-events: none !important;
      }
      .dark .pz-scale-badge-wrap {
        background-color: rgba(2, 6, 23, 0.92) !important;
        border-color: rgba(6, 78, 59, 0.8) !important;
        color: #94a3b8 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3) !important;
      }
      .pz-scale-badge {
        font-weight: 700 !important;
        color: #059669 !important;
      }
      .dark .pz-scale-badge {
        color: #34d399 !important;
      }

      /* Floating Bottom-Right D-Pad Controller */
      .pz-controls-wrap {
        position: absolute !important;
        bottom: 14px !important;
        right: 14px !important;
        z-index: 30 !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(203, 213, 225, 0.9) !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
        pointer-events: auto !important;
      }
      .dark .pz-controls-wrap {
        background-color: rgba(15, 23, 42, 0.92) !important;
        border-color: rgba(6, 78, 59, 0.8) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
      }

      /* 3x3 D-Pad Grid */
      .pz-dpad-grid {
        display: grid !important;
        grid-template-columns: 32px 32px 32px !important;
        grid-template-rows: 32px 32px 32px !important;
        gap: 3px !important;
        width: 102px !important;
        height: 102px !important;
        box-sizing: border-box !important;
      }

      .pz-btn-cell {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 8px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: #475569 !important;
        cursor: pointer !important;
        transition: all 0.12s ease !important;
        padding: 0 !important;
        margin: 0 !important;
        user-select: none !important;
      }
      .pz-btn-cell:hover {
        background-color: rgba(16, 185, 129, 0.15) !important;
        color: #059669 !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
      }
      .pz-btn-cell:active {
        transform: scale(0.9) !important;
        background-color: rgba(16, 185, 129, 0.25) !important;
      }
      .dark .pz-btn-cell {
        color: #94a3b8 !important;
      }
      .dark .pz-btn-cell:hover {
        background-color: rgba(16, 185, 129, 0.2) !important;
        color: #34d399 !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
      }

      /* Viewport Area */
      .pz-viewport {
        width: 100% !important;
        height: 680px !important;
        min-height: 680px !important;
        overflow: hidden !important;
        cursor: grab !important;
        position: relative !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: rgba(241, 245, 249, 0.5) !important;
        background-image: radial-gradient(circle, rgba(16, 185, 129, 0.15) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
      }
      .dark .pz-viewport {
        background-color: rgba(2, 44, 34, 0.15) !important;
        background-image: radial-gradient(circle, rgba(16, 185, 129, 0.12) 1px, transparent 1px) !important;
      }
      .pz-viewport:active {
        cursor: grabbing !important;
      }

      /* Fullscreen Mode */
      .mermaid-interactive-box.is-fullscreen {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: 999999 !important;
        margin: 0 !important;
        border-radius: 0 !important;
        border: none !important;
      }
      .mermaid-interactive-box.is-fullscreen .pz-viewport {
        height: 100vh !important;
        min-height: 100vh !important;
      }

      /* Mermaid Typography & Sharp Vector Styling */
      .mermaid-interactive-box svg {
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
      }
      .mermaid-interactive-box .node rect,
      .mermaid-interactive-box .node circle,
      .mermaid-interactive-box .node polygon {
        stroke-width: 1.5px !important;
      }
      .mermaid-interactive-box .nodeLabel {
        font-size: 14px !important;
        font-weight: 500 !important;
        line-height: 1.35 !important;
      }
      .mermaid-interactive-box .cluster-label span {
        font-size: 15px !important;
        font-weight: 700 !important;
      }
      .mermaid-interactive-box .edgeLabel {
        font-size: 12px !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 2px 4px !important;
        border-radius: 4px !important;
      }
      .dark .mermaid-interactive-box .edgeLabel {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #cbd5e1 !important;
      }
    `;
    document.head.appendChild(styleEl);
  }

  function createPanZoomDiagram(boxWrapper, rawCode) {
    if (!boxWrapper || boxWrapper.classList.contains('panzoom-initialized')) return;
    boxWrapper.classList.add('panzoom-initialized');

    const svg = boxWrapper.querySelector('svg');
    if (!svg) return;

    if (!rawCode) {
      rawCode = boxWrapper.getAttribute('data-raw-mermaid') || '';
    }

    // Outer wrapper box
    const box = document.createElement('div');
    box.className = 'mermaid-interactive-box';

    box.innerHTML = `
      <!-- Top Right Floating Toolbar -->
      <div class="pz-toolbar panzoom-exclude">
        <button type="button" class="pz-btn-fullscreen pz-btn-toolbar panzoom-exclude" title="全画面表示 (Escで解除)">
          <svg class="pz-icon-expand" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
          <svg class="pz-icon-collapse" style="width:14px;height:14px;display:none;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/></svg>
          <span class="pz-fs-text">全画面</span>
        </button>

        <button type="button" class="pz-btn-actualsize pz-btn-toolbar panzoom-exclude" title="原寸表示 (100% / 文字を大きく読む)">
          <svg style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
          <span>原寸 100%</span>
        </button>

        <button type="button" class="pz-btn-fitview pz-btn-toolbar panzoom-exclude" title="全体表示にフィット">
          <svg style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          <span>全体</span>
        </button>

        <button type="button" class="pz-btn-copy pz-btn-toolbar panzoom-exclude" title="Mermaidコードをコピー">
          <svg class="pz-icon-copy" style="width:14px;height:14px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          <span class="pz-copy-text">コピー</span>
        </button>
      </div>

      <!-- Bottom Left Scale Badge -->
      <div class="pz-scale-badge-wrap panzoom-exclude">
        <span class="pz-scale-badge">100%</span>
        <span class="pz-scale-hint" style="color: #94a3b8; font-size: 11px;">| ドラッグで移動 / ホイールで拡大縮小</span>
      </div>

      <!-- Bottom Right Controls (GitHub Style D-Pad & Zoom) -->
      <div class="pz-controls-wrap panzoom-exclude">
        <div class="pz-dpad-grid panzoom-exclude">
          <!-- Row 1 -->
          <div></div>
          <button type="button" class="pz-btn-up pz-btn-cell panzoom-exclude" title="上へ移動 (Pan Up)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 15l-6-6-6 6"/></svg>
          </button>
          <button type="button" class="pz-btn-zoomin pz-btn-cell panzoom-exclude" title="拡大 (Zoom In)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M11 8v6M8 11h6"/></svg>
          </button>

          <!-- Row 2 -->
          <button type="button" class="pz-btn-left pz-btn-cell panzoom-exclude" title="左へ移動 (Pan Left)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
          </button>
          <button type="button" class="pz-btn-reset pz-btn-cell panzoom-exclude" title="全体表示にリセット (Fit to Screen)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
          </button>
          <button type="button" class="pz-btn-right pz-btn-cell panzoom-exclude" title="右へ移動 (Pan Right)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
          </button>

          <!-- Row 3 -->
          <div></div>
          <button type="button" class="pz-btn-down pz-btn-cell panzoom-exclude" title="下へ移動 (Pan Down)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <button type="button" class="pz-btn-zoomout pz-btn-cell panzoom-exclude" title="縮小 (Zoom Out)">
            <svg style="width:16px;height:16px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35M8 11h6"/></svg>
          </button>
        </div>
      </div>

      <!-- Viewport Canvas Area (Enforced 680px height) -->
      <div class="pz-viewport">
        <div class="pz-canvas will-change-transform" style="transform-origin: 50% 50%; display: inline-flex; align-items: center; justify-content: center;">
        </div>
      </div>
    `;

    // Move SVG into canvas with true native viewBox dimensions
    let nativeWidth = 1200;
    let nativeHeight = 800;
    if (svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width > 0) {
      nativeWidth = svg.viewBox.baseVal.width;
      nativeHeight = svg.viewBox.baseVal.height;
    } else {
      const bcr = svg.getBoundingClientRect();
      if (bcr.width > 0) nativeWidth = bcr.width;
      if (bcr.height > 0) nativeHeight = bcr.height;
    }

    svg.style.width = nativeWidth + 'px';
    svg.style.height = nativeHeight + 'px';
    svg.style.minWidth = nativeWidth + 'px';
    svg.style.minHeight = nativeHeight + 'px';
    svg.style.maxWidth = 'none';
    svg.removeAttribute('width');
    svg.removeAttribute('height');
    svg.style.display = 'block';
    svg.style.filter = 'drop-shadow(0 4px 12px rgba(0,0,0,0.12))';
    
    const canvas = box.querySelector('.pz-canvas');
    const viewport = box.querySelector('.pz-viewport');
    canvas.appendChild(svg);

    // Replace original boxWrapper in DOM
    boxWrapper.parentNode.replaceChild(box, boxWrapper);

    // Initialize Panzoom
    let panzoomInstance = null;
    if (typeof Panzoom !== 'undefined') {
      panzoomInstance = Panzoom(canvas, {
        maxScale: 10,
        minScale: 0.04,
        step: 0.3,
        canvas: true,
        contain: false,
        excludeClass: 'panzoom-exclude'
      });
      canvas._panzoom = panzoomInstance;
      box._panzoom = panzoomInstance;

      // Wheel zoom (centered on cursor)
      viewport.addEventListener('wheel', function (e) {
        e.preventDefault();
        panzoomInstance.zoomWithWheel(e);
      }, { passive: false });

      // Update scale badge
      canvas.addEventListener('panzoomchange', function (e) {
        const scaleText = Math.round(e.detail.scale * 100) + '%';
        const badge = box.querySelector('.pz-scale-badge');
        if (badge) badge.textContent = scaleText;
      });

      // Double-click zoom in
      viewport.addEventListener('dblclick', function(e) {
        if (!panzoomInstance) return;
        panzoomInstance.zoomToPoint(panzoomInstance.getScale() * 1.5, e);
      });
    }

    // Auto-fit function
    function fitDiagram() {
      if (!panzoomInstance) return;
      const vWidth = viewport.clientWidth || 900;
      const vHeight = viewport.clientHeight || 680;

      if (nativeWidth > 0 && nativeHeight > 0 && vWidth > 0 && vHeight > 0) {
        const padding = 36;
        const scaleX = (vWidth - padding) / nativeWidth;
        const scaleY = (vHeight - padding) / nativeHeight;
        // Fit nicely so the entire diagram is visible inside viewport initially
        const fitScale = Math.min(scaleX, scaleY);
        const initialScale = Math.min(1.0, Math.max(0.04, fitScale));
        panzoomInstance.zoom(initialScale, { animate: false });
        panzoomInstance.pan(0, 0, { animate: false });
        const badge = box.querySelector('.pz-scale-badge');
        if (badge) badge.textContent = Math.round(initialScale * 100) + '%';
      }
    }

    allFitCallbacks.push(fitDiagram);

    // ResizeObserver for auto-fit when tab becomes visible or window resizes
    let hasAutoFitted = false;
    if (window.ResizeObserver) {
      const ro = new ResizeObserver((entries) => {
        for (const entry of entries) {
          if (entry.contentRect.width > 50 && entry.contentRect.height > 50) {
            if (!hasAutoFitted) {
              hasAutoFitted = true;
              setTimeout(fitDiagram, 60);
            }
          }
        }
      });
      ro.observe(viewport);
    }

    // Isolate controls from Panzoom touch/drag events
    const toolbar = box.querySelector('.pz-toolbar');
    const controlsWrap = box.querySelector('.pz-controls-wrap');

    [toolbar, controlsWrap].forEach(el => {
      if (!el) return;
      ['pointerdown', 'mousedown', 'touchstart', 'pointerup', 'mouseup', 'touchend'].forEach(evt => {
        el.addEventListener(evt, e => e.stopPropagation());
      });
    });

    // Bind Button Events
    const btnZoomIn = box.querySelector('.pz-btn-zoomin');
    const btnZoomOut = box.querySelector('.pz-btn-zoomout');
    const btnReset = box.querySelector('.pz-btn-reset');
    const btnUp = box.querySelector('.pz-btn-up');
    const btnDown = box.querySelector('.pz-btn-down');
    const btnLeft = box.querySelector('.pz-btn-left');
    const btnRight = box.querySelector('.pz-btn-right');
    const btnFullscreen = box.querySelector('.pz-btn-fullscreen');
    const btnActualSize = box.querySelector('.pz-btn-actualsize');
    const btnFitView = box.querySelector('.pz-btn-fitview');
    const btnCopy = box.querySelector('.pz-btn-copy');

    if (panzoomInstance) {
      if (btnActualSize) {
        btnActualSize.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          panzoomInstance.zoom(1.0, { animate: true });
          panzoomInstance.pan(0, 0, { animate: true });
          const badge = box.querySelector('.pz-scale-badge');
          if (badge) badge.textContent = '100%';
        });
      }

      if (btnFitView) {
        btnFitView.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          fitDiagram();
        });
      }

      btnZoomIn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.zoomIn({ step: 0.3 });
      });
      btnZoomOut.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.zoomOut({ step: 0.3 });
      });
      btnReset.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        fitDiagram();
      });

      const panStep = 100;
      btnUp.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.pan(0, panStep, { relative: true });
      });
      btnDown.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.pan(0, -panStep, { relative: true });
      });
      btnLeft.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.pan(panStep, 0, { relative: true });
      });
      btnRight.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        panzoomInstance.pan(-panStep, 0, { relative: true });
      });
    }

    // Fullscreen Toggle
    btnFullscreen.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const isFs = box.classList.toggle('is-fullscreen');
      const iconExpand = box.querySelector('.pz-icon-expand');
      const iconCollapse = box.querySelector('.pz-icon-collapse');
      const fsText = box.querySelector('.pz-fs-text');

      if (isFs) {
        if (iconExpand) iconExpand.style.display = 'none';
        if (iconCollapse) iconCollapse.style.display = 'inline-block';
        if (fsText) fsText.textContent = '解除';
      } else {
        if (iconExpand) iconExpand.style.display = 'inline-block';
        if (iconCollapse) iconCollapse.style.display = 'none';
        if (fsText) fsText.textContent = '全画面';
      }
      setTimeout(fitDiagram, 150);
    });

    // Escape Key to Exit Fullscreen
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && box.classList.contains('is-fullscreen')) {
        btnFullscreen.click();
      }
    });

    // Copy Raw Mermaid Code
    btnCopy.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!rawCode) return;
      navigator.clipboard.writeText(rawCode).then(() => {
        const copyText = box.querySelector('.pz-copy-text');
        const origHtml = btnCopy.innerHTML;
        btnCopy.innerHTML = `
          <svg style="width:14px;height:14px;color:#10b981;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
          <span style="color:#10b981;font-weight:bold;">コピー完了</span>
        `;
        setTimeout(() => {
          btnCopy.innerHTML = origHtml;
        }, 2000);
      });
    });

    // Initial fit
    setTimeout(fitDiagram, 150);
  }

  // Master Render & Upgrade Function
  window.renderAllMermaidPanZoom = async function () {
    if (typeof mermaid === 'undefined') return;

    // Detect dark or light mode
    const isDark = document.documentElement.classList.contains('dark');
    mermaid.initialize({
      startOnLoad: false,
      theme: isDark ? 'dark' : 'default',
      themeVariables: isDark ? {
        darkMode: true,
        background: '#04100e',
        primaryColor: '#10b981',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#059669',
        lineColor: '#10b981',
        secondaryColor: '#0f766e',
        tertiaryColor: '#1e293b',
        fontSize: '15px',
        fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      } : {
        primaryColor: '#10b981',
        primaryTextColor: '#0f172a',
        primaryBorderColor: '#059669',
        lineColor: '#059669',
        fontSize: '15px',
        fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
      }
    });

    const targets = document.querySelectorAll('.mermaid-wrapper, .mermaid-panzoom-target');
    for (let i = 0; i < targets.length; i++) {
      const target = targets[i];
      if (target.classList.contains('panzoom-initialized')) continue;

      let rawCode = target.getAttribute('data-raw-mermaid') || '';
      const pre = target.querySelector('pre.mermaid, .mermaid');
      if (!rawCode && pre) {
        rawCode = pre.textContent.trim();
        target.setAttribute('data-raw-mermaid', rawCode);
      }

      // If SVG already exists inside target (e.g. rendered by mermaid)
      const existingSvg = target.querySelector('svg');
      if (existingSvg) {
        createPanZoomDiagram(target, rawCode);
        continue;
      }

      if (!rawCode) continue;

      const uniqueId = 'mermaid-pz-' + i + '-' + Math.floor(Math.random() * 10000);
      try {
        const { svg } = await mermaid.render(uniqueId, rawCode);
        target.innerHTML = svg;
        createPanZoomDiagram(target, rawCode);
      } catch (err) {
        console.warn('Mermaid render warning for item ' + i, err);
      }
    }
  };

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => window.renderAllMermaidPanZoom());
  } else {
    window.renderAllMermaidPanZoom();
  }

})();
