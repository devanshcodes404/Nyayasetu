import { createBrowserRouter } from 'react-router-dom';
import { AppLayout } from '../layouts/app-layout';
import { AuthLayout } from '../layouts/auth-layout';
import { ProtectedRoute } from './protected-route';

import { LandingPage } from '../pages/landing';
import { LoginPage } from '../pages/login';
import { RegisterPage } from '../pages/register';
import { DashboardPage } from '../pages/dashboard';
import { CasesPage } from '../pages/cases';
import { CaseCreatePage } from '../pages/case-create';
import { CaseDetailPage } from '../pages/case-detail';
import { JudgmentsPage } from '../pages/judgments';
import { JudgmentDetailPage } from '../pages/judgment-detail';
import { DocumentsPage } from '../pages/documents';
import { ResearchPage } from '../pages/research';
import { CitationsPage } from '../pages/citations';
import { InsightsPage } from '../pages/insights';
import { SettingsPage } from '../pages/settings';
import { NotFoundPage } from '../pages/not-found';

export const router = createBrowserRouter([
  // Public landing page
  {
    path: '/',
    element: <LandingPage />,
  },

  // Auth routes (unauthenticated)
  {
    element: <AuthLayout />,
    children: [
      { path: '/login', element: <LoginPage /> },
      { path: '/register', element: <RegisterPage /> },
    ],
  },

  // Protected application routes
  {
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      { path: '/dashboard', element: <DashboardPage /> },
      { path: '/cases', element: <CasesPage /> },
      { path: '/cases/new', element: <CaseCreatePage /> },
      { path: '/cases/:id', element: <CaseDetailPage /> },
      { path: '/judgments', element: <JudgmentsPage /> },
      { path: '/judgments/:id', element: <JudgmentDetailPage /> },
      { path: '/documents', element: <DocumentsPage /> },
      { path: '/research', element: <ResearchPage /> },
      { path: '/citations', element: <CitationsPage /> },
      { path: '/insights', element: <InsightsPage /> },
      { path: '/settings', element: <SettingsPage /> },
    ],
  },

  // Fallback 404
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);
