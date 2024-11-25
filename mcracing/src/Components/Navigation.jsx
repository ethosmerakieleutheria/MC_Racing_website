import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Trophy, GraduationCap, Award, MessageSquare } from 'lucide-react';

function Navbar(){
  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/races', label: 'Races', icon: Trophy },
    { path: '/training', label: 'Training', icon: GraduationCap },
    { path: '/leaderboard', label: 'Leaderboard', icon: Award },
    { path: '/contact', label: 'Contact', icon: MessageSquare }
  ];

  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            {navItems.map(({ path, label, icon: Icon }) => (
              <NavLink
                key={path}
                to={path}
                className={({ isActive }) =>
                  `flex items-center space-x-2 px-3 py-2 rounded-md transition-colors
                  ${isActive ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'}`
                }
              >
                <Icon size={20} />
                <span>{label}</span>
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;