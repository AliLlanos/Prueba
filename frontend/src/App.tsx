/**
 * 🏢 ERP Professional - Componente Principal de la Aplicación
 * ===========================================================
 * 
 * Este es el componente raíz de la aplicación React TypeScript.
 * Configura el enrutamiento, el tema de Material-UI, el estado global
 * y todos los providers necesarios para un sistema ERP empresarial.
 * 
 * Características incluidas:
 * - Routing con React Router v6
 * - Tema personalizado de Material-UI
 * - Estado global con Redux Toolkit
 * - Autenticación y autorización
 * - Layout responsivo empresarial
 * - Manejo de errores global
 */

import React, { Suspense, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box, CircularProgress, Alert } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Provider } from 'react-redux';

// Importaciones internas
import { store } from './store/store';
import { useAppSelector } from './hooks/useRedux';
import MainLayout from './components/layout/MainLayout';
import ErrorBoundary from './components/common/ErrorBoundary';
import LoadingSpinner from './components/common/LoadingSpinner';

// Importaciones lazy de páginas para code splitting
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const Login = React.lazy(() => import('./pages/auth/Login'));
const Inventory = React.lazy(() => import('./pages/inventory/Inventory'));
const Sales = React.lazy(() => import('./pages/sales/Sales'));
const Purchasing = React.lazy(() => import('./pages/purchasing/Purchasing'));
const Accounting = React.lazy(() => import('./pages/accounting/Accounting'));
const HumanResources = React.lazy(() => import('./pages/hr/HumanResources'));
const Settings = React.lazy(() => import('./pages/settings/Settings'));
const Profile = React.lazy(() => import('./pages/auth/Profile'));
const NotFound = React.lazy(() => import('./pages/common/NotFound'));

// ================================================================
// 🎨 CONFIGURACIÓN DEL TEMA MATERIAL-UI
// ================================================================

/**
 * 🎨 Tema personalizado para ERP Professional
 * 
 * Define la paleta de colores, tipografía y componentes personalizados
 * siguiendo las mejores prácticas de Material Design para aplicaciones empresariales.
 */
const createERPTheme = (darkMode: boolean) =>
  createTheme({
    // ============================================================
    // 🎨 PALETA DE COLORES EMPRESARIAL
    // ============================================================
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#1976d2',      // Azul corporativo profesional
        light: '#42a5f5',     // Azul claro para hover
        dark: '#1565c0',      // Azul oscuro para elementos activos
        contrastText: '#ffffff',
      },
      secondary: {
        main: '#dc004e',      // Rojo corporativo para acciones importantes
        light: '#ff5983',     // Rojo claro
        dark: '#9a0036',      // Rojo oscuro
        contrastText: '#ffffff',
      },
      success: {
        main: '#2e7d32',      // Verde para estados exitosos
        light: '#4caf50',
        dark: '#1b5e20',
      },
      warning: {
        main: '#ed6c02',      // Naranja para advertencias
        light: '#ff9800',
        dark: '#e65100',
      },
      error: {
        main: '#d32f2f',      // Rojo para errores
        light: '#f44336',
        dark: '#c62828',
      },
      background: {
        default: darkMode ? '#121212' : '#f5f5f5',
        paper: darkMode ? '#1e1e1e' : '#ffffff',
      },
      text: {
        primary: darkMode ? '#ffffff' : '#212121',
        secondary: darkMode ? '#b0b0b0' : '#757575',
      },
    },
    
    // ============================================================
    // ✏️ TIPOGRAFÍA EMPRESARIAL
    // ============================================================
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      h1: {
        fontSize: '2.5rem',
        fontWeight: 300,
        lineHeight: 1.2,
      },
      h2: {
        fontSize: '2rem',
        fontWeight: 400,
        lineHeight: 1.3,
      },
      h3: {
        fontSize: '1.75rem',
        fontWeight: 400,
        lineHeight: 1.4,
      },
      h4: {
        fontSize: '1.5rem',
        fontWeight: 500,
        lineHeight: 1.4,
      },
      h5: {
        fontSize: '1.25rem',
        fontWeight: 500,
        lineHeight: 1.5,
      },
      h6: {
        fontSize: '1rem',
        fontWeight: 600,
        lineHeight: 1.6,
      },
      body1: {
        fontSize: '1rem',
        lineHeight: 1.5,
      },
      body2: {
        fontSize: '0.875rem',
        lineHeight: 1.43,
      },
    },
    
    // ============================================================
    // 📐 ESPACIADO Y FORMA
    // ============================================================
    spacing: 8, // 8px base unit
    shape: {
      borderRadius: 8, // Bordes redondeados modernos
    },
    
    // ============================================================
    // 🎛️ COMPONENTES PERSONALIZADOS
    // ============================================================
    components: {
      // AppBar personalizado
      MuiAppBar: {
        styleOverrides: {
          root: {
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          },
        },
      },
      // Paper con sombra suave
      MuiPaper: {
        styleOverrides: {
          root: {
            boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
          },
        },
      },
      // Botones con diseño corporativo
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none', // Sin mayúsculas automáticas
            fontWeight: 500,
            borderRadius: 8,
          },
        },
      },
      // DataGrid personalizado
      MuiDataGrid: {
        styleOverrides: {
          root: {
            border: 'none',
            '& .MuiDataGrid-cell': {
              borderBottom: '1px solid rgba(224, 224, 224, 1)',
            },
          },
        },
      },
    },
  });

