import React from 'react';
import { Outlet } from 'react-router-dom';
import { AppShell } from '../components/layout/app-shell';

export const AppLayout: React.FC = () => {
  return (
    <AppShell>
      <Outlet />
    </AppShell>
  );
};

