import { useState } from 'react';

interface SidebarProps {
  onNavigate: (route: string) => void;
}

export function Sidebar({ onNavigate }: SidebarProps) {
  const [isHidden, setIsHidden] = useState(false);

  const menuItems = [
    {
      id: 'products',
      label: 'Products',
      icon: (
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
        />
      ),
    },
    {
      id: 'meals',
      label: 'Meals',
      icon: (
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
        />
      ),
    },
    {
      id: 'calendar',
      label: 'Calendar',
      icon: (
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
        />
      ),
    },
  ];

  return (
    <>
      {/* Hamburger button */}
      <button
        onClick={() => setIsHidden(!isHidden)}
        className="fixed top-4 left-4 z-50 p-2 rounded-md hover:bg-gray-100"
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d={isHidden ? "M4 6h16M4 12h16M4 18h16" : "M6 18L18 6M6 6l12 12"}
          />
        </svg>
      </button>

      {/* Overlay - only show when sidebar is visible on mobile */}
      {!isHidden && (
        <div
          className="fixed inset-0 top-16 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setIsHidden(true)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out z-40 ${
          isHidden ? '-translate-x-full' : 'translate-x-0'
        }`}
      >
        <div className="px-4 py-4">
          <nav className="space-y-2">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  setIsHidden(true);
                }}
                className="w-full text-left px-4 py-2 rounded-md hover:bg-gray-100 flex items-center space-x-2"
              >
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  {item.icon}
                </svg>
                <span>{item.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>
    </>
  );
} 