// ================================================================
// 🌐 CONFIGURACIÓN DE REACT QUERY
// ================================================================

/**
 * 🌐 Cliente de React Query para manejo de estado del servidor
 * 
 * Configura cache, refetch automático y manejo de errores
 * optimizado para aplicaciones empresariales.
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Cache durante 5 minutos por defecto
      staleTime: 5 * 60 * 1000,
      // Mantener en cache durante 10 minutos
      cacheTime: 10 * 60 * 1000,
      // Reintentar 3 veces en caso de error
      retry: 3,
      // Refetch automático cuando la ventana recibe focus
      refetchOnWindowFocus: false,
    },
    mutations: {
      // Reintentar mutaciones fallidas una vez
      retry: 1,
    },
  },
});

// ================================================================
// 🛡️ COMPONENTE DE RUTAS PROTEGIDAS
// ================================================================

/**
 * 🛡️ Componente para proteger rutas que requieren autenticación
 * 
 * Verifica si el usuario está autenticado antes de permitir
 * acceso a rutas protegidas.
 */
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAppSelector(state => state.auth);

  // Mostrar loading mientras verifica autenticación
  if (isLoading) {
    return <LoadingSpinner message="Verificando autenticación..." />;
  }

  // Redirigir a login si no está autenticado
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

// ================================================================
// 🔧 COMPONENTE DE INICIALIZACIÓN
// ================================================================

/**
 * 🔧 Componente interno que maneja la lógica de la aplicación
 * 
 * Separado del componente principal para poder usar hooks de Redux
 * después de configurar el Provider.
 */
const AppContent: React.FC = () => {
  const { darkMode } = useAppSelector(state => state.ui);
  const { isAuthenticated } = useAppSelector(state => state.auth);

  // Crear tema dinámicamente basado en preferencias
  const theme = React.useMemo(
    () => createERPTheme(darkMode),
    [darkMode]
  );

  // ============================================================
  // 🚀 EFECTOS DE INICIALIZACIÓN
  // ============================================================
  
  useEffect(() => {
    // TODO: Verificar token almacenado al cargar la aplicación
    console.log('🚀 Inicializando ERP Professional...');
    
    // TODO: Configurar interceptores de Axios
    // TODO: Cargar configuración inicial
    // TODO: Verificar permisos del usuario
    
  }, []);

  // ============================================================
  // 📱 RENDERIZADO DE LA APLICACIÓN
  // ============================================================

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <ErrorBoundary>
          <Suspense fallback={<LoadingSpinner message="Cargando..." />}>
            <Routes>
              {/* ================================================ */}
              {/* 🔐 RUTAS DE AUTENTICACIÓN (PÚBLICAS) */}
              {/* ================================================ */}
              <Route 
                path="/login" 
                element={
                  isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />
                } 
              />

              {/* ================================================ */}
              {/* 🏢 RUTAS PRINCIPALES (PROTEGIDAS) */}
              {/* ================================================ */}
              <Route 
                path="/" 
                element={
                  <ProtectedRoute>
                    <MainLayout />
                  </ProtectedRoute>
                }
              >
                {/* Dashboard principal */}
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />

                {/* Módulos del ERP */}
                <Route path="inventory/*" element={<Inventory />} />
                <Route path="sales/*" element={<Sales />} />
                <Route path="purchasing/*" element={<Purchasing />} />
                <Route path="accounting/*" element={<Accounting />} />
                <Route path="hr/*" element={<HumanResources />} />

                {/* Configuración y perfil */}
                <Route path="settings/*" element={<Settings />} />
                <Route path="profile" element={<Profile />} />
              </Route>

              {/* ================================================ */}
              {/* 🚫 RUTA DE ERROR 404 */}
              {/* ================================================ */}
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </Router>
    </ThemeProvider>
  );
};

// ================================================================
// 🏢 COMPONENTE PRINCIPAL DE LA APLICACIÓN
// ================================================================

/**
 * 🏢 Componente principal de ERP Professional
 * 
 * Configura todos los providers necesarios y la estructura
 * base de la aplicación empresarial.
 */
const App: React.FC = () => {
  return (
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100vh',
            backgroundColor: 'background.default',
          }}
        >
          <AppContent />
        </Box>
      </QueryClientProvider>
    </Provider>
  );
};

export default App;

// ================================================================
// 📊 INFORMACIÓN DE DESARROLLO
// ================================================================

/**
 * 📊 Información para desarrolladores
 * 
 * Esta aplicación incluye:
 * - ⚛️ React 18 con TypeScript
 * - 🎨 Material-UI v5 con tema personalizado
 * - 🗂️ Redux Toolkit para estado global
 * - 🌐 React Query para estado del servidor
 * - 🛣️ React Router v6 para navegación
 * - 🔐 Sistema de autenticación robusto
 * - 📱 Diseño responsivo y moderno
 * - 🚀 Code splitting para mejor rendimiento
 * - 🛡️ Manejo de errores y loading states
 * - 🎯 TypeScript para seguridad de tipos
 */