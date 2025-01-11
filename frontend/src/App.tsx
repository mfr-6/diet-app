import { useState } from 'react';
import { ProductList } from './components/ProductList';
import { Sidebar } from './components/Sidebar';
import { TopBar } from './components/TopBar';
import { Home } from './components/Home';
import { Calendar } from './components/Calendar';
import { Toast } from './components/Toast';

function App() {
  const [currentRoute, setCurrentRoute] = useState<string>('');
  const [toast, setToast] = useState<{ message: string; type: 'info' | 'error' } | null>(null);

  const handleNavigate = (route: string) => {
    if (route === 'meals') {
      setToast({ message: 'This feature is not implemented yet', type: 'info' });
    } else {
      setCurrentRoute(route);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <TopBar onNavigate={handleNavigate} />
      <Sidebar onNavigate={handleNavigate} />
      
      <main className="pt-20 pb-8">
        {currentRoute === 'products' && <ProductList />}
        {currentRoute === 'calendar' && <Calendar />}
        {!currentRoute && <Home />}
      </main>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

export default App;
