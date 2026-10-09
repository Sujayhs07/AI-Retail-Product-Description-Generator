import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { DashboardPage } from './pages/DashboardPage';
import { GeneratePage } from './pages/GeneratePage';
import { BatchPage } from './pages/BatchPage';
import { CataloguePage } from './pages/CataloguePage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { BrandSettingsPage } from './pages/BrandSettingsPage';
import { ResponsibleAIPage } from './pages/ResponsibleAIPage';
import { HelpPage } from './pages/HelpPage';
import { NotFoundPage } from './pages/NotFoundPage';

import { ErrorBoundary } from './components/common/ErrorBoundary';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="generate" element={<GeneratePage />} />
            <Route path="batch" element={<BatchPage />} />
            <Route path="catalogue" element={<CataloguePage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="brand-settings" element={<BrandSettingsPage />} />
            <Route path="responsible-ai" element={<ResponsibleAIPage />} />
            <Route path="help" element={<HelpPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default App;
