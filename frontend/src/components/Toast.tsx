import { useEffect } from 'react';

interface ToastProps {
  message: string;
  onClose: () => void;
  type?: 'info' | 'error';
}

export function Toast({ message, onClose, type = 'info' }: ToastProps) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onClose]);

  const bgColor = type === 'error' ? 'bg-red-500' : 'bg-blue-500';

  return (
    <div className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in-up`}>
      {message}
    </div>
  );
} 