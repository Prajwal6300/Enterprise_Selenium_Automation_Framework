import React from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { getFailureScreenshots } from '@/lib/result-parser';
import { ScreenshotGalleryClient } from './ScreenshotGalleryClient';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function ScreenshotsPage() {
  const screenshots = getFailureScreenshots();

  return (
    <DashboardLayout>
      <div className="page-header">
        <div className="page-title-group">
          <h1>Failure Screenshot Gallery</h1>
          <p>
            High-resolution viewport captures recorded at the moment of Selenium test assertion failures.
          </p>
        </div>
      </div>

      <ScreenshotGalleryClient initialScreenshots={screenshots} />
    </DashboardLayout>
  );
}
