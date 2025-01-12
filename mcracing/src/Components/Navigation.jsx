import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Trophy, GraduationCap, Award, MessageSquare } from 'lucide-react';

function Navbar() {
  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/races', label: 'Races', icon: Trophy },
    { path: '/training', label: 'Training', icon: GraduationCap },
    { path: '/leaderboard', label: 'Leaderboard', icon: Award },
    { path: '/contact', label: 'Contact', icon: MessageSquare },
  ];

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo Section */}
          <div className="flex items-center">
            <NavLink to="/" className="flex items-center">
              <img
                src="/smol_logo.jpg" // Replace with the correct path if necessary
                alt="MC Racing Logo"
                className="h-10 w-auto mr-2"
              />
              {/* <span className="text-3xl font-bold text-blue-600">MC Racing</span> */}
            </NavLink>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center space-x-6">
            {navItems.map(({ path, label, icon: Icon }) => (
              <NavLink
                key={path}
                to={path}
                className={({ isActive }) =>
                  `flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition
                  ${
                    isActive
                      ? 'bg-blue-500 text-white'
                      : 'text-gray-600 hover:bg-gray-100 hover:text-blue-500'
                  }`
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
