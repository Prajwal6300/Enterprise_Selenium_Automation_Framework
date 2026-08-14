'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ScreenshotModal } from '@/components/modals/ScreenshotModal';
import { EmptyState } from '@/components/common/FeedbackStates';
import { Camera, Download, Maximize2, Calendar, Globe2, Layers } from 'lucide-react';

interface ScreenshotItem {
  filename: string;
  test_name: string;
  timestamp: string;
  browser: string;
  environment: string;
  url: string;
  size_kb: number;
}

interface ScreenshotGalleryClientProps {
  initialScreenshots: ScreenshotItem[];
}

export const ScreenshotGalleryClient: React.FC<ScreenshotGalleryClientProps> = ({
  initialScreenshots,
}) => {
  const [selected, setSelected] = useState<ScreenshotItem | null>(null);

  if (initialScreenshots.length === 0) {
    return (
      <EmptyState
        title="No Failure Screenshots"
        message="No test execution failures have been recorded in screenshots/failures."
      />
    );
  }

  return (
    <div>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '20px',
        }}
      >
        {initialScreenshots.map((item, idx) => (
          <div key={idx} className="card" style={{ padding: '0', overflow: 'hidden' }}>
            {/* Thumbnail */}
            <div
              style={{
                height: '200px',
                backgroundColor: '#0f172a',
                position: 'relative',
                cursor: 'pointer',
                overflow: 'hidden',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
              onClick={() => setSelected(item)}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={item.url}
                alt={item.test_name}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  opacity: 0.9,
                  transition: 'transform 0.2s ease',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  backgroundColor: 'rgba(15, 23, 42, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  opacity: 0,
                  transition: 'opacity 0.15s ease',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.opacity = '1')}
                onMouseLeave={(e) => (e.currentTarget.style.opacity = '0')}
              >
                <div
                  className="btn btn-sm btn-primary"
                  style={{ gap: '6px', pointerEvents: 'none' }}
                >
                  <Maximize2 size={13} />
                  <span>Inspect Screenshot</span>
                </div>
              </div>
            </div>

            {/* Details */}
            <div style={{ padding: '16px' }}>
              <Link
                href={`/tests/${item.test_name}`}
                style={{
                  fontSize: '13.5px',
                  fontWeight: '600',
                  color: 'var(--text-primary)',
                  display: 'block',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                {item.test_name}
              </Link>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  marginTop: '10px',
                  fontSize: '12px',
                  color: '#64748b',
                  flexWrap: 'wrap',
                }}
              >
                <span className="badge badge-gray">{item.browser}</span>
                <span className="badge badge-gray">{item.environment}</span>
                <span style={{ marginLeft: 'auto', fontSize: '11px' }}>{item.size_kb} KB</span>
              </div>

              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginTop: '14px',
                  paddingTop: '12px',
                  borderTop: '1px solid var(--border-color)',
                }}
              >
                <button
                  onClick={() => setSelected(item)}
                  className="btn btn-sm"
                  style={{ gap: '5px' }}
                >
                  <Maximize2 size={12} />
                  <span>Zoom</span>
                </button>

                <a href={item.url} download={item.filename} className="btn btn-sm btn-icon">
                  <Download size={13} color="#64748b" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selected && (
        <ScreenshotModal
          isOpen={true}
          onClose={() => setSelected(null)}
          screenshotUrl={selected.url}
          testName={selected.test_name}
          browser={selected.browser}
          environment={selected.environment}
        />
      )}
    </div>
  );
};
