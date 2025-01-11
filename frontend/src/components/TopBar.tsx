interface TopBarProps {
  onNavigate: (route: string) => void;
}

export function TopBar({ onNavigate }: TopBarProps) {
  return (
    <div className="fixed top-0 left-0 right-0 h-16 bg-blue-600 shadow-md z-40">
      <div className="h-full px-16 flex items-center">
        <button
          onClick={() => onNavigate('')}
          className="text-xl font-bold text-white hover:text-gray-100 transition-colors"
        >
          Diet App
        </button>
      </div>
    </div>
  );
} 