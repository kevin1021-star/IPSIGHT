import { createBrowserRouter, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from './lib/auth.tsx';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import AssessmentDetail from './pages/AssessmentDetail';
import Reports from './pages/Reports';

// Protected route wrapper
function ProtectedLayout() {
  const { token, loading } = useAuth();
  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full" />
      </div>
    );
  }
  if (!token) return <Navigate to="/login" replace />;
  return (
    <Layout>
      <Outlet />
    </Layout>
  );
}

export const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: <ProtectedLayout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'upload', element: <Upload /> },
      { path: 'assessment/:id', element: <AssessmentDetail /> },
      { path: 'reports', element: <Reports /> },
    ],
  },
  { path: '*', element: <Navigate to="/" replace /> },
]);
