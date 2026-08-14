'use client';

import React, { useState } from 'react';
import {
  X,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Minimize2,
  Download,
  Camera,
  Calendar,
  Globe2,
  Layers,
} from 'lucide-react';

interface ScreenshotModalProps {
  isOpen: boolean;
  onClose: () => void;
  screenshotUrl: string;
  testName: string;
  timestamp?: string;
  browser?: string;
  environment?: string;
}

export const ScreenshotModal: React.FC<ScreenshotModalProps> = ({
  isOpen,
  onClose,
  screenshotUrl,
  testName,
  timestamp = 'Recent Execution',
  browser = 'Chrome',
  environment = 'QA',
}) => {
  const [zoomLevel, setZoomLevel] = useState<number>(1);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);

  if (!isOpen) return null;

  const handleZoomIn = () => setZoomLevel((prev) => Math.min(prev + 0.25, 2.5));
  const handleZoomOut = () => setZoomLevel((prev) => Math.max(prev - 0.25, 0.5));
  const handleResetZoom = () => setZoomLevel(1);

  const handleDownload = () => {
    const a = document.createElement('a');
    a.href = screenshotUrl;
    a.download = `${testName}_failure_screenshot.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content"
        style={{
          maxWidth: isFullscreen ? '98vw' : '960px',
          maxHeight: isFullscreen ? '98vh' : '90vh',
          height: isFullscreen ? '98vh' : 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                backgroundColor: '#fef2f2',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Camera size={16} color="#ef4444" />
            </div>
            <div>
              <h3 style={{ fontSize: '15px', fontWeight: '700', color: '#0f172a' }}>
                Failure Screenshot Inspection
              </h3>
              <div style={{ fontSize: '12px', color: '#64748b', fontFamily: 'var(--font-mono)' }}>
                {testName}
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <button onClick={handleZoomOut} className="btn btn-sm btn-icon" title="Zoom Out">
              <ZoomOut size={14} />
            </button>
            <span style={{ fontSize: '12px', color: '#64748b', minWidth: '40px', textAlign: 'center' }}>
              {Math.round(zoomLevel * 100)}%
            </span>
            <button onClick={handleZoomIn} className="btn btn-sm btn-icon" title="Zoom In">
              <ZoomIn size={14} />
            </button>
            <button onClick={handleResetZoom} className="btn btn-sm" title="Fit to screen">
              Fit
            </button>
            <button
              onClick={() => setIsFullscreen(!isFullscreen)}
              className="btn btn-sm btn-icon"
              title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
            >
              {isFullscreen ? <Minimize2 size={14} /> : <Maximize2 size={14} />}
            </button>
            <button onClick={handleDownload} className="btn btn-sm" style={{ gap: '6px' }}>
              <Download size={13} />
              <span>Download</span>
            </button>
            <button onClick={onClose} className="btn btn-sm btn-icon" style={{ marginLeft: '6px' }}>
              <X size={16} />
            </button>
          </div>
        </div>

        {/* Metadata Banner */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            padding: '8px 24px',
            backgroundColor: '#f8fafc',
            borderBottom: '1px solid var(--border-color)',
            fontSize: '12px',
            color: '#475569',
            flexWrap: 'wrap',
          }}
        >
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Calendar size={13} color="#64748b" /> {timestamp}
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Globe2 size={13} color="#64748b" /> Browser: <strong>{browser}</strong>
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Layers size={13} color="#64748b" /> Environment: <strong>{environment}</strong>
          </span>
          <span style={{ marginLeft: 'auto', color: '#10b981', fontWeight: '600' }}>
            ✓ Secrets Redacted
          </span>
        </div>

        {/* Image Display Area */}
        <div
          className="modal-body"
          style={{
            backgroundColor: '#0f172a',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'auto',
            padding: '20px',
            minHeight: '400px',
          }}
        >
          <div
            style={{
              transform: `scale(${zoomLevel})`,
              transformOrigin: 'center center',
              transition: 'transform 0.15s ease-out',
              maxWidth: '100%',
            }}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={screenshotUrl}
              alt={`Failure screenshot for ${testName}`}
              style={{
                maxWidth: '100%',
                height: 'auto',
                borderRadius: '8px',
                boxShadow: '0 8px 30px rgba(0, 0, 0, 0.4)',
                border: '1px solid #334155',
                display: 'block',
              }}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="modal-footer">
          <button onClick={onClose} className="btn btn-sm">
            Close Viewer
          </button>
        </div>
      </div>
    </div>
  );
};
