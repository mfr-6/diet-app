import { useState } from 'react';

function getWeekDates(date: Date): Date[] {
  const curr = new Date(date);
  // Adjust to Monday start
  const day = curr.getDay();
  const diff = curr.getDate() - (day === 0 ? 6 : day - 1);
  const weekDates = [];
  
  for (let i = 0; i < 7; i++) {
    const newDate = new Date(curr);
    newDate.setDate(diff + i);
    weekDates.push(newDate);
  }
  
  return weekDates;
}

function formatTime(hour: number): string {
  return `${hour.toString().padStart(2, '0')}:00`;
}

function formatMonthYear(date: Date): string {
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
}

export function Calendar() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const weekDates = getWeekDates(currentDate);
  const hours = Array.from({ length: 24 }, (_, i) => i);

  const navigateWeek = (direction: 'prev' | 'next') => {
    const newDate = new Date(currentDate);
    newDate.setDate(currentDate.getDate() + (direction === 'prev' ? -7 : 7));
    setCurrentDate(newDate);
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  return (
    <div className="max-w-[1200px] mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg">
        {/* Navigation header */}
        <div className="p-4 border-b flex items-center justify-between">
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigateWeek('prev')}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={() => navigateWeek('next')}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
            <button
              onClick={goToToday}
              className="ml-2 px-3 py-1 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded"
            >
              Today
            </button>
          </div>
          <h2 className="text-lg font-semibold text-gray-900">
            {formatMonthYear(weekDates[0])}
            {formatMonthYear(weekDates[0]) !== formatMonthYear(weekDates[6]) && 
              ` - ${formatMonthYear(weekDates[6])}`}
          </h2>
        </div>

        {/* Header with dates */}
        <div className="grid grid-cols-[100px_repeat(7,1fr)] border-b">
          <div className="p-4 font-semibold text-gray-500">Time</div>
          {weekDates.map((date, index) => (
            <div
              key={index}
              className={`p-4 text-center border-l ${
                date.toDateString() === new Date().toDateString()
                  ? 'bg-blue-50'
                  : ''
              }`}
            >
              <div className="font-semibold">
                {date.toLocaleDateString('en-US', { weekday: 'short' })}
              </div>
              <div className="text-sm text-gray-500">
                {date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </div>
            </div>
          ))}
        </div>

        {/* Time grid */}
        <div className="grid grid-cols-[100px_repeat(7,1fr)]">
          {hours.map((hour) => (
            <div key={`row-${hour}`} className="contents">
              <div
                className="p-2 text-right pr-4 text-sm text-gray-500 border-r relative"
              >
                <span className="relative -top-2">{formatTime(hour)}</span>
              </div>
              {weekDates.map((_, dayIndex) => (
                <div
                  key={`cell-${hour}-${dayIndex}`}
                  className="border-b border-l h-12 relative group"
                >
                  <div className="absolute inset-0 group-hover:bg-gray-50/50"></div>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 